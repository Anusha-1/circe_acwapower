# Power Curves

## Manufacturer

In the case of Khalladi data, we have different information of manufacturer's power curve.

Each one of these turbines can operate in three different "normal" modes: 2791, 2792, 2794. For each one of these three modes, we have 4 power curves at different densities: 1.09, 1.12, 1.15 and 1.18.

Additionally, the turbines can operate in different LaPM modes that activate at specific wind directions. The sectors of activation are defined in the metadata table vis.sectors. For each LaPM mode, we also have different Power Curves at different densities. We have collected all these original power curves in input/power_curves/original_pc.csv.

To organize all the power curves in the system (not only the power curves given by the manufacturer, but also the data-driven power curves), we create an id for each curve. We will have a power curve for each:

- Turbine
- Concept: Manufacturer, Historical, etc.
- Period: The period of data taken for the calculation (doesn't apply for manufacturer power curves)
- Sector
- Density

We organize an initial collection of the power curves metadata for manufacturer curves in the file input/power_curves/pc_metadata.csv

The script acwa.scripts.power_curves.manufacturer will read from both files, and organize the information in two output table:

- vis.pc_metadata: Metadata for each curve
- vis.power_curves: Actual power vs speed values of the power curves

vis.pc_metadata has the following columns:

| Column Name          | Type   | Description                         | Boundaries | Comments |
| -------------------- | ------ | ----------------------------------- | ---------- | -------- |
| pc_id                | varchar| Unique ID of the Power Curve        |            |          |
| id_wtg_complete      | varchar| Unique ID of the WTG                |            |          |
| concept              | varchar| Type of Power Curve (Manufacturer, Historical, ...)         |  |          |
| period               | varchar| Period of data taken                |            | MN for manufacturer    |
| sector_name          | varchar| Name of the sector                  |            |          |
| density              | varchar| Density selected for wind speed correction |     |          |
| main                 | bit    | 1 if it is the main sector of the WTG | | |

For vis.power_curves we have:

| Column Name          | Type   | Description                         | Boundaries | Comments |
| -------------------- | ------ | ----------------------------------- | ---------- | -------- |
| pc_id                | varchar| Unique ID of the Power Curve        |            |          |
| bin                  | float  | Wind Speed (m/s)                    |            | Center of the bin |
| power                | float  | Power (kW)                          |            |          |
| sigma                | float  | Standard Deviation                  |            | 0 for manufacturer |

We can join the power curves with its metadata through pc_id. As we are storing power curves per turbine, we will have some duplicated manufacturer curves (i.e. different turbines having actually the same reference).

The calculated power curves will be added to these tables.

We will calculate also power curves with 1 min data. We duplicate these tables, creating vis.pc_metadata_1min and vis.power_curves_1min , to allocate 1-min power curves. The manufacturer power curves will be the same in both.

This script creates these tables from zero, so we will need to run this before the scripts that calculates historical power curves that we will see later.