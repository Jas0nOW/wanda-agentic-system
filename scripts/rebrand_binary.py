#!/usr/bin/env python3
import os
import shutil

BINARY_PATH = os.path.expanduser("~/.opencode/bin/opencode")
BACKUP_PATH = os.path.expanduser("~/.opencode/bin/opencode.bak")

def patch_binary():
    if not os.path.exists(BINARY_PATH):
        print(f"Error: Binary not found at {BINARY_PATH}")
        return False

    # Backup if not exists
    if not os.path.exists(BACKUP_PATH):
        print(f"Backing up to {BACKUP_PATH}...")
        shutil.copy2(BINARY_PATH, BACKUP_PATH)
    else:
        print(f"Backup already exists at {BACKUP_PATH}")

    print("Reading binary...")
    with open(BINARY_PATH, 'rb') as f:
        data = f.read()

    target = b'OpenCode'
    replacement = b'Wanda   ' # Must be same length
    
    # Simple replacement counting
    count = data.count(target)
    print(f"Found {count} occurrences of 'OpenCode'")

    # Smart replacement
    # We want to avoid replacing paths like /home/jannis/.opencode or package names like @anthropic-ai/opencode
    # We look for OpenCode preceded by space, newline, quotes, or null bytes, but NOT / or . or -
    
    new_data = bytearray(data)
    replaced = 0
    
    pos = -1
    while True:
        pos = data.find(target, pos + 1)
        if pos == -1:
            break
            
        # Check byte before
        if pos > 0:
            prev = data[pos-1]
            # ASCII: 47=/, 46=., 45=-, 95=_, 64=@
            if prev in [47, 46, 45, 95, 64]:
                # Skip paths, dotfiles, kebab-case, snake_case, scoped-packages
                continue
        
        # Apply patch
        new_data[pos:pos+len(replacement)] = replacement
        replaced += 1

    print(f"Replaced {replaced} instances (skipped {count - replaced} paths/internal references).")
    
    if replaced > 0:
        print("Writing patched binary to temp file...")
        temp_path = BINARY_PATH + ".patched"
        with open(temp_path, 'wb') as f:
            f.write(new_data)
        
        print("Replacing original binary...")
        os.chmod(temp_path, 0o755)
        os.rename(temp_path, BINARY_PATH)
        print("✅ Successfully rebranded to WANDA!")
        return True
    else:
        print("⚠ No suitable strings found to replace.")
        return False

if __name__ == "__main__":
    patch_binary()
