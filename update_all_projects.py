import os
import shutil

# 1. Source Directory (Ultimate Research Team - The Brain)
source_dir = r"d:\AI 자동화 연구\AI 에이전트 협업\ultimate_research_team"
core_dir = r"d:\AI 자동화 연구\_ANTIGRAVITY_CORE"
target_dirs = [
    r"d:\AI 자동화 연구\모두의 렌탈"
]

files_to_sync = [
    "agents.py",
    "ANTIGRAVITY_MASTER_MANUAL.md"
]

def sync_core_files():
    # 1. Ensure Core Directory Exists
    if not os.path.exists(core_dir):
        os.makedirs(core_dir)
        print(f"[Core] Created central repository at: {core_dir}")

    # 2. Backup to Core from Source (Ultimate Research Team)
    print("--- [Step 1] Syncing Source to Core ---")
    for filename in files_to_sync:
        src_path = os.path.join(source_dir, filename)
        dst_path = os.path.join(core_dir, filename)
        
        if os.path.exists(src_path):
            shutil.copy2(src_path, dst_path)
            print(f"✅ Copied {filename} to Core")
        else:
            print(f"❌ Source file missing: {src_path}")

    # 3. Propagate Core to Target Projects (Universal Update)
    print("\n--- [Step 2] Propagating Core to Targets ---")
    for target_dir in target_dirs:
        if not os.path.exists(target_dir):
            print(f"⚠️ Target directory not found: {target_dir}")
            continue
            
        print(f"📂 Updating Project: {os.path.basename(target_dir)}")
        for filename in files_to_sync:
            core_path = os.path.join(core_dir, filename)
            target_path = os.path.join(target_dir, filename)
            
            if os.path.exists(core_path):
                # Backup existing file before overwrite (Safety)
                if os.path.exists(target_path):
                    backup_path = target_path + ".bak"
                    shutil.copy2(target_path, backup_path)
                    print(f"  Existing file backed up to .bak")
                
                shutil.copy2(core_path, target_path)
                print(f"  ✅ Updated {filename} (v11.2 SOTA)")
            else:
                print(f"  ❌ Core file missing: {filename}")

if __name__ == "__main__":
    sync_core_files()
