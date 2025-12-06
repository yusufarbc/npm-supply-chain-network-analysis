# Methodology: Topological Risk Analysis and CRS Model

This document details how the NPM supply chain network is modeled, the centrality metrics used, and the **Composite Risk Score (CRS)** calculation method.

## 1. Data Collection and Network Modeling

The project models the NPM ecosystem as a directed graph:
- **Nodes:** NPM packages.
- **Edges:** Inter-package dependencies.

### Sampling Strategy
Instead of analyzing the entire NPM ecosystem (3M+ packages), a sampling strategy focused on systemic impact was followed:
1.  **Seed Set:** The top 1,000 packages with the most *dependents* according to `ecosyste.ms` data.
2.  **Depth Scanning:** The dependency tree of these packages was scanned up to depth level 7.
3.  **Preprocessing:** Circular dependencies were cleaned and isolated nodes were filtered out.

As a result, a network consisting of approximately **1,506 nodes** and **3,058 edges** representing the backbone of the ecosystem was obtained.

## 2. Centrality Metrics

Three fundamental metrics were used to determine the importance of packages within the network:

| Metric | Definition | Risk Context Meaning |
| :--- | :--- | :--- |
| **In-Degree** | Number of packages directly dependent on a package. | **Popularity and Impact Radius:** Shows how many projects will be directly affected in case of a vulnerability. |
| **Out-Degree** | Number of external packages a package depends on. | **Attack Surface:** Shows how exposed the package is to external threats. |
| **Betweenness** | Frequency of the package being on shortest paths between other nodes in the network. | **Bridge Role:** Shows the package's potential to control network traffic and propagate risk (strategic position). |

## 3. Behavioral Risk Score (BRS)

A single metric is insufficient to express complex supply chain risks. Therefore, a **Behavioral Risk Score (BRS)** was developed through weighted combination of structural and popularity metrics.

### Normalization
Each metric is normalized to the $[0,1]$ range using the Min-Max method before calculation. Skewed metrics like Downloads and Dependents use Log-Normalization.

$$ x' = \frac{x - \min(x)}{\max(x) - \min(x)} $$

### Formula (Structural Model)
The model focuses on **topological importance** and **structural fragility**.

$$ \text{BRS} = 0.4 \cdot \text{Betweenness}' + 0.2 \cdot \text{In-Degree}' + 0.1 \cdot \text{Dependents}' + 0.1 \cdot \text{Out-Degree}' + 0.1 \cdot \text{Clustering}' + 0.1 \cdot \text{Downloads}' $$

### Weight Rationale
*   **Betweenness (40%):** Highest weight. Identifies "bridge" packages that connect different parts of the ecosystem. Their removal causes the most fragmentation.
*   **In-Degree (20%):** Represents local popularity within the analyzed graph backbone.
*   **Dependents (10%):** Represents global popularity in the wider NPM ecosystem.
*   **Out-Degree (10%):** Represents complexity and attack surface (dependency chain risk).
*   **Clustering (10%):** Inverse clustering coefficient. Low clustering indicates a structural hole (bridge role), increasing risk.
*   **Downloads (10%):** Usage intensity proxy.

## 4. Robustness and Cascade Analysis

The model's validity was tested through **targeted attack simulations**:
*   Packages with high BRS scores are sequentially removed from the network.
*   At each step, the network's **Largest Connected Component (LCC)** size is measured.
*   **Result:** Targeted attacks using BRS cause an **exponential decay** in network connectivity, whereas random attacks show a linear or negligible decline, proving the scale-free nature of the network.
