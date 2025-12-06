# 🛡️ NPM Security Landscape: Threats and Attack Vectors

> **Context:** This document forms the theoretical foundation of the [NPM Supply Chain Network Analysis](../README.md) project. It explains *why* the topological risk model used in the project is necessary, through the lens of active threats in the ecosystem.

## 1. Introduction: Why is NPM a Primary Attack Surface?

Node Package Manager (NPM) is the world's largest software registry, hosting over 3 million packages and processing billions of downloads weekly. Modern software development processes heavily rely on third-party code libraries (dependencies) to increase speed. However, when a single NPM package is added to a project, an average of 79 transitive (indirect) packages are also implicitly included in the trust chain.

This "implicit trust" model makes NPM an attractive target for attackers. By compromising a single popular package or a dependency deep within it, attackers gain access to a "one-to-many" distribution mechanism that can affect millions of developers and end users. This document defines the active threats in the NPM ecosystem and the technical defense mechanisms that should be taken against them.

---

## 2. Attack Types and Technical Taxonomy

The following attack vectors represent the most common and critical techniques targeting the modern software supply chain.

### 2.1. Shrinkwrapped Clones (Packaged Clones)
**Risk Level:** High
**Definition:** When an attacker or careless developer copies a legitimate package and publishes it under a new name without referencing the original package.

*   **How It Works?** Unlike GitHub, there is no "fork" mechanism in the NPM ecosystem. When a package is cloned, the link with the original source (provenance) is broken.
*   **Technical Detail:**
    *   **Manifest Manipulation:** The attacker modifies the `package.json` file of the copied package but retains all or part of the code.
    *   **Lockfile Exploitation:** `package-lock.json` or `npm-shrinkwrap.json` files are manipulated to "pin" older versions with known security vulnerabilities in the dependency tree.
    *   **Security Risk:** When a security vulnerability in the original package is discovered and patched, this fix is not reflected in the Shrinkwrapped Clone. Since tools like `npm audit` don't know the relationship between the clone and the original package, they cannot detect this vulnerability. This causes known vulnerabilities to persist in the system through "ghost" versions.

### 2.2. Typosquatting (Typo Hunting)
**Risk Level:** Medium-High
**Definition:** Publishing malicious packages with names similar to popular packages (e.g., `raect` instead of `react` or `clolors` instead of `colors`).

*   **How It Works?** It exploits a momentary carelessness when a developer types the `npm install` command.
*   **Technical Detail:** Attackers choose names with low Levenshtein distance (character difference between two words). When the package is installed, malware is executed through `preinstall` or `postinstall` scripts in `package.json`, attempting to steal environment variables or SSH keys from the system.

### 2.3. Dependency Confusion (Dependency Confusion)
**Risk Level:** Critical
**Definition:** Publishing the same name as a private package used by companies in their internal networks on the public NPM registry with a higher version number.

*   **How It Works?** Package managers (npm, pip, etc.) by default check both private and public registries. If there are two packages with the same name, they usually prefer the one with the **higher version number**.
*   **Technical Detail:**
    *   *Private Package:* `@internal/auth-utils` (v1.0.0)
    *   *Malicious Public Package:* `@internal/auth-utils` (v99.0.0)
    *   During automatic updates or installation, the system pulls the malicious package from the public registry, resulting in internal network infiltration.

### 2.4. Account Takeover (ATO) & Worms (Account Hijacking)
**Risk Level:** Critical
**Definition:** Compromise of trusted package developer accounts (due to weak passwords, phishing, or leaked tokens) and injection of malicious code into their packages.

*   **How It Works?** The attacker, assuming the identity of a legitimate developer, publishes a "new and malicious" version of a trusted package.
*   **Technical Detail (Shai-Hulud Example):** In an incident in September 2025, attackers hijacked developer accounts through phishing. The malware called "Shai-Hulud" automatically propagated itself to other packages (worm-like behavior) by stealing publishing tokens from the `.npmrc` file in the compromised system, infecting hundreds of packages.

### 2.5. Protestware / Malicious Updates (Malicious Updates)
**Risk Level:** High
**Definition:** A legitimate package owner intentionally breaking (sabotaging) the package or adding malicious functionality to it.

*   **How It Works?** As seen in the `node-ipc` or `faker.js` incidents, the developer adds code that deletes files at specific IP addresses or locks the system by entering an infinite loop for political or personal reasons to their popular package.
*   **Technical Detail:** These attacks are usually distributed through `minor` or `patch` updates (expected to be safe according to SemVer rules) and target automatic update mechanisms (e.g., `^1.0.0`).

---

## 3. Technical Defense Strategies and Measures

The defense-in-depth principle should be applied to narrow the attack surface.

### 3.1. Installation and CI/CD Security

| Method | Description and Implementation |
| :--- | :--- |
| **`npm ci` Usage** | Never use `npm install` in CI/CD environments. `npm ci` (clean install) adheres to versions in `package-lock.json`, doesn't update `package.json`, and guarantees reproducibility of installation. |
| **Lockfile Analysis** | Lockfiles contain `integrity` hashes (SHA-512) and `resolved` URLs of packages. Tools like `lockfile-lint` should be used to check whether packages are being downloaded from untrusted sources (e.g., attacker's own server). |
| **Script Disabling** | If possible, use the `npm install --ignore-scripts` parameter during installation to prevent the execution of `preinstall` and `postinstall` scripts, which are most commonly used by attackers. |

### 3.2. Developer and Organizational Measures

#### Scoped Packages
For internal company packages, **Scoped Packages** in the format `@company/package-name` must be used. This informs the NPM registry that the package belongs to a user or organization and allows the `.npmrc` file to route this scope only to the private registry (e.g., Artifactory, Verdaccio) to prevent Dependency Confusion attacks.

#### 2FA and Token Security
**Two-Factor Authentication (2FA)** should be made mandatory for NPM accounts (especially for accounts with `publish` privileges). When using Automation Tokens, granular authorizations should be set to allow only necessary packages and IP addresses (CIDR whitelist).

#### Software Composition Analysis (SCA) and Security Tools
*   **Socket.dev / OSSF Scorecard:** Unlike traditional vulnerability scanners, these tools analyze the "behavior" and "health" of packages. They detect anomalies such as a package suddenly requesting network access, attempting to write to the file system, or adding an `install` script.
*   **Snyk / npm audit:** Used to scan for known CVE (Common Vulnerabilities and Exposures) entries. However, it should be noted that they may not always catch hidden vulnerabilities like Shrinkwrapped Clones.

### 3.3. Manifest File Inspection
Developers should pay particular attention to the following areas in the `package.json` file:
*   **`scripts`**: Are there `curl`, `wget`, or encrypted (base64) commands in the `preinstall`, `postinstall` areas?
*   **`dependencies`**: Are there typos in names (Typosquatting)? Do version numbers make sense?

---

## 4. Summary Table: Attack and Mitigation Matrix

| Attack Type | Primary Vector | Key Mitigation |
| :--- | :--- | :--- |
| **Shrinkwrapped Clones** | Cloned/Modified Code | Source code analysis, OSSF Scorecard (Maintenance metrics) |
| **Typosquatting** | Name Similarity | Careful package name verification, Scoped packages usage |
| **Dependency Confusion** | Version Priority | `@scope` usage, Private registry configuration (.npmrc) |
| **Account Takeover** | Identity Theft | Mandatory 2FA, Granular Tokens |
| **Malicious Updates** | Automatic Updates (`^`, `~`) | Dependency Pinning (Version Pinning), `npm ci` |
| **Install Scripts** | `postinstall` Scripts | `--ignore-scripts`, Socket.dev behavior analysis |
