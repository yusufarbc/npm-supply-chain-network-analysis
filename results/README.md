# Results Summary

This file is an auto-generated summary of the dependency network analysis.

## Quick Usage

- All CSV outputs are in this `results/` directory (`edges.csv`, `metrics.csv`, `risk_scores.csv`, etc.).
- To inspect the graph in Gephi: run the exporter to produce `gephi_nodes.csv` and `gephi_edges.csv`, or open `graph.gexf` if present.

## Top-20 (All Nodes) - In-Degree
- @babel/helper-plugin-utils: 110
- call-bound: 41
- postcss-value-parser: 39
- call-bind: 36
- debug: 34
- @types/node: 34
- es-errors: 33
- @babel/types: 32
- define-properties: 29
- chalk: 28
- @csstools/css-tokenizer: 27
- @jest/types: 26
- @csstools/css-parser-algorithms: 26
- @csstools/utilities: 23
- get-intrinsic: 22
- jest-util: 22
- postcss-selector-parser: 21
- graceful-fs: 21
- @babel/traverse: 20
- es-object-atoms: 20

## Top-20 (All Nodes) - Out-Degree
- @babel/preset-env: 70
- postcss-preset-env: 67
- es-abstract: 54
- react-scripts: 48
- workbox-build: 37
- eslint: 34
- cssnano-preset-default: 30
- webpack-dev-server: 28
- @jest/core: 28
- express: 27
- webpack: 25
- jest-config: 24
- react-dev-utils: 24
- @jest/reporters: 23
- jest-runtime: 22
- jest-runner: 22
- jest-snapshot: 21
- jsdom: 20
- jest-circus: 20
- eslint-plugin-import: 19

## Top-20 (All Nodes) - Betweenness
- jest-circus: 0.001144
- @babel/core: 0.001112
- babel-jest: 0.001087
- jest-runner: 0.001000
- @babel/helper-create-class-features-plugin: 0.000798
- get-intrinsic: 0.000771
- jest-snapshot: 0.000549
- @babel/traverse: 0.000523
- babel-preset-current-node-syntax: 0.000499
- babel-plugin-istanbul: 0.000466
- @babel/helper-compilation-targets: 0.000316
- micromatch: 0.000316
- babel-preset-jest: 0.000299
- call-bound: 0.000283
- jest-haste-map: 0.000266
- @istanbuljs/load-nyc-config: 0.000266
- @babel/code-frame: 0.000255
- @babel/generator: 0.000244
- @babel/types: 0.000236
- @jest/types: 0.000211

## Top-20 (Top N Cohort) - In-Degree
- @babel/helper-plugin-utils: 110
- postcss-value-parser: 39
- debug: 34
- @babel/types: 32
- @jest/types: 26
- jest-util: 22
- get-intrinsic: 22
- postcss-selector-parser: 21
- @babel/traverse: 20
- browserslist: 16
- minimatch: 15
- workbox-core: 14
- slash: 14
- @babel/core: 12
- @jridgewell/trace-mapping: 12
- pretty-format: 12
- has-symbols: 12
- has-tostringtag: 11
- schema-utils: 11
- @babel/helper-create-class-features-plugin: 10

## Top-20 (Top N Cohort) - Out-Degree
- @babel/preset-env: 70
- postcss-preset-env: 67
- react-scripts: 48
- workbox-build: 37
- eslint: 34
- cssnano-preset-default: 30
- webpack-dev-server: 28
- @jest/core: 28
- express: 27
- jest-config: 24
- react-dev-utils: 24
- @jest/reporters: 23
- jest-runtime: 22
- jest-runner: 22
- jest-snapshot: 21
- jsdom: 20
- eslint-plugin-react: 18
- deep-equal: 18
- babel-preset-react-app: 17
- jest-jasmine2: 17

## Top-20 (Top N Cohort) - Betweenness
- @babel/core: 0.001112
- babel-jest: 0.001087
- jest-runner: 0.001000
- @babel/helper-create-class-features-plugin: 0.000798
- get-intrinsic: 0.000771
- jest-snapshot: 0.000549
- @babel/traverse: 0.000523
- babel-plugin-istanbul: 0.000466
- micromatch: 0.000316
- @babel/helper-compilation-targets: 0.000316
- babel-preset-jest: 0.000299
- @istanbuljs/load-nyc-config: 0.000266
- jest-haste-map: 0.000266
- @babel/generator: 0.000244
- @babel/types: 0.000236
- @jest/transform: 0.000211
- @jest/types: 0.000211
- browserslist: 0.000200
- jest-resolve: 0.000200
- jest-environment-node: 0.000189

## Files Created

- `edges.csv` — edge list (source=dependent, target=dependency)
- `metrics.csv` — per-node metrics: in_degree,out_degree,betweenness,is_topN
- `risk_scores.csv` — combined risk score and component metrics
- `graph_stats.json` and `graph_stats.csv` — overall graph statistics
- `gephi_nodes.csv`, `gephi_edges.csv` — optional Gephi import files

## Notes & Next Steps

- Betweenness centrality is expensive for large graphs; consider sampling via `sample_k`.
- The exporter assigns deterministic numeric ids to packages for Gephi import.
- You can extend this report by adding sections with vulnerability data, CVE cross-references, or manual annotations.