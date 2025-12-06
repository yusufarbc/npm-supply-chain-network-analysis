import os
import pandas as pd
import networkx as nx
import shutil

def export_results(risk_df, G, impact_df=None, output_dir='../results'):
    # Ensure results directory exists (at project root)
    os.makedirs(output_dir, exist_ok=True)

    print("Exporting results...")

    # 1. Full Analysis Table
    risk_df.to_csv(f'{output_dir}/risk_scores.csv', index=False)
    print(f" - Saved {output_dir}/risk_scores.csv")

    # 1b. Simplified BRS List (Package, Risk Score)
    risk_df[['package', 'risk_score']].to_csv(f'{output_dir}/package_risk_scores.csv', index=False)
    print(f" - Saved {output_dir}/package_risk_scores.csv")

    # 1c. Cascade Impact Scores (if available)
    if impact_df is not None and not impact_df.empty:
        impact_df.to_csv(f'{output_dir}/impact_scores.csv', index=False)
        print(f" - Saved {output_dir}/impact_scores.csv")

    # 1d. Top 20 Lists for Each Metric
    top_lists_dir = os.path.join(output_dir, 'top_lists')
    os.makedirs(top_lists_dir, exist_ok=True)
    
    metrics_to_export = [
        ('risk_score', 'top20_risk_score.csv', False), # False = Descending (High is good/bad)
        ('in_degree', 'top20_in_degree.csv', False),
        ('out_degree', 'top20_out_degree.csv', False),
        ('betweenness', 'top20_betweenness.csv', False),
        ('dependents_count', 'top20_dependents.csv', False),
        ('downloads', 'top20_downloads.csv', False),
        ('staleness_days', 'top20_staleness.csv', False),
        ('clustering', 'top20_clustering.csv', False) 
    ]
    
    print(f"Exporting Top 20 lists to {top_lists_dir}...")
    for col, filename, ascending in metrics_to_export:
        if col in risk_df.columns:
            top_20 = risk_df.sort_values(col, ascending=ascending).head(20)
            # Select only relevant columns for the top list
            if col == 'risk_score':
                cols_to_keep = ['package', 'risk_score']
            else:
                cols_to_keep = ['package', col, 'risk_score']
            
            top_20[cols_to_keep].to_csv(os.path.join(top_lists_dir, filename), index=False)
            print(f"   - {filename}")
            
    # Create ZIP archive of top lists
    shutil.make_archive(os.path.join(output_dir, 'top_lists'), 'zip', top_lists_dir)
    print(f" - Saved {output_dir}/top_lists.zip")

    # 2. Gephi Nodes
    # Create numeric ID map for Gephi (safer than string IDs)
    # Sort by rank/risk for consistent IDs
    sorted_nodes = risk_df.sort_values('risk_score', ascending=False)['package'].tolist()
    id_map = {pkg: i+1 for i, pkg in enumerate(sorted_nodes)}
    
    # Prepare Gephi DataFrame
    gephi_nodes = risk_df.copy()
    gephi_nodes['Id'] = gephi_nodes['package'].map(id_map)
    gephi_nodes['Label'] = gephi_nodes['package']
    
    # Rename columns to Gephi standard (CamelCase often preferred)
    col_mapping = {
        'risk_score': 'RiskScore',
        'in_degree': 'InDegree',
        'out_degree': 'OutDegree',
        'betweenness': 'Betweenness',
        # 'pagerank': 'PageRank', # Removed PageRank
        'dependents_count': 'DependentsCount',
        'downloads': 'Downloads',
        'staleness_days': 'StalenessDays',
        'clustering': 'ClusteringCoeff',
        'maintainer_risk': 'MaintainerRisk',
        # 'rank': 'Rank', # Removed Rank as it is redundant/calculated
        'type': 'Type'
    }
    gephi_nodes = gephi_nodes.rename(columns=col_mapping)
    
    # Select columns that exist
    cols_to_export = ['Id', 'Label'] + [c for c in col_mapping.values() if c in gephi_nodes.columns]
    gephi_nodes = gephi_nodes[cols_to_export]
    
    gephi_nodes.to_csv(f'{output_dir}/gephi_nodes.csv', index=False)
    print(f" - Saved {output_dir}/gephi_nodes.csv")

    # 3. Gephi Edges
    # Columns: Source, Target, Type
    gephi_edges = pd.DataFrame(list(G.edges()), columns=['Source', 'Target'])
    
    # Map Source and Target to numeric IDs
    gephi_edges['Source'] = gephi_edges['Source'].map(id_map)
    gephi_edges['Target'] = gephi_edges['Target'].map(id_map)
    
    # Filter out edges where nodes might be missing (shouldn't happen but safe)
    gephi_edges = gephi_edges.dropna()
    gephi_edges['Source'] = gephi_edges['Source'].astype(int)
    gephi_edges['Target'] = gephi_edges['Target'].astype(int)
    
    gephi_edges['Type'] = 'Directed'
    gephi_edges.to_csv(f'{output_dir}/gephi_edges.csv', index=False)
    print(f" - Saved {output_dir}/gephi_edges.csv")

    # 3b. Global Network Statistics Report
    print("Calculating global network statistics...")
    stats_file = os.path.join(output_dir, 'network_stats.txt')
    
    try:
        # Basic stats
        num_nodes = G.number_of_nodes()
        num_edges = G.number_of_edges()
        density = nx.density(G)
        
        # Connectivity
        is_strongly_connected = nx.is_strongly_connected(G)
        is_weakly_connected = nx.is_weakly_connected(G)
        num_weakly_connected_components = nx.number_weakly_connected_components(G)
        num_strongly_connected_components = nx.number_strongly_connected_components(G)
        
        # Assortativity (Degree correlation)
        try:
            degree_assortativity = nx.degree_assortativity_coefficient(G)
        except:
            degree_assortativity = float('nan')
        
        # Transitivity (Global Clustering)
        transitivity = nx.transitivity(G)
        
        # Average Clustering
        avg_clustering = nx.average_clustering(G)
        
        with open(stats_file, 'w') as f:
            f.write("=== NPM Supply Chain Network Statistics ===\n")
            f.write(f"Nodes: {num_nodes}\n")
            f.write(f"Edges: {num_edges}\n")
            f.write(f"Density: {density:.6f}\n")
            f.write(f"Is Strongly Connected: {is_strongly_connected}\n")
            f.write(f"Is Weakly Connected: {is_weakly_connected}\n")
            f.write(f"Number of Weakly Connected Components: {num_weakly_connected_components}\n")
            f.write(f"Number of Strongly Connected Components: {num_strongly_connected_components}\n")
            f.write(f"Degree Assortativity: {degree_assortativity:.6f}\n")
            f.write(f"Transitivity: {transitivity:.6f}\n")
            f.write(f"Average Clustering Coefficient: {avg_clustering:.6f}\n")
            
        print(f" - Saved {stats_file}")
        
    except Exception as e:
        print(f"Error calculating network stats: {e}")

    # 4. Generate README.md Report
    generate_results_readme(risk_df, G, impact_df, output_dir)

def generate_results_readme(risk_df, G, impact_df, output_dir):
    readme_path = f'{output_dir}/Readme.md'
    
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write("# Analysis Results\n\n")
        f.write("Automated analysis report generated by the pipeline.\n\n")
        
        # Network Statistics
        f.write("## 📊 Network Statistics\n")
        f.write(f"- **Nodes**: {G.number_of_nodes()}\n")
        f.write(f"- **Edges**: {G.number_of_edges()}\n")
        f.write(f"- **Density**: {nx.density(G):.6f}\n")
        if nx.is_directed(G):
            f.write(f"- **Strongly Connected Components**: {nx.number_strongly_connected_components(G)}\n")
            f.write(f"- **Weakly Connected Components**: {nx.number_weakly_connected_components(G)}\n")
        f.write("\n")

        # Top 20 Risk Score
        f.write("## 🚨 Top 20 Critical Packages (Risk Score)\n")
        f.write("Packages with the highest Composite Risk Score (BRS).\n\n")
        top_risk = risk_df.sort_values('risk_score', ascending=False).head(20)
        # Manual markdown table generation to avoid tabulate dependency if not present
        f.write("| Package | Risk Score | In-Degree | Betweenness |\n")
        f.write("| :--- | :--- | :--- | :--- |\n")
        for _, row in top_risk.iterrows():
            f.write(f"| {row['package']} | {row['risk_score']:.4f} | {row['in_degree']:.4f} | {row['betweenness']:.4f} |\n")
        f.write("\n")
        
        # Top 20 In-Degree
        f.write("## 🔗 Top 20 Most Depended-upon Packages (In-Degree)\n")
        f.write("Packages that have the most direct dependents in this network.\n\n")
        top_in = risk_df.sort_values('in_degree', ascending=False).head(20)
        f.write("| Package | In-Degree | Out-Degree | Risk Score |\n")
        f.write("| :--- | :--- | :--- | :--- |\n")
        for _, row in top_in.iterrows():
            f.write(f"| {row['package']} | {row['in_degree']:.4f} | {row['out_degree']:.4f} | {row['risk_score']:.4f} |\n")
        f.write("\n")

        # Top 20 Out-Degree
        f.write("## 📦 Top 20 Most Dependent Packages (Out-Degree)\n")
        f.write("Packages that have the most dependencies (highest complexity).\n\n")
        top_out = risk_df.sort_values('out_degree', ascending=False).head(20)
        f.write("| Package | Out-Degree | In-Degree | Risk Score |\n")
        f.write("| :--- | :--- | :--- | :--- |\n")
        for _, row in top_out.iterrows():
            f.write(f"| {row['package']} | {row['out_degree']:.4f} | {row['in_degree']:.4f} | {row['risk_score']:.4f} |\n")
        f.write("\n")

        # Top 20 Betweenness
        f.write("## 🌉 Top 20 Bridges (Betweenness Centrality)\n")
        f.write("Packages that act as bridges or bottlenecks in the network.\n\n")
        top_bet = risk_df.sort_values('betweenness', ascending=False).head(20)
        f.write("| Package | Betweenness | In-Degree | Risk Score |\n")
        f.write("| :--- | :--- | :--- | :--- |\n")
        for _, row in top_bet.iterrows():
            f.write(f"| {row['package']} | {row['betweenness']:.4f} | {row['in_degree']:.4f} | {row['risk_score']:.4f} |\n")
        f.write("\n")

        # Top 20 Dependents Count
        f.write("## 🌍 Top 20 Ecosystem Critical (Dependents Count)\n")
        f.write("Packages with the highest number of dependents in the entire NPM ecosystem.\n\n")
        top_dep = risk_df.sort_values('dependents_count', ascending=False).head(20)
        f.write("| Package | Dependents Count | In-Degree | Risk Score |\n")
        f.write("| :--- | :--- | :--- | :--- |\n")
        for _, row in top_dep.iterrows():
            f.write(f"| {row['package']} | {row['dependents_count']:,} | {row['in_degree']:.4f} | {row['risk_score']:.4f} |\n")
        f.write("\n")

        # Top 20 Cascade Impact (if available)
        if impact_df is not None:
            f.write("## 💥 Top 20 Cascade Impact (Network Damage)\n")
            f.write("Packages that cause the largest reduction in network connectivity (LCC) when removed.\n\n")
            top_impact = impact_df.sort_values('cascade_impact', ascending=False).head(20)
            f.write("| Package | Cascade Impact | Risk Score |\n")
            f.write("| :--- | :--- | :--- |\n")
            # Merge with risk_df to get risk score if not present
            if 'risk_score' not in top_impact.columns:
                top_impact = top_impact.merge(risk_df[['package', 'risk_score']], on='package', how='left')
            
            for _, row in top_impact.iterrows():
                f.write(f"| {row['package']} | {row['cascade_impact']:.4f} | {row.get('risk_score', 0):.4f} |\n")
            f.write("\n")
        
    print(f" - Saved {readme_path}")
