import networkx as nx
import random
import pandas as pd
from tqdm.notebook import tqdm

def simulate_attacks(G, risk_df, num_removals=50):
    # Prepare targets
    targets_targeted = risk_df['package'].head(num_removals).tolist()
    targets_random = random.sample(list(G.nodes()), min(len(G), num_removals))
    
    # Simulation results
    results = {
        'step': list(range(num_removals + 1)),
        'targeted_lcc': [],
        'random_lcc': []
    }
    
    # Initial LCC
    initial_lcc = len(max(nx.connected_components(G.to_undirected()), key=len))
    results['targeted_lcc'].append(initial_lcc)
    results['random_lcc'].append(initial_lcc)
    
    print(f"Running simulations (Targeted vs Random) for {num_removals} steps...")
    
    # Targeted Simulation
    G_target = G.copy()
    for node in tqdm(targets_targeted, desc="Targeted Attack"):
        if node in G_target:
            G_target.remove_node(node)
        if len(G_target) > 0:
            lcc = len(max(nx.connected_components(G_target.to_undirected()), key=len))
        else:
            lcc = 0
        results['targeted_lcc'].append(lcc)
        
    # Random Simulation
    # IMPORTANT: We run multiple random simulations and average them to get a stable baseline
    # A single random run can be misleading if it accidentally hits a hub
    random_runs = 5
    avg_random_lcc = [0] * (num_removals + 1)
    
    print(f"Running {random_runs} random simulations to average...")
    
    for run in range(random_runs):
        G_random = G.copy()
        # Resample random targets for each run
        current_random_targets = random.sample(list(G.nodes()), min(len(G), num_removals))
        
        # Initial state for this run
        lcc = len(max(nx.connected_components(G_random.to_undirected()), key=len))
        avg_random_lcc[0] += lcc
        
        for i, node in enumerate(current_random_targets):
            if node in G_random:
                G_random.remove_node(node)
            
            if len(G_random) > 0:
                lcc = len(max(nx.connected_components(G_random.to_undirected()), key=len))
            else:
                lcc = 0
            avg_random_lcc[i+1] += lcc
            
    # Calculate average
    results['random_lcc'] = [x / random_runs for x in avg_random_lcc]
        
    return pd.DataFrame(results)

def calculate_single_node_impact(G, risk_df, sample_size=100):
    """
    Calculates the impact of removing a single node on the LCC size.
    Returns a DataFrame with risk scores and impact values.
    """
    initial_lcc = len(max(nx.connected_components(G.to_undirected()), key=len))
    
    # Select top N nodes by risk score to analyze
    # (Analyzing all nodes might be too slow for large graphs)
    targets = risk_df.head(sample_size).copy()
    
    impacts = []
    print(f"Calculating single-node cascade impact for top {sample_size} nodes...")
    
    for _, row in tqdm(targets.iterrows(), total=len(targets), desc="Impact Analysis"):
        node = row['package']
        if node not in G:
            impacts.append(0)
            continue
            
        # Create a temporary view/copy with the node removed
        # Note: G.copy() is safer but slower. For 1500 nodes it's fine.
        G_temp = G.copy()
        G_temp.remove_node(node)
        
        if len(G_temp) > 0:
            new_lcc = len(max(nx.connected_components(G_temp.to_undirected()), key=len))
        else:
            new_lcc = 0
            
        # Impact is the reduction in LCC size
        impact = initial_lcc - new_lcc
        impacts.append(impact)
        
    targets['cascade_impact'] = impacts
    return targets
