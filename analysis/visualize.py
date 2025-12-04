import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
import pandas as pd
import os
import numpy as np

def ensure_plot_dir(output_dir='results/plots'):
    os.makedirs(output_dir, exist_ok=True)

def plot_network_structure(G, output_dir='results/plots'):
    """
    Plots the network structure (Fig 1 in paper).
    Note: For very large graphs, this might be cluttered.
    """
    ensure_plot_dir(output_dir)
    plt.figure(figsize=(12, 12))
    pos = nx.spring_layout(G, k=0.15, iterations=20)
    
    # Draw nodes based on degree
    d = dict(G.degree)
    node_sizes = [v * 5 for v in d.values()]
    
    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color="#3498db", alpha=0.6)
    nx.draw_networkx_edges(G, pos, alpha=0.1, edge_color="gray", arrows=False)
    
    plt.title("NPM Dependency Network Topology (Top N)")
    plt.axis('off')
    plt.savefig(f'{output_dir}/network_full_topN.png', dpi=300, bbox_inches='tight')
    plt.show()
    print(f" - Saved {output_dir}/network_full_topN.png")

def plot_degree_distributions(G, output_dir='results/plots'):
    """
    Plots In-Degree and Out-Degree histograms (Fig 2 in paper).
    """
    ensure_plot_dir(output_dir)
    in_degrees = [d for n, d in G.in_degree()]
    out_degrees = [d for n, d in G.out_degree()]
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    sns.histplot(in_degrees, bins=30, kde=True, ax=axes[0], color='teal')
    axes[0].set_title("In-Degree Distribution")
    axes[0].set_xlabel("In-Degree")
    axes[0].set_yscale("log")
    
    sns.histplot(out_degrees, bins=30, kde=True, ax=axes[1], color='orange')
    axes[1].set_title("Out-Degree Distribution")
    axes[1].set_xlabel("Out-Degree")
    axes[1].set_yscale("log")
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/degree_histograms.png', dpi=300)
    plt.show()
    print(f" - Saved {output_dir}/degree_histograms.png")

def plot_correlations(risk_df, output_dir='results/plots'):
    """
    Plots correlations between metrics (Fig 3 in paper).
    """
    ensure_plot_dir(output_dir)
    metrics = risk_df[['in_degree', 'out_degree', 'betweenness', 'risk_score']]
    
    g = sns.pairplot(metrics, diag_kind="kde", plot_kws={'alpha': 0.5})
    g.fig.suptitle("Correlation Matrix of Metrics", y=1.02)
    
    plt.savefig(f'{output_dir}/scatter_correlations.png', dpi=300)
    plt.show()
    print(f" - Saved {output_dir}/scatter_correlations.png")

def plot_top_risk_scores(risk_df, top_n=20, output_dir='results/plots'):
    """
    Plots top 20 packages by Risk Score (Fig 4 in paper).
    """
    ensure_plot_dir(output_dir)
    top_df = risk_df.head(top_n).sort_values('risk_score', ascending=True)
    
    plt.figure(figsize=(10, 8))
    sns.barplot(x='risk_score', y='package', data=top_df, palette='viridis')
    plt.title(f"Top {top_n} Packages by Composite Risk Score (BRS)")
    plt.xlabel("Risk Score")
    plt.ylabel("Package")
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/top20_risk_scores.png', dpi=300)
    plt.show()
    print(f" - Saved {output_dir}/top20_risk_scores.png")

def plot_simulation_results(sim_results, output_dir='results/plots'):
    """
    Plots the LCC decay simulation (Fig 6 in paper).
    """
    ensure_plot_dir(output_dir)
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=sim_results, x='step', y='targeted_lcc', label='Targeted Attack (Top BRS)', marker='o', color='red')
    sns.lineplot(data=sim_results, x='step', y='random_lcc', label='Random Attack', marker='x', color='grey')
    
    plt.title('Network Robustness: LCC Decay under Attack')
    plt.xlabel('Number of Nodes Removed')
    plt.ylabel('Size of Largest Connected Component (LCC)')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    
    plt.savefig(f'{output_dir}/top20_cascade_impact.png', dpi=300)
    plt.show()
    print(f" - Saved {output_dir}/top20_cascade_impact.png")

def plot_risk_vs_cascade(impact_df, output_dir='results/plots'):
    """
    Plots the correlation between BRS and Cascade Impact (Fig 5 in paper).
    """
    ensure_plot_dir(output_dir)
    plt.figure(figsize=(10, 6))
    
    sns.scatterplot(data=impact_df, x='risk_score', y='cascade_impact', 
                    hue='risk_score', palette='viridis', size='cascade_impact', sizes=(20, 200), legend=False)
    
    # Add a regression line
    sns.regplot(data=impact_df, x='risk_score', y='cascade_impact', scatter=False, color='red', line_kws={'alpha':0.5})
    
    plt.title("Correlation: Composite Risk Score (BRS) vs. Cascade Impact")
    plt.xlabel("Composite Risk Score (BRS)")
    plt.ylabel("Cascade Impact (LCC Reduction)")
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/risk_vs_cascade.png', dpi=300)
    plt.show()
    print(f" - Saved {output_dir}/risk_vs_cascade.png")
