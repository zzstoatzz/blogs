# Commoditizing data integration alongside Airbyte
<details>
<summary>Contents</summary>

+ Background
    + What and how?
    + Specific Usefulness
+ Developing your own Python *source* connector
    + Setup
        + Java
        + Docker
        + Credentials
    + Implementation
        + `spec()`
        + `check()`
        + `discover()`
        + `read()`
    + Testing
    

</details>

<div align="center">
<img src="imgs/chasm.png" height=350/>
</div>

<br>

Hello there! I'm Nate, a junior data engineer at [SLATE](https://slateco.io) (yes, the rhyme was why I was hired).

My purpose here is to give a little background on what's exciting about Airbyte to organizations like us and to demonstrate how you can extend its functionality to benefit the Airbyte community or just to suit your use-case. Some [documentation](https://docs.airbyte.io/integrations/custom-connectors) on this topic exists, but it didn't seem very sequential or comprehensive, so here we are.

For more info on how to use out-of-the-box Airbyte, explore [here](https://docs.airbyte.io/).

## What *is* Airbyte?

[Airbyte](https://airbyte.io/) soft-launched in late September 2020 as an open-source data integration platform. It's backed by a friendly group of engineers, enthusiastic community contributions, and some [impressive seed funding](https://airbyte.io/articles/our-story/we-raised-a-5m-seed-round-with-accel-to-commoditize-data-integration/).

<div align="center">
<img src="imgs/schema.png" height=400/>
</div>

<br>

Their core product, a self-hosted EL(T) engine, effectively addresses the established need for an enterprise-scale solution to moving enterprise-scale amounts of data. It does this by abstracting the EL(T) process, using `connector` instances between sources, destinations and the all-orchestrating Airbyte instance.

## Airbyte's Unique Usefulness
I entered the data engineering space shortly after Airbyte came into being, and it seems that this coincidence has ended up drastically improving my life as a fresh lamb to the data engineering slaughter. 

If Airbyte wasn't around to do my job, I'd probably be writing all of our clients' ETLs in Python (maybe trying to learn Singer, Luigi, Airflow) or maybe would've become a degenerate consultant and begun advising clients that they should pay a subscription to some low-code platform that likely exceeds their use-case... looking at you, Talend.

Thankfully, Airbyte does exist. At SLATE, we leverage their core ELT tool in dozens of use-cases to automatically move data at a near-arbitrary scale, paying for nothing but the deployment of the EC2 instances that run Airbyte.

So, to summarize how we find Airbyte useful:
- Airbyte allows us to avoid the potentially unsavory hours involved in re-purposing Python code to build one-off ELTs that are fast, schedule-able, and reliable
- Unlike many ELT services with subscription or usage-based pricing, Airbyte's open-source ETL engine is freely customizable and easily integrated into your own application or simple use-case.

Chances are that if you need for large-scale data integration, you're probably using platform to store data that Airbyte has already integrated. [Here](https://docs.airbyte.io/integrations) are full lists of sources and destinations.

### **I'll admit, that's cool... but I don't see the connector I want!**
..but, if you're like I was, then you need something beyond the standard integrations.

Now I'll outline how to add a connector to Airbyte, based on my experience implementing [Airbyte's Smartsheets source connector](https://github.com/airbytehq/airbyte/pull/2880).

If at any point you need help, feel free to reach out to the good folks in the [Airbyte slack community](https://airbyte.io/community/) or [me](mailto:nate.nowack@slateco.io).

## Develop a Connector (Python source)
In Airbyte-speak, source and destination connectors are different things - they require a different set of steps to implement. However, I found that learning to interact with Airbyte's deployment and OOP framework took the most time, which is common to both development workflows. 

So, hopefully you can still benefit from this article if you're here looking to make a new destination connector.

### Setup

**[TO DO]**

#### Java and gradlew

**[TO DO]**

#### Docker 

**[TO DO]**

#### Source Credentials

**[TO DO]**

### Implementation
While your connector's implementation is going to platform specific, all Airbyte source connectors are written as a class with the four methods outlined below.

```python
# main class definition for your source
class SourceSmartsheets(Source):

        # "check" that your credentials give a good connection to your data source
        # e.g. Smartsheets api call on smartsheet of interest -> status 200
    def check(self, logger, config) -> AirbyteConnectionStatus:
        # TODO


        # create your source's JSONschema catalog from column names and types
    def discover(self, logger, config) -> AirbyteCatalog:
        # TODO


        # create AirbyteMessage instances for each record from your source's catalog
    def read(self, logger, config, catalog, state) -> Generator:
        # TODO


```
It's going to be helpful to check out [the docs]() during these implementations, but I'll describe where I got stuck during the process and how I got around it.

#### `spec.json`
The first file to edit in the directory that was generated is the JSON configuration specification. This where you specify what credentials an end-user would need to use your connector in Airbyte. In the case of my source connector, I'm using the Smartsheets API under the hood so users of my connector need to provide both an API token and their Smartsheet's ID.
```json
{
  "documentationUrl": "https://docs.airbyte.io",
  "connectionSpecification": {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Smartsheets Source Spec",
    "type": "object",
    "required": ["access_token", "spreadsheet_id"],
    "additionalProperties": false,
    "properties": {
      "access_token": {
        "title": "API Access token",
        "description": "Found in Profile > Apps & Integrations > API Access within Smartsheet app",
        "type": "string",
        "airbyte_secret": true
      },
      "spreadsheet_id": {
        "title": "Smartsheet ID",
        "description": "Found in File > Properties",
        "type": "string"
      }
    }
  }
}
```

#### `check`
```python
def check(self, logger: AirbyteLogger, config: json) -> AirbyteConnectionStatus:
    try:
        access_token = config["access_token"]
        spreadsheet_id = config["spreadsheet_id"] + 1

        smartsheet_client = smartsheet.Smartsheet(access_token)
        smartsheet_client.errors_as_exceptions(True)
        smartsheet_client.Sheets.get_sheet(spreadsheet_id)

        return AirbyteConnectionStatus(status=Status.SUCCEEDED)
    except Exception as e:
        if isinstance(e, smartsheet.exceptions.ApiError):
            err = e.error.result
            code = 404 if err.code == 1006 else err.code
            reason = f"{err.name}: {code} - {err.message} | Check your spreadsheet ID."
        else:
            reason = str(e)
        logger.error(reason)
    return AirbyteConnectionStatus(status=Status.FAILED)
```
#### `discover`
```python
def discover(self, logger: AirbyteLogger, config: json) -> AirbyteCatalog:
    access_token = config["access_token"]
    spreadsheet_id = config["spreadsheet_id"]
    streams = []

    smartsheet_client = smartsheet.Smartsheet(access_token)
    try:
        sheet = smartsheet_client.Sheets.get_sheet(spreadsheet_id)
        sheet = json.loads(str(sheet))  # make it subscriptable
        sheet_json_schema = get_json_schema(sheet)

        logger.info(f"Running discovery on sheet: {sheet['name']} with {spreadsheet_id}")

        try:
            stream = AirbyteStream(name=sheet["name"], json_schema=sheet_json_schema)
            streams.append(stream)
        except Exception as e:
            rec = "Check that your source's column names don't contain spaces or _"
            logger.error(f"Stream creation failed: {str(e)} - {rec} ")
    except Exception as e:
        raise Exception(f"Could not run discovery: {str(e)}")

    return AirbyteCatalog(streams=streams)
```
#### `read`

```python

def read(
    self,
    logger: AirbyteLogger,
    config: json,
    catalog: ConfiguredAirbyteCatalog,
    state: Dict[str, any]
) -> Generator[AirbyteMessage, None, None]:

    access_token = config["access_token"]
    spreadsheet_id = config["spreadsheet_id"]
    smartsheet_client = smartsheet.Smartsheet(access_token)

    for configured_stream in catalog.streams:
        stream = configured_stream.stream
        properties = stream.json_schema["properties"]
        if isinstance(properties, list):
            columns = tuple(key for dct in properties for key in dct.keys())
        elif isinstance(properties, dict):
            columns = tuple(i for i in properties.keys())
        else:
            logger.error("Could not read properties from the JSONschema in this stream")
        name = stream.name

        try:
            sheet = smartsheet_client.Sheets.get_sheet(spreadsheet_id)
            sheet = json.loads(str(sheet))  # make it subscriptable
            logger.info(f"Starting syncing spreadsheet {sheet['name']}")
            logger.info(f"Row count: {sheet['totalRowCount']}")

            for row in sheet["rows"]:
                values = tuple(i["value"] for i in row["cells"])
                try:
                    data = dict(zip(columns, values))

                    yield AirbyteMessage(
                        type=Type.RECORD,
                        record=AirbyteRecordMessage(stream=name, data=data, emitted_at=int(datetime.now().timestamp()) * 1000),
                    )
                except TypeError as e:
                    logger.error(f"{e}: BOGUS!")

        except Exception as e:
            logger.error(f"Could not read smartsheet: {name}")
            raise e
    logger.info(f"Finished syncing spreadsheet with ID: {spreadsheet_id}")

```
### Testing

**[TO DO]**

#### Integration Tests

**[TO DO]**

#### Unit Tests
see google-sheets

**[TO DO]**

#### From the UI

**[TO DO]**

## Open a PR

## Victory screech