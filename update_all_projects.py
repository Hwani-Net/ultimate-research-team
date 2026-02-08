import os
import shutil
from pathlib import Path

# --- PORTABLE PATH DISCOVERY ---
def find_core_directory():
    # 1. Check Environment Variable (Highest Priority)
    env_path = os.getenv("ANTIGRAVITY_CORE_PATH")
    if env_path and os.path.exists(env_path):
        return Path(env_path)
    
    # 2. Search Upwards (Relative Discovery - Find '_ANTIGRAVITY_CORE')
    current_path = Path(__file__).resolve().parent
    # Check current and up to 3 parent levels
    search_ptr = current_path
    for _ in range(3):
        potential_core = search_ptr / "_ANTIGRAVITY_CORE"
        if potential_core.exists() and potential_core.is_dir():
            return potential_core
        search_ptr = search_ptr.parent
            
    # Default Fallback: Assume it should be a sibling of the current project directory
    fallback = current_path.parent / "_ANTIGRAVITY_CORE"
    if not fallback.exists():
        try:
            fallback.mkdir(parents=True, exist_ok=True)
            print(f"✨ Created new Core directory at: {fallback}")
        except:
            return current_path # Last resort: fallback to current dir
    return fallback

CORE_DIR = find_core_directory()
SOURCE_DIR = Path(__file__).resolve().parent
CORE_FILES = ["agents.py", "ANTIGRAVITY_MASTER_MANUAL.md"]

# Dynamic target discovery: Any sibling folder that contains an 'agents.py' OR is in the manual list
KNOWN_TARGETS = ["모두의 렌탈", "combined_rental"]

def get_target_projects():
    targets = []
    parent_dir = SOURCE_DIR.parent
    for item in parent_dir.iterdir():
        if item.is_dir() and item.name != SOURCE_DIR.name and not item.name.startswith(("_", ".")):
            # If it's a known project or has agents.py, it's a target
            if item.name in KNOWN_TARGETS or (item / "agents.py").exists():
                targets.append(item)
    return targets

def sync_to_core():
    print(f"\n--- [Step 1] Syncing {SOURCE_DIR.name} to Core ---")
    print(f"📍 Core Path: {CORE_DIR}")
    for file_name in CORE_FILES:
        src = SOURCE_DIR / file_name
        dest = CORE_DIR / file_name
        if src.exists():
            shutil.copy2(src, dest)
            print(f"✅ Copied {file_name} to Core")

def propagate_core():
    targets = get_target_projects()
    print(f"\n--- [Step 2] Propagating Core to {len(targets)} Targets ---")
    for project_path in targets:
        print(f"📂 Updating Project: {project_path.name}")
        for file_name in CORE_FILES:
            src = CORE_DIR / file_name
            dest = project_path / file_name
            
            if src.exists():
                if dest.exists():
                    shutil.copy2(dest, dest.with_suffix(".bak")) # Backup
                shutil.copy2(src, dest)
                print(f"  ✅ Updated {file_name}")

if __name__ == "__main__":
    sync_to_core()
    propagate_core()
    print("\n[COMPLETE] Universal Portable Sync Finished.")
