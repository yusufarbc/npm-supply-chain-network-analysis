# 📚 Literature Review and Academic Background

> **Context:** This document summarizes academic studies on the NPM ecosystem and software supply chain security, key findings, and the project's position within this literature.
>
> 🏠 [Return to Home](./README.md)

## 1. General Background and Gap Analysis

This study compiles and synthesizes key works, findings, and gaps in the field of Software Supply Chain Attacks (SSCA) in open-source package ecosystems (especially NPM). The goal is to illuminate the path to the question "which nodes should we invest in first at the ecosystem level?" and to strengthen the topological risk framework by linking it with literature.

- **Threat Taxonomies:** Threat taxonomies and case compilations classify cross-ecosystem installation/runtime techniques well: *Backstabber’s Knife Collection* (2015–2019, 174 cases) and *Hitchhiker’s Guide* provide the baseline.
- **NPM-Focused Risks:** Practical risks and phenomena focused on NPM (Wyss; Kang Yip) are detailed. However, this literature does not directly translate the question "which nodes should be invested in first at the ecosystem level?" into operational prioritization.
- **Network Science:** On the network science front, NPM's small-world/scale-free structure and the disproportionate impact of single maintainers/packages have been clearly demonstrated (Zimmermann; Hafner; Oldnall). However, an approach that combines structural/topological centrality with usage intensity into a single composite "criticality" metric remains missing.

**Our Contribution:** A **Composite Criticality Score (CCS/BRS)** that fuses topological measures + usage intensity + maintenance/freshness signals on a directed graph established with official resolution rules on the download-based core (Top 1000) of the last 12 months, and operational priority lists based on it.

## 2. NPM Network Topology and Fragility

- **Zimmermann (2019):** Few maintainer accounts have capacity to affect the majority; SPOF (single point of failure) and maintenance gap impact.
- **Hafner (2021):** Quantifies that the network is fragile under targeted node removals; relatively resilient under random failures; community formations.
- **Oldnall (2017):** Five-year NPM topology at version level; small-world + scale-free architecture; example of up to 200,000 reverse transitive dependencies.

> **Main Message:** Compromise of hub/backbone nodes dramatically increases systemic risk; therefore network-based prioritization is necessary.

## 3. Dependency Resolution and Propagation

- **Liu et al. (ICSE 2022):** DVGraph/DTResolver — Faithful to NPM's official resolution rules, large-scale (10M+ versions, 60M+ relationships) knowledge graph and transitive propagation paths.
- **Duan et al. (2020):** Registry exploitation measurement in interpreted languages; qualitative framework + 339 new malicious package reports through meta/static/dynamic analysis.

> **Main Message:** Correct resolution rules are a prerequisite for accurately measuring transitive propagation and impacts.

## 4. Detection Pipeline: ML/Dynamic Analysis and Signatures

- **Amalfi (2022):** ML + reproduction + clone detection; 95 new samples; lightweight and fast pipeline.
- **Cerebro (2023):** Cross-language detection with behavior sequences; total 196+ new samples in NPM/PyPI.
- **OSCAR (2024):** Strong F1 in sandbox + fuzz + hooked tracing; 10,404 NPM, 1,235 PyPI malicious packages in industrial deployment.
- **ACME (2021):** Signature generation with AST clustering; extract signatures from clusters and scan registry.

> **Main Message:** Detection pipelines are maturing; however, producing a priority scanning queue with a **topological pre-filter** (BRS) is critical for limited analyst capacity.

## 5. Maintenance/Recency and Operational Signals

- **TOOD/PFET (Rahman et al., 2024):** 2.9M packages, 66.8M versions; PyPI fast in general updates; Cargo ahead in security fix adoption.
- **Cogo (2020):** Downgrade, same-day releases, deprecation mining; maintenance phenomena.
- **Ahlstrom (2025):** Dramatic reduction of license/security risks (%86–94, %57–91) through dependency pruning.

> **Main Message:** When recency and maintenance signals are used together with CRS, they produce actionable **investment plans**.

## 6. Policy, Signing, and Integrity

- **in‑toto (Torres‑Arias, 2020):** End-to-end integrity; cryptographic binding of chain steps conforming to policy.
- **Schorlemmer (2024):** Signature adoption; policy impact; tooling improving quality.
- **Vaidya (2022):** Repository integrity, commit signing, software certification service (SCS).

> **Main Message:** Policy/integrity pipeline emphasizes the role of registry managers and signing infrastructure; **target lists** with CRS feed this pipeline.

## 7. Synthesis: Gap → Contribution Mapping

| Area | Current Gap | Project's Contribution |
|------|---------------|------------------|
| **Prioritization** | Lack of operational prioritization criteria at ecosystem level. | **Behavioral Risk Score (BRS)** = 0.35·btw' + 0.30·in' + 0.15·inv_clust' + ... |
| **Detection** | Detection pipeline not connected with transitive propagation/high-fidelity resolution. | Directed graph built with official rules + BRS pre-filter → **Priority scanning queue** |
| **Policy** | Policy/integrity and community health signals not operationalized. | BRS target lists + TOOD/PFET → **Targeted intervention plans** |

---

## 8. Selected References (Summary)

### Foundational Works
1. **Backstabber's Knife Collection (Ohm et al., 2020):** 174 real cases, attack trees.
2. **Hitchhiker's Guide (Ladisa et al., 2023):** 7 ecosystems, 3 installation, 5 runtime techniques.
3. **Small World with High Risks (Zimmermann, 2019):** SPOF and maintainer centrality.
4. **The Web of Dependencies (Oldnall, 2017):** NPM network evolution, 200K reverse dependency example.

### Detection and Analysis
5. **DVGraph/DTResolver (Liu, 2022):** Precise dependency resolution.
6. **Amalfi (2022), Cerebro (2023), OSCAR (2024):** Automated detection systems.

### Maintenance and Security
7. **Dependency Update Practice (Rahman, 2024):** Recency metrics (TOOD/PFET).
8. **in-toto (Torres-Arias, 2020):** Supply chain integrity.

---
*This document is compiled from the literature review section in the `academic/Readme.md` file.*
