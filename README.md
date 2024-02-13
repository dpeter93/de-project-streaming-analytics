# Data Engineer End to End project

Around a year ago I made a deliberate decision to pivot my career towards the IT field, leveraging my previous experiences gained as a Mechanical Engineer. To facilitate this transition, I undertook an intensive Junior Software Engineer course specializing in Data Engineering. This final project represents the culmination of that training.

## CRM System Streaming Analytics with Real Time Sales Dashboard

The project entails the development of a real-time Power BI dashboard for an online CRM (Customer Relationship Management) system, aimed at extracting insights from client interactions and business opportunities. Below is a brief summary of the project components and technologies employed.

At the end of the project the interactive, nice looking dashboard look like this:

![image](https://github.com/dpeter93/de-project-streaming-analytics/assets/101528495/655f89ef-e85d-4497-b8b1-2c6b76fec654)


## Data Pipeline - Flowchart of the Solution

The project contains the systems and technologies listed below with data flow route in the picture:

 1. Capsule CRM - Data Source / Producer
 2. Upstash Kafka - Kafka Broker
 3. Google Cloud Functions - Consumer
 4. Google BigQuery - Data Warehouse
 5. Google Cloud Run - Fully managed Docker containerized dbt project
 6. dbt - Data Transformation tool
 7. Power BI - Data Visualization tool

<br/><br/>

<p align="center">
  <img src=https://github.com/dpeter93/de-project-streaming-analytics/assets/101528495/4244242b-9946-4418-bc33-6edccb2d88ba />
</p>

## Steps of the Solution

### First Step

Making webhook connection between CRM and Upstash Kafka to capture updates to opportunities made by the sales team:

**opportunity/{created/updated/deleted/closed}**

To enable seamless communication between the CRM and Kafka, I leverage Resthooks, a powerful tool designed to trigger notifications when specific events occur within the Capsule system. To facilitate this integration, a custom Python script has been developed. This script is engineered to establish a secure and reliable connection, capable of capturing a range of events, including opportunity creation, updates, deletions, and closures. By utilizing this approach, we can efficiently generate (**Produce**) messages containing necessary data, essential for populating the dashboard.

> scripts/webhook_crm_kafka.py -> def post_resthook()

### Second Step

Creating Google Function service to load the raw data into Google BigQuery:

First I separated the uploaded file and I just created the ingestion part of that, after it worked properly I made some changes to the current stage - it will be shown in a later step. The function fetch (**Consume**) the messages from the Kafka broker and then load the warehouse in its orginal form. 

> cloud-functions-svc/main.py

### Third Step

Implementing Kafka HTTP connector to trigger the Google Function:

To allow communication from the consumer side between Kafka and the implemented Python function I added an HTTP connector and trigger my ingestion process. After this process when a user change something in the CRM system, the raw data with the modification were inserted to the warehouse.

### Fourth Step

Initializing dbt project for the transformation, Docker contanarized the service and deploy to Google Cloud Run:

The dbt data modeling tool is running under a Docker container to make a live and working alone box product which can be installed to the cloud. The generated HTTPS endpoint is used in the above presented Cloud Function before to trigger this service after the raw data was inserted to BigQuery. The result is making the staging, intermediate and mart tables in a separated dataset.
As it was a bigger step in my project, I separated it different sections:

1. dbt model creation locally and test it
2. Implementing Flask application
3. Dockerfile creation and built the image
4. Deployed to Cloud Run

> gc-dbt-svc/.

### Fifth Step

Power BI integration and dashboard creation:

Integrated Power BI with the dbt mart models from BigQuery as a DirectQuery data source, enabling the creation of an interactive dashboard showcasing real-time data charts.

## Conclusion

By seamlessly integrating the above steps, I've crafted a unique solution where every user interaction within the CRM system reflects in the Power BI dashboard, empowering informed decision-making. It's worth noting that while the exercise encapsulates the problem context and the end result, detailed procedural information on achieving the solution was not provided.

### Key Learnings:

1. Streaming Data Processes with Kafka
2. Google Cloud tools for running services
3. Google Cloud tools for Data Warehouse / Data Mart ingetration
4. dbt Data Transfomration Tool
5. Docker Containerization Tool
