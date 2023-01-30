from prefect import flow, task
from prefect_airbyte import AirbyteConnection, AirbyteServer
from prefect_airbyte.connections import AirbyteSyncResult
from prefect_dbt.cli.commands import trigger_dbt_cli_command
from prefect_snowflake.database import SnowflakeConnector, snowflake_multiquery

airbyte_server = AirbyteServer(server_host="localhost", server_port=8000)

airbyte_connections = [
    AirbyteConnection(connection_id=connection_id, airbyte_server=airbyte_server)
    for connection_id in [
        "fa8d5164-ca22-47da-83e0-829cc86a70b8",  # Airbyte Github Stats
        "8e3a3ef1-6c2d-4255-99d4-21e9e542d853",  # DBT Github Stats
        "980c14d9-2992-46a7-a1dc-2b92e60e1475",  # Prefect Github Stats
    ]
]


@task
def run_airbyte_sync(connection: AirbyteConnection) -> AirbyteSyncResult:
    job_run = connection.trigger()
    return job_run.wait_for_completion()


@flow(log_prints=True)
def my_elt_flow():
    # run Airbyte syncs
    airbyte_results = run_airbyte_sync.map(airbyte_connections)
    # run dbt models
    dbt_result = trigger_dbt_cli_command(  # run dbt models
        command="dbt run",
        project_dir="github_common_contributors",
        wait_for=airbyte_results,
    )
    # ask some questions about transformed data
    common_authors, common_issue_submitters = snowflake_multiquery(
        queries=[
            "select login from commit_authors",
            "select login from issue_submitters",
        ],
        snowflake_connector=SnowflakeConnector.load("github-contributors"),
        wait_for=dbt_result,
    )
    print(
        f"Common authors: {common_authors} "
        f"Common issue submitters: {common_issue_submitters}"
    )


if __name__ == "__main__":
    my_elt_flow()
