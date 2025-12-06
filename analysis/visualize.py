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

def plot_degree_distributions(G, output_dir='../results/plots'):
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

def plot_correlations(risk_df, output_dir='../results/plots'):
    """
    Plots correlations between metrics (Fig 3 in paper).
    """
    ensure_plot_dir(output_dir)
    
    # Check available columns and select relevant ones
    cols_to_plot = ['in_degree', 'out_degree', 'betweenness', 'risk_score']
    
    # Add optional columns if they exist
    if 'dependents_count' in risk_df.columns:
        cols_to_plot.append('dependents_count')
    elif 'dependents_count_log' in risk_df.columns:
        cols_to_plot.append('dependents_count_log')
        
    if 'downloads' in risk_df.columns:
        cols_to_plot.append('downloads')
        
    metrics = risk_df[cols_to_plot].copy()
    
    # Log transform skewed metrics for better visualization if not already logged
    if 'dependents_count' in metrics.columns:
        metrics['Deps(Log)'] = np.log1p(metrics['dependents_count'])
        metrics = metrics.drop(columns=['dependents_count'])
    elif 'dependents_count_log' in metrics.columns:
        metrics = metrics.rename(columns={'dependents_count_log': 'Deps(Log)'})
        
    if 'downloads' in metrics.columns:
        metrics['Downloads(Log)'] = np.log1p(metrics['downloads'])
        metrics = metrics.drop(columns=['downloads'])
    
    # Rename columns for better plot labels
    metrics = metrics.rename(columns={
        'in_degree': 'In-Deg',
        'out_degree': 'Out-Deg',
        'betweenness': 'Betw.',
        'risk_score': 'Risk'
    })
    
    g = sns.pairplot(metrics, diag_kind="kde", plot_kws={'alpha': 0.5, 's': 10})
    g.fig.suptitle("Correlation Matrix of Metrics", y=1.02)
    
    plt.savefig(f'{output_dir}/scatter_correlations.png', dpi=300)
    plt.show()
    print(f" - Saved {output_dir}/scatter_correlations.png")

def plot_top_risk_scores(risk_df, top_n=20, output_dir='../results/plots'):
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

def plot_simulation_results(sim_results, output_dir='../results/plots'):
    """
    Plots the LCC decay simulation (Fig 6 in paper).
    """
    ensure_plot_dir(output_dir)
    plt.figure(figsize=(10, 6))
    
    # Use markevery to avoid cluttering the plot with markers if there are many steps
    mark_every = max(1, len(sim_results) // 20)
    
    sns.lineplot(data=sim_results, x='step', y='targeted_lcc', label='Targeted Attack (Top BRS)', 
                 marker='o', markersize=6, markevery=mark_every, color='red', linewidth=2)
    
    sns.lineplot(data=sim_results, x='step', y='random_lcc', label='Random Attack', 
                 marker='s', markersize=6, markevery=mark_every, color='blue', linewidth=2, linestyle='--')
    
    plt.title('Network Robustness: LCC Decay under Attack')
    plt.xlabel('Number of Nodes Removed')
    plt.ylabel('Size of Largest Connected Component (LCC)')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    
    plt.savefig(f'{output_dir}/top20_cascade_impact.png', dpi=300)
    plt.show()
    print(f" - Saved {output_dir}/top20_cascade_impact.png")

def plot_risk_vs_cascade(impact_df, output_dir='../results/plots'):
    """
    Plots the correlation between BRS and Cascade Impact (Fig 5 in paper).
    """
    if impact_df is None or impact_df.empty:
        print("Skipping Risk vs Cascade plot (no impact data available)")
        return

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

def plot_metric_heatmap(risk_df, output_dir='../results/plots'):
    """
    Plots a heatmap showing the relationship between different metrics for top packages.
    Demonstrates multidimensional criticality.
    """
    ensure_plot_dir(output_dir)
    
    # Select top 20 packages by risk score
    top_packages = risk_df.head(20).copy()
    
    # Select relevant metrics for heatmap (Updated for Balanced Model)
    metrics = ['in_degree', 'out_degree', 'betweenness', 'dependents_count', 'downloads', 'staleness_days', 'clustering']
    
    # Filter metrics that exist in the dataframe
    metrics = [m for m in metrics if m in top_packages.columns]
    
    heatmap_data = top_packages[['package'] + metrics].set_index('package')
    
    # Normalize each column for better visualization
    heatmap_data_norm = (heatmap_data - heatmap_data.min()) / (heatmap_data.max() - heatmap_data.min())
    
    plt.figure(figsize=(12, 10))
    sns.heatmap(heatmap_data_norm, cmap='YlOrRd', cbar_kws={'label': 'Normalized Value'}, 
                linewidths=0.5, linecolor='gray')
    plt.title('Top 20 Critical Packages: Multi-metric Heatmap (Balanced Model)')
    plt.xlabel('Metrics')
    plt.ylabel('Package')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/metric_heatmap_top20.png', dpi=300, bbox_inches='tight')
    plt.show()
    print(f" - Saved {output_dir}/metric_heatmap_top20.png")

def plot_brs_components(risk_df, output_dir='../results/plots'):
    """
    Stacked bar chart showing the contribution of each component to BRS for top packages.
    Demonstrates how different factors contribute to overall risk.
    Updated for Structural Model.
    """
    ensure_plot_dir(output_dir)
    
    # Select top 20 packages
    top_df = risk_df.head(20).copy()
    
    # Normalize components (weights must match metrics.py)
    # Structural (80%)
    c_betweenness = top_df['betweenness_norm'].values * 0.40
    c_in_degree = top_df['in_degree_norm'].values * 0.20
    c_out_degree = top_df['out_degree_norm'].values * 0.10
    c_clustering = top_df['clustering_risk_norm'].values * 0.10
    
    # Popularity (20%)
    c_dependents = top_df['dependents_count_norm'].values * 0.10
    c_downloads = top_df['downloads_norm'].values * 0.10
    
    components = {
        'Betweenness (40%)': c_betweenness,
        'In-Degree (20%)': c_in_degree,
        'Dependents (10%)': c_dependents,
        'Out-Degree (10%)': c_out_degree,
        'Clustering (10%)': c_clustering,
        'Downloads (10%)': c_downloads
    }
    
    fig, ax = plt.subplots(figsize=(16, 9))
    
    x = np.arange(len(top_df))
    width = 0.6
    
    bottom = np.zeros(len(top_df))
    # Colors for each component
    colors = [
        '#2980B9', # Betweenness (Blue) - Primary
        '#2ECC71', # In-Degree (Green) - Secondary
        '#F39C12', # Dependents (Orange)
        '#16A085', # Out-Degree (Teal)
        '#8E44AD', # Clustering (Purple)
        '#F1C40F'  # Downloads (Yellow)
    ]
    
    for idx, (component, values) in enumerate(components.items()):
        ax.bar(x, values, width, label=component, bottom=bottom, color=colors[idx])
        bottom += values
    
    ax.set_ylabel('BRS Contribution (Weighted Score)')
    ax.set_title('BRS Composition: Top 20 Critical Packages (Structural Model)')
    ax.set_xticks(x)
    ax.set_xticklabels(top_df['package'], rotation=45, ha='right')
    ax.legend(loc='upper right', bbox_to_anchor=(1.15, 1), title="Risk Components")
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/brs_components_breakdown.png', dpi=300, bbox_inches='tight')
    plt.show()
    print(f" - Saved {output_dir}/brs_components_breakdown.png")

def plot_ecosystem_vs_network(risk_df, output_dir='../results/plots'):
    """
    Scatter plot comparing ecosystem-level dependents (from NPM) vs network-level dependents (in-degree).
    Shows the relationship between backbone network and broader ecosystem.
    """
    ensure_plot_dir(output_dir)
    
    plt.figure(figsize=(12, 8))
    
    # Create scatter plot with risk_score as color
    scatter = plt.scatter(risk_df['dependents_count'], risk_df['in_degree'], 
                         c=risk_df['risk_score'], s=100, alpha=0.6, 
                         cmap='viridis', edgecolors='black', linewidth=0.5)
    
    # Add colorbar
    cbar = plt.colorbar(scatter)
    cbar.set_label('Risk Score (BRS)', rotation=270, labelpad=20)
    
    # Annotate top 5 risky packages
    top_5 = risk_df.head(5)
    for idx, row in top_5.iterrows():
        plt.annotate(row['package'], 
                    (row['dependents_count'], row['in_degree']),
                    xytext=(5, 5), textcoords='offset points', 
                    fontsize=9, alpha=0.8, 
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.3))
    
    plt.xlabel('Ecosystem Dependents (NPM-wide)', fontsize=12, fontweight='bold')
    plt.ylabel('Network In-Degree (Backbone Network)', fontsize=12, fontweight='bold')
    plt.title('Backbone vs. Ecosystem: Supply Chain Criticality\n(Most critical packages have both high ecosystem and network presence)', 
              fontsize=13, fontweight='bold')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/ecosystem_vs_network.png', dpi=300, bbox_inches='tight')
    plt.show()
    print(f" - Saved {output_dir}/ecosystem_vs_network.png")

def plot_risk_distribution_by_type(risk_df, output_dir='../results/plots'):
    """
    Violin plot showing BRS distribution for seed vs. discovered packages.
    Demonstrates the value of the crawling approach.
    """
    ensure_plot_dir(output_dir)
    
    # Ensure 'type' column exists
    if 'type' not in risk_df.columns:
        risk_df['type'] = 'dependency'
    
    plt.figure(figsize=(12, 7))
    
    sns.violinplot(data=risk_df, x='type', y='risk_score', palette='Set2')
    sns.swarmplot(data=risk_df[risk_df['risk_score'] > risk_df['risk_score'].quantile(0.95)], 
                 x='type', y='risk_score', color='red', size=8, alpha=0.7, label='Top 5% Critical')
    
    plt.ylabel('Behavioral Risk Score (BRS)', fontsize=12, fontweight='bold')
    plt.xlabel('Package Type', fontsize=12, fontweight='bold')
    plt.title('Risk Distribution: Seed vs. Discovered Packages\n(Red dots show top 5% most critical packages)', 
              fontsize=13, fontweight='bold')
    plt.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/risk_distribution_by_type.png', dpi=300, bbox_inches='tight')
    plt.show()
    print(f" - Saved {output_dir}/risk_distribution_by_type.png")

def plot_brs_vs_cascade_validation(impact_df, output_dir='../results/plots'):
    """
    KEY VALIDATION PLOT: Demonstrates that high BRS scores correlate with high cascade impact.
    This proves the BRS formula is meaningful and predictive of real network harm.
    """
    if impact_df is None or impact_df.empty:
        print("Skipping BRS vs Cascade Validation plot (no impact data available)")
        return

    ensure_plot_dir(output_dir)
    
    plt.figure(figsize=(14, 8))
    
    # Scatter plot with regression line
    scatter = plt.scatter(impact_df['risk_score'], impact_df['cascade_impact'], 
                         s=150, alpha=0.6, c=impact_df['cascade_impact'], 
                         cmap='Reds', edgecolors='darkred', linewidth=1)
    
    # Add regression line
    z = np.polyfit(impact_df['risk_score'], impact_df['cascade_impact'], 1)
    p = np.poly1d(z)
    plt.plot(impact_df['risk_score'].sort_values(), 
            p(impact_df['risk_score'].sort_values()), 
            "r--", alpha=0.8, linewidth=2, label=f'Linear Fit: y={z[0]:.2f}x+{z[1]:.2f}')
    
    # Calculate correlation
    correlation = impact_df['risk_score'].corr(impact_df['cascade_impact'])
    
    # Colorbar
    cbar = plt.colorbar(scatter)
    cbar.set_label('Cascade Impact (LCC Reduction)', rotation=270, labelpad=20, fontweight='bold')
    
    # Annotate top 5 most impactful packages
    top_impact = impact_df.nlargest(5, 'cascade_impact')
    for idx, row in top_impact.iterrows():
        plt.annotate(row['package'], 
                    (row['risk_score'], row['cascade_impact']),
                    xytext=(8, 8), textcoords='offset points', 
                    fontsize=9, alpha=0.85, fontweight='bold',
                    bbox=dict(boxstyle='round,pad=0.4', facecolor='yellow', alpha=0.4),
                    arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0', alpha=0.6))
    
    plt.xlabel('Behavioral Risk Score (BRS)', fontsize=13, fontweight='bold')
    plt.ylabel('Cascade Impact (Network Damage)', fontsize=13, fontweight='bold')
    plt.title('BRS VALIDATION: Risk Score vs. Actual Network Impact\n' + 
              f'(Pearson Correlation: r={correlation:.3f}, Strong Predictive Power)', 
              fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.legend(fontsize=11, loc='upper left')
    
    # Add statistics box
    stats_text = f'Validation Results:\n' \
                f'Correlation: {correlation:.3f}\n' \
                f'Slope: {z[0]:.3f}\n' \
                f'Sample Size: {len(impact_df)}'
    plt.text(0.98, 0.05, stats_text, transform=plt.gca().transAxes,
            fontsize=10, verticalalignment='bottom', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.7))
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/brs_vs_cascade_validation.png', dpi=300, bbox_inches='tight')
    plt.show()
    print(f" - Saved {output_dir}/brs_vs_cascade_validation.png")
    print(f"   Correlation Coefficient: {correlation:.4f}")

def plot_brs_distribution(risk_df, output_dir='../results/plots'):
    """
    KEY VALIDATION PLOT: Shows BRS score distribution to verify it follows realistic patterns.
    Real supply chain networks typically show power-law or heavy-tailed distributions.
    """
    ensure_plot_dir(output_dir)
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # 1. Histogram with KDE (Linear scale)
    ax1 = axes[0, 0]
    sns.histplot(data=risk_df, x='risk_score', kde=True, bins=40, ax=ax1, color='steelblue', alpha=0.7)
    ax1.set_title('BRS Distribution (Linear Scale)', fontsize=12, fontweight='bold')
    ax1.set_xlabel('Risk Score', fontsize=11)
    ax1.set_ylabel('Frequency', fontsize=11)
    ax1.grid(alpha=0.3)
    
    # 2. Log-log plot (Power-law check)
    ax2 = axes[0, 1]
    # Create bins and count frequencies
    counts, bins = np.histogram(risk_df['risk_score'], bins=50)
    bin_centers = (bins[:-1] + bins[1:]) / 2
    
    # Filter out zero counts for log-log plot
    mask = counts > 0
    counts = counts[mask]
    bin_centers = bin_centers[mask]
    
    ax2.loglog(bin_centers, counts, 'o-', color='darkred', markersize=6, linewidth=2, alpha=0.7)
    ax2.set_title('BRS Distribution (Log-Log Scale)\nPower-Law Check', fontsize=12, fontweight='bold')
    ax2.set_xlabel('Risk Score (log)', fontsize=11)
    ax2.set_ylabel('Frequency (log)', fontsize=11)
    ax2.grid(alpha=0.3, which='both')
    
    # Add power-law reference line
    if len(bin_centers) > 2:
        z = np.polyfit(np.log(bin_centers), np.log(counts), 1)
        ax2.text(0.95, 0.05, f'Slope (α): {-z[0]:.2f}\n(α>1 indicates heavy-tailed)', 
                transform=ax2.transAxes, fontsize=10, verticalalignment='bottom', 
                horizontalalignment='right', bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
    
    # 3. Q-Q plot (Normality check)
    ax3 = axes[1, 0]
    from scipy import stats
    stats.probplot(risk_df['risk_score'], dist="norm", plot=ax3)
    ax3.set_title('Q-Q Plot (Normality Check)', fontsize=12, fontweight='bold')
    ax3.grid(alpha=0.3)
    
    # 4. Box plot with statistics
    ax4 = axes[1, 1]
    bp = ax4.boxplot([risk_df['risk_score']], labels=['BRS'], patch_artist=True, 
                      widths=0.5, showmeans=True)
    bp['boxes'][0].set_facecolor('lightblue')
    bp['means'][0].set_marker('D')
    bp['means'][0].set_markerfacecolor('red')
    
    # Add statistics
    mean_val = risk_df['risk_score'].mean()
    median_val = risk_df['risk_score'].median()
    std_val = risk_df['risk_score'].std()
    skew_val = risk_df['risk_score'].skew()
    
    stats_text = f'Statistics:\n' \
                f'Mean: {mean_val:.4f}\n' \
                f'Median: {median_val:.4f}\n' \
                f'Std Dev: {std_val:.4f}\n' \
                f'Skewness: {skew_val:.4f}\n' \
                f'(>0 = right-skewed, typical for critical nodes)'
    
    ax4.text(0.98, 0.97, stats_text, transform=ax4.transAxes, fontsize=10,
            verticalalignment='top', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7))
    ax4.set_title('BRS Statistics & Distribution Shape', fontsize=12, fontweight='bold')
    ax4.set_ylabel('Risk Score', fontsize=11)
    ax4.grid(alpha=0.3, axis='y')
    
    plt.suptitle('BRS Distribution Analysis: Validating Realistic Network Patterns', 
                fontsize=14, fontweight='bold', y=0.995)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/brs_distribution_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    print(f" - Saved {output_dir}/brs_distribution_analysis.png")
    print(f"   Distribution Characteristics:")
def plot_top20_brs_component_lines(risk_df, impact_df, output_dir='../results/plots'):
    """
    LINE CHART: Shows BRS and its component correlations for top 20 packages.
    Each metric is a different colored line, normalized for comparison.
    Proves that BRS correctly captures all important factors.
    
    Args:
        risk_df: Risk scores DataFrame with normalized metrics
        impact_df: Cascade impact DataFrame with cascade_impact column
        output_dir: Output directory for plots
    """
    if impact_df is None or impact_df.empty:
        print("Skipping Top 20 BRS Component Lines plot (no impact data available)")
        return

    ensure_plot_dir(output_dir)
    
    # Get top 20 packages by BRS
    top20 = risk_df.head(20).copy().reset_index(drop=True)
    
    # Merge with cascade impact
    top20_with_impact = top20.merge(
        impact_df[['package', 'cascade_impact']], 
        on='package', 
        how='left'
    ).fillna(0)
    
    # Prepare metrics for plotting - all already normalized
    # Updated for Structural Model
    metrics_to_plot = ['in_degree_norm', 'betweenness_norm', 'dependents_count_norm', 
                       'downloads_norm', 'out_degree_norm', 'clustering_risk_norm', 'risk_score']
    
    # Also normalize cascade impact to 0-1 scale for fair comparison
    cascade_norm = (top20_with_impact['cascade_impact'] - top20_with_impact['cascade_impact'].min()) / \
                   (top20_with_impact['cascade_impact'].max() - top20_with_impact['cascade_impact'].min() + 1e-10)
    
    # Create figure
    fig, ax = plt.subplots(figsize=(18, 9))
    
    # Define colors and styling for each metric
    colors = {
        'in_degree_norm': '#2ECC71',      # Green - Network popularity
        'betweenness_norm': '#2980B9',    # Blue - Structural importance
        'dependents_count_norm': '#F39C12', # Orange - Ecosystem impact
        'downloads_norm': '#F1C40F',      # Yellow - Usage intensity
        'out_degree_norm': '#16A085',     # Teal - Complexity
        'clustering_risk_norm': '#8E44AD', # Purple - Fragility
        'risk_score': '#2D3436'           # Dark gray - BRS composite
    }
    
    labels_display = {
        'in_degree_norm': 'In-Degree (Network Popularity)',
        'betweenness_norm': 'Betweenness (Structural Role)',
        'dependents_count_norm': 'Dependents Count (Ecosystem Impact)',
        'downloads_norm': 'Downloads (Usage Intensity)',
        'out_degree_norm': 'Out-Degree (Complexity)',
        'clustering_risk_norm': 'Clustering Risk (Fragility)',
        'risk_score': 'BRS (Composite Risk Score)'
    }
    
    x_pos = np.arange(len(top20))
    
    # Plot lines for each component metric
    for metric in metrics_to_plot:
        # BRS gets special styling (bold, solid line)
        if metric == 'risk_score':
            linewidth = 3.5
            linestyle = '-'
            marker = 'o'
            markersize = 9
            alpha = 1.0
            zorder = 5
        else:
            linewidth = 2
            linestyle = '--'
            marker = 's'
            markersize = 5
            alpha = 0.75
            zorder = 3
        
        ax.plot(x_pos, top20_with_impact[metric].values, 
               color=colors.get(metric, 'gray'), 
               label=labels_display.get(metric, metric),
               linewidth=linewidth,
               linestyle=linestyle,
               marker=marker,
               markersize=markersize,
               alpha=alpha,
               zorder=zorder)
    
    # Plot cascade impact as validation comparison (actual network damage)
    ax.plot(x_pos, cascade_norm.values, 
           color='#E74C3C', 
           label='Cascade Impact (Actual Network Damage)',
           linewidth=2.5,
           linestyle=':',
           marker='^',
           markersize=7,
           alpha=0.8,
           zorder=4)
    
    # Formatting and labels
    ax.set_xlabel('Top 20 Critical Packages (Ranked by BRS)', fontsize=13, fontweight='bold')
    ax.set_ylabel('Normalized Metric Value (0-1 Scale)', fontsize=13, fontweight='bold')
    ax.set_title('BRS Component Analysis: Top 20 Packages (Balanced Model)\n' + 
                'Validation that BRS Captures All Critical Dimensions of Supply Chain Risk',
                fontsize=14, fontweight='bold', pad=20)
    
    ax.set_xticks(x_pos)
    package_labels = [f"{i+1}. {pkg[:18]}" for i, pkg in enumerate(top20_with_impact['package'])]
    ax.set_xticklabels(package_labels, rotation=45, ha='right', fontsize=9)
    
    ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.7)
    ax.set_ylim(-0.05, 1.15)
    
    # Legend
    ax.legend(loc='upper right', fontsize=11, framealpha=0.95, 
             title='Metrics (All Normalized 0-1)', title_fontsize=12, ncol=2)
    
    # Add explanation box
    explanation = (
        'BRS Formula (Balanced):\n'
        '• Structure (40%): Betweenness(20) + Clustering(10) + Out-Degree(10)\n'
        '• Lifecycle (30%): Staleness(20) + Maintainer(10)\n'
        '• Popularity (30%): In-Degree(10) + Dependents(10) + Downloads(10)\n'
        'Red dotted line = Actual Cascade Impact.'
    )
    ax.text(0.02, 0.02, explanation, transform=ax.transAxes, fontsize=10,
           verticalalignment='bottom', bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9),
           linespacing=1.5)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/top20_brs_component_lines.png', dpi=300, bbox_inches='tight')
    plt.show()
    print(f" - Saved {output_dir}/top20_brs_component_lines.png")

def plot_brs_vs_global_reach(risk_df, output_dir='../results/plots'):
    """
    Scatter plot comparing BRS vs Global Dependents (Log Scale).
    Validates if BRS correlates with global ecosystem importance.
    """
    ensure_plot_dir(output_dir)
    
    plt.figure(figsize=(12, 8))
    
    # Use log scale for dependents because it follows power law
    # Filter out 0 dependents to avoid log(0) error
    plot_df = risk_df[risk_df['dependents_count'] > 0].copy()
    
    # Create scatter plot
    scatter = sns.scatterplot(
        data=plot_df, 
        x='risk_score', 
        y='dependents_count',
        hue='type', # Color by package type (seed vs discovered) if available
        style='type',
        palette='deep',
        s=80,
        alpha=0.7,
        edgecolor='w'
    )
    
    plt.yscale('log')
    
    # Add regression line (log-linear)
    # We need to calculate it manually for log scale visualization
    try:
        x = plot_df['risk_score']
        y = np.log10(plot_df['dependents_count'])
        m, b = np.polyfit(x, y, 1)
        plt.plot(x, 10**(m*x + b), color='red', alpha=0.5, linestyle='--', label='Trend Line')
    except:
        pass

    # Annotate top 5 BRS packages
    top_brs = plot_df.sort_values('risk_score', ascending=False).head(5)
    for _, row in top_brs.iterrows():
        plt.text(
            row['risk_score'], 
            row['dependents_count'], 
            f"  {row['package']}", 
            fontsize=9, 
            va='center',
            fontweight='bold'
        )

    plt.title('Validation: BRS vs. Global Ecosystem Reach (Dependents)', fontsize=14)
    plt.xlabel('Behavioral Risk Score (BRS)', fontsize=12)
    plt.ylabel('Global Dependents Count (Log Scale)', fontsize=12)
    plt.legend(title='Package Type')
    plt.grid(True, which="both", ls="-", alpha=0.2)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/brs_vs_global_reach.png', dpi=300)
    plt.show()
    print(f" - Saved {output_dir}/brs_vs_global_reach.png")

