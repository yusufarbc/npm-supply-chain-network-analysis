"""Reusable exporter functions for Gephi and other consumers.

This module contains importable functions so other scripts or notebooks
can programmatically produce Gephi-compatible CSVs or a GEXF file.
"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Dict, Optional, Iterable


def read_metrics(path: Path) -> Dict[str, Dict[str, str]]:
    """
    metrics.csv dosyasını oku ve paket adına göre dict olarak döndür.
    
    Türkçe açıklama: Her paket için metrik değerlerini key-value çiftleri halinde tutar.
    """
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
    """
    edges.csv dosyasını oku ve satırları dict listesi olarak döndür.
    
    Türkçe açıklama: Her kenar (source->target) için bir dict oluşturur.
    """
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as f:
        r = csv.DictReader(f)
        rows = [row for row in r]
    return rows


def build_id_map(pkgs: set) -> Dict[str, int]:
    """
    Paket adlarından deterministik numerik ID haritası oluştur.
    
    Türkçe açıklama: Alfabetik sıralama ile tutarlı ID'ler üretir (Gephi için).
    """
    ordered = sorted(pkgs)
    return {p: i + 1 for i, p in enumerate(ordered)}


def write_nodes(nodes_path: Path, id_map: Dict[str, int], metrics: Dict[str, Dict[str, str]], risks: Optional[Dict[str, Dict[str, str]]] = None) -> None:
    """
    Düğüm listesini Gephi formatında CSV olarak yaz.
    
    Türkçe açıklama: Her düğüm için ID, etiket, metrikler ve risk skoru içerir.
    """
    nodes_path.parent.mkdir(parents=True, exist_ok=True)
    with nodes_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "label", "package", "in_degree", "out_degree", "betweenness", "risk_score", "is_topN", "dependents_count", "downloads", "rank"])
        for pkg, pid in sorted(id_map.items(), key=lambda kv: kv[1]):
            m = metrics.get(pkg, {})
            in_d = m.get("in_degree", "0")
            out_d = m.get("out_degree", "0")
            btw = m.get("betweenness", "0.000000")
            is_top = m.get("is_topN", m.get("is_top100", "False"))
            dep_count = m.get("dependents_count", "0")
            downloads = m.get("downloads", "0")
            rank = m.get("rank", "0")
            
            risk = ""
            if risks and pkg in risks:
                risk = risks[pkg].get("risk_score", "")
            w.writerow([pid, pkg, pkg, in_d, out_d, btw, risk, is_top, dep_count, downloads, rank])


def write_edges_csv(edges_path: Path, edges_rows, id_map: Dict[str, int]) -> None:
    """
    Kenar listesini Gephi formatında CSV olarak yaz.
    
    Türkçe açıklama: Numerik ID'ler kullanarak source->target ilişkilerini yazar.
    """
    edges_path.parent.mkdir(parents=True, exist_ok=True)
    with edges_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["source", "target", "directed"])
        for r in edges_rows:
            src = (r.get("source") or r.get("u") or "").strip()
            tgt = (r.get("target") or r.get("v") or "").strip()
            if not src or not tgt:
                continue
            sid = id_map.get(src)
            tid = id_map.get(tgt)
            if sid is None or tid is None:
                continue
            w.writerow([sid, tid, True])


def write_gexf(gexf_path: Path, id_map: Dict[str, int], metrics: Dict[str, Dict[str, str]], edges_rows) -> None:
    """
    NetworkX kullanarak GEXF formatında graf dosyası üret.
    
    Türkçe açıklama: Gephi ve diğer araçlar için XML-tabanlı graf formatı.
    """
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


def export_gephi_from_graph(G, metrics_dict: Dict[str, Dict], risks_dict: Optional[Dict[str, Dict]], results_dir: Path) -> Dict[str, int]:
    """
    NetworkX grafından direkt Gephi dosyalarını üret (optimize edilmiş).
    
    Türkçe açıklama: Graf objesinden ID haritası oluşturur ve Gephi CSV'lerini yazar.
    Bu fonksiyon pipeline içinden çağrılır, daha hızlı ve memory-efficient.
    
    Çıktı formatı:
    - gephi_nodes.csv: 12 sütun (Id, Label, package, in_degree, out_degree, betweenness, 
                       risk_score, is_topN, dependents_count, downloads, rank, is_seed)
    - gephi_edges.csv: 4 sütun (Source, Target, Type, Weight)
    """
    # Tüm düğümleri topla
    all_nodes = set(G.nodes())
    
    # Deterministik ID haritası (alfabetik sıralı)
    id_map = build_id_map(all_nodes)
    
    # İstatistikler için sayaçlar
    nodes_with_metrics = 0
    
    # Nodes CSV - zenginleştirilmiş (node attributes + metrics + risks)
    nodes_path = results_dir / "gephi_nodes.csv"
    nodes_path.parent.mkdir(parents=True, exist_ok=True)
    with nodes_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Id", "Label", "package", "in_degree", "out_degree", "betweenness", "risk_score", "is_topN", 
                   "dependents_count", "downloads", "rank", "is_seed"])
        for pkg in sorted(id_map.keys(), key=lambda x: id_map[x]):
            pid = id_map[pkg]
            
            # Metrics dict'ten değerler
            m = metrics_dict.get(pkg, {})
            in_d = m.get("in_degree", "0")
            out_d = m.get("out_degree", "0")
            btw = m.get("betweenness", "0.000000")
            is_top = m.get("is_topN", "False")
            if m:
                nodes_with_metrics += 1
            
            # Risk dict'ten risk skoru
            risk = risks_dict.get(pkg, {}).get("risk_score", "") if risks_dict else ""
            
            # Graf node attributes'dan metadata çek (güvenli)
            node_attrs = G.nodes.get(pkg, {})
            deps_count = node_attrs.get("dependents_count", 0)
            downloads = node_attrs.get("downloads", 0)
            rank = node_attrs.get("rank", 0)
            is_seed = node_attrs.get("is_seed", False)
            
            w.writerow([pid, pkg, pkg, in_d, out_d, btw, risk, is_top, deps_count, downloads, rank, is_seed])
    
    # Edges CSV - ID bazlı (ANA ÇIKTI)
    edges_path = results_dir / "gephi_edges.csv"
    with edges_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Source", "Target", "Type"])
        for src, tgt in G.edges():
            sid = id_map.get(src)
            tid = id_map.get(tgt)
            if sid is not None and tid is not None:
                w.writerow([sid, tid, "Directed"])
    
    print(f"✅ Gephi dosyaları oluşturuldu:")
    print(f"   📊 Nodes: {len(id_map)} düğüm")
    print(f"      - Metrics olan: {nodes_with_metrics}")
    print(f"   🔗 Edges: {G.number_of_edges()} kenar")
    print(f"   📁 Dosyalar:")
    print(f"      - {nodes_path.name}")
    print(f"      - {edges_path.name}")
    
    return id_map


def export_for_gephi(results_dir: str = "results", write_gexf_flag: bool = False) -> Dict[str, int]:
    """
    Mevcut CSV'lerden Gephi dışa aktarım (geriye uyumluluk için).
    
    Türkçe açıklama: edges.csv, metrics.csv ve risk_scores.csv'den okur, 
    gephi_nodes.csv ve gephi_edges.csv üretir. Opsiyonel olarak GEXF de oluşturur.
    
    NOT: Pipeline kullanıyorsanız, export_gephi_from_graph() otomatik çağrılır.
    """
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
