# Reliability

```mermaid
graph LR

    Table1[Data]:::SQLTable --> A1(Fit):::Action --> I1[Models]:::IntermediateResult
    Table1 -- only new data --> A2(Predict):::Action
    I1 --> A2
    A2 --> Table2[Results]:::SQLTable

    classDef SQLTable fill: #f58231, color: #000
    classDef Action fill: #4363d8, color: #FFF
    classDef IntermediateResult fill:#fffac8, color: #000

```

## Normalized Temperature

$$T_{\text{norm}} = \frac{T - \text{Lower Bound}}{\text{Upper Bound} - \text{Lower Bound}}$$

thus,

- $T_{\text{norm}} < 0$ if $T < \text{Lower Bound}$
- $T_{\text{norm}} = 0$ if $T = \text{Lower Bound}$
- 0 < $T_{\text{norm}} < 1$ if $\text{Lower Bound} < T < \text{Upper Bound}$
- $T_{\text{norm}} = 1$ if $T = \text{Upper Bound}$
- $T_{\text{norm}} > 1$ if $T > \text{Upper Bound}$ (over-temperature)
