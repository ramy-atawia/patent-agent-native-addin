#!/usr/bin/env python3
"""
INDENTATION FIXER
================

This script fixes all indentation issues in Python files, particularly
around import statements that got misaligned during the import fixing process.
"""

import os
import re
from pathlib import Path

def fix_file_indentation(file_path: Path):
    """Fix indentation issues in a single file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix common indentation patterns
        lines = content.split('\n')
        fixed_lines = []
        
        for line in lines:
            # Fix import statements that are not properly indented
            if line.strip().startswith('from src.') or line.strip().startswith('import src.'):
                # Find the proper indentation level
                if 'try:' in lines[max(0, lines.index(line)-2):lines.index(line)]:
                    # This is inside a try block, should be indented
                    line = '            ' + line.strip()
                elif 'if ' in lines[max(0, lines.index(line)-2):lines.index(line)]:
                    # This is inside an if block, should be indented
                    line = '        ' + line.strip()
                elif 'async def' in lines[max(0, lines.index(line)-5):lines.index(line)]:
                    # This is inside an async function, should be indented
                    line = '        ' + line.strip()
                elif 'def ' in lines[max(0, lines.index(line)-5):lines.index(line)]:
                    # This is inside a function, should be indented
                    line = '        ' + line.strip()
                elif 'class ' in lines[max(0, lines.index(line)-5):lines.index(line)]:
                    # This is inside a class, should be indented
                    line = '        ' + line.strip()
            
            fixed_lines.append(line)
        
        fixed_content = '\n'.join(fixed_lines)
        
        # Only write if changes were made
        if fixed_content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            print(f"✅ Fixed indentation in: {file_path.relative_to(Path.cwd())}")
            return True
        else:
            print(f"⏭️ No indentation fixes needed in: {file_path.relative_to(Path.cwd())}")
            return False
            
    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")
        return False

def main():
    """Main function to fix all indentation issues"""
    root_dir = Path("/Users/Mariam/agentic-native-drafting/agentic_native_drafting")
    
    print("🔧 AGENTIC NATIVE DRAFTING - INDENTATION FIXER")
    print("=" * 60)
    print(f"Fixing indentation in: {root_dir}")
    print()
    
    # Get all Python files
    python_files = list(root_dir.rglob("*.py"))
    print(f"📁 Found {len(python_files)} Python files to process")
    
    fixed_count = 0
    
    for py_file in python_files:
        if fix_file_indentation(py_file):
            fixed_count += 1
    
    print(f"\n🎯 Indentation fixing completed!")
    print(f"✅ Fixed {fixed_count} files")
    
    # Suggest next steps
    print(f"\n💡 NEXT STEPS:")
    print(f"   1. Test import resolution: python3 -c 'from src.agent_core.orchestrator import AgentOrchestrator'")
    print(f"   2. Try starting the backend: cd src && uvicorn agent_core.api:app --port 8000")

if __name__ == "__main__":
    main()
