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

<script src="https://gist.github.com/zzstoatzz/4865b48699f8b6eda80f3dfd37d70b4a.js"></script>

#### `spec`

**[TO DO]**

#### `check`

**[TO DO]**

#### `discover`

**[TO DO]**

#### `read`

**[TO DO]**

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