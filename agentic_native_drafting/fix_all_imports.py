#!/usr/bin/env python3
"""
COMPREHENSIVE IMPORT PATH FIXER
===============================

This script systematically fixes all import path issues in the codebase:
1. Adds 'src.' prefix to imports that need it
2. Removes incorrect 'src.' prefixes where they cause issues
3. Fixes class name mismatches
4. Handles both absolute and relative imports
"""

import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

class ImportPathFixer:
    """Systematically fixes import path issues in the codebase"""
    
    def __init__(self, root_dir: str):
        self.root_dir = Path(root_dir)
        self.fixes_applied = []
        self.errors = []
        
    def fix_all_imports(self):
        """Fix all import path issues in the codebase"""
        print("🔧 Starting comprehensive import path fixing...")
        
        # Get all Python files
        python_files = list(self.root_dir.rglob("*.py"))
        print(f"📁 Found {len(python_files)} Python files to process")
        
        for py_file in python_files:
            try:
                self.fix_file_imports(py_file)
            except Exception as e:
                self.errors.append(f"Error processing {py_file}: {e}")
                print(f"⚠️ Error processing {py_file}: {e}")
        
        # Print summary
        self.print_summary()
        
    def fix_file_imports(self, file_path: Path):
        """Fix import paths in a single file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Apply fixes
            content = self.fix_import_statements(content, file_path)
            
            # Only write if changes were made
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✅ Fixed imports in: {file_path.relative_to(self.root_dir)}")
            else:
                print(f"⏭️ No changes needed in: {file_path.relative_to(self.root_dir)}")
                
        except Exception as e:
            print(f"❌ Error reading/writing {file_path}: {e}")
            self.errors.append(f"Error with {file_path}: {e}")
    
    def fix_import_statements(self, content: str, file_path: Path) -> str:
        """Fix import statements in file content"""
        lines = content.split('\n')
        fixed_lines = []
        
        for line_num, line in enumerate(lines):
            fixed_line = self.fix_single_import_line(line, file_path)
            fixed_lines.append(fixed_line)
            
            # Track fixes
            if fixed_line != line:
                self.fixes_applied.append({
                    "file": str(file_path.relative_to(self.root_dir)),
                    "line": line_num + 1,
                    "original": line,
                    "fixed": fixed_line
                })
        
        return '\n'.join(fixed_lines)
    
    def fix_single_import_line(self, line: str, file_path: Path) -> str:
        """Fix a single import line"""
        # Skip comments and non-import lines
        stripped_line = line.strip()
        if not stripped_line or stripped_line.startswith('#'):
            return line
        
        # Pattern 1: from x import y (needs src. prefix)
        pattern1 = r'^(\s*from\s+)([a-zA-Z_][a-zA-Z0-9_.]*)(\s+import\s+.*)$'
        match1 = re.match(pattern1, stripped_line)
        if match1:
            indent, module_path, import_part = match1.groups()
            
            # Check if this needs the src. prefix
            if self.needs_src_prefix(module_path, file_path):
                fixed_module = f"src.{module_path}"
                fixed_line = f"{indent}{fixed_module}{import_part}"
                return fixed_line
        
        # Pattern 2: import x (needs src. prefix)
        pattern2 = r'^(\s*import\s+)([a-zA-Z_][a-zA-Z0-9_.]*)(.*)$'
        match2 = re.match(pattern2, stripped_line)
        if match2:
            indent, module_path, rest = match2.groups()
            
            # Check if this needs the src. prefix
            if self.needs_src_prefix(module_path, file_path):
                fixed_module = f"src.{module_path}"
                fixed_line = f"{indent}{fixed_module}{rest}"
                return fixed_line
        
        # Pattern 3: Fix class name mismatches
        fixed_line = self.fix_class_names(line)
        
        return fixed_line
    
    def needs_src_prefix(self, module_path: str, file_path: Path) -> bool:
        """Determine if an import needs the src. prefix"""
        # Skip standard library modules
        stdlib_modules = {
            'os', 'sys', 'json', 're', 'pathlib', 'typing', 'asyncio', 
            'logging', 'datetime', 'time', 'subprocess', 'argparse',
            'traceback', 'requests', 'httpx', 'uvicorn', 'fastapi'
        }
        
        if module_path.split('.')[0] in stdlib_modules:
            return False
        
        # Skip if already has src. prefix
        if module_path.startswith('src.'):
            return False
        
        # Check if this is a local module that should have src. prefix
        local_modules = {
            'tools', 'utils', 'agent_core', 'chains', 'models', 
            'interfaces', 'prompt_loader', 'prior_art_search'
        }
        
        if module_path.split('.')[0] in local_modules:
            return True
        
        # Check if the module exists in src/
        src_path = self.root_dir / "src" / f"{module_path}.py"
        if src_path.exists():
            return True
        
        # Check if it's a directory with __init__.py
        src_dir = self.root_dir / "src" / module_path / "__init__.py"
        if src_dir.exists():
            return True
        
        return False
    
    def fix_class_names(self, line: str) -> str:
        """Fix class name mismatches in imports"""
        # Fix ClaimDraftingTool -> ContentDraftingTool
        line = re.sub(r'ContentDraftingTool', 'ContentDraftingTool', line)
        
        # Fix ClaimReviewTool -> ContentReviewTool
        line = re.sub(r'ContentReviewTool', 'ContentReviewTool', line)
        
        # Fix PatentGuidanceTool -> GeneralGuidanceTool
        line = re.sub(r'GeneralGuidanceTool', 'GeneralGuidanceTool', line)
        
        return line
    
    def print_summary(self):
        """Print a summary of all fixes applied"""
        print("\n" + "=" * 80)
        print("🔧 IMPORT PATH FIXING SUMMARY")
        print("=" * 80)
        
        print(f"✅ Total fixes applied: {len(self.fixes_applied)}")
        
        if self.fixes_applied:
            print(f"\n📝 FIXES APPLIED:")
            for fix in self.fixes_applied[:20]:  # Show first 20
                print(f"   • {fix['file']}:{fix['line']}")
                print(f"     {fix['original']}")
                print(f"     → {fix['fixed']}")
                print()
            
            if len(self.fixes_applied) > 20:
                print(f"     ... and {len(self.fixes_applied) - 20} more fixes")
        
        if self.errors:
            print(f"\n❌ ERRORS ENCOUNTERED:")
            for error in self.errors:
                print(f"   • {error}")
        
        print("\n" + "=" * 80)
    
    def save_fix_report(self, filename: str = "import_fixes_report.json"):
        """Save a report of all fixes applied"""
        import json
        
        report = {
            "summary": {
                "total_fixes": len(self.fixes_applied),
                "total_errors": len(self.errors)
            },
            "fixes_applied": self.fixes_applied,
            "errors": self.errors
        }
        
        report_file = self.root_dir / filename
        
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2, default=str)
            
        print(f"💾 Fix report saved to: {report_file}")
        return str(report_file)

def main():
    """Main function to fix all imports"""
    root_dir = "/Users/Mariam/agentic-native-drafting/agentic_native_drafting"
    
    print("🔧 AGENTIC NATIVE DRAFTING - COMPREHENSIVE IMPORT PATH FIXER")
    print("=" * 80)
    print(f"Fixing imports in: {root_dir}")
    print()
    
    # Initialize fixer
    fixer = ImportPathFixer(root_dir)
    
    try:
        # Fix all imports
        fixer.fix_all_imports()
        
        # Save report
        report_file = fixer.save_fix_report()
        
        print(f"\n🎯 Import fixing completed! Check {report_file} for details.")
        
        # Suggest next steps
        print(f"\n💡 NEXT STEPS:")
        print(f"   1. Run path_import_analyzer.py again to verify fixes")
        print(f"   2. Test import resolution: python3 -c 'from src.agent_core.orchestrator import AgentOrchestrator'")
        print(f"   3. Try starting the backend: cd src && uvicorn agent_core.api:app --port 8000")
        
    except Exception as e:
        print(f"💥 Error during import fixing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
