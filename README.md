# NPM Supply Chain Network Analysis and Criticality Mapping


> **Mapping systemic risks in the NPM ecosystem using topological analysis methods independent of package content.**

While centralized package managers like NPM accelerate software development, the intricate web of dependencies has created a fragile ecosystem. Current security approaches often fail to detect systemic risks stemming from the network's architecture. This project maps these risks by modeling the NPM ecosystem as a directed graph and introducing the **Behavioral Risk Score (BRS)** to identify critical "bridge" nodes that form the backbone of the supply chain.

🔗 **Live Preview:** [yusufarbc.github.io/npm-supply-chain-network-analysis](https://yusufarbc.github.io/npm-supply-chain-network-analysis/)

---

## 💡 Key Findings

This study presents critical insights into the topological structure of the NPM ecosystem:

*   **Scale-Free Topology:** The network exhibits scale-free properties, meaning risk is concentrated in a small number of critical nodes that form the ecosystem's backbone.
*   **Bridge Nodes:** Packages with high *Betweenness Centrality* act as "bridges". Their compromise can propagate risks across disparate sub-clusters, even if they aren't the most downloaded.
*   **Asymmetric Risk:** There is a weak correlation between popularity (downloads) and structural importance. Security focusing only on popularity misses hidden structural risks.
*   **Robustness:** Targeted removal of high-BRS nodes leads to a destructive collapse in network integrity (exponential decay in connectivity), validating the BRS model.

---

## 📚 Documentation and Background

For the theoretical foundation of the project and case analyses, please review the following documents:

*   **[🛡️ NPM Security Landscape](docs/npm_security_landscape.md):** Active threats in the ecosystem (Typosquatting, Dependency Confusion, etc.) and why topological analysis is needed.
*   **[🐛 Case Study: Shai-Hulud](docs/shai_hulud_incident.md):** Technical analysis of the first large-scale wormable NPM attack and how the project can predict such attacks.
*   **[📚 Literature Review](docs/literature.md):** Academic studies, gap analysis, and the project's position in the literature.
*   **[📐 Methodology and BRS Model](docs/methodology.md):** Network modeling, centrality metrics used (In-Degree, Betweenness), and mathematical formula of the risk score.

---

## 🚀 Quick Start

### Prerequisites
*   Python 3.11.x (Recommended: 3.11.9)

### Installation

1.  **Clone the repository and navigate to the directory:**
    ```powershell
    git clone https://github.com/yusufarbc/npm-supply-chain-network-analysis.git
    cd npm-supply-chain-network-analysis
    ```

2.  **Set up and activate the virtual environment (Windows PowerShell):**
    ```powershell
    python -m venv .venv
    .\.venv\Scripts\Activate.ps1
    ```

3.  **Install dependencies:**
    ```powershell
    pip install -r analysis/requirements.txt
    python -m pip install notebook
    ```

4.  **Start the analysis:**
    ```powershell
    python -m notebook
    # Open the analysis/analysis.ipynb file
    ```

---

## 📊 Usage (Pipeline)

The analysis engine runs through `analysis/run_pipeline.py`. You can perform a complete analysis by running the **first cell** in the notebook.

```python
from analysis.run_pipeline import run_pipeline

# Default: Most critical infrastructure packages (Top 1000 Dependents + Depth 7)
result = run_pipeline(
    top_n=1000,                    # Number of packages (per leaderboard category)
    leaderboard_mode="combined",    # Mode: combined (dependents + downloads)
    depth=7,                        # Scanning depth
    results_dir="../results",      # Output directory
    compute_plots=True              # Generate plots
)
```

### Analysis Modes

| Mode | Parameter | Description | Use Case |
|-----|-----------|----------|---------------------|
| **Most Dependent** | `dependents` | Most depended-upon packages | **Critical Infrastructure Analysis (Default)** |
| **Most Downloaded**| `downloads` | Most downloaded packages | General popularity and traffic analysis |
| **Trending** | `trending` | Rapidly rising packages | Early warning and anomaly detection |

---

## 📂 Project Structure

*   `paper/`: Academic paper and LaTeX source files.
*   `analysis/`: Python analysis code, data fetching and processing modules.
*   `results/`: Analysis outputs (CSV, JSON, GEXF) and generated plots.
*   `docs/`: Web documentation and HTML pages.
*   `css/`: Shared styles for web pages.

---

## 📜 License

This project is licensed under the MIT License.
