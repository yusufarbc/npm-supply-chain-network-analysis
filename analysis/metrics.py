import networkx as nx
import pandas as pd
import numpy as np
from datetime import datetime, timezone

def calculate_risk_scores(G, betweenness_k=100):
    """
    Calculates BRS with Abandonware, Clustering, and Downloads.
    """
    print("Calculating network metrics...")
    
    # 1. Basic Centrality
    in_degree = dict(G.in_degree())
    out_degree = dict(G.out_degree())
    
    # 2. Betweenness
    if betweenness_k and betweenness_k < len(G):
        print(f"Approximating betweenness centrality (k={betweenness_k})...")
        betweenness = nx.betweenness_centrality(G, k=betweenness_k)
    else:
        print("Calculating exact betweenness centrality...")
        betweenness = nx.betweenness_centrality(G)

    # 3. Clustering Coefficient (Local Fragility)
    # Low clustering = Structural Hole (Bridge) = High Risk
    print("Calculating clustering coefficient...")
    clustering = nx.clustering(G)

    # 4. Extract Metadata Metrics
    dependents_count = {}
    downloads = {}
    maintainer_risk = {}
    staleness_days = {} # NEW: Days since last update
    
    now = datetime.now(timezone.utc)
    
    for node in G.nodes():
        data = G.nodes[node]
        
        # Dependents
        try: dependents_count[node] = int(float(data.get('dependents_count', 0)))
        except: dependents_count[node] = 0
            
        # Downloads
        try: downloads[node] = int(float(data.get('downloads', 0)))
        except: downloads[node] = 0
            
        # Maintainer Risk (1 / count)
        try:
            m_count = int(float(data.get('maintainers_count', 1)))
            maintainer_risk[node] = 1.0 / m_count if m_count > 0 else 1.0
        except:
            maintainer_risk[node] = 1.0
            
        # Staleness (Abandonware Risk)
        last_mod_str = data.get('last_modified', '')
        days_diff = 0
        if last_mod_str:
            try:
                # Parse ISO format (e.g., 2023-10-05T14:30:00.000Z)
                last_mod_date = datetime.fromisoformat(last_mod_str.replace('Z', '+00:00'))
                days_diff = (now - last_mod_date).days
            except:
                days_diff = 365 # Default to 1 year if parse fails
        else:
            days_diff = 365 # Default
        
        staleness_days[node] = max(0, days_diff)

    # --- Normalization ---
    def normalize(metric_dict):
        values = np.array(list(metric_dict.values()))
        if len(values) == 0: return metric_dict
        min_val = np.min(values)
        max_val = np.max(values)
        if max_val == min_val: return {k: 0 for k in metric_dict}
        return {k: (v - min_val) / (max_val - min_val) for k, v in metric_dict.items()}

    def log_normalize(metric_dict):
        values = np.array(list(metric_dict.values()))
        if len(values) == 0: return metric_dict
        # Log1p transformation
        log_values = np.log1p(values)
        min_val = np.min(log_values)
        max_val = np.max(log_values)
        if max_val == min_val: return {k: 0 for k in metric_dict}
        
        norm_dict = {}
        for k, v in metric_dict.items():
            norm_dict[k] = (np.log1p(v) - min_val) / (max_val - min_val)
        return norm_dict

    norm_in = normalize(in_degree)
    norm_out = normalize(out_degree)
    norm_bet = normalize(betweenness)
    norm_maint = normalize(maintainer_risk)
    
    # Log Normalization for skewed data
    norm_deps = log_normalize(dependents_count)
    norm_downloads = log_normalize(downloads) # NEW
    norm_staleness = log_normalize(staleness_days) # NEW (Time is also skewed)
    
    # Inverse Clustering (Low Clustering = High Risk)
    norm_clustering_risk = {}
    for k, v in clustering.items():
        norm_clustering_risk[k] = 1.0 - v # Invert

    # --- BRS Calculation (Updated Formula - Balanced) ---
    # Weights:
    # POPULARITY (30%):
    #   In-Degree: 10%
    #   Dependents: 10%
    #   Downloads: 10%
    # STRUCTURE (40%):
    #   Betweenness: 20% (Critical Bridge Role)
    #   Clustering: 10% (Structural Fragility)
    #   Out-Degree: 10% (Complexity)
    # LIFECYCLE (30%):
    #   Staleness: 20% (Abandonware Risk)
    #   Maintainer: 10% (Bus Factor)
    
    risk_scores = {}
    for node in G.nodes():
        score = (
            # Popularity
            0.10 * norm_in.get(node, 0) +
            0.10 * norm_deps.get(node, 0) +
            0.10 * norm_downloads.get(node, 0) +
            # Structure
            0.20 * norm_bet.get(node, 0) +
            0.10 * norm_clustering_risk.get(node, 0) +
            0.10 * norm_out.get(node, 0) +
            # Lifecycle
            0.20 * norm_staleness.get(node, 0) +
            0.10 * norm_maint.get(node, 0)
        )
        risk_scores[node] = score

    # Create DataFrame
    df = pd.DataFrame({
        'package': list(G.nodes()),
        'risk_score': [risk_scores[n] for n in G.nodes()],
        'in_degree': [in_degree[n] for n in G.nodes()],
        'out_degree': [out_degree[n] for n in G.nodes()],
        'betweenness': [betweenness[n] for n in G.nodes()],
        'clustering': [clustering[n] for n in G.nodes()], # Raw clustering
        'dependents_count': [dependents_count.get(n, 0) for n in G.nodes()],
        'downloads': [downloads.get(n, 0) for n in G.nodes()],
        'staleness_days': [staleness_days.get(n, 0) for n in G.nodes()],
        'maintainer_risk': [maintainer_risk.get(n, 0) for n in G.nodes()],
        
        # Normalized columns for visualization
        'in_degree_norm': [norm_in.get(n, 0) for n in G.nodes()],
        'out_degree_norm': [norm_out.get(n, 0) for n in G.nodes()],
        'betweenness_norm': [norm_bet.get(n, 0) for n in G.nodes()],
        'dependents_count_norm': [norm_deps.get(n, 0) for n in G.nodes()],
        'downloads_norm': [norm_downloads.get(n, 0) for n in G.nodes()],
        'staleness_norm': [norm_staleness.get(n, 0) for n in G.nodes()],
        'clustering_risk_norm': [norm_clustering_risk.get(n, 0) for n in G.nodes()],
        
        'type': [G.nodes[n].get('type', 'unknown') for n in G.nodes()]
    })
    
    # Rank calculation
    df = df.sort_values('dependents_count', ascending=False)
    df['rank'] = range(1, len(df) + 1)
    
    return df.sort_values('risk_score', ascending=False)
