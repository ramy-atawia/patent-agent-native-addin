#!/usr/bin/env python3
"""
PATH AND IMPORT ANALYZER
========================

This script performs a comprehensive analysis of all files in the codebase:
1. Maps all file paths and their relative positions
2. Analyzes all import statements
3. Compares import paths to actual file locations
4. Identifies path mismatches and import errors
"""

import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Set
import json

class PathImportAnalyzer:
    """Analyzes file paths and import statements for path mismatches"""
    
    def __init__(self, root_dir: str):
        self.root_dir = Path(root_dir)
        self.file_paths = {}
        self.import_statements = {}
        self.path_mismatches = []
        self.duplicate_files = []
        
    def scan_all_files(self) -> Dict[str, str]:
        """Scan all files in the directory and map their paths"""
        print("🔍 Scanning all files in the codebase...")
        
        all_files = {}
        
        # Scan Python files
        for py_file in self.root_dir.rglob("*.py"):
            relative_path = py_file.relative_to(self.root_dir)
            absolute_path = str(py_file.absolute())
            
            # Store both relative and absolute paths
            all_files[str(relative_path)] = {
                "absolute_path": absolute_path,
                "relative_path": str(relative_path),
                "parent_dir": str(relative_path.parent),
                "filename": relative_path.name,
                "is_python": True
            }
            
        # Scan other important file types
        for ext in ["*.md", "*.txt", "*.yaml", "*.yml", "*.json", "*.xml", "*.ts", "*.tsx", "*.js", "*.jsx"]:
            for file in self.root_dir.rglob(ext):
                relative_path = file.relative_to(self.root_dir)
                absolute_path = str(file.absolute())
                
                all_files[str(relative_path)] = {
                    "absolute_path": absolute_path,
                    "relative_path": str(relative_path),
                    "parent_dir": str(relative_path.parent),
                    "filename": relative_path.name,
                    "is_python": False
                }
        
        self.file_paths = all_files
        print(f"✅ Found {len(all_files)} files")
        return all_files
    
    def analyze_imports(self) -> Dict[str, List[str]]:
        """Analyze all import statements in Python files"""
        print("📥 Analyzing import statements...")
        
        imports_by_file = {}
        
        for file_path, file_info in self.file_paths.items():
            if not file_info["is_python"]:
                continue
                
            try:
                with open(file_info["absolute_path"], 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Find all import statements
                imports = self._extract_imports(content)
                if imports:
                    imports_by_file[file_path] = imports
                    
            except Exception as e:
                print(f"⚠️ Error reading {file_path}: {e}")
                
        self.import_statements = imports_by_file
        print(f"✅ Analyzed imports in {len(imports_by_file)} Python files")
        return imports_by_file
    
    def _extract_imports(self, content: str) -> List[str]:
        """Extract all import statements from file content"""
        imports = []
        
        # Match various import patterns
        import_patterns = [
            r'^from\s+([a-zA-Z_][a-zA-Z0-9_.]*)\s+import\s+.*$',  # from x import y
            r'^import\s+([a-zA-Z_][a-zA-Z0-9_.]*).*$',            # import x
            r'^from\s+([a-zA-Z_][a-zA-Z0-9_.]*)\s+import\s*\*$',  # from x import *
        ]
        
        lines = content.split('\n')
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            
            # Skip comments and empty lines
            if not line or line.startswith('#'):
                continue
                
            for pattern in import_patterns:
                match = re.match(pattern, line)
                if match:
                    import_path = match.group(1)
                    imports.append({
                        "line": line_num,
                        "statement": line,
                        "import_path": import_path,
                        "full_line": line
                    })
                    break
        
        return imports
    
    def find_path_mismatches(self) -> List[Dict]:
        """Find mismatches between import paths and actual file locations"""
        print("🔍 Finding path mismatches...")
        
        mismatches = []
        
        for file_path, imports in self.import_statements.items():
            file_info = self.file_paths[file_path]
            file_dir = file_info["parent_dir"]
            
            for import_info in imports:
                import_path = import_info["import_path"]
                
                # Check if this is a relative import
                if import_path.startswith('.'):
                    # Handle relative imports
                    resolved_path = self._resolve_relative_import(import_path, file_dir)
                    if resolved_path and resolved_path not in self.file_paths:
                        mismatches.append({
                            "file": file_path,
                            "line": import_info["line"],
                            "import_statement": import_info["statement"],
                            "import_path": import_path,
                            "resolved_path": resolved_path,
                            "issue": "Relative import path not found",
                            "type": "relative_import_not_found"
                        })
                else:
                    # Check absolute imports
                    if not self._is_valid_import_path(import_path):
                        mismatches.append({
                            "file": file_path,
                            "line": import_info["line"],
                            "import_statement": import_info["statement"],
                            "import_path": import_path,
                            "issue": "Absolute import path not found",
                            "type": "absolute_import_not_found"
                        })
        
        self.path_mismatches = mismatches
        print(f"✅ Found {len(mismatches)} path mismatches")
        return mismatches
    
    def _resolve_relative_import(self, import_path: str, current_dir: str) -> str:
        """Resolve a relative import path to an absolute path"""
        if not import_path.startswith('.'):
            return None
            
        # Count dots to determine relative level
        dot_count = 0
        for char in import_path:
            if char == '.':
                dot_count += 1
            else:
                break
                
        # Remove dots and get the actual module path
        module_path = import_path[dot_count:]
        
        # Navigate up directories
        current_parts = current_dir.split('/')
        if dot_count > len(current_parts):
            return None  # Too many dots
            
        # Go up the specified number of directories
        parent_dir = '/'.join(current_parts[:-dot_count + 1])
        
        # Construct the full path
        if module_path:
            full_path = f"{parent_dir}/{module_path}"
        else:
            full_path = parent_dir
            
        return full_path
    
    def _is_valid_import_path(self, import_path: str) -> bool:
        """Check if an absolute import path is valid"""
        # Check if it's a standard library module
        if import_path in ['os', 'sys', 'json', 're', 'pathlib', 'typing', 'asyncio', 'logging', 'datetime']:
            return True
            
        # Check if it's a third-party package (common ones)
        third_party_packages = ['uvicorn', 'fastapi', 'httpx', 'openai', 'langchain']
        if import_path.split('.')[0] in third_party_packages:
            return True
            
        # Check if it's a local module
        if import_path in self.file_paths:
            return True
            
        # Check if it's a local module with .py extension
        if f"{import_path}.py" in self.file_paths:
            return True
            
        # Check if it's a directory with __init__.py
        if f"{import_path}/__init__.py" in self.file_paths:
            return True
            
        return False
    
    def find_duplicate_files(self) -> List[Dict]:
        """Find duplicate files with different paths"""
        print("🔍 Finding duplicate files...")
        
        duplicates = []
        filename_map = {}
        
        for file_path, file_info in self.file_paths.items():
            filename = file_info["filename"]
            
            if filename not in filename_map:
                filename_map[filename] = []
            
            filename_map[filename].append(file_path)
        
        # Find files with multiple paths
        for filename, paths in filename_map.items():
            if len(paths) > 1:
                duplicates.append({
                    "filename": filename,
                    "paths": paths,
                    "count": len(paths)
                })
        
        self.duplicate_files = duplicates
        print(f"✅ Found {len(duplicates)} duplicate files")
        return duplicates
    
    def generate_report(self) -> Dict:
        """Generate a comprehensive analysis report"""
        print("📊 Generating analysis report...")
        
        report = {
            "summary": {
                "total_files": len(self.file_paths),
                "python_files": len([f for f in self.file_paths.values() if f["is_python"]]),
                "total_imports": sum(len(imports) for imports in self.import_statements.values()),
                "path_mismatches": len(self.path_mismatches),
                "duplicate_files": len(self.duplicate_files)
            },
            "file_structure": self.file_paths,
            "import_analysis": self.import_statements,
            "path_mismatches": self.path_mismatches,
            "duplicate_files": self.duplicate_files,
            "recommendations": self._generate_recommendations()
        }
        
        return report
    
    def _generate_recommendations(self) -> List[str]:
        """Generate recommendations based on analysis"""
        recommendations = []
        
        if self.path_mismatches:
            recommendations.append("Fix import path mismatches to resolve ModuleNotFoundError")
            
        if self.duplicate_files:
            recommendations.append("Review duplicate files to avoid confusion")
            
        # Check for common import issues
        src_imports = [imp for file_imports in self.import_statements.values() 
                      for imp in file_imports 
                      if imp["import_path"].startswith("src.")]
        
        if src_imports:
            recommendations.append("Remove 'src.' prefixes from imports - they cause path issues")
            
        # Check for missing __init__.py files
        python_dirs = set()
        for file_path, file_info in self.file_paths.items():
            if file_info["is_python"]:
                python_dirs.add(file_info["parent_dir"])
        
        missing_init_files = []
        for dir_path in python_dirs:
            if dir_path != "." and f"{dir_path}/__init__.py" not in self.file_paths:
                missing_init_files.append(dir_path)
        
        if missing_init_files:
            recommendations.append(f"Add __init__.py files to directories: {missing_init_files}")
        
        return recommendations
    
    def save_report(self, report: Dict, filename: str = "path_import_analysis.json"):
        """Save the analysis report to a JSON file"""
        report_file = self.root_dir / filename
        
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2, default=str)
            
        print(f"💾 Report saved to: {report_file}")
        return str(report_file)
    
    def print_summary(self, report: Dict):
        """Print a summary of the analysis"""
        print("\n" + "=" * 80)
        print("📊 PATH AND IMPORT ANALYSIS SUMMARY")
        print("=" * 80)
        
        summary = report["summary"]
        print(f"📁 Total Files: {summary['total_files']}")
        print(f"🐍 Python Files: {summary['python_files']}")
        print(f"📥 Total Imports: {summary['total_imports']}")
        print(f"❌ Path Mismatches: {summary['path_mismatches']}")
        print(f"🔄 Duplicate Files: {summary['duplicate_files']}")
        
        if self.path_mismatches:
            print(f"\n❌ PATH MISMATCHES FOUND:")
            for mismatch in self.path_mismatches[:10]:  # Show first 10
                print(f"   • {mismatch['file']}:{mismatch['line']} - {mismatch['issue']}")
                print(f"     Import: {mismatch['import_statement']}")
            if len(self.path_mismatches) > 10:
                print(f"     ... and {len(self.path_mismatches) - 10} more")
        
        if self.duplicate_files:
            print(f"\n🔄 DUPLICATE FILES FOUND:")
            for dup in self.duplicate_files[:5]:  # Show first 5
                print(f"   • {dup['filename']} appears in {dup['count']} locations:")
                for path in dup['paths']:
                    print(f"     - {path}")
            if len(self.duplicate_files) > 5:
                print(f"     ... and {len(self.duplicate_files) - 5} more")
        
        if report["recommendations"]:
            print(f"\n💡 RECOMMENDATIONS:")
            for rec in report["recommendations"]:
                print(f"   • {rec}")
        
        print("\n" + "=" * 80)

def main():
    """Main analysis function"""
    root_dir = "/Users/Mariam/agentic-native-drafting/agentic_native_drafting"
    
    print("🔍 AGENTIC NATIVE DRAFTING - PATH AND IMPORT ANALYZER")
    print("=" * 80)
    print(f"Analyzing: {root_dir}")
    print()
    
    # Initialize analyzer
    analyzer = PathImportAnalyzer(root_dir)
    
    try:
        # Perform analysis
        analyzer.scan_all_files()
        analyzer.analyze_imports()
        analyzer.find_path_mismatches()
        analyzer.find_duplicate_files()
        
        # Generate and save report
        report = analyzer.generate_report()
        report_file = analyzer.save_report(report)
        
        # Print summary
        analyzer.print_summary(report)
        
        print(f"\n🎯 Analysis completed! Check {report_file} for detailed results.")
        
    except Exception as e:
        print(f"💥 Error during analysis: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
