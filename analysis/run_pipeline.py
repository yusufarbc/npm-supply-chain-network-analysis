"""Orchestrator to run the full analysis from a notebook.

Provides a single `run_pipeline()` function that notebooks can import and
call to execute the typical end-to-end workflow producing files in `results/`.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, List, Optional

from . import analysis_helpers as ah
from . import exporter as ex
import json
import csv


def run_pipeline(
    top_packages: Optional[Iterable[str]] = None,
    top_n: int = 1000,
    cache_path: Optional[str] = None,
    include_peer_deps: bool = False,
    sample_k: Optional[int] = None,
    results_dir: str = "results",
    compute_plots: bool = True,
    export_gexf: bool = False,
) -> dict:
    """Run the full analysis pipeline.

    Typical usage from a notebook:
        from analysis import run_pipeline
        res = run_pipeline(top_n=1000)

    Returns a dict with summary info and paths to major outputs.
    """
    res_dir = Path(results_dir)
    res_dir.mkdir(parents=True, exist_ok=True)

    # 1) Determine top package list
    if top_packages is None:
        print(f"Fetching top {top_n} packages (may take a while)...")
        top_list: List[str] = ah.fetch_top_packages(top_n)
    else:
        top_list = list(top_packages)

    # 2) Build dependency graph (Dependent -> Dependency)
    cachep = Path(cache_path) if cache_path else None
    print("Building dependency graph...")
    G, top_set = ah.build_dependency_graph(top_list, cache_path=cachep, include_peer_deps=include_peer_deps)

    # 3) Compute metrics
    print("Computing metrics (degree, betweenness)...")
    in_deg, out_deg, btw = ah.compute_metrics(G, sample_k=sample_k)

    # 4) Compute risk scores
    print("Computing risk scores and saving outputs...")
    risk = ah.compute_risk_scores(in_deg, out_deg, btw)

    # Paths
    edges_p = res_dir / "edges.csv"
    metrics_p = res_dir / "metrics.csv"
    risk_p = res_dir / "risk_scores.csv"
    stats_p = res_dir / "graph_stats.json"

    # 5) Save primary outputs
    ah.save_edges(G, edges_p)
    ah.save_metrics(in_deg, out_deg, btw, top_set, metrics_p)
    ah.save_risk_scores(risk, in_deg, out_deg, btw, top_set, risk_p)
    # save graph stats (JSON) and also CSV equivalent
    ah.save_graph_stats(G, stats_p)
    try:
        stats = json.loads((stats_p).read_text(encoding="utf-8"))
        csv_stats_p = res_dir / "graph_stats.csv"
        with csv_stats_p.open("w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["metric", "value"])
            for k, v in stats.items():
                w.writerow([k, v])
    except Exception:
        pass

    # also produce CSV top-k reports (in/out/betweenness for all nodes and top_set)
    ah.save_report(in_deg, out_deg, btw, top_set, res_dir / "report.md")
    try:
        # top 20 across all nodes
        top_in_all = sorted(in_deg.items(), key=lambda kv: kv[1], reverse=True)[:20]
        top_out_all = sorted(out_deg.items(), key=lambda kv: kv[1], reverse=True)[:20]
        top_btw_all = sorted(btw.items(), key=lambda kv: kv[1], reverse=True)[:20]
        with (res_dir / "top20_in_degree.csv").open("w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["package", "in_degree"])
            for n, v in top_in_all:
                w.writerow([n, v])
        with (res_dir / "top20_out_degree.csv").open("w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["package", "out_degree"])
            for n, v in top_out_all:
                w.writerow([n, v])
        with (res_dir / "top20_betweenness.csv").open("w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["package", "betweenness"])
            for n, v in top_btw_all:
                w.writerow([n, f"{v:.6f}"])

        # top 20 restricted to Top N cohort
        top_in_top = sorted(((n, in_deg.get(n, 0)) for n in top_set), key=lambda kv: kv[1], reverse=True)[:20]
        top_out_top = sorted(((n, out_deg.get(n, 0)) for n in top_set), key=lambda kv: kv[1], reverse=True)[:20]
        top_btw_top = sorted(((n, btw.get(n, 0.0)) for n in top_set), key=lambda kv: kv[1], reverse=True)[:20]
        with (res_dir / "top20_in_top.csv").open("w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["package", "in_degree"])
            for n, v in top_in_top:
                w.writerow([n, v])
        with (res_dir / "top20_out_top.csv").open("w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["package", "out_degree"])
            for n, v in top_out_top:
                w.writerow([n, v])
        with (res_dir / "top20_btw_top.csv").open("w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["package", "betweenness"])
            for n, v in top_btw_top:
                w.writerow([n, f"{v:.6f}"])
    except Exception:
        pass

    # 6) Cascade impact
    print("Computing cascade impacts for Top N cohort...")
    seeds = list(top_set)
    impact = ah.cascade_impact_counts(G, seeds)
    ah.save_cascade_impact(impact, res_dir / "cascade_impact.csv")

    # 7) Edge betweenness top N
    ah.save_edge_betweenness_topn(G, 10, res_dir / "edge_betweenness_top10.csv")

    # 8) Plots (optional)
    if compute_plots:
        print("Generating plots (may require matplotlib, numpy)...")
        try:
            out_plot_dir = res_dir / "plots"
            out_plot_dir.mkdir(exist_ok=True)
            ah.plot_degree_histograms(in_deg, out_deg, out_plot_dir)
            ah.plot_scatter_correlations(in_deg, out_deg, btw, out_plot_dir)
            ah.plot_topk_bars(in_deg, out_deg, btw, risk, out_plot_dir)
            ah.plot_risk_vs_cascade(risk, impact, out_plot_dir)
            ah.plot_top_risk(risk, out_plot_dir)
        except Exception as e:
            print("Plot generation failed:", e)

    # 9) Export for Gephi
    print("Exporting for Gephi...")
    id_map = ex.export_for_gephi(results_dir, write_gexf_flag=export_gexf)

    summary = {
        "nodes": G.number_of_nodes(),
        "edges": G.number_of_edges(),
        "results_dir": str(res_dir),
        "gephi_nodes": str(res_dir / "gephi_nodes.csv"),
        "gephi_edges": str(res_dir / "gephi_edges.csv"),
        "graph_gexf": str(res_dir / "graph.gexf") if export_gexf else None,
        "id_map_sample": dict(list(id_map.items())[:10]),
    }
    print("Pipeline finished.")
    return summary


if __name__ == "__main__":
    # simple CLI for convenience
    import argparse

    p = argparse.ArgumentParser(description="Run full npm network analysis pipeline (from analysis package)")
    p.add_argument("--top-n", type=int, default=1000)
    p.add_argument("--results", default="results")
    p.add_argument("--no-plots", dest="plots", action="store_false")
    p.add_argument("--gexf", action="store_true")
    args = p.parse_args()
    run_pipeline(top_n=args.top_n, results_dir=args.results, compute_plots=args.plots, export_gexf=args.gexf)
