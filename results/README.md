# Results Summary

This file is an auto-generated summary of the dependency network analysis.

## Quick Usage

- All CSV outputs are in this `results/` directory (`edges.csv`, `metrics.csv`, `risk_scores.csv`, etc.).
- To inspect the graph in Gephi: run the exporter to produce `gephi_nodes.csv` and `gephi_edges.csv`, or open `graph.gexf` if present.

## Top-20 (All Nodes) - In-Degree
- tslib: 138
- @smithy/types: 93
- @babel/helper-plugin-utils: 81
- @aws-sdk/types: 57
- @smithy/protocol-http: 45
- debug: 40
- call-bound: 39
- @smithy/util-utf8: 35
- @smithy/node-config-provider: 34
- @types/node: 31
- es-errors: 31
- @aws-sdk/core: 31
- @smithy/util-middleware: 29
- @smithy/smithy-client: 28
- call-bind: 27
- chalk: 26
- @smithy/core: 26
- @smithy/util-base64: 25
- @jest/types: 24
- @smithy/middleware-endpoint: 23

## Top-20 (All Nodes) - Out-Degree
- telecom-mas-agent: 83
- @babel/preset-env: 70
- @aws-sdk/client-s3: 55
- es-abstract: 54
- @aws-sdk/client-s3-control: 45
- @aws-sdk/client-lambda: 44
- cypress: 42
- @aws-sdk/client-cloudfront: 41
- @aws-sdk/client-cloudwatch: 41
- @aws-sdk/client-dynamodb: 41
- @aws-sdk/client-ec2: 41
- @aws-sdk/client-rds: 41
- @aws-sdk/client-sqs: 41
- @aws-sdk/client-cloudformation: 40
- @aws-sdk/client-iam: 40
- @aws-sdk/client-ses: 40
- @aws-sdk/client-cloudhsm: 39
- @aws-sdk/client-cloudsearch: 39
- @aws-sdk/client-cloudtrail: 39
- @aws-sdk/client-kms: 39

## Top-20 (All Nodes) - Betweenness
- es-abstract: 0.002503
- http-signature: 0.000482
- form-data: 0.000466
- get-intrinsic: 0.000439
- es-set-tostringtag: 0.000346
- call-bind: 0.000322
- reflect.getprototypeof: 0.000322
- which-builtin-type: 0.000289
- side-channel: 0.000273
- sshpk: 0.000257
- qs: 0.000209
- typed-array-length: 0.000201
- typed-array-byte-offset: 0.000185
- define-properties: 0.000174
- unbox-primitive: 0.000161
- call-bound: 0.000131
- internal-slot: 0.000129
- jsprim: 0.000129
- which-boxed-primitive: 0.000096
- which-collection: 0.000096

## Top-20 (Top N Cohort) - In-Degree
- tslib: 138
- @smithy/types: 93
- @babel/helper-plugin-utils: 81
- @aws-sdk/types: 57
- @smithy/protocol-http: 45
- debug: 40
- call-bound: 39
- @smithy/util-utf8: 35
- @smithy/node-config-provider: 34
- @aws-sdk/core: 31
- @types/node: 31
- es-errors: 31
- @smithy/util-middleware: 29
- @smithy/smithy-client: 28
- call-bind: 27
- @smithy/core: 26
- chalk: 26
- @smithy/util-base64: 25
- @jest/types: 24
- @smithy/url-parser: 23

## Top-20 (Top N Cohort) - Out-Degree
- telecom-mas-agent: 83
- @babel/preset-env: 70
- es-abstract: 54
- @aws-sdk/client-sso: 38
- eslint: 34
- @jest/core: 28
- express: 27
- webpack: 25
- jest-config: 24
- @jest/reporters: 23
- jest-runtime: 22
- jest-runner: 22
- jest-snapshot: 21
- jest-circus: 20
- jsdom: 20
- eslint-plugin-import: 19
- eslint-plugin-react: 18
- @babel/core: 15
- babel-preset-current-node-syntax: 15
- @jest/transform: 15

## Top-20 (Top N Cohort) - Betweenness
- es-abstract: 0.002503
- form-data: 0.000466
- get-intrinsic: 0.000439
- es-set-tostringtag: 0.000346
- reflect.getprototypeof: 0.000322
- call-bind: 0.000322
- which-builtin-type: 0.000289
- side-channel: 0.000273
- qs: 0.000209
- typed-array-length: 0.000201
- typed-array-byte-offset: 0.000185
- define-properties: 0.000174
- unbox-primitive: 0.000161
- call-bound: 0.000131
- internal-slot: 0.000129
- which-collection: 0.000096
- which-boxed-primitive: 0.000096
- get-proto: 0.000075
- hasown: 0.000075
- @babel/types: 0.000064

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