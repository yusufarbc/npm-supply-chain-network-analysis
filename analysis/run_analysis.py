
import os
import sys
import argparse
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns

def setup_paths():
    """Add necessary directories to the system path."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
    
    if current_dir not in sys.path:
        sys.path.append(current_dir)
    if parent_dir not in sys.path:
        sys.path.append(parent_dir)

# It's better to set up paths before importing custom modules
setup_paths()

try:
    from data_loader import get_combined_seed_packages
    from network_builder import build_dependency_graph
    from metrics import calculate_risk_scores
    from simulation import simulate_attacks, calculate_single_node_impact
    from utils import export_results
    from visualize import (
        plot_network_structure, 
        plot_degree_distributions, 
        plot_correlations, 
        plot_top_risk_scores, 
        plot_simulation_results,
        plot_risk_vs_cascade,
        plot_metric_heatmap, 
        plot_brs_components, 
        plot_ecosystem_vs_network, 
        plot_risk_distribution_by_type,
        plot_brs_vs_cascade_validation, 
        plot_brs_distribution, 
        plot_top20_brs_component_lines,
        plot_brs_vs_global_reach
    )
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Please ensure you are running this script from the 'analysis' directory.")
    sys.exit(1)

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="NPM Supply Chain Network Analysis Pipeline")
    
    # --- Main Configuration ---
    parser.add_argument('--top-n', type=int, default=1000, help="Number of seed packages to fetch (per category).")
    parser.add_argument('--max-depth', type=int, default=7, help="Traversal depth for the crawler.")
    parser.add_argument('--api-delay', type=float, default=0.1, help="Delay between API calls in seconds.")
    parser.add_argument('--output-dir', type=str, default='../results', help="Output directory for results.")
    parser.add_argument('--force-rerun', action='store_true', help="Force re-crawling and re-calculation, ignoring cached files.")

    # --- Simulation Configuration ---
    parser.add_argument('--simulation-removals', type=int, default=500, help="Number of nodes to remove in robustness simulation.")
    parser.add_argument('--impact-sample-size', type=int, default=100, help="Number of top nodes to analyze for cascade impact.")
    
    return parser.parse_args()

def main():
    """Main function to run the analysis pipeline."""
    args = parse_arguments()
    
    # --- Setup ---
    print("--- Environment Setup ---")
    output_dir = args.output_dir
    plots_dir = os.path.join(output_dir, 'plots')
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(plots_dir, exist_ok=True)

    sns.set_theme(style="whitegrid", context="notebook", palette="deep")
    plt.rcParams['figure.figsize'] = (12, 6)
    plt.rcParams['figure.dpi'] = 100
    print("Environment setup complete. Configuration loaded.")

    # === 1. Network Construction (or Load from Disk) ===
    print("\n--- 1. Network Construction ---")
    graph_file = os.path.join(output_dir, "network.gml")
    graph_loaded = False
    G = None

    if os.path.exists(graph_file) and not args.force_rerun:
        print(f"Found existing graph at {graph_file}. Loading...")
        try:
            G = nx.read_gml(graph_file)
            if len(G) > 0:
                graph_loaded = True
                print(f"Graph loaded successfully: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges.")
            else:
                print("Loaded graph is empty. Will re-build.")
        except Exception as e:
            print(f"Error loading graph: {e}. Will re-build.")

    if not graph_loaded:
        print("Fetching seed packages...")
        seed_packages = get_combined_seed_packages(limit_dependents=args.top_n, limit_downloads=args.top_n, api_delay=args.api_delay)
        print(f"Total unique seed packages: {len(seed_packages)}")
        
        print("Starting network crawler (this may take a while)...")
        G = build_dependency_graph(seed_packages, max_depth=args.max_depth, api_delay=args.api_delay)
        
        print(f"Saving graph to {graph_file}...")
        nx.write_gml(G, graph_file)
        print("Graph saved.")

    if G is None:
        raise RuntimeError("Failed to initialize Graph G.")

    # === 2. Metrics & Risk Scoring (or Load from Disk) ===
    print("\n--- 2. Metrics & Risk Scoring ---")
    risk_file = os.path.join(output_dir, "risk_scores.csv")
    metrics_loaded = False
    risk_df = None
    
    should_recalc = args.force_rerun or not graph_loaded

    if os.path.exists(risk_file) and not should_recalc:
        print(f"Found existing risk scores at {risk_file}. Loading...")
        try:
            risk_df = pd.read_csv(risk_file)
            if 'package' not in risk_df.columns and 'name' in risk_df.columns:
                 risk_df = risk_df.rename(columns={'name': 'package'})
            if len(risk_df) > 0:
                print(f"Risk scores loaded successfully ({len(risk_df)} packages).")
                metrics_loaded = True
            else:
                print("Risk scores file is empty. Will re-calculate.")
        except Exception as e:
            print(f"Error loading risk scores: {e}. Will re-calculate.")

    if not metrics_loaded:
        print("Calculating metrics (this may take a moment)...")
        # Perform exact betweenness calculation as requested by user
        risk_df = calculate_risk_scores(G, betweenness_k=None)
        print(f"Saving risk scores to {risk_file}...")
        risk_df.to_csv(risk_file, index=False)
        print("Risk scores saved.")

    # === 3. Robustness Simulation (or Load from Disk) ===
    print("\n--- 3. Robustness Simulation & Cascade Analysis ---")
    sim_results_file = os.path.join(output_dir, "sim_results.csv")
    impact_results_file = os.path.join(output_dir, "impact_scores.csv")
    
    # Robustness Simulation
    if os.path.exists(sim_results_file) and not args.force_rerun:
        print(f"Loading simulation results from {sim_results_file}...")
        sim_results = pd.read_csv(sim_results_file)
    else:
        print(f"Running robustness simulations (Removals: {args.simulation_removals})...")
        sim_results = simulate_attacks(G, risk_df, num_removals=args.simulation_removals)
        sim_results.to_csv(sim_results_file, index=False)
        print(f"Simulation results saved to {sim_results_file}")

    # Cascade Impact Analysis
    if os.path.exists(impact_results_file) and not args.force_rerun:
        print(f"Loading cascade impact results from {impact_results_file}...")
        impact_df = pd.read_csv(impact_results_file)
    else:
        print(f"Calculating cascade impact for top {args.impact_sample_size} nodes...")
        impact_df = calculate_single_node_impact(G, risk_df, sample_size=args.impact_sample_size)
        impact_df.to_csv(impact_results_file, index=False)
        print(f"Cascade impact results saved to {impact_results_file}")

    # === 4. Visualization ===
    print("\n--- 4. Generating Visualizations ---")
    plot_network_structure(G, output_dir=plots_dir)
    plot_degree_distributions(G, output_dir=plots_dir)
    plot_correlations(risk_df, output_dir=plots_dir)
    plot_top_risk_scores(risk_df, output_dir=plots_dir)
    plot_simulation_results(sim_results, output_dir=plots_dir)
    plot_risk_vs_cascade(impact_df, output_dir=plots_dir)
    plot_metric_heatmap(risk_df, output_dir=plots_dir)
    plot_brs_components(risk_df, output_dir=plots_dir)
    plot_ecosystem_vs_network(risk_df, output_dir=plots_dir)
    plot_risk_distribution_by_type(risk_df, output_dir=plots_dir)
    plot_brs_vs_cascade_validation(impact_df, output_dir=plots_dir)
    plot_brs_distribution(risk_df, output_dir=plots_dir)
    plot_top20_brs_component_lines(risk_df, impact_df, output_dir=plots_dir)
    plot_brs_vs_global_reach(risk_df, output_dir=plots_dir)
    print(f"All visualizations saved to {plots_dir}")

    # === 5. Export & Conclusion ===
    print("\n--- 5. Exporting Final Results ---")
    export_results(risk_df, G, impact_df=impact_df, output_dir=output_dir)
    nx.write_gml(G, os.path.join(output_dir, "network.gml"))
    print(f"All data artifacts exported to {output_dir}")

    print("\n" + "="*70)
    print("ANALYSIS COMPLETE!")
    print("="*70)
    print(f"Total packages analyzed: {len(risk_df)}")
    print(f"Network nodes: {G.number_of_nodes()}, edges: {G.number_of_edges()}")
    print("="*70)

if __name__ == "__main__":
    main()
