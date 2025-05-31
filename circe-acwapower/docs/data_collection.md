# Data Collection

For each wind farm added to the project we'll have different realtime data. For each wind farm we should have four tables (in the raw schema):

- realtime_input_10min_{Wind Farm Name}
- realtime_input_1min_{Wind Farm Name}
- realtime_alarms_{Wind Farm Name}
- realtime_pitch_{Wind Farm Name}

and also a table for each met mast, with the name realtime_met_mast_{Met Mast ID}

It's up to ACWA to maintain these tables updated, or to point to the real data sources.

For each one of these data sources, we'll build a standarized table with data from all the wind farms (or Met Mast). This process will standarized column names, and add the 'id_wf' column to mark the procedence of the data.

The output tables of this process are:

- intermediate.input_10min
- intermediate.input_1min
- intermediate.input_alarms
- intermediate.pitch
- vis.oper_met_mast

The scripts have an incremental flag that can be True or False. If True we only update new data, if False we overwrite the entire table.

The scripts run a loop on the different Wind Farms, and execute the following logic:

```mermaid

graph TD

    Q1{Incremental flag is on and table exists?} -- Yes --> Q2
    Q1 -- No --> A6

    Q2{Wind Farm exists in table?} -- Yes --> A1
    Q2 -- No --> A6

    A1(1 Obtain maximum datetime in previous collected data) --> A2
    A2(2 Extract new data after maximum datetime) --> A3
    A3(3 Format and standarize data) --> A4
    A4(4 Transform timestamps to UTC) --> A5
    A5(5 Append in table)

    A6(6 Read all available data) --> A7
    A7(7 Format and standarize data) --> A8
    A8(8 Transform timestamps to UTC) --> A9
    A9(9 Write in table)
```

Updating alarms is a bit more complicated:

```mermaid

graph TD

    Q1{Incremental flag is on and table exists?} -- Yes --> Q2
    Q1 -- No --> A7

    Q2{Wind Farm exists in table?} -- Yes --> A1
    Q2 -- No --> A7

    A1(1 Obtain maximum start datetime in previous collected alarms) --> A2
    A2(2 Extract recent alarms in realtime tables) --> A3
    A3(3 Delete recent alarms in collection tables) --> A4
    A4(4 Format and standarize data) --> A5
    A5(5 Transform timestamps to UTC) --> A6
    A6(6 Append in table)

    A7(7 Read all available data) --> A8
    A8(8 Format and standarize data) --> A9
    A9(9 Transform timestamps to UTC) --> A10
    A10(10 Write in table)
```