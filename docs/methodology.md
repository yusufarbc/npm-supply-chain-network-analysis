# Methodology: Topological Risk Analysis and CRS Model

### 1. Data Collection and Network Modeling

The project models the NPM ecosystem as a directed graph:
- **Nodes:** NPM packages.
- **Edges:** Inter-package dependencies.

### Sampling Strategy
Instead of analyzing the entire NPM ecosystem (3M+ packages), a **Combined Sampling Strategy** was followed to capture both infrastructural backbone and popular end-user packages:
1.  **Seed Set:** The top 1,000 packages by **Dependents** (infrastructure) AND the top 1,000 packages by **Downloads** (popularity) were selected from `ecosyste.ms`.
2.  **Merging:** These lists were combined, resulting in ~1,452 unique seed packages.
3.  **Depth Scanning:** The dependency tree of these seeds was scanned up to depth level 7.
4.  **Preprocessing:** Circular dependencies were cleaned and isolated nodes were filtered out.

As a result, a directed graph of **2,183 nodes** and **5,417 edges** (after full traversal) was constructed.

## 2. Centrality Metrics

Three fundamental metrics were used to determine the importance of packages within the network:

| Metric | Definition | Risk Context Meaning |
| :--- | :--- | :--- |
| **In-Degree** | Number of packages directly dependent on a package. | **Popularity and Impact Radius:** Shows how many projects will be directly affected in case of a vulnerability. |
| **Out-Degree** | Number of external packages a package depends on. | **Attack Surface:** Shows how exposed the package is to external threats. |
| **Betweenness** | Frequency of the package being on shortest paths between other nodes. | **Bridge Role:** Shows the package's potential to control network traffic and propagate risk. |
| **Inverted Clustering** | $1 - \text{ClusteringCoefficient}$ | **Structural Holes:** Low clustering suggests a node bridges distinct communities, increasing systemic risk. |

## 3. Behavioral Risk Score (BRS) v3

A single metric is insufficient to express complex supply chain risks. Therefore, a **Behavioral Risk Score (BRS)** was developed through weighted combination of structural and popularity metrics.

### Normalization
Each metric is normalized to the $[0,1]$ range using the Min-Max method. To focus on orders of magnitude rather than raw counts, skewed metrics (**Dependents**, **Downloads**, **Staleness**) are **Log-Normalized** before scaling:

$$ x' = \frac{\ln(1+x) - \min(\ln(1+x))}{\max(\ln(1+x)) - \min(\ln(1+x))} $$

### Formula (Structural Model)
The v3 model prioritizes **strategic position** (Betweenness) and **impact radius** (In-Degree), while accounting for **local fragility** (Inverted Clustering).

$$
\begin{aligned}
\text{BRS} = & \ 0.35 \cdot \text{Betweenness}' + 0.30 \cdot \text{In-Degree}' \\
& + 0.15 \cdot \text{ClusteringInv}' + 0.10 \cdot \text{Out-Degree}' \\
& + 0.05 \cdot \text{Dependents}' + 0.05 \cdot \text{Downloads}'
\end{aligned}
$$

### Weight Rationale
*   **Betweenness (35%):** High weight. Identifies "bridge" packages that connect different parts of the ecosystem.
*   **In-Degree (30%):** Represents direct impact radius and immediate reach within the graph.
*   **Inverted Clustering (15%):** Penalizes high redundancy; rewards nodes that bridge structural holes.
*   **Out-Degree (10%):** Represents complexity and attack surface.
*   **Dependents & Downloads (5% each):** Global popularity metrics given lower weight to prioritize hidden structural risks over raw fame.

## 4. Robustness and Cascade Analysis

The model's validity was tested through **targeted attack simulations**:
*   Packages with high BRS scores are sequentially removed from the network.
*   At each step, the network's **Largest Connected Component (LCC)** size is measured.
*   **Result:** Targeted attacks using BRS cause an **exponential decay** in network connectivity, whereas random attacks show a linear or negligible decline, proving the scale-free nature of the network.
