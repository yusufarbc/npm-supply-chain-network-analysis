# NPM Supply Chain Network Analysis and Criticality Mapping


> **Mapping systemic risks in the NPM ecosystem through topology-independent analysis methods.**

This project models dependency relationships between NPM packages as a directed graph and measures structural risk using the **Behavioral Risk Score (BRS)**. The goal is to go beyond traditional vulnerability scans (CVE) and make visible systemic threats arising from a package's *position* within the network.

🔗 **Live Preview:** [yusufarbc.github.io/npm-supply-chain-network-analysis](https://yusufarbc.github.io/npm-supply-chain-network-analysis/)

---

## 💡 Key Findings

This study presents critical insights into the topological structure of the NPM ecosystem:

*   **Scale-Free Fragility:** The network exhibits scale-free properties, where targeted attacks on high-BRS nodes cause exponential collapse, while random failures have minimal impact.
*   **Systemic Fragility:** The collapse of "bridge" packages (high betweenness) that constitute less than 1% of the network threatens the accessibility of more than 40% of the ecosystem.
*   **Hidden Risks:** Attacks on unpopular but critical packages (low popularity, high centrality) are the most difficult to detect and most devastating in impact.
*   **Shai-Hulud Validation:** The developed BRS model successfully classified 85% of packages targeted in the Shai-Hulud attack as "High Risk".

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
    top_n=1000,                    # Number of packages to analyze
    leaderboard_mode="dependents",  # Mode: dependents, downloads, trending
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

*   `academic/`: Academic paper and LaTeX source files.
*   `analysis/`: Python analysis code, data fetching and processing modules.
*   `results/`: Analysis outputs (CSV, JSON, GEXF) and generated plots.
*   `media/`: Project images.

---

## 📜 License

This project is licensed under the MIT License.
