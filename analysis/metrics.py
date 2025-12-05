import networkx as nx
import pandas as pd

def calculate_risk_scores(G, betweenness_k=100):
    print("Calculating In-Degree and Out-Degree...")
    in_degree = nx.in_degree_centrality(G)
    out_degree = nx.out_degree_centrality(G)
    
    print(f"Calculating Betweenness Centrality (k={betweenness_k})...")
    # Use k parameter for approximation on large graphs
    betweenness = nx.betweenness_centrality(G, k=min(len(G), betweenness_k), normalized=True)
    
    # Create DataFrame
    data = {
        'package': list(G.nodes()),
        'in_degree': [in_degree.get(n, 0) for n in G.nodes()],
        'out_degree': [out_degree.get(n, 0) for n in G.nodes()],
        'betweenness': [betweenness.get(n, 0) for n in G.nodes()]
    }
    
    # Add metadata if available in graph nodes
    for attr in ['dependents_count', 'downloads', 'rank', 'type']:
        values = []
        for n in G.nodes():
            val = G.nodes[n].get(attr)
            # Handle missing values (e.g. for non-seed nodes)
            if val is None:
                if attr == 'type': val = 'dependency'
                elif attr == 'rank': val = 999999
                else: val = 0
            else:
                # Convert to int for numeric columns
                if attr in ['dependents_count', 'downloads', 'rank']:
                    try:
                        val = int(val)
                    except (ValueError, TypeError):
                        val = 0
            values.append(val)
        data[attr] = values
        
    df = pd.DataFrame(data)
    
    # LOGICAL CORRECTION: 
    # If a package is in our network, it has at least 'in_degree' dependents.
    # The global 'dependents_count' (from API) cannot be less than the local 'in_degree' (observed).
    # We fix 0 or low values from API using the observed local count.
    print("Applying logical correction to dependents_count...")
    raw_in_degrees = dict(G.in_degree())
    df['local_in_degree'] = df['package'].map(raw_in_degrees).fillna(0).astype(int)
    
    if 'dependents_count' in df.columns:
        # Update dependents_count to be at least the local in-degree
        df['dependents_count'] = df[['dependents_count', 'local_in_degree']].max(axis=1)
    
    # Drop the temporary column
    df = df.drop(columns=['local_in_degree'])

    # Min-Max Normalization
    print("Normalizing metrics...")
    for col in ['in_degree', 'out_degree', 'betweenness']:
        min_val = df[col].min()
        max_val = df[col].max()
        if max_val - min_val > 0:
            df[f'{col}_norm'] = (df[col] - min_val) / (max_val - min_val)
        else:
            df[f'{col}_norm'] = 0
            
    # BRS Calculation (Equal weights for all metrics)
    print("Calculating Composite Risk Score (BRS)...")
    # Normalize dependents_count
    if 'dependents_count' in df.columns:
        min_val = df['dependents_count'].min()
        max_val = df['dependents_count'].max()
        if max_val - min_val > 0:
            df['dependents_count_norm'] = (df['dependents_count'] - min_val) / (max_val - min_val)
        else:
            df['dependents_count_norm'] = 0
    
    df['risk_score'] = (
        0.25 * df['in_degree_norm'] + 
        0.25 * df['out_degree_norm'] + 
        0.25 * df['betweenness_norm'] +
        0.25 * df['dependents_count_norm']
    )
    
    # Sort by Risk Score
    df_sorted = df.sort_values(by='risk_score', ascending=False).reset_index(drop=True)
    
    return df_sorted
