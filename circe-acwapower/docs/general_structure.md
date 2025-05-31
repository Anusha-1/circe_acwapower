# General Structure

For this project we have built a SQL database with different table with relevant data about the operation of wind farms, and a Power BI app that reads from the database and offers different relevant visualizations.

Several Python scripts maintains the SQL database updated as new raw data becomes available.

## Levels of data algorithms

To visualize the proper results we will need to perform dfferent operations on the raw data. Depending on the context, we will organize the different algorithms in three different levels.

1. Python scripts.
2. SQL views and functions.
3. Power BI manipulations.

The higher the level, the more flexibility we gain to offer filtering options but we will have less complexity in the operations themselves.

For instance, we will calculate Power Curves at level 1 (Python script) with a complex algorithm that applies a smoothing to the curve (among other features). The counterpart is that we will not be able to select on the fly the exact period of data we want to calculate the power curves with. These Power Curves need to be pre-calculated, and Power BI's only role here will be to read the table that has the resulting power curves and represent them.

In this case, we cannot run Python scripts from the front-end (a Power BI online app) directly. To adapt to the client requirements, we needed to move some algorithms to levels 2 and 3. Some structural decisions might not be optimal with other front-end solutions.


## Cloud architecture

We are using the following Azure resources:

- SQL Server Database. It hosts the database that serves as the input for the Power BI tool.
- Azure Function App. It hosts different function apps to run periodically the scripts that update the different database tables. The same scripts can also be run locally at any time.
- Azure Key Vault: It saves the credentials to access the different service.
- Azure Storage Account: Used to save the different files.


The algorithms developed here would be transfer to NOMAC / ACWA POWER to be deployed in production in their own infrastructure. 

The SQL database is divided into three main schemas:

- raw: For raw input data
- intermediate: Intermediate results, not to be represented
- vis: Tables thought to be used by Power BI

In occasions some SQL functions or procedures have been saved in the default dbo schema

## Data Provided

ACWA POWER / NOMAC provided Circe the following data files from the Khalladi wind farm to develop the tool:

- 10-min data
- 1-min data
- Alarms logbooks
- Alarms metadata (it required manual manipulation)
- Manufacturer and LaPM power curves (it required to be manually uploaded)
- Met Mast data
- Pitch Angles data
- Acceleration data
- LaPM events (separated from the other alarms)
- Other metadata information (it required a manual adequation of this info):
    - LaPM and WSM sectors
    - Coordinates of WTGs
    - Groups of WTGs
