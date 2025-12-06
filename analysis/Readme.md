## analysis/ — Run with Notebook (Single Method)

The analysis in this folder runs **only through Jupyter Notebook**. Please open the `analysis/analysis.ipynb` file and execute the cells in order.

## 🎨 Using Gephi

The analysis generates Gephi-compatible files in the `results/` directory:

### 1. `gephi_nodes.csv` (Node List)
Contains columns like `Id`, `Label`, `RiskScore`, `InDegree`, `OutDegree`, `Betweenness`, `DependentsCount`, `Downloads`, `CommunityGroup`.

### 2. `gephi_edges.csv` (Edge List)
Contains 3 columns (Source, Target, Type).

### 3. Top 20 Lists (`results/top_lists/`)
CSV files containing the top 20 packages for each metric:
- `top20_risk_score.csv`
- `top20_betweenness.csv`
- `top20_in_degree.csv`
- ...and others.

### 4. Network Statistics (`results/network_stats.txt`)
A text report containing global network metrics such as Density, Transitivity, Assortativity, and Component counts.

### Opening in Gephi

1. **Import Nodes:**
   - File → Import spreadsheet...
   - File: `gephi_nodes.csv`
   - Separator: Comma
   - Import as: Nodes table
   - Force nodes to be created as new ones: ✓

2. **Import Edges:**
   - File → Import spreadsheet...
   - File: `gephi_edges.csv`
   - Separator: Comma
   - Import as: Edges table
   - Create missing nodes: ✗ (nodes already exist)

### Visualization Recommendations

- **Layout:** Force Atlas 2 (Scaling: 10.0, Prevent Overlap: ✓)
- **Node Size:** Ranking → InDegree or Betweenness
- **Node Color:** Partition → CommunityGroup (for clusters) OR Ranking → RiskScore (Green-Red)

## 🎯 Goal

Criticality mapping in the software supply chain: Analyzing the topological risk of the NPM ecosystem using **complex network theory**:

1. **Data Collection:** Fetch the most popular NPM packages and their dependencies
2. **Network Construction:** Create a directed dependency graph (Dependent → Dependency)
3. **Metric Calculation:** In-degree, out-degree, betweenness centrality, clustering, community detection
4. **Risk Scoring:** Generate Behavioral Risk Score (BRS) using weighted structural metrics
5. **Expansion (Optional):** Add packages dependent on Top N (1st degree expansion)

## 📊 Data Source

### Three Different Data Sources and Limits

#### 1. ecosyste.ms Leaderboard API (Tier 0 - Initial Seed List)
- **URL:** `https://ecosyste.ms/api/v1/registry/npm/leaderboard`
- **Limit:** Max **2000 packages** → This limit applies **ONLY** to the initial list (Tier 0)!
- **Usage:** `top_n` and `leaderboard_mode` parameters
- **Ranking Modes:**
  - `downloads`: By download count (default)
  - `dependents`: Most depended-upon packages
  - `trending`: Packages with sudden download spikes
- **Example:** `top_n=1000, leaderboard_mode="dependents"` → Top 1000 most critical packages

**IMPORTANT:** This 2000 limit is not for the entire graph, only for the Top N selection!

**Leaderboard Mode Comparison:**

| Mode | What it Measures | Advantage | Disadvantage | Use Case |
|-----|----------|---------|------------|---------------------|
| `downloads` | Weekly download volume | Widespread usage → Broad impact | Popularity ≠ criticality | General ecosystem analysis |
| `dependents` | How many packages depend on it | High infrastructure criticality | Low volatility | **Criticality mapping** ⭐ |
| `trending` | Sudden growth rate | Early signal, anomaly detection | Short-term volatile | Supply chain monitoring |

**Recommendation:** Use `leaderboard_mode="dependents"` for criticality analysis!

#### 2. NPM Registry (Tier 1, 2, 3... - Unlimited Dependencies)
- **URL:** `https://registry.npmjs.org/{package}`
- **Limit:** **Unlimited!** Dependencies can be fetched for every package
- **Usage:** Controlled by `depth` parameter
- **Version:** Latest tag or most current version
- **Field:** `dependencies` (optional: `peerDependencies`)
- **Cache:** `results/cache_deps.json` (prevents re-queries)

**How the depth Parameter Works:**
```
top_n=1000, depth=1:
  Tier 0: 1000 packages (ecosyste.ms - max 2000)
  Tier 1: ~3K-5K packages (NPM Registry - unlimited)
  Total: ~4K-6K nodes

top_n=1000, depth=2:
  Tier 0: 1000 packages (ecosyste.ms - max 2000)
  Tier 1: ~3K-5K packages (NPM Registry - unlimited)
  Tier 2: ~8K-15K packages (NPM Registry - unlimited)
  Total: ~12K-20K nodes

top_n=1000, depth=7:
  Tier 0: 1000 packages (ecosyste.ms - max 2000)
  Tier 1-7: ~50K-100K packages (NPM Registry - unlimited)
  Total: ~50K-100K nodes (!!!) - Not Recommended
```

**Result:** With 1000 packages and depth=7 → 10K-50K nodes are possible!

#### 3. Libraries.io API (Dependents - Rate Limited)
- **URL:** `https://libraries.io/api/npm/{package}/dependents`
- **Limit:** Rate limited (~60 requests/minute)
- **Usage:** Activated with `expand_with_dependents=True` parameter
- **Direction:** Reverse dependency (who uses this package?)
- **Feature:** Slow but shows dependent relationships

## 📁 Contents

- **`analysis.ipynb`** — Step-by-step data fetching, graph construction, metrics, and visualization (the only way to run)
- **`analysis_helpers.py`** — API, cache, metric, and visualization helpers
- **`run_pipeline.py`** — Full pipeline orchestrator (called from notebook)
- **`exporter.py`** — Gephi export functions
- **`make_tables.py`** — LaTeX table generators
- **`requirements.txt`** — Runtime dependencies
- **`GEPHI_GUIDE.md`** — Gephi visualization guide
- **`regenerate_exports.py`** — Script to safely regenerate data exports

## 🔄 How it Works

The analysis pipeline consists of the following steps:

```
┌─────────────────────────────────────────────┐
│  1. Top N Package List (Leaderboard API)    │
│     • Three modes: downloads/dependents/trending │
│     • MAX 2000 packages (Tier 0 seed list)  │
│     • This limit refers ONLY to the initial list! │
│     • Recommended: leaderboard_mode=dependents │
└──────────────────┬──────────────────────────┘
                   ↓
┌─────────────────────────────────────────────┐
│  2. Fetch Dependencies (NPM Registry)       │
│     • Get package.json for each package     │
│     • Control Tier with depth parameter     │
│     • Tier 1, 2, ... are fetched UNLIMITED  │
│     • Prevent re-queries with Cache         │
└──────────────────┬──────────────────────────┘
                   ↓
┌─────────────────────────────────────────────┐
│  3. Build Directed Graph (NetworkX)         │
│     • Edge: Dependent → Dependency          │
│     • Node count varies by depth:           │
│       - depth=1: ~3K-5K nodes               │
│       - depth=2: ~8K-15K nodes              │
│       - depth=7: ~50K-100K nodes (!!!)      │
└──────────────────┬──────────────────────────┘
                   ↓
┌─────────────────────────────────────────────┐
│  4. Compute Metrics                         │
│     • In-Degree: Impact domain (dependent)  │
│     • Out-Degree: Complexity (dependency)   │
│     • Betweenness: Bridge role (k=200)      │
└──────────────────┬──────────────────────────┘
                   ↓
┌─────────────────────────────────────────────┐
│  5. Risk Scoring (V3 Model)                 │
│     Risk = 0.35×Btw + 0.30×In + 0.15×Clust  │
│          + 0.10×Out + 0.10×Global           │
│     • Identify most critical packages       │
│     • Combined: Infrastructure + Popularity │
│       - Dependents, Downloads, Staleness    │
│         (Log-Normalized)                    │
└──────────────────┬──────────────────────────┘
                   ↓
┌─────────────────────────────────────────────┐
│  6. Export & Visualization                  │
│     • CSV: edges, metrics, risk_scores      │
│     • Gephi: nodes.csv + edges.csv          │
│     • PNG/SVG: Distribution and top N plots │
└─────────────────────────────────────────────┘
```

**Expected Results (based on depth and leaderboard_mode):**

| top_n | mode | depth | Nodes | Edges | Time | Description |
|-------|------|-------|-------|-------|------|-------------|
| 1000 | dependents | 1 | ~3K-5K | ~8K-12K | 2-3 min | **⭐ Recommended** (critical infrastructure) |
| 1000 | downloads | 1 | ~3K-5K | ~8K-12K | 2-3 min | Widespread usage analysis |
| 1000 | trending | 1 | ~2K-4K | ~5K-10K | 2-3 min | Early warning (volatile) |
| 1000 | dependents | 2 | ~8K-15K | ~25K-40K | 5-10 min | Deep criticality analysis |
| 2000 | dependents | 1 | ~6K-10K | ~15K-25K | 5-8 min | Max seed (ecosyste.ms limit) |

**Critical Packages (by mode):**
- `dependents`: tslib, @smithy/types, @babel/helper-plugin-utils (high in-degree)
- `downloads`: react, lodash, chalk (common usage)
- `trending`: Newly rising packages (volatile, early detection)

**ATTENTION:**
- ecosyste.ms's 2000 limit is **only for Tier 0**
- Tier 1, 2, 3... are fetched **unlimited** from NPM Registry
- depth > 2 is not recommended (exponential growth)

## ⚠️ Technical Challenges and Limitations

### 1. Lack of Dependent (Reverse Dependency) Data

**Problem:** Finding **who uses** a package (dependents) in the NPM ecosystem is technically difficult.

#### 1.1 Libraries.io API Disabled
```
❌ https://libraries.io/api/npm/{package}/dependents
→ {"message": "Disabled for performance reasons"}
```
- **Explanation:** Libraries.io has **disabled** the `/dependents` endpoint due to performance reasons
- **Tested:** Verified on 2025-11-23 (on popular packages like react, lodash)
- **Impact:** 1st degree dependent data cannot be fetched via API

#### 1.2 No Reverse Dependency in NPM Registry API
- NPM Registry only provides **forward dependencies**
- Finding who uses a package requires **scanning all 3.6M+ packages**
- **Cost:** Unacceptably slow and API rate limit issues

#### 1.3 Current Solution: In-Degree Metric
✅ **Alternative approach:** We fetch dependencies of Top N packages and use the **in-degree** (how many Top N packages depend on it) metric of each dependency for **indirect dependent analysis**.

**Example:**
```
react → loose-envify  (react depends on loose-envify)
babel → loose-envify  (babel depends on loose-envify)
→ loose-envify's in-degree = 2 (2 packages dependent on it)
```

**Result:** Instead of full dependent data, **in-degree metric is sufficient to detect critical packages**.

### 2. Network Size and Computational Performance

#### 2.1 Cost of Second Tier Dependencies
- **Tier 1:** Top 1000 packages → ~1200-1500 nodes, ~2000-4000 edges
- **Tier 2:** + Dependencies of dependencies → ~10K-50K nodes, ~100K+ edges
- **Problem:** Betweenness centrality calculation is O(n³) complexity, can take hours on large graphs

#### 2.2 Current Solution: Sampling and Tier 1 Limit
```python
# k-node sampling for Betweenness
btw = nx.betweenness_centrality(G, k=200, normalized=True)

# Only 1st tier dependencies (2nd tier disabled)
G, top_set = build_dependency_graph(top_packages, expand_with_dependents=False)
```

### 3. API Rate Limiting and Reliability

#### 3.1 Ecosyste.ms API
- **Limit:** Max 1000 packages/page, total ~2000-5000 packages can be fetched
- **Sorting:** By download count, but may not be up-to-date
- **Problem:** Rare timeout or empty response cases

#### 3.2 NPM Registry
- **Rate Limit:** Unlimited (public endpoint) but slow
- **Reliability:** 99%+ uptime, but network errors can occur
- **Solution:** 3-retry mechanism and local cache

#### 3.3 Cache Strategy
```python
cache_deps.json  # Dependencies cache for each package
→ No API query on rerun (fast test)
```

### 4. Data Quality and Completeness

#### 4.1 Deprecated and Old Packages
- **Problem:** Top N list may contain deprecated or unmaintained packages
- **Impact:** Risk analysis may not be current
- **Example:** Removed packages like left-pad

#### 4.2 Exclusion of PeerDependencies
- **Default:** Only `dependencies` are fetched
- **Optional:** Can be activated with `include_peer_deps=True`
- **Problem:** If PeerDeps are included, graph grows too large, noise increases

## 🔧 Installation

### Windows PowerShell
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r analysis/requirements.txt
python -m pip install notebook
```

### macOS/Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r analysis/requirements.txt
python -m pip install notebook
```

## 🚀 Starting the Notebook

```bash
python -m notebook
```
Then open `analysis/analysis.ipynb` and run cells in order.

### ⚡ Quick Start (Single Cell)

Run the first code cell in Notebook - entire pipeline runs automatically:

```python
from analysis.run_pipeline import run_pipeline

# Standard analysis (Top 1000)
result = run_pipeline(
    top_n=1000,
    results_dir="../results",
    compute_plots=True
)
```

**This single command does the following:**
1. ✅ Fetches Top N package list (ecosyste.ms API)
2. ✅ Fetches dependencies for each package (npm registry + cache)
3. ✅ Builds directed graph (NetworkX DiGraph)
4. ✅ Computes metrics (degree, betweenness)
5. ✅ Generates risk scores
6. ✅ Automatically generates Gephi CSV files ⭐
7. ✅ Creates visualizations (PNG+SVG)
8. ✅ Prepares LaTeX tables

## 🔄 Two Types of Network Expansion

### 📌 Key Difference: depth vs expand_with_dependents

| Feature | **depth=N** | **expand_with_dependents=True** |
|---------|-------------|----------------------------------|
| **Direction** | Forward (→) | Backward (←) + Forward |
| **Question** | "What does this package depend on?" | "Who uses this package?" |
| **API** | NPM Registry | Libraries.io + NPM Registry |
| **Limit** | **Unlimited** (NPM Registry) | Rate limited (~60/min) |
| **2000 Limit** | **Only for Tier 0** | **Only for Tier 0** |
| **Speed** | Fast (2-10 min) | Slow (30 min - 2 hours) |
| **Node Growth** | Controlled (exponential) | Very large (depends on dependent count) |
| **Usage** | **Default - Recommended** | Special analysis (dependent map) |

---

### Mode 1: Dependency Chaining (depth parameter) **[RECOMMENDED]**

**Direction:** Forward → "What does this package depend on?"

```
Tier 0: [react, lodash, webpack] (Top 1000 - ecosyste.ms)
    ↓ (dependencies - NPM Registry)
Tier 1: [prop-types, scheduler, ...] (~3K packages - UNLIMITED)
    ↓ (dependencies - with depth=2)
Tier 2: [object-assign, fbjs, ...] (~8K packages - UNLIMITED)
    ↓ (with depth=3)
Tier 3: [...] (~20K packages - UNLIMITED)
```

**Example:**
```python
result = run_pipeline(
    top_n=1000,     # Top 1000 from ecosyste.ms (Tier 0)
    depth=2,        # Fetch Tier 1 + Tier 2 dependencies
)
# Tier 0: 1000 packages (ecosyste.ms limit)
# Tier 1: ~3K packages (NPM Registry - unlimited)
# Tier 2: ~8K packages (NPM Registry - unlimited)
# Total: ~12K nodes
```

**Data Source:** NPM Registry (unlimited, fast)
**2000 Limit:** Applies only to Tier 0 seed list, Tier 1+ is unlimited!

---

### Mode 2: Dependent Expansion (expand_with_dependents) **[SPECIAL USE]**

**Direction:** Backward (←) + Forward → "Who uses this package?"

```
Top N Packages: [react, lodash, ...]
    ↑ (who uses it? - Libraries.io API)
Dependents: [gatsby, next, create-react-app, ...]
    ↓ (dependencies - NPM Registry)
Dependencies of Dependents: [...]
```

**Example:**
```python
result = run_pipeline(
    top_n=2000,                      # Max 2000 (ecosyste.ms limit)
    expand_with_dependents=True,     # 🆕 Dependent addition ON
    max_packages_to_expand=500,      # Fetch dependents for first 500 packages
    max_dependents_per_package=20,   # Max 20 dependents per package
)
# Top 2000 + 20 dependents for each + dependencies of dependents
# Total: ~15K-30K nodes
```

**Data Source:** Libraries.io API (rate limited, slow)
**Result:** Graph grows very large, dependent relationships become visible

### How it Works?

```python
result = run_pipeline(
    top_n=2000,                        # Top 2000 packages (ecosyste.ms max 2K)
    expand_with_dependents=True,       # 🔄 Expansion ON
    max_packages_to_expand=500,        # Fetch dependents for first 500 packages
    max_dependents_per_package=20,     # Max 20 dependents per package
    results_dir="../results"
)
```

### Expansion Steps:

1. **Phase 1:** Add dependencies of Top N packages (normal)
   ```
   react → [react-dom, prop-types, ...]
   lodash → []
   ```

2. **Phase 2:** Fetch dependents for first `max_packages_to_expand` packages
   ```
   Libraries.io API: "who uses react?"
   → [gatsby, next, create-react-app, ...]
   ```

3. **Phase 3:** Add these dependent packages to graph as nodes
   ```
   gatsby → react (add edge)
   next → react (add edge)
   ```

4. **Phase 4:** Fetch dependencies of dependent packages
   ```
   gatsby → [react, webpack, babel, ...]
   next → [react, styled-jsx, ...]
   ```

### Why the Limit?

- **Libraries.io rate limit:** ~60 requests/minute
- **2000 packages × 50 dependents** = 100K API calls = **28+ hours!** 😱
- **Solution:** Control with `max_packages_to_expand` and `max_dependents_per_package`

### Recommended Settings (depth vs expand_with_dependents):

#### 🚀 Standard Analysis (depth parameter - Recommended)

| Scenario | top_n | depth | Time | Nodes | Edges | Description |
|---------|-------|-------|------|-------|-------|-------------|
| **Test** | 100 | 1 | 1 min | ~500-800 | ~1K-2K | Fast test |
| **Small** | 500 | 1 | 2 min | ~2K-3K | ~5K-8K | Basic analysis |
| **Medium** | 1000 | 1 | 3-5 min | ~3K-5K | ~8K-12K | **Recommended** |
| **Deep** | 1000 | 2 | 8-15 min | ~8K-15K | ~25K-40K | Advanced analysis |
| **Max Seed** | 2000 | 1 | 5-8 min | ~6K-10K | ~15K-25K | ecosyste.ms max |
| ⚠️ **Explosion** | 1000 | 7 | 1-2 hours | ~50K-100K | ~200K+ | **Not Recommended!** |

#### 🔬 Dependent Expansion (expand_with_dependents - Special)

| Scenario | top_n | max_expand | max_deps | Time | Nodes | Description |
|---------|-------|------------|----------|------|-------|-------------|
| **Test** | 100 | 50 | 10 | 5-10 min | ~800-1200 | Dependent test |
| **Small** | 500 | 200 | 15 | 20-30 min | ~3K-6K | Dependent analysis |
| **Medium** | 1000 | 500 | 20 | 1-1.5 hours | ~8K-15K | Dependent map |
| **Large** | 2000 | 1000 | 20 | 2-3 hours | ~15K-30K | Full dependent network |

⚠️ **IMPORTANT:**
- **ecosyste.ms limit (2000):** Only for **Tier 0** (initial seed list)!
- **NPM Registry:** Can fetch **unlimited** dependencies for Tier 1, 2, 3...
- **depth parameter:** Fetches unlimited tiers, but depth>2 is not recommended due to exponential growth
- **expand_with_dependents:** Slow due to Libraries.io rate limit, for special use

## 📦 Outputs

All files are written to the `results/` directory.

### 🎯 Main Output Files

#### 1. Gephi Visualization (Automatically Generated) ⭐
- **`gephi_edges.csv`** — ID-based edge list (Source, Target, Type, Weight)
- **`gephi_nodes.csv`** — ID-based node list (Id, Label, metrics)
- **Usage:** Gephi → Import spreadsheet (detail: `GEPHI_GUIDE.md`)

#### 2. Raw Data Files
- **`edges.csv`** — Edge list (source=dependent, target=dependency)
- **`metrics.csv`** — Metrics for all packages
- **`risk_scores.csv`** — Composite risk scores
- **`graph_stats.json`** — General network statistics
- **`cache_deps.json`** — Dependency cache (prevents re-queries)

#### 3. Analysis Outputs
- **`edge_betweenness_top10.csv`** — Highest bridge edges
- **`cascade_impact_top20.csv`** — Reverse direction (dependents) cascade impact
- **`metrics_top20_*.tex`** — LaTeX tables (in_degree, out_degree, betweenness)
- **`risk_scores_top20.tex`** — Riskiest 20 packages table

#### 4. Visualizations (PNG + SVG)
```
results/plots/
├── in_degree_distribution.png
├── out_degree_distribution.png
├── betweenness_distribution.png
├── risk_score_distribution.png
├── top10_in_degree.png
├── top20_risk_scores.png
└── *.svg (vector versions)
```

## 💡 Tips and Optimization

### For Large Graphs
- **Betweenness sampling:** `sample_k=200` (for 1000+ nodes)
- **Expansion limit:** `max_packages_to_expand=500` (for rate limit)
- **Disable plots:** `compute_plots=False` (faster)

### Cache Management
```python
# Clear cache (to fetch new data)
import os
os.remove("results/cache_deps.json")
```

### Reproducibility
```python
# Random seed fixed
np.random.seed(42)
nx.betweenness_centrality(G, k=200, seed=42)
```

## 🔧 Module Structure
```
analysis/
├── analysis.ipynb              # Main notebook (single entry point)
├── run_pipeline.py             # Orchestrator (single function: run_pipeline)
├── analysis_helpers.py         # Core functions
│   ├── fetch_top_packages()    # Fetch Top N list
│   ├── fetch_dependencies()    # Fetch dependencies
│   ├── fetch_dependents()      # Fetch dependents (expansion)
│   ├── build_dependency_graph()# Build graph
│   ├── compute_metrics()       # Compute metrics
│   ├── compute_risk_scores()   # Risk scores
│   ├── estimate_cascade_impact() # Cascade analysis
│   ├── plot_*()                # Visualizations
│   └── save_*()                # Write files
├── exporter.py                 # Gephi exporter
├── make_tables.py              # LaTeX table generators
├── GEPHI_GUIDE.md              # Gephi guide
├── requirements.txt            # Python dependencies
└── Readme.md                   # This file
```
