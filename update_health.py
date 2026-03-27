import libtorrent as lt
import time
import sys
import re
import os
import tempfile

def check_magnet_health(magnet_link, timeout=15):
    if not magnet_link or magnet_link.strip() == "":
        return 'unknown'
        
    print(f"Checking link: {magnet_link[:50]}...")
    ses = lt.session({'listen_interfaces': '0.0.0.0:6881'})
    params = {
        'save_path': tempfile.gettempdir(), # Use OS temp dir to prevent junk folders
        'storage_mode': lt.storage_mode_t(2), # storage_mode_sparse
    }
    
    try:
        handle = lt.add_magnet_uri(ses, magnet_link, params)
    except Exception as e:
        print(f"Failed to add magnet: {e}")
        return 'red'
    
    start_time = time.time()
    while not handle.has_metadata():
        if time.time() - start_time > timeout:
            print("  -> Timeout (No metadata). Marking as DEAD/WEAK.")
            return 'red'
        time.sleep(1)

    # Let it gather peers for a few seconds
    time.sleep(3)
    s = handle.status()
    print(f"  -> Seeds: {s.num_seeds}, Peers: {s.num_peers}")
    
    if s.num_seeds >= 20:
        return 'green' # Best
    elif s.num_seeds >= 10:
        return 'blue'  # Better
    elif s.num_seeds > 0:
        return 'yellow' # Good
    else:
        return 'red' # Bad

def update_movies_js(filepath='movies.js'):
    if not os.path.exists(filepath):
        print(f"File {filepath} not found!")
        return

    with open(filepath, 'r') as f:
        content = f.read()

    # Find all magnet links in the file
    magnet_pattern = r'magnetUrl:\s*"(magnet:\?xt=urn:[^"]*)"'
    matches = re.finditer(magnet_pattern, content)
    
    replacements = {}
    
    for match in matches:
        magnet_url = match.group(1)
        # Avoid checking the same magnet multiple times
        if magnet_url not in replacements:
            health = check_magnet_health(magnet_url)
            replacements[magnet_url] = health
            
    # Modify the content string - add magnetHealth right below magnetUrl
    new_content = content
    for url, health in replacements.items():
        original_str = f'magnetUrl: "{url}"'
        # Check if magnetHealth already exists, if so replace it
        if f'magnetUrl: "{url}",\n                magnetHealth:' in new_content:
            new_content = re.sub(
                r'magnetUrl: "' + re.escape(url) + r'",\s*magnetHealth:\s*"[^"]*"',
                f'magnetUrl: "{url}",\n                magnetHealth: "{health}"',
                new_content
            )
        else:
            # Insert health property right after magnetUrl
            new_content = new_content.replace(
                original_str,
                f'{original_str},\n                magnetHealth: "{health}"'
            )

    # Also add default unknown for empty magnet links if it doesn't have health yet
    empty_magnet_pattern = r'magnetUrl:\s*""(?!\s*,\s*magnetHealth)'
    new_content = re.sub(empty_magnet_pattern, 'magnetUrl: "",\n                magnetHealth: "unknown"', new_content)

    with open(filepath, 'w') as f:
        f.write(new_content)
        
    print(f"\nSuccessfully updated health markers in {filepath}!")

if __name__ == "__main__":
    update_movies_js()
