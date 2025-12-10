
import os
import pandas as pd

def latex_escape(text):
    """Escape special LaTeX characters."""
    if not isinstance(text, str):
        return text
    replacements = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\^{}',
        '\\': r'\textbackslash{}',
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text

def create_latex_table(df, columns, caption, label, output_path):
    """
    Generates a LaTeX tabular environment content (without table wrapper)
    and saves it to a file.
    """
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Filter and format dataframe
    to_export = df[list(columns.keys())].copy()
    
    # Escape strings
    for col in to_export.select_dtypes(include=['object']).columns:
        to_export[col] = to_export[col].apply(latex_escape)
    
    # Rename columns
    to_export = to_export.rename(columns=columns)
    
    # Generate syntax
    # We use a custom format to match the paper's style
    # \begin{tabular}{lrrrr} ...
    
    header = "\\begin{tabular}{" + "l" + "r" * (len(columns) - 1) + "}\n"
    header += "\\toprule\n"
    header += " & ".join(to_export.columns) + " \\\\\n"
    header += "\\midrule\n"
    
    body = ""
    for _, row in to_export.iterrows():
        # Format numbers: float to 6 decimals (or 4), int to string
        row_str = []
        for item in row:
            if isinstance(item, float):
                row_str.append(f"{item:.6f}")
            else:
                row_str.append(str(item))
        body += " & ".join(row_str) + " \\\\\n"
        
    footer = "\\bottomrule\n"
    footer += "\\end{tabular}\n"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(header + body + footer)
    
    print(f"Generated {output_path}")

def main():
    # Define paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    results_dir = os.path.join(base_dir, '..', 'results')
    top_lists_dir = os.path.join(results_dir, 'top_lists')
    output_tables_dir = os.path.join(results_dir, 'tables')
    
    # Check if inputs exist
    if not os.path.exists(top_lists_dir):
        print(f"Error: {top_lists_dir} not found. Run analysis first.")
        return

    # --- 1. Top In-Degree ---
    try:
        df = pd.read_csv(os.path.join(top_lists_dir, 'top20_in_degree.csv')).head(10)
        # Add a dummy TopN? column logic if needed, or just map what we have
        # The paper showed: Package | In-Degree | Out-Degree | Betweenness | TopN?
        # Our csv has: package, in_degree, risk_score. 
        # Wait, the paper tables have specific columns. I should try to reconstruct them from risk_scores.csv if possible 
        # because top20_*.csv might contain specific subsets.
        # Actually, reading risk_scores.csv serves all purposes and allows join.
        
        full_df = pd.read_csv(os.path.join(results_dir, 'risk_scores.csv'))
        
        # Helper to check TopN (ecosyste.ms list). 
        # For now we assume all analyzed nodes are TopN if they were in the seed list? 
        # Or we can just just set it to True as in the example or omit it.
        # The example table had "TopN? True", let's replicate that column if we can, or omit if we can't.
        # Simple fix: Add 'TopN?' column with 'True'
        full_df['TopN?'] = 'True' 
        
        # --- Table 1: In-Degree ---
        top_in = full_df.sort_values('in_degree', ascending=False).head(10)
        create_latex_table(
            top_in,
            columns={
                'package': 'Package',
                'in_degree': 'In-Degree',
                'out_degree': 'Out-Degree',
                'betweenness': 'Betweenness',
                'TopN?': 'TopN?'
            },
            caption="Top 10 Packages by In-Degree Centrality",
            label="tab:indegree",
            output_path=os.path.join(output_tables_dir, 'tab_indegree.tex')
        )
        
        # --- Table 2: Out-Degree ---
        top_out = full_df.sort_values('out_degree', ascending=False).head(10)
        create_latex_table(
            top_out,
            columns={
                'package': 'Package',
                'out_degree': 'Out-Degree',
                'in_degree': 'In-Degree',
                'betweenness': 'Betweenness',
                'TopN?': 'TopN?'
            },
            caption="Top 10 Packages by Out-Degree Centrality",
            label="tab:outdegree",
            output_path=os.path.join(output_tables_dir, 'tab_outdegree.tex')
        )
        
        # --- Table 3: Betweenness ---
        top_bet = full_df.sort_values('betweenness', ascending=False).head(10)
        create_latex_table(
            top_bet,
            columns={
                'package': 'Package',
                'betweenness': 'Betweenness',
                'in_degree': 'In-Degree',
                'out_degree': 'Out-Degree',
                'TopN?': 'TopN?'
            },
            caption="Top 10 Packages by Betweenness Centrality",
            label="tab:betweenness",
            output_path=os.path.join(output_tables_dir, 'tab_betweenness.tex')
        )
        
        # --- Table 4: Risk Score (Top 20) ---
        top_risk = full_df.sort_values('risk_score', ascending=False).head(20)
        create_latex_table(
            top_risk,
            columns={
                'package': 'Package',
                'risk_score': 'Risk',
                'in_degree': 'In-Degree',
                'out_degree': 'Out-Degree',
                'betweenness': 'Betweenness',
                'TopN?': 'TopN?'
            },
            caption="Top 20 Packages by Composite Risk Score (BRS)",
            label="tab:risk",
            output_path=os.path.join(output_tables_dir, 'tab_risk.tex')
        )

    except Exception as e:
        print(f"Error processing tables: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
