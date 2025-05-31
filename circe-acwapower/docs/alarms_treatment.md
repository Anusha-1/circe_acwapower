# Alarms treatment

We need to make several transformation at the level of 10-min data and individual events to fully explore availability.

This is the proposed schema.

```mermaid

graph TD

    SQLTable1[intermediate.input_alarms]:::SQLTable --> A1(Clean overlaps):::Action
    A1 --> SQLTable4[intermediate.basic_alarms]:::SQLTable

    SQLTable2[intermediate.input_10min]:::SQLTable --> A7(Add variables):::Action
    SQLTable8[intermediate.input_1min]:::SQLTable --> A7
    A7 --> IR4[10min data with extra variables]:::IntermediateResult

    IR4 --> A2(join):::Action
    SQLTable3[vis.wtg_config]:::SQLTable --> A2
    SQLTable4 --> A2

    A2 --> IR1[10 min data with alarms]:::IntermediateResult
    SQLTable9[vis.oper_met_mast]:::SQLTable --> A8(Calculate density):::Action
    IR1 --> A8
    SQLTable10[vis.oper_met_mast_metadata]:::SQLTable --> A8
    A8 --> IR5[10 min data with air density]:::IntermediateResult

    IR5 --> A3(Format, calculate KPIs, ...):::Action
    A3 --> IR2[10 min data with extra KPIs]:::IntermediateResult

    IR2 --> A4(Correct to all densities):::Action
    A4 --> SQLTable5[intermediate.wind_speed_corrections_10min]:::SQLTable

    IR2 --> A5(Classify bins, calculate sector, static yaw, ...):::Action
    A5 --> SQLTable7[intermediate.basic_10min]:::SQLTable


    classDef SQLTable fill: #f58231, color: #000
    classDef Action fill: #4363d8, color: #FFF
    classDef IntermediateResult fill:#fffac8, color: #000


```

[CONTINUAR AQUI]





```mermaid

graph TD

    DynTable2[intermediate.input_alarms]:::DynTable --> Func1(obtain priority alarms):::Function
    StaticTable3[raw.alarms_metadata]:::StaticTable --> Func1
    DynTable1[intermediate.input_10min]:::DynTable -->Func2
    PC[Power Curves] --> Func4

    subgraph AZ1[azure_operational]
    Func1 --> IntResult4[priority alarms]:::InternalResult
    IntResult4 --> Func2(assign alarms to 10 min data):::Function
    Func2 --> IntResult1[basic 10min with alarms]:::InternalResult
    
    IntResult1 --> Func4(calculate losses):::Function
    Func4 --> DynTable6[vis.oper_10min]:::DynTable

    DynTable6 --> Func5(introduce losses in alarms):::Function
    IntResult4 --> Func5
    Func5 --> DynTable7[vis.treated_events]:::DynTable
    end
    
    subgraph AZ2[azure_availabilities]
    DynTable7 --> Func6(obtain alarm availabilities):::Function
    Func6 --> IntResult2[alarm availabilties]:::InternalResult
    DynTable6 --> Func8(daily average and combine):::Function
    IntResult2 --> Func8
    Func8 --> DynTable10[vis.oper_1day]:::DynTable
    IntResult2 -.-> DynTable10
    DynTable7 ----> Func9(daily collection):::Function
    Func9 --> DynTable11(vis.treated_events_1day):::DynTable
    end

    classDef DynTable fill: #fabed4, color: #000
    classDef AzFunc fill: #4363d8, color: #FFF
    classDef StaticTable fill: #ffe119, color: #000
    classDef Function fill:#000075, color: #FFF
    classDef InternalResult fill:#fffac8, color: #000


    style AZ1 fill:#FFF, color: #000
    style AZ2 fill:#FFF, color: #000
```


The legend is:

- Yellow boxes represent static tables (they are not supposed to be updated)
- Pink boxes represent dynamic tables (they will be updated periodically)
- Beige boxes represent internal results (not intended to be written in a SQL table)

- Subgraph boxes represent Azure functions (set with a timer)
- Navy boxes represent different algorithms and processes that we need to develop

Thus, following the algorithms we need to develop (top to bottom) we have:

1. Obtain priority alarms. 

    - It takes the raw alarms and returns a treated logbook in which we don't have overlapping alarms. The cases of overlap are solved based on the severity scale and start datetime (in case of tie). __Issue #22: 27 May - 28 May__

    - Also, here we calculate the times between alarms. __Issue #28: 27 May - 30 May__

2. Assign alarms to 10-min data.

    - We need to take every 10-min data and assign its correspondant alarm (if any). In case of coexistence alarms in the same 10-min, we assign one based on the severity scale and duration. __Issue #23: 30 May - 31 May__

    - Also, we need to find non-registered events. __Issue #34 (Partially): 31 May - 5 June__  

3. Calculate losses.

    - We need to have some Power Curves to calculate the losses. Eventually, will have to calculate them, for the moment we'll upload the manufacturer curves, and use them instead. __Issue #26: 27 May - 31 June__

    - Migrate the algorithm for loss calculations. __Issue #24: June 3 - June 4__

4. Introduce the losses in the alarms

    - We need to add to the treated logbook the non-registered events we have found. __Issue #34 (Partially): 31 May - 5 June__

    - The losses we have obtain for each 10-min, need to be added up into their respective alarms. __Issue #25: 4 June - 5 June__

5. Calculate availabilities.

    - Operational Availability (and general framework). __Issue #27: May 28 - May 31__
    
    - Wind Availability. __Issue #29: May 30 - May 31__

    - Production Availability. __Issue #31: May 30 - May 31__   

    - Technical Availability. __Issue #30: May 30 - May 31__

    - Effective availability. __Issue #32: May 30 - May 31__ 

    - Manufacturer Availability (also including a yearly variable to accumulate maintenance time). __Issue #33: May 30 - June 5__
   

6. Daily average and combine.

    - Average the different 10-min data daily, and merge the info with the different availabilities. __Issue #16: June 4 - June 7__

7. Daily collection.

    - From the treated events table, generate also daily stats. __Issue #17: June 4 - June 7__

These different processes are planned to be implemented in two Azure function:

- azure_operational: Functions 1-4. The main output is vis.oper_10min and vis.treated_events. Ideally should run every 10 minutes.

- azure_availabilities: Function 5-8. The main output is vis.oper_1day and vis.treated_events_1day. It should run every day.

In order to parallelize work, we have implemented some temporary shortcuts represented with dash lines in the scheme:

- After calculating the priority alarms (first intermediate result of operational), we are "copying" it to vis.treated_alarms, filling missing values

- After calculating the operational availability, we are creating a temporary vis.oper_1day table. It has the final structure, but most values (like losses) are set to zero.


## Risks

- Should the join of realtime alarms and metadata be incremental or global? Global is less efficient, but easier to implement and less dangerous (as alarms have a duration, can be tricky to fix the time limits to consider). 
Initially, we'll develop these algorithms globally. Later on, we'll try to collect and append only new data.

- We could interact with WOD package. This could save time in the end, but it could has some problems at the beginning and slow down some development.

- We'll need to be careful with running time and optimization. Maybe this won't fit in 10 minutes (if we are not being incremental) and we need a longer period of refresh.

- Right now we have gaps of data. We'll need to think on how to fill them.

- We need to identify lapm and sector management