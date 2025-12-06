# 🐛 Case Study: The Shai-Hulud Incident

> **Context:** This report is a concrete example of the "topological risk" concept proposed in the [NPM Supply Chain Network Analysis](../README.md) project. The Shai-Hulud attack demonstrates how attackers weaponize the network structure.

## 1. Introduction: A Turning Point
The year 2025 has been recorded as a definitive breaking point in the software supply chain security literature. The NPM ecosystem was subjected to the first large-scale "wormable" malware attack, named "Shai-Hulud" in reference to the giant sandworms in Frank Herbert's *Dune* universe. This sequence of events not only affected thousands of projects but also painfully exposed the inadequacy of existing security paradigms—especially traditional scanners focusing on package content.

This report analyzes the two waves of the Shai-Hulud attack (September and November 2025) in technical depth and demonstrates the necessity of the **topological risk model (Composite Risk Score - BRS)** developed against such threats.

## 2. First Wave: The Awakening (Shai-Hulud 1.0)
**Date Range:** September 5 – 23, 2025
**Code Name:** "Chalk & Debug Attack"

The first wave in September was a reconnaissance attack targeting the ecosystem's central nodes. Threat actors compromised 18 critical packages such as `@ctrl/tinycolor`, `chalk`, and `debug`, which exceeded 2.6 billion weekly downloads.

### Attack Vector and Execution
The attack began with phishing-based compromise of critical maintainer accounts, such as Josh Junon, through convincing fake domains like `npmjs.help`.
* **Mechanism:** Malicious code was executed through `postinstall` scripts.
* **Payload:** A *crypto-clipper* running in the browser environment. By hooking `fetch` and `XMLHttpRequest` structures, crypto wallet addresses were instantly replaced with the attacker's addresses using Levenshtein distance algorithm.
* **Impact:** Although financial damage (~$503 USD) remained limited due to early detection, the attack's reach potential proved the ecosystem's fragility.

## 3. Second Wave: Destruction and Propagation (Shai-Hulud 2.0)
**Date Range:** November 21, 2025 – Present (Active)
**Code Name:** "The Second Coming"

The second wave beginning in November transformed from a theft attempt into **an autonomous cyber weapon**. Attackers used much more sophisticated methods to make detection difficult and ensure persistence.

### Technical Innovations and Sophistication
Unlike the previous version, Shai-Hulud 2.0 was equipped with these four key capabilities:

1.  **Preinstall Triggers and Bun Runtime:** Malicious code activates before the package is fully formed on disk (`preinstall`) and bypasses Node.js-based monitoring tools by using the **Bun** runtime, which security tools have not yet fully adapted to.
2.  **GitHub Actions and CI/CD Poisoning:** Using `pull_request_target` vulnerabilities, attackers infiltrated the CI/CD processes of giants like Zapier, Postman, and NextAuth, adding persistent *self-hosted runners* to the system through `discussion.yaml` files.
3.  **Cross-Exfiltration:** Instead of sending stolen data to a single center, it was distributed to the repositories of other compromised victims, making forensics tracking impossible.
4.  **Sabotage Mechanism (Dead Man's Switch):** When the malware detects it's being analyzed or blocked, it destroys files on the system using secure overwrite methods with the `rm -rf /home` command.

### Numerical Scale of Destruction (As of End of November)
* **Infected Packages:** 830+ unique NPM packages.
* **Affected Repos:** 25,000+ GitHub repositories.
* **Leaked Critical Data:** 14,000+ API keys and tokens (2,485 of which were still active at the time of attack).

## 4. Comparative Technical Analysis

The table below compares the two attack waves carried out by the same threat actor but evolving in terms of motivation and technical capacity.

| Criterion | Shai-Hulud 1.0 (September) | Shai-Hulud 2.0 (November - Active) |
| :--- | :--- | :--- |
| **Main Target** | End-user crypto wallets | Developer identities and Cloud access |
| **Entry Vector** | Classic Phishing + 2FA Bypass | GitHub Actions PR Exploit + Phishing |
| **Runtime** | Node.js | **Bun** (Faster, less detected) |
| **Execution** | `postinstall` (Post-installation) | `preinstall` (Pre-installation - more aggressive) |
| **Data Exfiltration** | Simple scripts | TruffleHog integration + Cloud SDK Full Dump |
# 🐛 Case Study: The Shai-Hulud Incident

> **Context:** This report is a concrete example of the "topological risk" concept proposed in the [NPM Supply Chain Network Analysis](./README.md) project. The Shai-Hulud attack demonstrates how attackers weaponize the network structure.

## 1. Introduction: A Turning Point
The year 2025 has been recorded as a definitive breaking point in the software supply chain security literature. The NPM ecosystem was subjected to the first large-scale "wormable" malware attack, named "Shai-Hulud" in reference to the giant sandworms in Frank Herbert's *Dune* universe. This sequence of events not only affected thousands of projects but also painfully exposed the inadequacy of existing security paradigms—especially traditional scanners focusing on package content.

This report analyzes the two waves of the Shai-Hulud attack (September and November 2025) in technical depth and demonstrates the necessity of the **topological risk model (Behavioral Risk Score - BRS)** developed against such threats.

## 2. First Wave: The Awakening (Shai-Hulud 1.0)
**Date Range:** September 5 – 23, 2025
**Code Name:** "Chalk & Debug Attack"

The first wave in September was a reconnaissance attack targeting the ecosystem's central nodes. Threat actors compromised 18 critical packages such as `@ctrl/tinycolor`, `chalk`, and `debug`, which exceeded 2.6 billion weekly downloads.

### Attack Vector and Execution
The attack began with phishing-based compromise of critical maintainer accounts, such as Josh Junon, through convincing fake domains like `npmjs.help`.
* **Mechanism:** Malicious code was executed through `postinstall` scripts.
* **Payload:** A *crypto-clipper* running in the browser environment. By hooking `fetch` and `XMLHttpRequest` structures, crypto wallet addresses were instantly replaced with the attacker's addresses using Levenshtein distance algorithm.
* **Impact:** Although financial damage (~$503 USD) remained limited due to early detection, the attack's reach potential proved the ecosystem's fragility.

## 3. Second Wave: Destruction and Propagation (Shai-Hulud 2.0)
**Date Range:** November 21, 2025 – Present (Active)
**Code Name:** "The Second Coming"

The second wave beginning in November transformed from a theft attempt into **an autonomous cyber weapon**. Attackers used much more sophisticated methods to make detection difficult and ensure persistence.

### Technical Innovations and Sophistication
Unlike the previous version, Shai-Hulud 2.0 was equipped with these four key capabilities:

1.  **Preinstall Triggers and Bun Runtime:** Malicious code activates before the package is fully formed on disk (`preinstall`) and bypasses Node.js-based monitoring tools by using the **Bun** runtime, which security tools have not yet fully adapted to.
2.  **GitHub Actions and CI/CD Poisoning:** Using `pull_request_target` vulnerabilities, attackers infiltrated the CI/CD processes of giants like Zapier, Postman, and NextAuth, adding persistent *self-hosted runners* to the system through `discussion.yaml` files.
3.  **Cross-Exfiltration:** Instead of sending stolen data to a single center, it was distributed to the repositories of other compromised victims, making forensics tracking impossible.
4.  **Sabotage Mechanism (Dead Man's Switch):** When the malware detects it's being analyzed or blocked, it destroys files on the system using secure overwrite methods with the `rm -rf /home` command.

### Numerical Scale of Destruction (As of End of November)
* **Infected Packages:** 830+ unique NPM packages.
* **Affected Repos:** 25,000+ GitHub repositories.
* **Leaked Critical Data:** 14,000+ API keys and tokens (2,485 of which were still active at the time of attack).

## 4. Comparative Technical Analysis

The table below compares the two attack waves carried out by the same threat actor but evolving in terms of motivation and technical capacity.

| Criterion | Shai-Hulud 1.0 (September) | Shai-Hulud 2.0 (November - Active) |
| :--- | :--- | :--- |
| **Main Target** | End-user crypto wallets | Developer identities and Cloud access |
| **Entry Vector** | Classic Phishing + 2FA Bypass | GitHub Actions PR Exploit + Phishing |
| **Runtime** | Node.js | **Bun** (Faster, less detected) |
| **Execution** | `postinstall` (Post-installation) | `preinstall` (Pre-installation - more aggressive) |
| **Data Exfiltration** | Simple scripts | TruffleHog integration + Cloud SDK Full Dump |
| **Propagation Model** | Manual / Semi-automatic | **Fully Automated Worm** (Self-publishing with stolen token) |
| **Persistence** | None | Self-hosted runner + Workflow manipulation |
| **Sabotage** | None | "Dead man’s switch" (Data destruction) |

## 5. Conclusion: The Necessity of Topological Analysis

The Shai-Hulud attack is the most concrete example proving the "small-world" structure of the NPM ecosystem and the systemic importance of central packages (hubs). While traditional security tools focus on package *content* (code analysis), attackers weaponized the network's *topology* and *trust relationships* (graph structure).

In this context, the **"NPM Supply Chain Network Analysis"** project being conducted is a proactive necessity rather than a reactive solution. The **Behavioral Risk Score (BRS)** developed within the project aims to mathematically model and predict the propagation routes targeted by Shai-Hulud 2.0 by identifying packages with high "betweenness centrality" and "dependent count" values. Shai-Hulud is not a warning, but proof of the system's topological vulnerability.