# Literature & References

This document provides a comprehensive analysis of the existing literature on NPM supply chain security, including key threat taxonomies, network analysis studies, and defense mechanisms.

## 📋 Table of Contents

1. [Executive Summary](#executive-summary)
2. [Annotated Bibliography](#annotated-bibliography)

---


## Executive Summary

### Threat Landscape & Attack Analysis

### 1. Introduction: NPM Ecosystem Scale and Fragility

Node Package Manager (NPM) is a strategic and indispensable component at the center of modern JavaScript/Node.js development. The NPM ecosystem hosts millions of unique packages and serves billions of download requests weekly. While this enormous scale increases productivity on one hand, on the other hand, it exposes each project to security risks through uncontrollably expanding transitive dependencies. Software supply chain breaches have generally shown a 438% increase from 2017 to 2019.

The NPM network exhibits small-world behavior and a scale-free architecture. This structure carries great systemic risk by creating single points of failure (SPOF) when a small number of "hub" (backbone) packages are compromised.

### 2. Major NPM Attack Incidents and Vectors

Attackers use a wide range of vectors, from account takeover to typosquatting, to infiltrate malicious code into the ecosystem.

#### 2.1. Autonomous Worm Attacks: Shai-Hulud (September 2025)

September 2025's "Shai-Hulud" worm represents a systemic evolution in supply chain threats and is a wormable threat with self-replicating capability.

• Attack Vector (Phishing): The attack began with an organized phishing campaign targeting NPM package maintainers. Attackers stole credentials using fake domain names like npmjs.help for Multi-Factor Authentication (MFA) reset fraud of maintainers.
• Scope and Impact: The attack started in 18 packages including chalk, debug, and @ctrl/tinycolor (2.2 million weekly downloads) and quickly affected over 500 NPM packages. The weekly download count of affected packages exceeded 2.6 billion (chalk/debug).
• Payload and Propagation: The worm used compromised NPM tokens to download legitimate packages' tarballs, modify the package.json file, inject malicious script (bundle.js), and republish the package (NpmModule.updatePackage). The malware was designed to steal cloud service tokens (e.g., AWS, GCP) and scan for secret credentials by mimicking legitimate security tools like Trufflehog.
• LLM Usage: It is assessed with moderate confidence that a Large Language Model (LLM) was used to assist in writing the malicious code.
• Result: As a result of the attack, 2,349 credentials (GitHub PATs, cloud keys, etc.) were leaked. Wiz telemetry reported that 500 private repos were made public.

#### 2.2. CI/CD Infrastructure Takeover: Nx / S1ngularity (August 2025)

This incident targeting Nx packages is seen as a direct precursor to the Shai-Hulud attack.

• Vector: Attackers exploited a GitHub Actions injection vulnerability to steal NPM publishing token.
• Action: With the stolen token, malicious versions of Nx's legitimate packages were published for 4 hours. The malicious code scanned user systems for sensitive data and uploaded them to public GitHub repositories.
• Response: After the attack, Nx aimed to avoid token-based authentication by implementing NPM Trusted Publishers mechanism.

#### 2.3. High-Profile Account Takeover and Package Transfer

• UAParser.js (2021): This package used by many large tech companies was modified to contain malicious code through a maintainer's compromised account. The goal was to install coinminer and collect user/credentials.
• event-stream (2018): This popular package was transferred to a malicious actor through social engineering and the new maintainer added payload targeting crypto wallets to the package.
• eslint-scope (2018): An incident based on account takeover where developer credentials were stolen.
• chalk/debug (September 2025): In the first phase of Shai-Hulud, crypto stealer payload was injected into 18 packages.

#### 2.4. Social and Naming Attacks

• Typosquatting: Malicious packages are published with similar names like crossenv instead of cross-env.
• Dependency Confusion: A malicious public package with the same name as an internal package is published with a higher version number and is preferred by the package manager.

### Literature Review Synthesis

The scope and techniques of open-source supply chain attacks have been taxonomized through 174 real incidents occurring between 2015–2019 in **Backstabber’s Knife Collection** [4]; this line is complemented by the cross-ecosystem installation/runtime technique map **Hitchhiker’s Guide** [24] and the study measuring registry abuse and misuse in interpreted languages [28]. Npm-focused practical risks and phenomena are detailed by **Wyss** [1] and **Kang Yip** [12]. However, this literature does not transform the question "which nodes should be invested in first at the ecosystem level?" into an operational prioritization.

On the network science front, npm's small-world/scale-free structure and the disproportionate impact of single maintainers/packages have been clearly demonstrated: **Zimmermann et al.** highlight single maintainer and SPOF risks [20]; **Hafner et al.** quantify fragility and trends in targeted node removals [16]; an early network-topology picture is provided by **Oldnall** [25]. However, transforming structural/topological centrality (degree, betweenness, eigenvector/PageRank, k-core) and usage intensity (download share, reverse-dependency coverage) into a single **composite "criticality" metric** remains missing. We propose the **Composite Criticality Score**, which fuses these two dimensions in the download-based core (top 1000 dependencies downloaded in the last 12 months).

In dependency resolution, **Liu et al.**'s DVGraph/DTResolver pipeline extracts correct transitive trees by adhering to npm's **official resolution rules**; it quantifies propagation and evolution at the ecosystem scale and advances practice in repair [8]. Yet, the findings are not directly translated into an **operational priority list**. We generate a **criticality ranking** on the directed graph we built based on these correctness principles.

In the "Detection" pipeline, while **Amalfi** [19], **OSCAR** [29], **Cerebro** [14], **cross-language** approaches [17], **ACME** [23], and **MeMPtec** [15] produce strong results, a **topological pre-filter** determining where limited analyst capacity should be directed first is missing; our scoring provides a **prioritized scanning queue** to these pipelines. Repository behavior anomalies and intra-pool threat perception [11] offer complementary signals to this queue.

Operational indicators/freshness metrics and maintenance practices feed prioritization: **TOOD/PFET** quantifies freshness and post-vulnerability exposure [5]; **Jafari et al.** reveal practices predicting rapid fix adoption [10]; **Zerouali et al.** examine vulnerability impact and propagation dynamics [18]; **Cogo** mines maintenance phenomena (downgrade, same-day release, deprecation) [22]; **Ahlstrom** shows that pruning unnecessary/test dependencies dramatically reduces license and security risks [9]; **Jaisri/Reid/Kula** map self-contained package dynamics [2]. These signals alone are not sufficient for critical node selection; we integrate them into a **single score** with topological centrality and usage intensity.

On the policy and integrity axis, **in-toto** provides end-to-end chain integrity [13]; factors affecting signature adoption and policy/tool impact are measured by **Schorlemmer** [21]; **SBOM** accuracy/efficiency improvements [3] and repo/artifact authentication proposals [27] define "what should be done?". Additionally, the defense line centered on education-tools-techniques for **source poisoning/NG attacks** [6] and the chain threat portrait [7] offer a contextual framework. Our contribution is to answer the question "**who should it be done on first?**" with a **topological investment plan** and **operational priority lists** in the download-based core.

**In summary:** Threat taxonomies and case compilations [4],[24],[28],[1],[12], network-topology fragility [20],[16],[25], correct transitive resolution [8], robust detection pipelines [19],[29],[14],[17],[23],[15],[11], maintenance/freshness signals [5],[10],[18],[22],[9],[2], and policy/SBOM/integrity frameworks [13],[21],[3],[27],[6],[7] have matured. **What is missing** is the unification of popularity and structural centrality into a single **operational "criticality" measure** in the download-based core, and the reflection of this measure as **ordered priority lists** to detection and policy pipelines. We define the **Composite Criticality Score**, which fuses topological measures + usage intensity + maintenance/freshness signals, using the directed graph built with official resolution rules on the top 1000 npm dependencies selected by last 12 months' downloads; and we **calibrate** the score with targeted/random node removal experiments (reachability, LCC, average path, functional coverage losses). Thus, **prioritized scanning queues** for detection systems, **target package lists** for maintenance and security policies, and **risk-based intervention plans** for ecosystem governance can be produced.

---

## Annotated Bibliography

## 1. A New Frontier for Software Security: Diving Deep Into npm

- **Authors:** Wyss, Elizabeth
- **Year:** 2025
- **Type:** Dissertations & Theses
- **Keywords:** Open-source , Open-source package repository , Package ecosystem , Software supply chain , Security impacts
- **URL:** https://www.proquest.com/dissertations-theses/new-frontier-software-security-diving-deep-into/docview/3246016591/se-2?accountid=25087
- **Database:** ProQuest Dissertations & Theses Global

**Abstract:**
Open-source package managers (e.g., npm for Node.js) have become an established component of modern software development. Rather than creating applications from scratch, developers may employ modular software dependencies and frameworks–called packages –to serve as building blocks for writing larger applications. Package managers make this process easy. With a simple command line directive, developers are able to quickly fetch and install packages across vast open-source repositories. npm–the largest of such repositories–alone hosts millions of unique packages and serves billions of package downloads each week. However, the widespread code sharing resulting from open-source package managers also presents novel security implications. Vulnerable or malicious code hiding deep within package dependency trees can be leveraged downstream to attack both software developers and the end-users of their applications. This downstream flow of software dependencies–dubbed the software supply chain –is critical to secure. This research provides a deep dive into the npm-centric software supply chain, exploring distinctive phenomena that impact its overall security and usability. Such factors include (i) hidden code clones–which may stealthily propagate known vulnerabilities, (ii) install-time attacks enabled by unmediated installation scripts, (iii) hard-coded URLs residing in package code, (iv) the impacts of open-source development practices, (v) package compromise via malicious updates, (vi) spammers disseminating phishing links within package metadata, and (vii) abuse of cryptocurrency protocols designed to reward the creators of high-impact packages. For each facet, tooling is presented to identify and/or mitigate potential security impacts. Ultimately, it is our hope that this research fosters greater awareness, deeper understanding, and further efforts to forge a new frontier for the security of modern software supply chains.


---


## 2. A Preliminary Study on Self-Contained Libraries in the NPM Ecosystem

- **Authors:** Pongchai Jaisri; Reid, Brittany; Kula, Raula Gaikovina
- **Year:** 2024
- **Type:** Working Papers
- **Keywords:** Software Engineering
- **URL:** https://www.proquest.com/working-papers/preliminary-study-on-self-contained-libraries-npm/docview/3069347774/se-2?accountid=25087
- **Database:** Publicly Available Content Database

**Abstract:**
The widespread of libraries within modern software ecosystems creates complex networks of dependencies. These dependencies are fragile to breakage, outdated, or redundancy, potentially leading to cascading issues in dependent libraries. One mitigation strategy involves reducing dependencies; libraries with zero dependencies become to self-contained. This paper explores the characteristics of self-contained libraries within the NPM ecosystem. Analyzing a dataset of 2763 NPM libraries, we found that 39.49\% are self-contained. Of these self-contained libraries, 40.42\% previously had dependencies that were later removed. This analysis revealed a significant trend of dependency reduction within the NPM ecosystem. The most frequently removed dependency was babel-runtime. Our investigation indicates that the primary reasons for dependency removal are concerns about the performance and the size of the dependency. Our findings illuminate the nature of self-contained libraries and their origins, offering valuable insights to guide software development practices.


---

## 4. Backstabber's Knife Collection: A Review of Open Source Software Supply Chain Attacks

- **Authors:** Ohm, Marc; Plate, Henrik; Arnold Sykosch; Meier, Michael
- **Year:** 2020
- **Type:** Working Papers
- **Keywords:** Cryptography and Security , Software Engineering
- **URL:** https://www.proquest.com/working-papers/backstabbers-knife-collection-review-open-source/docview/2405057286/se-2?accountid=25087
- **Database:** Publicly Available Content Database

**Abstract:**
A software supply chain attack is characterized by the injection of malicious code into a software package in order to compromise dependent systems further down the chain. Recent years saw a number of supply chain attacks that leverage the increasing use of open source during software development, which is facilitated by dependency managers that automatically resolve, download and install hundreds of open source packages throughout the software life cycle. This paper presents a dataset of 174 malicious software packages that were used in real-world attacks on open source software supply chains, and which were distributed via the popular package repositories npm, PyPI, and RubyGems. Those packages, dating from November 2015 to November 2019, were manually collected and analyzed. The paper also presents two general attack trees to provide a structured overview about techniques to inject malicious code into the dependency tree of downstream users, and to execute such code at different times and under different conditions. This work is meant to facilitate the future development of preventive and detective safeguards by open source and research communities.


---

## 5. Characterizing Dependency Update Practice of NPM, PyPI and Cargo Packages

- **Authors:** Rahman, Imranur; Zahan, Nusrat; Magill, Stephen; Enck, William; Williams, Laurie
- **Year:** 2024
- **Type:** Working Papers
- **Keywords:** Software Engineering , Cryptography and Security
- **URL:** https://www.proquest.com/working-papers/characterizing-dependency-update-practice-npm/docview/3000390682/se-2?accountid=25087
- **Database:** Publicly Available Content Database

**Abstract:**
Keeping dependencies up-to-date prevents software supply chain attacks through outdated and vulnerable dependencies. Developers may use packages' dependency update practice as one of the selection criteria for choosing a package as a dependency. However, the lack of metrics characterizing packages' dependency update practice makes this assessment difficult. To measure the up-to-date characteristics of packages, we focus on the dependency management aspect and propose two update metrics: Time-Out-Of-Date (TOOD) and Post-Fix-Exposure-Time (PFET), to measure the updatedness of dependencies and updatedness of vulnerable dependencies, respectively. We design an algorithm to stabilize the dependency relationships in different time intervals and compute the proposed metrics for each package. Using our proposed metrics, we conduct a large-scale empirical study of update metrics with 2.9M packages, 66.8M package versions, and 26.8M unique package-dependency relations in NPM, PyPI, and Cargo, ranging from the year 2004 to 2023. We analyze the characteristics of the proposed metrics for capturing packages' dependency update practice in the three ecosystems. Given that the TOOD metric generates a greater volume of data than the PFET metric, we further explore the numerical relationship between these metrics to assess their potential as substitutes for vulnerability counts metrics. We find that PyPI packages update dependencies faster than NPM and Cargo. Conversely, Cargo packages update their vulnerable dependencies faster than NPM and PyPI. We also find that the general purpose update metric, TOOD, can be a proxy for the security-focused update metric, PFET.


---

## 6. Combating Source Poisoning and Next-Generation Software Supply Chain Attacks Using Education, Tools, and Techniques

- **Authors:** Hastings, Thomas G.
- **Year:** 2024
- **Type:** Dissertations & Theses
- **Keywords:** Software projects , Supply chain attacks , Web browser , Package managers
- **URL:** https://www.proquest.com/dissertations-theses/combating-source-poisoning-next-generation/docview/3042954782/se-2?accountid=25087
- **Database:** ProQuest Dissertations & Theses Global

**Abstract:**
We are heading for a perfect storm, making open-source software poisoning and next-generation supply chain attacks easier to execute, which could have significant implications for organizations. The widespread adoption of open source, the ease of today’s package managers, and the best practice of implementing continuous delivery for software projects provide an unprecedented opportunity for attack. It used to be patch on a Friday to prevent a breach on Monday. Now, it is patch on Friday and a breach on Monday. Open-source projects are being targeted at an alarming rate by malicious maintainers and actors. These exploits flow to downstream projects that ingest the compromised patch, and those projects are potentially running the malicious code. Software developers must stay aware of such risks, and organizations must equip themselves to understand or monitor the thousands or tens of thousands of dependencies in their software. This thesis develops and evaluates techniques organizations can use to protect their software from next-generation supply chain attacks. The first set of techniques evaluates organizational procedures for a framework for continuously evaluating open-source components throughout the software life-cycle. Our evaluation takes a holistic approach to evaluating open-source components starting at Day 0 with the decision to incorporate a component into a software project through Day 2 operations, which occurs after the software has been deployed to production and is in maintenance. We start with evaluating the known knowns of an open-source component beginning with the component’s community and code base. Then, we move on to the known unknowns and the unknown unknowns and place techniques and procedures in place to mitigate the risks of the unknowns. Defined controls combine the techniques and procedures into a flexible and repeatable framework that any organization leveraging code-reuse and open-source components in their software development can apply. The second set of techniques is foundational to an organization’s workforce, focusing on education for software engineers. The curriculum gives students the background and knowledge they need to protect the organization. First, students learn to identify risks associated with open-source components. Second, students learn how malicious actors target and execute attacks on open-source components. Third, students learn tactics to mitigate the risks of next-generation supply chain attacks using our open-source platform that provides a standardized development environment for each student running on cloud infrastructure, providing an equitable experience. Our curriculum had a 84% efficiency rate when taught to undergraduate and graduate students at the University of Colorado Colorado Springs. Additionally, we developed a cloud-based platform that removes barriers to our curriculum and provides an inclusive platform, giving students access to computing resources independently of their local hardware, which they access through a web browser.


---

## 7. Construction of Software Supply Chain Threat Portrait Based on Chain Perspective

- **Authors:** Wang, Maoyang; Wu, Peng; Luo, Qin
- **Year:** 2023
- **Type:** Scholarly Journals
- **Keywords:** software supply chain , Supply chain , Software industry , Threat model , software supply chain threat model , attack technique matrix , software supply chain portrait
- **URL:** https://www.proquest.com/scholarly-journals/construction-software-supply-chain-threat/docview/2899423524/se-2?accountid=25087
- **Database:** Publicly Available Content Database

**Abstract:**
With the rapid growth of the software industry, the software supply chain (SSC) has become the most intricate system in the complete software life cycle, and the security threat situation is becoming increasingly severe. For the description of the SSC, the relevant research mainly focuses on the perspective of developers, lacking a comprehensive understanding of the SSC. This paper proposes a chain portrait framework of the SSC based on a resource perspective, which comprehensively depicts the threat model and threat surface indicator system of the SSC. The portrait model includes an SSC threat model and an SSC threat indicator matrix. The threat model has 3 levels and 32 dimensions and is based on a generative artificial intelligence model. The threat indicator matrix is constructed using the Attack Net model comprising 14-dimensional attack strategies and 113-dimensional attack techniques. The proposed portrait model’s effectiveness is verified through existing SSC security events, domain experts, and event visualization based on security analysis models.


---

## 8. Demystifying Vulnerability Propagation via Dependency Trees in npm

- **Authors:** Liu, C., Chen, S., et al.
- **Year:** 2022
- **Type:** Konferans (ICSE 2022)
- **Keywords:** Vulnerability propagation, Dependency trees, Knowledge graph, Security

**Abstract:**
Third-party libraries with rich functionalities facilitate the fast development of JavaScript software, leading to the explosive growth of the NPM ecosystem. However, it also brings new security threats that vulnerabilities could be introduced through dependencies from third-party libraries. In particular, the threats could be excessively amplified by transitive dependencies. Existing research only considers direct dependencies or reasoning transitive dependencies based on reachability analysis, which neglects the NPM-specific dependency resolution rules as adapted during real installation, resulting in wrongly resolved dependencies. Consequently, further fine-grained analysis, such as precise vulnerability propagation and their evolution over time in dependencies, cannot be carried out precisely at a large scale, as well as deriving ecosystem-wide solutions for vulnerabilities in dependencies.

To fill this gap, we propose a knowledge graph-based dependency resolution, which resolves the inner dependency relations of dependencies as trees (i.e., dependency trees), and investigates the security threats from vulnerabilities in dependency trees at a large scale. Specifically, we first construct a complete dependency–vulnerability knowledge graph (DVGraph) that captures the whole NPM ecosystem (over 10 million library versions and 60 million well-resolved dependency relations). Based on it, we propose a novel algorithm (DTResolver) to statically and precisely resolve dependency trees, as well as transitive vulnerability propagation paths, for each package by taking the official dependency resolution rules into account. Based on that, we carry out an ecosystem-wide empirical study on vulnerability propagation and its evolution in dependency trees. Our study unveils lots of useful findings, and we further discuss the lessons learned and solutions for different stakeholders to mitigate the vulnerability impact in NPM based on our findings. For example, we implement a dependency tree–based vulnerability remediation method (DTReme) for NPM packages, and receive much better performance than the official tool (npm audit fix).


---

## 9. Dependency Analysis for Software Licensing and Security

* **Authors / Yazarlar:** Ahlstrom, Hannah Elizabeth
* **Year / Yıl:** 2025
* **Type / Tür:** Dissertations & Theses (Doctoral)
* **Keywords / Anahtar Kelimeler:** License compliance, Security, Dependency pruning, Maven/Gradle
* **URL / Bağlantı:** [https://www.proquest.com/dissertations-theses/dependency-analysis-software-licensing-security/docview/3199246675/se-2](https://www.proquest.com/dissertations-theses/dependency-analysis-software-licensing-security/docview/3199246675/se-2)
* **Database / Veritabanı:** ProQuest Dissertations & Theses Global

**Abstract:**
This dissertation investigates how non-distributed and test-scoped dependencies inflate legal and security risk. Using full dependency tree analysis across 514 OSS projects (Maven/Gradle), it proposes pruning unused, non-invoked, and test-only dependencies. The approach reduces license conflicts by **86–94%** and known vulnerabilities by **57–91%**, while substantially lowering the dependency count. The work demonstrates that risk exposure is often driven by artifacts not present in production deliverables and provides actionable guidance for dependency governance.


---

## 10. Dependency Practices for Vulnerability Mitigation

* **Authors / Yazarlar:** Abbas Javan Jafari; Costa, D. E.; Abdellatif, A.; Shihab, E.
* **Year / Yıl:** 2023
* **Type / Tür:** Working Paper (arXiv preprint)
* **Keywords / Anahtar Kelimeler:** npm, Vulnerability response, Prediction model, Propagation
* **URL / Bağlantı:** [http://arxiv.org/abs/2310.07847](http://arxiv.org/abs/2310.07847)
* **Database / Veritabanı:** arXiv

**Abstract:**
The paper introduces two update metrics—**TOOD** (Time-Out-Of-Date) and **PFET** (Post-Fix-Exposure-Time)—to quantify how promptly packages update dependencies and adopt security fixes. Leveraging an algorithm that stabilizes dependency relations over time, the authors analyze more than **2.9M packages**, **66.8M versions**, and **26.8M** dependency edges across npm, PyPI, and Cargo. Results show PyPI updates general dependencies fastest, while Cargo adopts security fixes fastest. TOOO (general freshness) correlates with PFET (security freshness), indicating TOOD can proxy PFET in some settings. A predictive model and survey insights identify traits of fast adopters and packages that curb vulnerability propagation.


---

## 11. Detection of Software Supply Chain Attacks in Code Repositories

- **Authors:** Correia, Miguel Luís Pereira
- **Year:** 2022
- **Type:** Dissertations & Theses
- **URL:** https://www.proquest.com/dissertations-theses/detection-software-supply-chain-attacks-code/docview/3110429026/se-2?accountid=25087
- **Database:** ProQuest Dissertations & Theses Global

**Abstract:**
Nowadays, the supply chain concept is something intrinsically deep-rooted in the software development life cycle; from the source code and dependencies that are inserted into the software, to its release. With the growing need to shift security left in the development, every step, and material that influences software needs to be secured. However, not all phases within the software supply chain are protected, and malicious actors exploit this lack of security to insert malicious code in the software code repositories. Through account takeovers, attackers can introduce themselves in the code repositories, and with meticulous planning create trojanized software. The 2019 SolarWinds attack is a perfect example that shows the extent that supply chain attacks can have. This dissertation is presented how malicious actions in the repositories can be classified as anomalies within the developers’ behaviours. From the users’ actions in the repositories, metrics are calculated and utilized to create behaviour profiles that are then used to detect anomalous behaviours.


---

## 12. Empirical Study on Dependency-Based Attacks in Node.js

- **Authors:** Kang Yip, Danny Yi
- **Year:** 2022
- **Type:** Dissertations & Theses
- **Keywords:** Dependency , Discord , Malicious module , Node.js , Prototype Pollution , Vulnerabilities
- **URL:** https://www.proquest.com/dissertations-theses/empirical-study-on-exploitation-dependency-based/docview/2674421314/se-2?accountid=25087
- **Database:** ProQuest Dissertations & Theses Global

**Abstract:**
Node.js is a server-side platform built on Google Chrome's JavaScript. Node.js developers share packages through the Node Package Manager (NPM) repository as open-source Node.js packages. Developers use packages published in the NPM repository as dependencies to their software with the understanding that the dependencies provide services to their software. By construction, Node.js allows dependencies to inspect the calling package and even overwrite its behavior, which we call dependency-based attacks. This thesis describes cases of dependency-based attacks and reports about our study to assess their frequency. First, we selected and analyzed two highly rated Node.js dependency-based malicious packages: a prototype pollution package and Discord.dll. Then, we identified the recent dependencies attacks from the reported Node.js attacks and associated vulnerabilities published in the Synk Vulnerability Database and NPM Security advisories and analyzed their behavior. Out of the 726 studied vulnerabilities, we found 111 prototype pollution packages (including code that changes the way JavaScript's root Object behaves) and 11 malicious modules that exploit the dependency-based weaknesses, 16.8\% of the packages. We conclude that dependency attacks on calling modules have become common and need attention given their high impact.


---

## 13. In-toto: Practical Software Supply Chain Security

- **Authors:** Torres-Arias, Santiago
- **Year:** 2020
- **Type:** Dissertations & Theses
- **Keywords:** Continuous delivery , Cryptography , Security , Software supply chain
- **URL:** https://www.proquest.com/dissertations-theses/toto-practical-software-supply-chain-security/docview/2427238266/se-2?accountid=25087
- **Database:** ProQuest Dissertations & Theses Global, Publicly Available Content Database

**Abstract:**
The software development process, or software supply chain, is quite complex and involves a number of independent actors throughout various organizations and jurisdictions. In most modern supply chains, developers check source code into version control systems, which is in turn compiled into binaries at a build farm, and multiple tests such as dynamic and static analysis, licensing and compliance, security audits, vulnerability scanning among a myriad of other operations are performed. Once all the required actions are carried out, the software is packaged and published for distribution into a delivered product to be consumed by end users. Unfortunately, software supply chain compromises are common and impactful. An attacker that is able to compromise any single step in the process can maliciously modify the software and harm any of this software’s users. According to the Symantec Internet Threat Security Report (ISTR), Software Supply Chain compromise is the fastest growing threat to internet users—which rose 438% from 2017 to 2019. High and low profile companies are affected alike, and the affected includes companies like Docker, NBC news, Microsoft, and RedHat. Protecting against attacks on the software supply chain presents a complicated challenge because, as mentioned above, the ecosystems in which software are made are incredibly varied and a compromise of a simple node in the pipeline often produces a complete subversion of the deliveredproduct. To tackle this challenge, we took a two-pronged approach: to secure every single operation within this chain (i.e., to build strong links) and build an expressive framework to cryptographically tie ever single step together (i.e., to build a chain out of these links). To do the former, we identified fundamental principles for trustworthy artifact transfer and ensured popular software can provide these principles by fixing vulnerabilities in them. For the latter, we designed in-toto, a framework that cryptographically ensures the integrity of the software supply chain. To do this, in-toto grants the end user the ability to verify the software supply chain from the project’s inception to its deployment and enforce compliance of the security policies of each individual step. This work drives the arc between identifying software supply chain compromises all the way to creating all the principles to prevent these compromises from taking place. The work on securing individual links has crystallized into increasing the security stance of applications such as git, Pacman and the tor browser. In addition, in-toto has been widely used by the time of this publication, as thousands of companies and various open source projects are using in-toto to secure their deployments used by millions of users.


---

## 14. Malicious Package Detection in NPM and PyPI using a Single Model of Malicious Behavior Sequence

- **Authors:** Zhang, Junan; Huang, Kaifeng; Chen, Bihuan; Wang, Chong; Tian, Zhenhao; Peng, Xin
- **Year:** 2023
- **Type:** Working Papers
- **Keywords:** Cryptography and Security , Software Engineering
- **URL:** https://www.proquest.com/working-papers/malicious-package-detection-npm-pypi-using-single/docview/2861990120/se-2?accountid=25087
- **Database:** Publicly Available Content Database

**Abstract:**
Open-source software (OSS) supply chain enlarges the attack surface, which makes package registries attractive targets for attacks. Recently, package registries NPM and PyPI have been flooded with malicious packages. The effectiveness of existing malicious NPM and PyPI package detection approaches is hindered by two challenges. The first challenge is how to leverage the knowledge of malicious packages from different ecosystems in a unified way such that multi-lingual malicious package detection can be feasible. The second challenge is how to model malicious behavior in a sequential way such that maliciousness can be precisely captured. To address the two challenges, we propose and implement Cerebro to detect malicious packages in NPM and PyPI. We curate a feature set based on a high-level abstraction of malicious behavior to enable multi-lingual knowledge fusing. We organize extracted features into a behavior sequence to model sequential malicious behavior. We fine-tune the BERT model to understand the semantics of malicious behavior. Extensive evaluation has demonstrated the effectiveness of Cerebro over the state-of-the-art as well as the practically acceptable efficiency. Cerebro has successfully detected 306 and 196 new malicious packages in PyPI and NPM, and received 385 thank letters from the official PyPI and NPM teams.


---

## 15. Malicious Package Detection using Metadata Information

- **Authors:** Halder, S; Bewong, M; Mahboubi, A; Jiang, Y; Islam, R; Islam, Z; R Ip; Ahmed, E; Ramachandran, G; Babar, A
- **Year:** 2024
- **Type:** Working Papers
- **Keywords:** Cryptography and Security
- **URL:** https://www.proquest.com/working-papers/malicious-package-detection-using-metadata/docview/2925761843/se-2?accountid=25087
- **Database:** Publicly Available Content Database

**Abstract:**
Protecting software supply chains from malicious packages is paramount in the evolving landscape of software development. Attacks on the software supply chain involve attackers injecting harmful software into commonly used packages or libraries in a software repository. For instance, JavaScript uses Node Package Manager (NPM), and Python uses Python Package Index (PyPi) as their respective package repositories. In the past, NPM has had vulnerabilities such as the event-stream incident, where a malicious package was introduced into a popular NPM package, potentially impacting a wide range of projects. As the integration of third-party packages becomes increasingly ubiquitous in modern software development, accelerating the creation and deployment of applications, the need for a robust detection mechanism has become critical. On the other hand, due to the sheer volume of new packages being released daily, the task of identifying malicious packages presents a significant challenge. To address this issue, in this paper, we introduce a metadata-based malicious package detection model, MeMPtec. This model extracts a set of features from package metadata information. These extracted features are classified as either easy-to-manipulate (ETM) or difficult-to-manipulate (DTM) features based on monotonicity and restricted control properties. By utilising these metadata features, not only do we improve the effectiveness of detecting malicious packages, but also we demonstrate its resistance to adversarial attacks in comparison with existing state-of-the-art. Our experiments indicate a significant reduction in both false positives (up to 97.56%) and false negatives (up to 91.86%).


---

## 16. Node package manager's dependency network robustness

- **Authors:** Hafner, Andrej; Mur, Anže; Jaka Bernard
- **Year:** 2021
- **Type:** Working Papers
- **Keywords:** Social and Information Networks
- **URL:** https://www.proquest.com/working-papers/node-package-managers-dependency-network/docview/2585639033/se-2?accountid=25087
- **Database:** Publicly Available Content Database

**Abstract:**
The robustness of npm dependency network is a crucial property, since many projects and web applications heavily rely on the functionalities of packages, especially popular ones that have many dependant packages. In the past, there have been instances where the removal or update of certain npm packages has caused widespread chaos and web-page downtime on the internet. Our goal is to track the network's resilience to such occurrences through time and figure out whether the state of the network is trending towards a more robust structure. We show that the network is not robust to targeted attacks, since a security risk in a few crucial nodes affects a large part of the network. Because such packages are often backed up by serious communities with high standards, the issue is not alarming and is a consequence of power law distribution of the network. The current trend in average number of dependencies and effect of important nodes on the rest of the network is decreasing, which further improves the resilience and sets a positive path in development. Furthermore, we show that communities form around the most important packages, although they do not conform well to the common community definition using modularity. We also provide guidelines for package development that increases the robustness of the network and reduces the possibility of introducing security risks.


---

## 17. On the Feasibility of Cross-Language Detection of Malicious Packages in npm and PyPI

- **Authors:** Ladisa, Piergiorgio; Ponta, Serena Elisa; Ronzoni, Nicola; Martinez, Matias; Barais, Olivier
- **Year:** 2023
- **Type:** Working Papers
- **Keywords:** Cryptography and Security , Software Engineering
- **URL:** https://www.proquest.com/working-papers/on-feasibility-cross-language-detection-malicious/docview/2878367596/se-2?accountid=25087
- **Database:** Publicly Available Content Database

**Abstract:**
Current software supply chains heavily rely on open-source packages hosted in public repositories. Given the popularity of ecosystems like npm and PyPI, malicious users started to spread malware by publishing open-source packages containing malicious code. Recent works apply machine learning techniques to detect malicious packages in the npm ecosystem. However, the scarcity of samples poses a challenge to the application of machine learning techniques in other ecosystems. Despite the differences between JavaScript and Python, the open-source software supply chain attacks targeting such languages show noticeable similarities (e.g., use of installation scripts, obfuscated strings, URLs). In this paper, we present a novel approach that involves a set of language-independent features and the training of models capable of detecting malicious packages in npm and PyPI by capturing their commonalities. This methodology allows us to train models on a diverse dataset encompassing multiple languages, thereby overcoming the challenge of limited sample availability. We evaluate the models both in a controlled experiment (where labels of data are known) and in the wild by scanning newly uploaded packages for both npm and PyPI for 10 days. We find that our approach successfully detects malicious packages for both npm and PyPI. Over an analysis of 31,292 packages, we reported 58 previously unknown malicious packages (38 for npm and 20 for PyPI), which were consequently removed from the respective repositories.


---

## 18. On the Impact of Security Vulnerabilities in the npm and RubyGems Dependency Networks

- **Authors:** Zerouali, Ahmed; Mens, Tom; Decan, Alexandre; Coen De Roover
- **Year:** 2022
- **Type:** Working Papers
- **Keywords:** Software Engineering
- **URL:** https://www.proquest.com/working-papers/on-impact-security-vulnerabilities-npm-rubygems/docview/2541122103/se-2?accountid=25087
- **Database:** Publicly Available Content Database

**Abstract:**
The increasing interest in open source software has led to the emergence of large language-specific package distributions of reusable software libraries, such as npm and RubyGems. These software packages can be subject to vulnerabilities that may expose dependent packages through explicitly declared dependencies. Using Snyk's vulnerability database, this article empirically studies vulnerabilities affecting npm and RubyGems packages. We analyse how and when these vulnerabilities are disclosed and fixed, and how their prevalence changes over time. We also analyse how vulnerable packages expose their direct and indirect dependents to vulnerabilities. We distinguish between two types of dependents: packages distributed via the package manager, and external GitHub projects depending on npm packages. We observe that the number of vulnerabilities in npm is increasing and being disclosed faster than vulnerabilities in RubyGems. For both package distributions, the time required to disclose vulnerabilities is increasing over time. Vulnerabilities in npm packages affect a median of 30 package releases, while this is 59 releases in RubyGems packages. A large proportion of external GitHub projects is exposed to vulnerabilities coming from direct or indirect dependencies. 33% and 40% of dependency vulnerabilities to which projects and packages are exposed, respectively, have their fixes in more recent releases within the same major release range of the used dependency. Our findings reveal that more effort is needed to better secure open source package distributions.


---

## 19. Practical Automated Detection of Malicious npm Packages (Amalfi)

- **Authors:** Sejfia, Adriana; Schäfer, Max
- **Year:** 2022
- **Type:** Working Papers
- **Keywords:** Cryptography and Security , Software Engineering
- **URL:** https://www.proquest.com/working-papers/practical-automated-detection-malicious-npm/docview/2634669530/se-2?accountid=25087
- **Database:** Publicly Available Content Database

**Abstract:**
The npm registry is one of the pillars of the JavaScript and TypeScript ecosystems, hosting over 1.7 million packages ranging from simple utility libraries to complex frameworks and entire applications. Due to the overwhelming popularity of npm, it has become a prime target for malicious actors, who publish new packages or compromise existing packages to introduce malware that tampers with or exfiltrates sensitive data from users who install either these packages or any package that (transitively) depends on them. Defending against such attacks is essential to maintaining the integrity of the software supply chain, but the sheer volume of package updates makes comprehensive manual review infeasible. We present Amalfi, a machine-learning based approach for automatically detecting potentially malicious packages comprised of three complementary techniques. We start with classifiers trained on known examples of malicious and benign packages. If a package is flagged as malicious by a classifier, we then check whether it includes metadata about its source repository, and if so whether the package can be reproduced from its source code. Packages that are reproducible from source are not usually malicious, so this step allows us to weed out false positives. Finally, we also employ a simple textual clone-detection technique to identify copies of malicious packages that may have been missed by the classifiers, reducing the number of false negatives. Amalfi improves on the state of the art in that it is lightweight, requiring only a few seconds per package to extract features and run the classifiers, and gives good results in practice: running it on 96287 package versions published over the course of one week, we were able to identify 95 previously unknown malware samples, with a manageable number of false positives.


---

## 20. Small World with High Risks: Security Threats in npm

- **Authors:** Zimmermann, Markus; Cristian-Alexandru Staicu; Tenny, Cam; Pradel, Michael
- **Year:** 2019
- **Type:** Working Papers
- **Keywords:** Cryptography and Security
- **URL:** https://www.proquest.com/working-papers/small-world-with-high-risks-study-security/docview/2185999630/se-2?accountid=25087
- **Database:** Publicly Available Content Database

**Abstract:**
The popularity of JavaScript has lead to a large ecosystem of third-party packages available via the npm software package registry. The open nature of npm has boosted its growth, providing over 800,000 free and reusable software packages. Unfortunately, this open nature also causes security risks, as evidenced by recent incidents of single packages that broke or attacked software running on millions of computers. This paper studies security risks for users of npm by systematically analyzing dependencies between packages, the maintainers responsible for these packages, and publicly reported security issues. Studying the potential for running vulnerable or malicious code due to third-party dependencies, we find that individual packages could impact large parts of the entire ecosystem. Moreover, a very small number of maintainer accounts could be used to inject malicious code into the majority of all packages, a problem that has been increasing over time. Studying the potential for accidentally using vulnerable code, we find that lack of maintenance causes many packages to depend on vulnerable code, even years after a vulnerability has become public. Our results provide evidence that npm suffers from single points of failure and that unmaintained packages threaten large code bases. We discuss several mitigation techniques, such as trusted maintainers and total first-party security, and analyze their potential effectiveness.


---

## 21. Software Supply Chain Security: Attacks, Defenses, and Signing Adoption

- **Authors:** Schorlemmer, Taylor R.
- **Year:** 2024
- **Type:** Dissertations & Theses
- **URL:** https://www.proquest.com/dissertations-theses/software-supply-chain-security-attacks-defenses/docview/3122639657/se-2?accountid=25087
- **Database:** ProQuest Dissertations & Theses Global

**Abstract:**
Modern software relies heavily on third-party dependencies (often distributed via public package registries), making software supply chain attacks a growing threat. Prior work investigated attacks and defenses, but only taxonomized attacks or proposed defensive techniques, did not consistently define software supply chain attacks, and did not provide properties to assess the security of software supply chains. We do not have a unified definition of software supply chain attacks nor a set of properties that a secure software supply chain should follow. Guaranteeing authorship in a software supply chain is also a challenge. Package maintainers can guarantee package authorship through software signing. However, it is unclear how common this practice is or if existing signatures are created properly. Prior work provided raw data on registry signing practices, but only measured single platforms, did not consider quality, did not consider time, and did not assess factors that may influence signing. We do not have up-to-date measurements of signing practices nor do we know the quality of existing signatures. Furthermore, we lack a comprehensive understanding of factors that influence signing adoption. This thesis addresses these gaps. First, we systematize existing knowledge into: (1) a four-stage supply chain attack pattern; and (2) a set of properties for secure supply chains (transparency, validity, and separation). Next, we measure current signing quantity and quality across three kinds of package registries: traditional software (Maven Central, PyPI), container images (Docker Hub), and machine learning models (Hugging Face). Then, we examine longitudinal trends in signing practices. Finally, we use a quasi-experiment to estimate the effect that various factors had on software signing practices. To summarize the findings of our quasi-experiment: (1) mandating signature adoption improves the quantity of signatures; (2) providing dedicated tooling improves the quality of signing; (3) getting started is the hard part — once a maintainer begins to sign, they tend to continue doing so; and (4) although many supply chain attacks are mitigable via signing, signing adoption is primarily affected by registry policy rather than by public knowledge of attacks, new engineering standards, etc. These findings highlight the importance of software package registry managers and signing infrastructure.


---

## 22. Studying Dependency Maintenance Practices through Mining NPM

- **Authors:** Cogo, Filipe Roseiro
- **Year:** 2020
- **Type:** Dissertations & Theses
- **Keywords:** Open source software
- **URL:** https://www.proquest.com/dissertations-theses/studying-dependency-maintenance-practices-through/docview/2524882679/se-2?accountid=25087
- **Database:** ProQuest Dissertations & Theses Global

**Abstract:**
Open source software ecosystems have gained significant importance in the last decade. In a software ecosystem, client packages can enable a dependency to reuse the functionalities of a provider package. On the one hand, the diversity of freely reusable provider packages in those ecosystems supports a fast-paced contemporary software development. On the other hand, developers need to cope with the overhead brought by dependency maintenance. Dependencies need to be kept in an updated and working state, otherwise defects from provider packages can negatively impact client packages. Notable incidents denote the importance of timely and proper dependency maintenance. For example, in the "Equifax data breach", a vulnerability coming from an out-of-date dependency was explored to illegally obtain hundreds of millions of financial customers information. Also, the "left-pad incident", in which a package with 11-lines of code was removed from npm, caused a significant downtime on major websites such as Facebook, Instagram and LinkedIn. Hence, proper dependency maintenance contributes to the viability of both individual packages and the whole ecosystem. In this thesis, we propose to leverage data from the npm ecosystem to understand the current dependency maintenance practices and provide actionable information to practitioners. Currently, npm is the largest and most popular open-source software ecosystem. We study three phenomena related to the dependency maintenance in software ecosystems: downgrade of dependencies, same-day releases, and releases deprecation. In this thesis, we discuss in detail the motivation and approach to study these three phenomena. We then perform an empirical analysis of the npm data to evaluate the driving forces behind these phenomena, as well as their prevalence and impact in the ecosystem. Based on our empirical observations, we propose a set of informed suggestions to improve dependency maintenance practices in npm.


---

## 23. Supporting Detection via Unsupervised Signature Generation (ACME)

- **Authors:** Ohm, Marc; Kempf, Lukas; Boes, Felix; Meier, Michael
- **Year:** 2021
- **Type:** Working Papers
- **Keywords:** Cryptography and Security
- **URL:** https://www.proquest.com/working-papers/supporting-detection-software-supply-chain/docview/2457813215/se-2?accountid=25087
- **Database:** Publicly Available Content Database

**Abstract:**
Trojanized software packages used in software supply chain attacks constitute an emerging threat. Unfortunately, there is still a lack of scalable approaches that allow automated and timely detection of malicious software packages and thus most detections are based on manual labor and expertise. However, it has been observed that most attack campaigns comprise multiple packages that share the same or similar malicious code. We leverage that fact to automatically reproduce manually identified clusters of known malicious packages that have been used in real world attacks, thus, reducing the need for expert knowledge and manual inspection. Our approach, AST Clustering using MCL to mimic Expertise (ACME), yields promising results with a \(F_{1}\) score of 0.99. Signatures are automatically generated based on characteristic code fragments from clusters and are subsequently used to scan the whole npm registry for unreported malicious packages. We are able to identify and report six malicious packages that have been removed from npm consequentially. Therefore, our approach can support analysts by reducing manual labor and hence may be employed to timely detect possible software supply chain attacks.


---

## 24. The Hitchhiker's Guide to Malicious Third-Party Dependencies

- **Authors:** Ladisa, Piergiorgio; Sahin, Merve; Ponta, Serena Elisa; Rosa, Marco; Martinez, Matias; Barais, Olivier
- **Year:** 2023
- **Type:** Working Papers
- **Keywords:** Cryptography and Security
- **URL:** https://www.proquest.com/working-papers/hitchhikers-guide-malicious-third-party/docview/2839581173/se-2?accountid=25087
- **Database:** Publicly Available Content Database

**Abstract:**
The increasing popularity of certain programming languages has spurred the creation of ecosystem-specific package repositories and package managers. Such repositories (e.g., NPM, PyPI) serve as public databases that users can query to retrieve packages for various functionalities, whereas package managers automatically handle dependency resolution and package installation on the client side. These mechanisms enhance software modularization and accelerate implementation. However, they have become a target for malicious actors seeking to propagate malware on a large scale. In this work, we show how attackers can leverage capabilities of popular package managers and languages to achieve arbitrary code execution on victim machines, thereby realizing open-source software supply chain attacks. Based on the analysis of 7 ecosystems, we identify 3 install-time and 5 runtime techniques, and we provide recommendations describing how to reduce the risk when consuming third-party dependencies. We will provide proof-of-concepts that demonstrate the identified techniques. Furthermore, we describe evasion strategies employed by attackers to circumvent detection mechanisms.


---

## 25. The Web of Dependencies: A Complex Network Analysis of the NPM

- **Authors:** Emilie-Rose Oldnall
- **Year:** 2017
- **Type:** Tez (Yüksek Lisans Tezi)

**Abstract:**
Open-source software development is a collaborative effort resulting in complex dependencies between software packages. Unlike proprietary software, the open-source model offers a unique opportunity to analyse and trace these dependencies due to its public availability. This thesis maps out the complex dependency network within the npm ecosystem, the package manager for JavaScript. JavaScript is the world’s most widely used programming language, and its package manager is a tool responsible for storing and distributing thousands of third-party software packages to the developer community. Yet, with greater interconnectivity comes greater vulnerability, a reality sharply highlighted in 2016 when removing the small utility left-pad package from the npm registry. This event precipitated widespread software breakage as many web applications transitively and unknowingly depended on it for functionality. This thesis uses complex network science to demonstrate how network measures can be used to determine the structure and level of complexity of the npm network and, more interestingly, how these parameters evolve over time. I analyse the npm network over five years, from 2012 to 2016. To the author’s knowledge, no study at the time of writing has analysed the npm package ecosystem at a version level from the perspective of complex network science. This thesis finds that the npm network exhibits small-world behaviour and a scale-free architecture, concurring with existing studies on open-source software systems. It underscores the pivotal role of hierarchical software design in moulding npm’s network topology and identifies versioned packages that disproportionately influence the network’s functionality. Notably, it reveals that central nodes can have up to 200,000 reverse transitive dependencies, highlighting the ecosystem’s vulnerability to cascading failures. By providing a detailed exploration of npm’s complex dependency network, this research deepens our understanding of npm’s infrastructure and highlights the critical network dynamics at play in open-source software development. These insights pave the way for further research on mitigating potential vulnerabilities and improving the resilience of software dependency networks


---

## 26. Toward Secure Use of Open Source Dependencies

- **Authors:** Imtiaz, Nasif
- **Year:** 2023
- **Type:** Dissertations & Theses
- **URL:** https://www.proquest.com/dissertations-theses/toward-secure-use-open-source-dependencies/docview/2890690575/se-2?accountid=25087
- **Database:** ProQuest Dissertations & Theses Global

**Abstract:**
Modern software extensively uses open source packages as upstream dependencies . While using the open source may be free, the downstream client projects must ensure their dependencies are secure. The goal of this dissertation is to aid software engineers in securely using open source dependencies. Managing open source security can be broadly characterized into two fronts: (a) reactive: when a vulnerability is discovered in a dependency, the clients should react to any potential threat; and (b) proactive : before pulling in new dependency code, the clients should make an informed decision about the security of the code. We work on both reactive and proactive open source security in this dissertation. On the reactive front, we performed a comparative study of nine existing software composition analysis (SCA) tools that notify a client of dependency vulnerabilities. We find that the tools vary in their vulnerability reporting. The count of reported vulnerable dependencies ranges from 17 to 332 for Maven and 32 to 239 for npm projects across the studied tools. Similarly, the count of unique known vulnerabilities reported by the tools ranges from 36 to 313 for Maven and 45 to 234 for npm projects. Our manual analysis of the tools’ results suggests that the accuracy of the vulnerability database is a key differentiator for SCA tools. Next, we empirically investigated 4,812 security releases from packages across seven ecosystems. Specifically, we studied (1) the time lag between fix and release; (2) how security fixes are documented in the release notes; (3) code change characteristics (size and semantic versioning) of the release; and (4) the time lag between the release and an advisory publication. We find a time lag between security fixes within open source packages and corresponding advisory publications, resulting in delayed notifications from SCA tools. The notification delay may occur even though we find the packages to typically document the security fixes in their release notes (61.5% of the time). Based on our findings, we recommend open source packages follow a standardized practice in announcing security fixes that can help automate the notification process to client projects. On the proactive front, we work on building trust in dependency updates by identifying the authors and reviewers behind the changes within these updates. We implemented Depdive, an update audit tool for packages in Crates.io, npm, PyPI, and RubyGems registries. Depdive first (i) identifies the files and code changes that cannot be traced back to the package’s source repository, i.e., phantom artifacts, and then (ii) measures what portion of changes in the update has passed through a code review process, i.e., code review coverage. We empirically evaluated Depdive over the most downloaded packages from the four registries. We find that phantom artifacts are not uncommon in the updates (20.1% of the analyzed updates had at least one phantom file). Further, we find only 11.0% of the updates to be fully code-reviewed, showing that even the most used packages introduce non-reviewed code in the software supply chain. Finally, we studied if a social network-based centrality rating for the authors and reviewers of package code can help client project developers review upstream changes.


---

## 27. Towards Ensuring Integrity and Authenticity of Software Repositories

- **Authors:** Vaidya, Sangat
- **Year:** 2022
- **Type:** Dissertations & Theses
- **Keywords:** Code management , Software distribution , Software repositories , Software security , Software supply chain
- **URL:** https://www.proquest.com/dissertations-theses/towards-ensuring-integrity-authenticity-software/docview/3099364373/se-2?accountid=25087
- **Database:** ProQuest Dissertations & Theses Global

**Abstract:**
The software development process comprises of a series of steps known as a software supply chain. These steps include managing the source code, testing, building and packaging it into a final product, and distributing the product to end users. Along this chain, software repositories are used for different purposes such as source code management (Git, SVN, mercurial), software distribution (PyPI, RubyGems, NPM) or for deploying software based on container images (Harbor, DockerHub, Artifact Hub). In the recent past, different types of repositories have increasingly been the target of attacks. As such, there is a need for mechanisms to ensure integrity and authenticity of repository data. This work seeks to design mechanisms for providing end users with integrity and authenticity guarantees for repositories used in the software development process. In the first part of this work, the focus is on version control systems that are used by software developers for software code management and collaboration. Recent history has shown that source code repositories represent appealing attack targets. Attacks that violate the integrity of repository data can impact negatively millions of users. This work designs and implements a commit signing mechanism for centralized version control systems that rely on a client-server architecture. When the proposed commit signing protocol is in place, the integrity and authenticity of the repository can be guaranteed even when the server hosting the repository is not trustworthy. The second part of this work, the focus is on the problem of bootstrapping trust in a piece of software. The work proposes to design and implement a Software Certification Service that receives certification requests from a project owner for a specific project and then issues a project certificate once the project owner successfully completes a procedure for proving ownership of the project. The certificate is then shipped with the software project and the end user uses it to bootstrap the verification of the software supply chain integrity. Here, the focus is on proving ownership of projects that are hosted on community repositories such as PyPI, RubyGems, NPM, or GitHub. The second part of this work proposes an approach for certifying the validity of software projects hosted on community repositories. This work designs and implements a Software Certification Service (SCS) that receives certification requests from a project owner for a specific project and then issues a project certificate once the project owner successfully completes a protocol for proving ownership of the project. The proposed certification protocol is inspired from the highly-successful ACME protocol used by the Let's Encrypt certification authority and can be be fully automated on the SCS side. However, it is fundamentally different in its attack mitigation capabilities and in how ownership is proven. It is also compatible with existing community repositories such as PyPI, RubyGems, NPM, or GitHub, without requiring any changes to these repositories. To support the claim, the work instantiates the proposed certification service with several practical deployments. In the last part of this work, the focus is on artifact repositories that are used for deployment of software. These repositories are used to manage deployment artifacts like container images, Helm charts, policy bundles etc. These artifact management systems currently lack proper version control features. This work defines an approach for uniform version control of deployment artifacts. The approach includes designing an algorithm to compute difference between two versions of an artifact and further propose a version control system to manage these artifacts. Here, in main focus are registries like Harbor and JFrog Artifactory that manage multiple deployment artifacts. In the last part of this work, the focus is on artifact repositories that are used for deployment of software. These repositories are used to manage deployment artifacts such as container images, Helm charts and policy bundles. Current artifact management systems lack proper version control features. This work proposes a uniform version control system for such artifacts. The primary focus here is on artifacts recognized by the Open Container Initiative (OCI) standards. The approach treats artifacts as structured objects with multiple components such as file systems, binary packages, and metadata, instead of treating them as just opaque binary objects. The work further leverages this structure to design a diff algorithm that computes the difference between two versions of artifacts. The approach examines challenges related to computing differences between versions, the persistence of older versions of artifacts, and the security aspects of a version controlling system. Finally, the work proposes commit and update mechanisms for version control that address these challenges. With the proposed commit and update protocols in place, various types of OCI artifacts can be version controlled uniformly, regardless of their types.


---

## 28. Towards Measuring Supply Chain Attacks on Package Managers

- **Authors:** Duan, Ruian; Alrawi, Omar; Ranjita Pai Kasturi; Elder, Ryan; Saltaformaggio, Brendan; Lee, Wenke
- **Year:** 2020
- **Type:** Working Papers
- **Keywords:** Cryptography and Security
- **URL:** https://www.proquest.com/working-papers/towards-measuring-supply-chain-attacks-on-package/docview/2351269484/se-2?accountid=25087
- **Database:** Publicly Available Content Database

**Abstract:**
Package managers have become a vital part of the modern software development process. They allow developers to reuse third-party code, share their own code, minimize their codebase, and simplify the build process. However, recent reports showed that package managers have been abused by attackers to distribute malware, posing significant security risks to developers and end-users. For example, eslint-scope, a package with millions of weekly downloads in Npm, was compromised to steal credentials from developers. To understand the security gaps and the misplaced trust that make recent supply chain attacks possible, we propose a comparative framework to qualitatively assess the functional and security features of package managers for interpreted languages. Based on qualitative assessment, we apply well-known program analysis techniques such as metadata, static, and dynamic analysis to study registry abuse. Our initial efforts found 339 new malicious packages that we reported to the registries for removal. The package manager maintainers confirmed 278 (82%) from the 339 reported packages where three of them had more than 100,000 downloads. For these packages we were issued official CVE numbers to help expedite the removal of these packages from infected victims. We outline the challenges of tailoring program analysis tools to interpreted languages and release our pipeline as a reference point for the community to build on and help in securing the software supply chain.


---

## 29. Towards Robust Detection of OSS Supply Chain Poisoning (OSCAR)

- **Authors:** Zheng, Xinyi; Chen, Wei; Wang, Shenao; Zhao, Yanjie; Gao, Peiming; Zhang, Yuanchao; Wang, Kailong; Wang, Haoyu
- **Year:** 2024
- **Type:** Working Papers
- **Keywords:** Cryptography and Security , Software Engineering
- **URL:** https://www.proquest.com/working-papers/towards-robust-detection-open-source-software/docview/3106232107/se-2?accountid=25087
- **Database:** Publicly Available Content Database

**Abstract:**
The exponential growth of open-source package ecosystems, particularly NPM and PyPI, has led to an alarming increase in software supply chain poisoning attacks. Existing static analysis methods struggle with high false positive rates and are easily thwarted by obfuscation and dynamic code execution techniques. While dynamic analysis approaches offer improvements, they often suffer from capturing non-package behaviors and employing simplistic testing strategies that fail to trigger sophisticated malicious behaviors. To address these challenges, we present OSCAR, a robust dynamic code poisoning detection pipeline for NPM and PyPI ecosystems. OSCAR fully executes packages in a sandbox environment, employs fuzz testing on exported functions and classes, and implements aspect-based behavior monitoring with tailored API hook points. We evaluate OSCAR against six existing tools using a comprehensive benchmark dataset of real-world malicious and benign packages. OSCAR achieves an F1 score of 0.95 in NPM and 0.91 in PyPI, confirming that OSCAR is as effective as the current state-of-the-art technologies. Furthermore, for benign packages exhibiting characteristics typical of malicious packages, OSCAR reduces the false positive rate by an average of 32.06% in NPM (from 34.63% to 2.57%) and 39.87% in PyPI (from 41.10% to 1.23%), compared to other tools, significantly reducing the workload of manual reviews in real-world deployments. In cooperation with Ant Group, a leading financial technology company, we have deployed OSCAR on its NPM and PyPI mirrors since January 2023, identifying 10,404 malicious NPM packages and 1,235 malicious PyPI packages over 18 months. This work not only bridges the gap between academic research and industrial application in code poisoning detection but also provides a robust and practical solution that has been thoroughly tested in a real-world industrial setting.


---

## 30. Unveiling the Invisible: Prototype Pollution Gadgets via Dynamic Taint

* **Authors / Yazarlar:** Shcherbakov, M.; Moosbrugger, P.; Balliu, M.
* **Year / Yıl:** 2021 *(konferans yılına göre güncellenebilir)*
* **Type / Tür:** Conference
* **Keywords / Anahtar Kelimeler:** Prototype pollution, Dynamic taint analysis, JavaScript, Gadgets, Supply chain

**Abstract:**
Prototype pollution (PP) has emerged as a pervasive class of JavaScript vulnerabilities that enables adversaries to tamper with `Object.prototype` and hijack program behavior. This paper presents a dynamic-taint–analysis approach to systematically uncover **PP gadgets**—execution contexts and code paths that make pollution exploitable in real applications and packages. The technique tracks attacker-controlled sources through property creation/propagation, models prototype lookups, and pinpoints sinks that yield privilege escalation, arbitrary write, or code-execution effects. Evaluated across popular npm packages and real-world apps, the approach reveals previously undocumented gadgets, shows how seemingly benign libraries can become exploitable under realistic inputs, and provides guidance for hardening package code and sanitizing merge/clone utilities.


