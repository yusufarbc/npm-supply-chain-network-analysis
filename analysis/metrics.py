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
            values.append(val)
        data[attr] = values
        
    df = pd.DataFrame(data)
    
    # Min-Max Normalization
    print("Normalizing metrics...")
    for col in ['in_degree', 'out_degree', 'betweenness']:
        min_val = df[col].min()
        max_val = df[col].max()
        if max_val - min_val > 0:
            df[f'{col}_norm'] = (df[col] - min_val) / (max_val - min_val)
        else:
            df[f'{col}_norm'] = 0
            
    # BRS Calculation
    print("Calculating Composite Risk Score (BRS)...")
    df['risk_score'] = (
        0.5 * df['in_degree_norm'] + 
        0.2 * df['out_degree_norm'] + 
        0.3 * df['betweenness_norm']
    )
    
    # Sort by Risk Score
    df_sorted = df.sort_values(by='risk_score', ascending=False).reset_index(drop=True)
    
    return df_sorted
