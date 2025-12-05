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
    
    print(f"Fetching top {limit} packages by DEPENDENTS from ecosyste.ms...")
    
    with tqdm(total=limit, desc="Fetching Dependent Seeds") as pbar:
        while len(packages) < limit:
            try:
                # Ecosyste.ms API sometimes struggles with deep pagination or complex sorts
                # We add a User-Agent header just in case
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
                params = {
                    "sort": "dependent_repos_count",
                    "per_page": per_page,
                    "page": page
                }
                response = requests.get(base_url, params=params, headers=headers, timeout=60)
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
                            # Rank will be calculated globally in metrics.py
                            "rank": 0 
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

def get_top_downloads(limit=1000, api_delay=0.1):
    """
    Fetches the most downloaded packages from the ecosyste.ms API using pagination.
    """
    base_url = "https://packages.ecosyste.ms/api/v1/registries/npmjs.org/packages"
    packages = []
    page = 1
    per_page = 100
    
    print(f"Fetching top {limit} packages by DOWNLOADS from ecosyste.ms...")
    
    with tqdm(total=limit, desc="Fetching Download Seeds") as pbar:
        while len(packages) < limit:
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
                params = {
                    "sort": "downloads",
                    "per_page": per_page,
                    "page": page
                }
                response = requests.get(base_url, params=params, headers=headers, timeout=60)
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
                            "rank": 0 
                        })
                        pbar.update(1)
                    else:
                        break
                
                page += 1
                time.sleep(api_delay)
                
            except requests.exceptions.RequestException as e:
                print(f"Error fetching page {page}: {e}. Retrying in 5 seconds...")
                time.sleep(5)
                continue
                
    return packages

def get_combined_seed_packages(limit_dependents=1000, limit_downloads=1000, api_delay=0.1):
    """
    Fetches both top dependent and top downloaded packages, merges them, and removes duplicates.
    """
    # 1. Fetch by Dependents
    deps_packages = get_top_dependents(limit=limit_dependents, api_delay=api_delay)
    
    # 2. Fetch by Downloads
    dl_packages = get_top_downloads(limit=limit_downloads, api_delay=api_delay)
    
    # 3. Merge and Remove Duplicates
    print("Merging lists and removing duplicates...")
    unique_packages = {}
    
    # Add dependents first
    for pkg in deps_packages:
        unique_packages[pkg['name']] = pkg
        
    # Add downloads (overwrite if exists to ensure we have the object, but keys are unique)
    for pkg in dl_packages:
        if pkg['name'] not in unique_packages:
            unique_packages[pkg['name']] = pkg
            
    combined_list = list(unique_packages.values())
    print(f"Total unique seed packages: {len(combined_list)}")
    
    return combined_list

def fetch_npm_dependencies(package_name):
    """
    Fetches the latest version metadata from the NPM Registry API 
    and extracts production dependencies.
    Fetches dependents count and downloads from Ecosyste.ms API.
    """
    # 1. Get dependencies from NPM Registry (Source of Truth for deps)
    url_latest = f"https://registry.npmjs.org/{package_name}/latest"
    # For dates, we need the full package info, not just latest
    url_full = f"https://registry.npmjs.org/{package_name}"
    
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
        
        # Fetch Full Data for Timestamps (Separate call usually needed for full 'time' field)
        last_modified = ""
        try:
            # Optimization: Try to get 'time' from latest if available, otherwise fetch full
            # Note: 'latest' endpoint usually doesn't have full 'time' history.
            # We make a quick call to full endpoint for accurate 'modified' date
            response_full = requests.get(url_full, timeout=10)
            if response_full.status_code == 200:
                data_full = response_full.json()
                # Get the modification date
                last_modified = data_full.get("time", {}).get("modified", "")
                if not last_modified:
                    # Fallback to latest version date
                    latest_ver = data_full.get("dist-tags", {}).get("latest", "")
                    last_modified = data_full.get("time", {}).get(latest_ver, "")
        except:
            pass
        
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

        # Fallback: Fetch downloads from NPM Registry API if 0
        if not downloads:
            try:
                url_npm_dl = f"https://api.npmjs.org/downloads/point/last-month/{package_name}"
                resp_dl = requests.get(url_npm_dl, timeout=5)
                if resp_dl.status_code == 200:
                    downloads = resp_dl.json().get("downloads", 0)
            except:
                pass

        # Extract comprehensive metadata
        metadata = {
            "version": str(data_latest.get("version", "")),
            "license": str(data_latest.get("license", "")),
            "maintainers_count": str(len(data_latest.get("maintainers", []))),
            "description": str(data_latest.get("description", "")),
            "downloads": str(downloads),
            "dependents_count": str(dependents_count),
            "rank": "0", # Placeholder, will be calculated in metrics.py
            "last_modified": str(last_modified), # NEW FIELD
            "created": "" 
        }
        
        return dependencies, metadata
        
    except requests.exceptions.RequestException:
        # Silently fail for individual package errors to keep crawler running
        return [], {}
    except Exception:
        return [], {}
