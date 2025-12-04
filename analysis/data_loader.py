import requests
import time
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
                response = requests.get(base_url, params=params, timeout=10)
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
                print(f"Error fetching page {page}: {e}")
                time.sleep(1) # Backoff
                continue
                
    return packages

def fetch_npm_dependencies(package_name):
    """
    Fetches the latest version metadata from the NPM Registry API 
    and extracts only production dependencies.
    """
    url = f"https://registry.npmjs.org/{package_name}/latest"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 404:
            return [] # Package not found or private
        response.raise_for_status()
        data = response.json()
        
        # Extract production dependencies only
        dependencies = data.get("dependencies", {})
        return list(dependencies.keys())
        
    except requests.exceptions.RequestException:
        # Silently fail for individual package errors to keep crawler running
        return []
    except Exception:
        return []
