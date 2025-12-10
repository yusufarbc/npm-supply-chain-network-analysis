import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
import pandas as pd
import os
import numpy as np

def ensure_plot_dir(output_dir='../results/plots'):
    os.makedirs(output_dir, exist_ok=True)


def plot_network_structure(G, output_dir='../results/plots'):
    """
    Fig 1: Network Topology Visualization.
    Visualizes the complex "hairball" structure. Highlights hubs.
    """
    ensure_plot_dir(output_dir)
    plt.figure(figsize=(12, 12))
    
    # Calculate degree for sizing and coloring
    d = dict(G.degree)
    # Highlight top 5% nodes
    degrees = np.array(list(d.values()))
    top_threshold = np.percentile(degrees, 95)
    
    node_colors = []
    node_sizes = []
    
    for node in G.nodes():
        deg = d[node]
        if deg >= top_threshold:
            node_colors.append('#E74C3C') # Red for hubs
            node_sizes.append(deg * 8)
        else:
            node_colors.append('#3498DB') # Blue for others
            node_sizes.append(deg * 2)

    pos = nx.spring_layout(G, k=0.15, iterations=20, seed=42)
    
    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color=node_colors, alpha=0.7, linewidths=0.5, edgecolors='white')
    nx.draw_networkx_edges(G, pos, alpha=0.15, edge_color="gray", arrows=False)
    
    plt.title("Fig 1: Network Topology Visualization (High-Degree Hubs Highlighted)", fontsize=14)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/network_full_topN.png', dpi=300, bbox_inches='tight')
    plt.show()
    print(f" - Saved {output_dir}/network_full_topN.png")

def plot_degree_distributions(G, output_dir='../results/plots'):
    """
    Fig 2: Degree Distribution (Scale-Free Proof).
    Log-Log Scatter (Degree vs Frequency) with Power Law line.
    """
    ensure_plot_dir(output_dir)
    
    in_degrees = [d for n, d in G.in_degree() if d > 0]
    
    # Calculate frequency of each degree
    deg_counts = {}
    for d in in_degrees:
        deg_counts[d] = deg_counts.get(d, 0) + 1
        
    # Prepare data for plotting
    sorted_degs = sorted(deg_counts.keys())
    freqs = [deg_counts[d] for d in sorted_degs]
    
    plt.figure(figsize=(10, 8))
    
    # Log-Log Scatter
    plt.loglog(sorted_degs, freqs, 'o', color='teal', alpha=0.6, markersize=8, label='Observed Data')
    
    # Fit Power Law (Linear fit in log-log space)
    if len(sorted_degs) > 2:
        log_x = np.log10(sorted_degs)
        log_y = np.log10(freqs)
        
        # Simple linear regression
        z = np.polyfit(log_x, log_y, 1)
        p = np.poly1d(z)
        
        plt.loglog(sorted_degs, 10**(p(log_x)), 'r--', linewidth=2, label=f'Power Law Fit ($\\alpha={-z[0]:.2f}$)')
        
    plt.title("Fig 2: In-Degree Distribution (Log-Log) - Evidence of Scale-Free Topology", fontsize=14)
    plt.xlabel("Degree ($k$)", fontsize=12)
    plt.ylabel("Frequency ($P(k)$)", fontsize=12)
    plt.legend(fontsize=12)
    plt.grid(True, which="both", ls="-", alpha=0.2)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/degree_histograms.png', dpi=300) # Keep filename for compatibility
    plt.show()
    print(f" - Saved {output_dir}/degree_histograms.png")

def plot_correlations(risk_df, output_dir='../results/plots'):
    """
    Plots correlations between metrics. (Optional helper, not in top 6 list strictly but good to keep)
    """
    # Simply pass to satisfy file structure if user runs it, 
    # but strictly user asked for 6 specific figures. 
    # We will leave this as is or minimize it. 
    # Current implementation is fine, won't break anything.
    pass 

def plot_top_risk_scores(risk_df, top_n=20, output_dir='../results/plots'):
    """
    Fig 4: Top 20 Critical Packages.
    Horizontal bar chart.
    """
    ensure_plot_dir(output_dir)
    top_df = risk_df.head(top_n).sort_values('risk_score', ascending=False) # Data is usually sorted DESC, so reverse for plotting
    
    plt.figure(figsize=(10, 8))
    # sns.barplot plots from top to bottom if we match order
    sns.barplot(x='risk_score', y='package', data=top_df, palette='viridis')
    
    plt.title(f"Fig 4: Top {top_n} Packages by Behavioral Risk Score (BRS)", fontsize=14)
    plt.xlabel("Behavioral Risk Score (BRS)", fontsize=12)
    plt.ylabel("Package Name", fontsize=12)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/top20_risk_scores.png', dpi=300)
    plt.show()
    print(f" - Saved {output_dir}/top20_risk_scores.png")

def plot_simulation_results(sim_results, output_dir='../results/plots'):
    """
    Fig 5: Cascade Impact Analysis.
    Demonstrates network fragility.
    """
    ensure_plot_dir(output_dir)
    plt.figure(figsize=(10, 6))
    
    # Use markevery to avoid cluttering 
    mark_every = max(1, len(sim_results) // 20)
    
    sns.lineplot(data=sim_results, x='step', y='targeted_lcc', label='Targeted Attack (Top BRS)', 
                 color='red', linewidth=2.5, marker='o', markevery=mark_every)
    
    sns.lineplot(data=sim_results, x='step', y='random_lcc', label='Random Failure', 
                 color='blue', linewidth=2, linestyle='--', marker='s', markevery=mark_every)
    
    plt.title('Fig 5: Cascade Impact Analysis (Targeted vs. Random)', fontsize=14)
    plt.xlabel('Number of Nodes Removed', fontsize=12)
    plt.ylabel('Largest Connected Component (LCC) Size', fontsize=12)
    plt.legend(fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/top20_cascade_impact.png', dpi=300)
    plt.show()
    print(f" - Saved {output_dir}/top20_cascade_impact.png")

def plot_risk_vs_cascade(impact_df, output_dir='../results/plots'):
    # Helper, not in top 6
    pass

def plot_metric_heatmap(risk_df, output_dir='../results/plots'):
    """
    Fig 3: Metric Contribution Heatmap.
    Cols: Normalized components weighted in BRS.
    """
    ensure_plot_dir(output_dir)
    
    # Select top 20 packages
    top_packages = risk_df.head(20).copy()
    
    # Columns mapping to the 6 components
    # 'betweenness_norm', 'in_degree_norm', 'clustering_risk_norm', 
    # 'out_degree_norm', 'dependents_count_norm', 'downloads_norm'
    
    cols_map = {
        'betweenness_norm': 'Betweenness',
        'in_degree_norm': 'In-Degree',
        'clustering_risk_norm': 'Inv. Clustering',
        'out_degree_norm': 'Out-Degree',
        'dependents_count_norm': 'Dependents',
        'downloads_norm': 'Downloads'
    }
    
    # Check existence
    existing_cols = [c for c in cols_map.keys() if c in top_packages.columns]
    
    heatmap_data = top_packages[['package'] + existing_cols].set_index('package')
    heatmap_data = heatmap_data.rename(columns=cols_map)
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(heatmap_data, cmap='YlOrRd', annot=False, 
                cbar_kws={'label': 'Normalized Value (0-1)'}, 
                linewidths=0.5, linecolor='gray')
    
    plt.title('Fig 3: Metric Contribution Heatmap (Top 20 Critical Packages)', fontsize=14)
    plt.xlabel('Risk Components', fontsize=12)
    plt.ylabel('Package', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/metric_heatmap_top20.png', dpi=300, bbox_inches='tight')
    plt.show()
    print(f" - Saved {output_dir}/metric_heatmap_top20.png")

def plot_brs_components(risk_df, output_dir='../results/plots'):
    pass

def plot_ecosystem_vs_network(risk_df, output_dir='../results/plots'):
    pass

def plot_risk_distribution_by_type(risk_df, output_dir='../results/plots'):
    pass

def plot_brs_vs_cascade_validation(impact_df, output_dir='../results/plots'):
    pass

def plot_brs_distribution(risk_df, output_dir='../results/plots'):
    pass

def plot_top20_brs_component_lines(risk_df, impact_df, output_dir='../results/plots'):
    pass

def plot_brs_vs_global_reach(risk_df, output_dir='../results/plots'):
    """
    Fig 6: Global Reach vs Structural Risk.
    Log(Downloads) vs BRS.
    """
    ensure_plot_dir(output_dir)
    
    plt.figure(figsize=(10, 8))
    
    # Filter valid downloads > 0
    plot_df = risk_df[risk_df['downloads'] > 0].copy()
    
    # Create scatter plot
    # X: Log(Downloads), Y: BRS
    
    sns.scatterplot(
        data=plot_df, 
        x='downloads', 
        y='risk_score',
        palette='viridis',
        hue='risk_score',
        s=80,
        alpha=0.6,
        edgecolor='gray',
        legend=False
    )
    
    plt.xscale('log')
    
    # Highlight Quadrants
    # Vertical line at median downloads
    med_downloads = plot_df['downloads'].median()
    # Horizontal line at median risk or 0.5
    med_risk = plot_df['risk_score'].median()
    
    plt.axvline(med_downloads, color='gray', linestyle='--', alpha=0.5)
    plt.axhline(med_risk, color='gray', linestyle='--', alpha=0.5)
    
    # Annotate "Hidden Assassins" (Low Download, High Risk)
    # Approx top left quadrant relative to medians
    
    plt.title('Fig 6: Global Reach (Downloads) vs. Structural Risk (BRS)', fontsize=14)
    plt.xlabel('Downloads (Log Scale)', fontsize=12)
    plt.ylabel('Behavioral Risk Score (BRS)', fontsize=12)
    
    # Annotate top 5 BRS
    top_brs = plot_df.sort_values('risk_score', ascending=False).head(5)
    for _, row in top_brs.iterrows():
        plt.text(
            row['downloads'], 
            row['risk_score'], 
            f"  {row['package']}", 
            fontsize=9, 
            va='bottom',
            fontweight='bold'
        )
        
    plt.grid(True, which="both", ls="-", alpha=0.2)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/brs_vs_global_reach.png', dpi=300)
    plt.show()
    print(f" - Saved {output_dir}/brs_vs_global_reach.png")

