import networkx as nx
import time
from tqdm.notebook import tqdm
from data_loader import fetch_npm_dependencies

def build_dependency_graph(seed_packages, max_depth=2, api_delay=0.1):
    """
    Builds a directed graph starting from seed packages using BFS.
    """
    G = nx.DiGraph()
    visited = set()
    queue = [] # Queue stores tuples: (package_name, current_depth)
    
    # Initialize queue with seed packages
    for pkg_data in seed_packages:
        # Handle both string (old behavior) and dict (new behavior)
        if isinstance(pkg_data, dict):
            pkg_name = pkg_data['name']
            attrs = pkg_data
        else:
            pkg_name = pkg_data
            attrs = {}
            
        queue.append((pkg_name, 0))
        visited.add(pkg_name)
        G.add_node(pkg_name, type='seed', **attrs)

    print(f"Starting crawler with {len(seed_packages)} seed packages up to depth {max_depth}...")
    
    # We use a progress bar, but total is unknown due to BFS expansion
    with tqdm(desc="Crawling Dependencies") as pbar:
        while queue:
            current_pkg, depth = queue.pop(0)
            pbar.update(1)
            
            # Fetch dependencies and metadata
            dependencies, metadata = fetch_npm_dependencies(current_pkg)
            
            # Update current node with metadata
            if metadata:
                for k, v in metadata.items():
                    # Ensure all values are strings for GML compatibility
                    G.nodes[current_pkg][k] = str(v) if v is not None else ""
            
            time.sleep(api_delay / 2) # Slight delay to be polite

            # Stop condition: Do not crawl children if current_depth >= MAX_DEPTH
            if depth >= max_depth:
                continue
            
            for dep in dependencies:
                # Add edge
                G.add_edge(current_pkg, dep)
                
                # If not visited, add to queue
                if dep not in visited:
                    visited.add(dep)
                    queue.append((dep, depth + 1))
                    G.add_node(dep, type='dependency')
    
    print(f"Graph construction complete. Nodes: {G.number_of_nodes()}, Edges: {G.number_of_edges()}")
    return G
