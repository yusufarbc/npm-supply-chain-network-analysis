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
    leaderboard_mode: str = "trending",
    depth: int = 7,
    cache_path: Optional[str] = None,
    include_peer_deps: bool = False,
    sample_k: Optional[int] = None,
    results_dir: str = "results",
    compute_plots: bool = True,
    export_gexf: bool = False,
    expand_with_dependents: bool = False,
    max_packages_to_expand: int = 1000,
    max_dependents_per_package: int = 20,
) -> dict:
    """
    Tam analiz pipeline'ını çalıştır.
    
    Türkçe açıklama: Top N paket listesinden graf kurar, metrikleri hesaplar,
    risk skorlarını üretir, CSV/JSON çıktılar oluşturur ve opsiyonel olarak
    görselleştirmeler yapar. Notebook'lardan tek fonksiyonla çağrılabilir.

    Yeni Varsayılanlar (2025-11-24):
        - leaderboard_mode="trending" (en çok trend olan paketler)
        - depth=7 (7 kademe derinlik, geniş ekosistem analizi)
        - top_n=1000 (API limiti dahilinde)

    Typical usage from a notebook:
        from analysis import run_pipeline
        
        # Varsayılan: Trending + 1000 paket + 7 kademe
        res = run_pipeline()
        
        # Downloads modu ile karşılaştırma
        res = run_pipeline(top_n=1000, leaderboard_mode="downloads", depth=3)
        
        # Ağı dependent paketlerle genişletmek için:
        res = run_pipeline(
            top_n=2000, 
            expand_with_dependents=True,
            max_packages_to_expand=1000,  # İlk 1000 paket için dependent çek
            max_dependents_per_package=20  # Her paket için max 20 dependent
        )

    Returns a dict with summary info and paths to major outputs.
    """
    res_dir = Path(results_dir)
    res_dir.mkdir(parents=True, exist_ok=True)

    # 1) Determine top package list with metadata
    packages_metadata = None
    if top_packages is None:
        print(f"Fetching top {top_n} packages from leaderboard (mode: {leaderboard_mode})...")
        packages_metadata = ah.fetch_leaderboard_packages(mode=leaderboard_mode, limit=top_n, return_metadata=True)
        top_list: List[str] = [p["name"] for p in packages_metadata]
        print(f"  ✅ {len(top_list)} paket alındı (dependents_count node weight olarak kullanılacak)")
    else:
        top_list = list(top_packages)
        print(f"  ⚠️ Özel paket listesi kullanılıyor, dependents_count metadata yok")

    # 2) Build dependency graph (Dependent -> Dependency) with depth=7
    cachep = Path(cache_path) if cache_path else None
    print(f"Building dependency graph (depth={depth}, expand_dependents={expand_with_dependents})...")
    
    # Eğer expand_with_dependents aktifse, sadece ilk N paketi genişlet
    packages_to_expand = top_list[:max_packages_to_expand] if expand_with_dependents else top_list
    
    G, top_set = ah.build_dependency_graph(
        packages_to_expand if expand_with_dependents else top_list,
        cache_path=cachep,
        include_peer_deps=include_peer_deps,
        expand_with_dependents=expand_with_dependents,
        max_dependents_per_package=max_dependents_per_package,
        depth=depth,
        packages_metadata=packages_metadata,
    )
    
    # Eğer genişlettikse ama bazı paketler atlandıysa, onları da node olarak ekle
    if expand_with_dependents and len(top_list) > max_packages_to_expand:
        print(f"  → Kalan {len(top_list) - max_packages_to_expand} paket node olarak ekleniyor (dependents çekilmeden)...")
        for pkg in top_list[max_packages_to_expand:]:
            G.add_node(pkg)

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
    ah.save_metrics(in_deg, out_deg, btw, top_set, metrics_p, G=G)  # Graf'ı da geç (metadata için)
    ah.save_risk_scores(risk, in_deg, out_deg, btw, top_set, risk_p)
    ah.save_graph_stats(G, stats_p)
    
    # 5.1) GEPHI EXPORT - Ana çıktı: ID bazlı edge CSV
    print("Generating Gephi-ready files with package IDs...")
    metrics_dict = {}
    with metrics_p.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            pkg = row.get("package", "")
            if pkg:
                metrics_dict[pkg] = row
    risks_dict = {}
    if risk_p.exists():
        with risk_p.open(encoding="utf-8") as f:
            for row in csv.DictReader(f):
                pkg = row.get("package", "")
                if pkg:
                    risks_dict[pkg] = row
    id_map = ex.export_gephi_from_graph(G, metrics_dict, risks_dict, res_dir)
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
    # Save expanded README-style summary inside results as `readme.md`
    ah.save_report(in_deg, out_deg, btw, top_set, res_dir / "readme.md")
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

    # 9) Optionally write GEXF if requested
    if export_gexf:
        print("Writing GEXF format...")
        try:
            ex.write_gexf(res_dir / "graph.gexf", id_map, metrics_dict, [])
        except Exception as e:
            print(f"GEXF export failed: {e}")

    summary = {
        "nodes": G.number_of_nodes(),
        "edges": G.number_of_edges(),
        "results_dir": str(res_dir),
        "gephi_nodes": str(res_dir / "gephi_nodes.csv"),
        "gephi_edges": str(res_dir / "gephi_edges.csv"),
        "graph_gexf": str(res_dir / "graph.gexf") if export_gexf else None,
        "id_map_sample": dict(list(id_map.items())[:10]),
    }
    print("\n" + "="*60)
    print("✓ Pipeline tamamlandı!")
    print("="*60)
    print(f"Düğüm sayısı: {G.number_of_nodes()}")
    print(f"Kenar sayısı: {G.number_of_edges()}")
    print(f"\nGephi için hazır dosyalar:")
    print(f"  → {res_dir / 'gephi_nodes.csv'}")
    print(f"  → {res_dir / 'gephi_edges.csv'}")
    print("="*60)
    return summary
