"""Reusable exporter functions for Gephi and other consumers.

This module contains importable functions so other scripts or notebooks
can programmatically produce Gephi-compatible CSVs or a GEXF file.
"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Dict, Optional, Iterable


def read_metrics(path: Path) -> Dict[str, Dict[str, str]]:
    data: Dict[str, Dict[str, str]] = {}
    if not path.exists():
        return data
    with path.open(encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            pkg = (row.get("package") or "").strip()
            if not pkg:
                continue
            data[pkg] = row
    return data


def read_edges(path: Path) -> Iterable[Dict[str, str]]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as f:
        r = csv.DictReader(f)
        rows = [row for row in r]
    return rows


def build_id_map(pkgs: set) -> Dict[str, int]:
    ordered = sorted(pkgs)
    return {p: i + 1 for i, p in enumerate(ordered)}


def write_nodes(nodes_path: Path, id_map: Dict[str, int], metrics: Dict[str, Dict[str, str]], risks: Optional[Dict[str, Dict[str, str]]] = None) -> None:
    nodes_path.parent.mkdir(parents=True, exist_ok=True)
    with nodes_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "label", "package", "in_degree", "out_degree", "betweenness", "risk_score", "is_topN"])
        for pkg, pid in sorted(id_map.items(), key=lambda kv: kv[1]):
            m = metrics.get(pkg, {})
            in_d = m.get("in_degree", "0")
            out_d = m.get("out_degree", "0")
            btw = m.get("betweenness", "0.000000")
            is_top = m.get("is_topN", m.get("is_top100", "False"))
            risk = ""
            if risks and pkg in risks:
                risk = risks[pkg].get("risk_score", "")
            w.writerow([pid, pkg, pkg, in_d, out_d, btw, risk, is_top])


def write_edges_csv(edges_path: Path, edges_rows, id_map: Dict[str, int]) -> None:
    edges_path.parent.mkdir(parents=True, exist_ok=True)
    with edges_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["source", "target", "weight", "directed"])
        for r in edges_rows:
            src = (r.get("source") or r.get("u") or "").strip()
            tgt = (r.get("target") or r.get("v") or "").strip()
            if not src or not tgt:
                continue
            sid = id_map.get(src)
            tid = id_map.get(tgt)
            if sid is None or tid is None:
                continue
            w.writerow([sid, tid, 1, True])


def write_gexf(gexf_path: Path, id_map: Dict[str, int], metrics: Dict[str, Dict[str, str]], edges_rows) -> None:
    try:
        import networkx as nx
    except Exception:
        print("networkx not available; skipping GEXF export")
        return
    G = nx.DiGraph()
    for pkg, pid in id_map.items():
        m = metrics.get(pkg, {})
        attrs = {
            "package": pkg,
            "label": pkg,
            "in_degree": int(m.get("in_degree", 0) or 0),
            "out_degree": int(m.get("out_degree", 0) or 0),
            "betweenness": float(m.get("betweenness", 0.0) or 0.0),
        }
        G.add_node(pid, **attrs)
    for r in edges_rows:
        src = (r.get("source") or r.get("u") or "").strip()
        tgt = (r.get("target") or r.get("v") or "").strip()
        if not src or not tgt:
            continue
        sid = id_map.get(src)
        tid = id_map.get(tgt)
        if sid is None or tid is None:
            continue
        G.add_edge(sid, tid, weight=1)
    try:
        gexf_path.parent.mkdir(parents=True, exist_ok=True)
        nx.write_gexf(G, str(gexf_path))
        print(f"Wrote GEXF: {gexf_path}")
    except Exception as e:
        print("Failed to write GEXF:", e)


def export_for_gephi(results_dir: str = "results", write_gexf_flag: bool = False) -> Dict[str, int]:
    res = Path(results_dir)
    edges_path = res / "edges.csv"
    metrics_path = res / "metrics.csv"
    risks_path = res / "risk_scores.csv"

    edges_rows = list(read_edges(edges_path))
    metrics = read_metrics(metrics_path)
    risks = read_metrics(risks_path) if risks_path.exists() else None

    pkgs = set()
    pkgs.update(metrics.keys())
    if risks:
        pkgs.update(risks.keys())
    for r in edges_rows:
        src = (r.get("source") or r.get("u") or "").strip()
        tgt = (r.get("target") or r.get("v") or "").strip()
        if src:
            pkgs.add(src)
        if tgt:
            pkgs.add(tgt)

    id_map = build_id_map(pkgs)

    out_nodes = res / "gephi_nodes.csv"
    out_edges = res / "gephi_edges.csv"
    write_nodes(out_nodes, id_map, metrics, risks)
    write_edges_csv(out_edges, edges_rows, id_map)
    print(f"Wrote: {out_nodes} and {out_edges} (nodes: {len(id_map)})")

    if write_gexf_flag:
        write_gexf(res / "graph.gexf", id_map, metrics, edges_rows)

    return id_map


def main():
    import argparse

    p = argparse.ArgumentParser(description="Export graph for Gephi (CSV + optional GEXF)")
    p.add_argument("--results", default="results", help="results directory (default: results)")
    p.add_argument("--gexf", action="store_true", help="also write results/graph.gexf if networkx available")
    args = p.parse_args()
    export_for_gephi(args.results, args.gexf)


if __name__ == "__main__":
    main()
