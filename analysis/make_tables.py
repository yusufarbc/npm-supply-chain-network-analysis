"""LaTeX uzun tabloları üretim yardımcıları (TR).

`results/` dizinindeki CSV'lerden top listeleri oluşturarak longtable
formatında `.tex` dosyaları üretir.
"""

import csv
from pathlib import Path
from typing import List
import glob


def _escape_latex(s: str) -> str:
    """
    LaTeX özel karakterlerini kaçış karakteri ile kodla.
    
    Türkçe açıklama: &, %, $, #, _, {, } gibi karakterleri LaTeX-güvenli hale getirir.
    """
    if s is None:
        return ""
    return (
        str(s)
        .replace("&", "\\&")
        .replace("%", "\\%")
        .replace("$", "\\$")
        .replace("#", "\\#")
        .replace("_", "\\_")
        .replace("{", "\\{")
        .replace("}", "\\}")
    )


def _lt_begin(f, caption: str, cols: str, header_line: str) -> None:
    """Longtable başlangıç bloğunu yaz (TR)."""
    f.write('\\begin{longtable}{' + cols + '}' + '\n')
    f.write('\\caption{' + caption + '}\\\\' + '\n')
    f.write('\\toprule' + '\n')
    f.write(header_line + ' \\\\' + '\n')
    f.write('\\midrule' + '\n')
    f.write('\\endfirsthead' + '\n')
    f.write('\\toprule' + '\n')
    f.write(header_line + ' \\\\' + '\n')
    f.write('\\midrule' + '\n')
    f.write('\\endhead' + '\n')
    f.write('\\bottomrule' + '\n')
    f.write('\\endfoot' + '\n')
    f.write('\\bottomrule' + '\n')
    f.write('\\endlastfoot' + '\n')


def _lt_end(f) -> None:
    """Longtable bitişini yaz (TR)."""
    f.write('\\end{longtable}' + '\n')


def write_metrics_top20_in(res: Path) -> bool:
    """
    metrics.csv'den In-Degree'e göre ilk 20'yi uzun tablo olarak yaz.
    
    Türkçe açıklama: LaTeX longtable formatında .tex dosyası üretir.
    """
    mfile = res / 'metrics.csv'
    if not mfile.exists():
        return False
    with mfile.open(encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        try:
            r['in_degree'] = int(r.get('in_degree', 0))
        except Exception:
            r['in_degree'] = 0
    rows.sort(key=lambda r: r['in_degree'], reverse=True)
    top = rows[:20]
    tex = res / 'metrics_top20_in_degree.tex'
    with tex.open('w', encoding='utf-8') as f:
        _lt_begin(f, 'Top 20 In-Degree (Toplam Dugumler)', 'lrrrr', 'Paket & In-Degree & Out-Degree & Betweenness & TopN?')
        for r in top:
            pkg = (r.get('package','') or '').replace('&','\\&')
            indeg = r.get('in_degree', 0)
            outdeg = r.get('out_degree','0')
            btw = r.get('betweenness','0.000000')
            istop = r.get('is_topN', r.get('is_top100','False'))
            f.write(f"{pkg} & {indeg} & {outdeg} & {btw} & {istop} \\\\" + "\n")
        _lt_end(f)
    return True


def write_risk_top20(res: Path) -> bool:
    """
    risk_scores.csv'den en yüksek riskli ilk 20'yi uzun tablo olarak yaz.
    
    Türkçe açıklama: Risk skoru ile sıralı LaTeX tablosu oluşturur.
    """
    rfile = res / 'risk_scores.csv'
    if not rfile.exists():
        return False
    with rfile.open(encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        try:
            r['risk_score'] = float(r.get('risk_score', 0.0))
        except Exception:
            r['risk_score'] = 0.0
    rows.sort(key=lambda r: r['risk_score'], reverse=True)
    top = rows[:20]
    tex = res / 'risk_scores_top20.tex'
    with tex.open('w', encoding='utf-8') as f:
        _lt_begin(f, 'Top 20 Risk Skoru', 'lrrrrr', 'Paket & Risk & In-Degree & Out-Degree & Betweenness & TopN?')
        for r in top:
            pkg = (r.get('package','') or '').replace('&','\\&')
            risk = f"{float(r.get('risk_score',0)):.6f}"
            indeg = r.get('in_degree','0')
            outdeg = r.get('out_degree','0')
            btw = r.get('betweenness','0.000000')
            istop = r.get('is_topN','False')
            f.write(f"{pkg} & {risk} & {indeg} & {outdeg} & {btw} & {istop} \\\\" + "\n")
        _lt_end(f)
    return True


def write_edge_betweenness_top10(res: Path) -> bool:
    """
    Edge betweenness ilk 10'u uzun tablo olarak yaz.
    
    Türkçe açıklama: En yüksek köprü kenarları LaTeX tablosu olarak kaydeder.
    """
    p = res / 'edge_betweenness_top10.csv'
    if not p.exists():
        return False
    with p.open(encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    norm = []
    for r in rows:
        try:
            eb = float(r.get('edge_betweenness', '0') or 0)
        except Exception:
            eb = 0.0
        u = (r.get('u','') or '').replace('&','\\&')
        v = (r.get('v','') or '').replace('&','\\&')
        norm.append((u, v, eb))
    norm.sort(key=lambda t: t[2], reverse=True)
    tex = res / 'edge_betweenness_top10.tex'
    with tex.open('w', encoding='utf-8') as f:
        _lt_begin(f, 'Edge Betweenness Ilk 10 (Yuksek kopru kenarlar)', 'l l r', 'U & V & Edge Betweenness')
        for u,v,eb in norm[:10]:
            f.write(f"{u} & {v} & {eb:.6f} \\\\" + "\n")
        _lt_end(f)
    return True


def write_cascade_impact_top20(res: Path) -> bool:
    """
    Kaskad etki (ters yön) ilk 20'yi uzun tablo olarak yaz.
    
    Türkçe açıklama: Her paket için etkilenen dependent sayısını gösterir.
    """
    p = res / 'cascade_impact_top20.csv'
    if not p.exists():
        return False
    with p.open(encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    norm = []
    for r in rows:
        name = (r.get('package','') or '').replace('&','\\&')
        try:
            cnt = int(float(r.get('impacted_count', '0') or 0))
        except Exception:
            cnt = 0
        norm.append((name, cnt))
    norm.sort(key=lambda t: t[1], reverse=True)
    tex = res / 'cascade_impact_top20.tex'
    with tex.open('w', encoding='utf-8') as f:
        _lt_begin(f, 'Basamaklanma Etkisi: Top 20 (Ters yonde etkilenebilecek paket sayisi)', 'l r', 'Paket & Etkilenen Paket Sayisi')
        for name, cnt in norm[:20]:
            f.write(f"{name} & {cnt} \\\\" + "\n")
        _lt_end(f)
    return True


def write_metrics_top20_out(res: Path) -> bool:
    """
    metrics.csv'den Out-Degree'e göre ilk 20'yi uzun tablo olarak yaz.
    
    Türkçe açıklama: En çok bağımlılığa sahip paketleri listeler.
    """
    mfile = res / 'metrics.csv'
    if not mfile.exists():
        return False
    with mfile.open(encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        try:
            r['out_degree'] = int(r.get('out_degree', 0))
        except Exception:
            r['out_degree'] = 0
    rows.sort(key=lambda r: r['out_degree'], reverse=True)
    top = rows[:20]
    tex = res / 'metrics_top20_out_degree.tex'
    with tex.open('w', encoding='utf-8') as f:
        _lt_begin(f, 'Top 20 Out-Degree (Toplam Dugumler)', 'lrrrr', 'Paket & Out-Degree & In-Degree & Betweenness & TopN?')
        for r in top:
            pkg = (r.get('package','') or '').replace('&','\\&')
            outdeg = r.get('out_degree', 0)
            indeg = r.get('in_degree','0')
            btw = r.get('betweenness','0.000000')
            istop = r.get('is_topN', r.get('is_top100','False'))
            f.write(f"{pkg} & {outdeg} & {indeg} & {btw} & {istop} \\\\" + "\n")
        _lt_end(f)
    return True


def write_metrics_top20_betweenness(res: Path) -> bool:
    """
    metrics.csv'den Betweenness'e göre ilk 20'yi uzun tablo olarak yaz.
    
    Türkçe açıklama: Ağın en kritik köprü düğümlerini gösterir.
    """
    mfile = res / 'metrics.csv'
    if not mfile.exists():
        return False
    with mfile.open(encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        try:
            r['betweenness'] = float(r.get('betweenness', 0.0))
        except Exception:
            r['betweenness'] = 0.0
    rows.sort(key=lambda r: r['betweenness'], reverse=True)
    top = rows[:20]
    tex = res / 'metrics_top20_betweenness.tex'
    with tex.open('w', encoding='utf-8') as f:
        _lt_begin(f, 'Top 20 Betweenness (Toplam Dugumler)', 'lrrrr', 'Paket & Betweenness & In-Degree & Out-Degree & TopN?')
        for r in top:
            pkg = (r.get('package','') or '').replace('&','\\&')
            indeg = r.get('in_degree','0')
            outdeg = r.get('out_degree','0')
            btw = f"{float(r.get('betweenness',0.0)):.6f}"
            istop = r.get('is_topN', r.get('is_top100','False'))
            f.write(f"{pkg} & {btw} & {indeg} & {outdeg} & {istop} \\\\" + "\n")
        _lt_end(f)
    return True


def main():
    """
    results/ dizinindeki CSV'lerden LaTeX tablolarını üret.
    
    Türkçe açıklama: Tüm standart CSV'ler için .tex dosyaları oluşturur.
    """
    res = Path('results')
    res.mkdir(exist_ok=True)
    ok1 = write_metrics_top20_in(res)
    ok2 = write_risk_top20(res)
    ok3 = write_edge_betweenness_top10(res)
    ok4 = write_cascade_impact_top20(res)
    ok5 = write_metrics_top20_out(res)
    ok6 = write_metrics_top20_betweenness(res)
    print('metrics_top20_in_degree.tex', 'OK' if ok1 else 'SKIP')
    print('risk_scores_top20.tex', 'OK' if ok2 else 'SKIP')
    print('edge_betweenness_top10.tex', 'OK' if ok3 else 'SKIP')
    print('cascade_impact_top20.tex', 'OK' if ok4 else 'SKIP')
    print('metrics_top20_out_degree.tex', 'OK' if ok5 else 'SKIP')
    print('metrics_top20_betweenness.tex', 'OK' if ok6 else 'SKIP')


def write_table_for_csv(res: Path, csv_path: Path) -> bool:
    """
    Herhangi bir CSV dosyası için genel longtable yazıcı.
    
    Türkçe açıklama: CSV başlıklarını alarak otomatik LaTeX tablo üretir.

    Produces `results/table_<stem>.tex` with a caption equal to the CSV filename.
    """
    if not csv_path.exists():
        return False
    try:
        with csv_path.open(encoding='utf-8') as f:
            rdr = csv.reader(f)
            rows = list(rdr)
        if not rows:
            return False
        headers = rows[0]
        body = rows[1:]
        tex = res / f"table_{csv_path.stem}.tex"
        with tex.open('w', encoding='utf-8') as f:
            colspec = 'l' * len(headers)
            header_line = ' & '.join([_escape_latex(h) for h in headers])
            _lt_begin(f, f"Table: {_escape_latex(csv_path.name)}", colspec, header_line)
            for r in body:
                cells = [_escape_latex(c) for c in r]
                f.write(' & '.join(cells) + ' \\\\' + '\n')
            _lt_end(f)
        return True
    except Exception:
        return False


def write_all_csv_tables(res: Path) -> List[str]:
    """
    results/ dizinindeki tüm CSV dosyalarını tarar ve LaTeX tabloları üretir.
    
    Türkçe açıklama: Her CSV için otomatik tablo oluşturarak üretilen .tex dosya 
    yollarının listesini döndürür.

    Returns list of generated tex file paths (as strings).
    """
    generated: List[str] = []
    csv_files = sorted([Path(p) for p in glob.glob(str(res / '*.csv'))])
    for p in csv_files:
        ok = write_table_for_csv(res, p)
        if ok:
            generated.append(str(res / f"table_{p.stem}.tex"))
    return generated
