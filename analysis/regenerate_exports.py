
import os
import sys
import pandas as pd
import networkx as nx
from utils import export_results

def main():
    print("Loading data for export regeneration...")
    # Assume running from project root
    results_dir = 'results'
    
    # Load Network
    gml_path = os.path.join(results_dir, 'network.gml')
    if not os.path.exists(gml_path):
        print("Error: network.gml not found.")
        return
    G = nx.read_gml(gml_path)
    
    # Load Risk Scores
    risk_path = os.path.join(results_dir, 'risk_scores.csv')
    if not os.path.exists(risk_path):
         print("Error: risk_scores.csv not found.")
         return
    risk_df = pd.read_csv(risk_path)
    
    # Load Impact Scores
    impact_path = os.path.join(results_dir, 'impact_scores.csv')
    impact_df = None
    if os.path.exists(impact_path):
        impact_df = pd.read_csv(impact_path)
        
    print("Data loaded. Running export_results...")
    export_results(risk_df, G, impact_df, output_dir=results_dir)
    print("Export regeneration complete.")

if __name__ == "__main__":
    main()
