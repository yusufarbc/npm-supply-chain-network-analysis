import requests
import time
import urllib.parse
from tqdm.notebook import tqdm

def get_top_dependents(limit=1000, api_delay=0.1):
    """
    Fetches the most dependent packages from the ecosyste.ms API using pagination.
    """
    base_url = "https://packages.ecosyste.ms/api/v1/registries/npmjs.org/packages"
    packages = []
    page = 1
    per_page = 100
    
    print(f"Fetching top {limit} packages from ecosyste.ms...")
    
    with tqdm(total=limit, desc="Fetching Seed Packages") as pbar:
        while len(packages) < limit:
            try:
                params = {
                    "sort": "dependent_repos_count",
                    "per_page": per_page,
                    "page": page
                }
                response = requests.get(base_url, params=params, timeout=30)
                response.raise_for_status()
                data = response.json()
                
                if not data:
                    break
                
                for pkg in data:
                    if len(packages) < limit:
                        packages.append({
                            "name": pkg["name"],
                            "dependents_count": pkg.get("dependent_repos_count", 0),
                            "downloads": pkg.get("downloads", 0),
                            "rank": pkg.get("rank", len(packages) + 1)
                        })
                        pbar.update(1)
                    else:
                        break
                
                page += 1
                time.sleep(api_delay)
                
            except requests.exceptions.RequestException as e:
                print(f"Error fetching page {page}: {e}. Retrying in 5 seconds...")
                time.sleep(5) # Backoff
                continue
                
    return packages

def fetch_npm_dependencies(package_name):
    """
    Fetches the latest version metadata from the NPM Registry API 
    and extracts production dependencies.
    Fetches dependents count and downloads from Ecosyste.ms API.
    """
    # 1. Get dependencies from NPM Registry (Source of Truth for deps)
    url_latest = f"https://registry.npmjs.org/{package_name}/latest"
    
    # 2. Get metadata from Ecosyste.ms (Dependents, Downloads)
    # Encode package name to handle scoped packages (e.g., @types/node -> %40types%2Fnode)
    safe_pkg_name = urllib.parse.quote(package_name, safe='')
    url_ecosystems = f"https://packages.ecosyste.ms/api/v1/registries/npmjs.org/packages/{safe_pkg_name}"
    
    try:
        # A. Fetch Dependencies (NPM Registry)
        response_latest = requests.get(url_latest, timeout=20)
        if response_latest.status_code == 404:
            return [], {} # Package not found or private
        
        # If NPM fails, we can't build the graph, so we skip
        if response_latest.status_code != 200:
            return [], {}
            
        data_latest = response_latest.json()
        dependencies = list(data_latest.get("dependencies", {}).keys())
        
        # B. Fetch Metadata (Ecosyste.ms)
        # We use a separate try-except block so metadata failure doesn't stop graph building
        dependents_count = 0
        downloads = 0
        try:
            response_eco = requests.get(url_ecosystems, timeout=10)
            if response_eco.status_code == 200:
                data_eco = response_eco.json()
                dependents_count = data_eco.get("dependent_repos_count", 0)
                downloads = data_eco.get("downloads", 0)
        except:
            pass # Keep defaults if ecosyste.ms fails

        # Extract comprehensive metadata
        metadata = {
            "version": str(data_latest.get("version", "")),
            "license": str(data_latest.get("license", "")),
            "maintainers_count": str(len(data_latest.get("maintainers", []))),
            "description": str(data_latest.get("description", "")),
            "downloads": str(downloads),
            "dependents_count": str(dependents_count),
            # We can't easily get creation time from latest endpoint, skipping or using empty
            "created": "", 
            "modified": "" 
        }
        
        return dependencies, metadata
        
    except requests.exceptions.RequestException:
        # Silently fail for individual package errors to keep crawler running
        return [], {}
    except Exception:
        return [], {}
