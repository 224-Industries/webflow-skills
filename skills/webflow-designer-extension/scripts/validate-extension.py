#!/usr/bin/env python3
"""
Validate Webflow Designer Extension project structure.
Usage: python validate-extension.py [path]
"""

import sys
import os
import json
from pathlib import Path


def validate_extension(project_path: str) -> tuple[bool, list[str]]:
    """Validate a Webflow Designer Extension project structure."""
    path = Path(project_path)
    errors = []
    warnings = []
    
    # Check project directory exists
    if not path.exists():
        return False, [f"Project path does not exist: {project_path}"]
    
    if not path.is_dir():
        return False, [f"Path is not a directory: {project_path}"]
    
    # Required files
    required_files = [
        ("webflow.json", "Extension configuration file"),
        ("package.json", "Node.js package configuration"),
        ("public/index.html", "Entry point HTML file"),
    ]
    
    for file_path, description in required_files:
        if not (path / file_path).exists():
            errors.append(f"Missing required file: {file_path} ({description})")
    
    # Validate webflow.json
    webflow_json = path / "webflow.json"
    if webflow_json.exists():
        try:
            with open(webflow_json, 'r') as f:
                config = json.load(f)
            
            # Check required fields
            if 'name' not in config:
                errors.append("webflow.json: Missing 'name' field")
            if 'publicDir' not in config:
                warnings.append("webflow.json: Missing 'publicDir' field (defaults to 'public')")
        except json.JSONDecodeError as e:
            errors.append(f"webflow.json: Invalid JSON - {e}")
    
    # Validate package.json
    package_json = path / "package.json"
    if package_json.exists():
        try:
            with open(package_json, 'r') as f:
                pkg = json.load(f)
            
            # Check for recommended scripts
            scripts = pkg.get('scripts', {})
            if 'dev' not in scripts:
                warnings.append("package.json: Missing 'dev' script (recommended)")
            if 'build' not in scripts:
                warnings.append("package.json: Missing 'build' script (recommended)")
            
            # Check for type definitions
            dev_deps = pkg.get('devDependencies', {})
            if '@webflow/designer-extension-typings' not in dev_deps:
                warnings.append("Missing @webflow/designer-extension-typings in devDependencies")
        except json.JSONDecodeError as e:
            errors.append(f"package.json: Invalid JSON - {e}")
    
    # Check public directory structure
    public_dir = path / "public"
    if public_dir.exists():
        index_html = public_dir / "index.html"
        if index_html.exists():
            content = index_html.read_text()
            if '<script' not in content:
                warnings.append("public/index.html: No script tags found")
    
    # Check for source directory
    src_dir = path / "src"
    if not src_dir.exists():
        warnings.append("No 'src' directory found (common for TypeScript projects)")
    
    # Print results
    print(f"\n🔍 Validating: {path.absolute()}\n")
    
    if errors:
        print("❌ ERRORS:")
        for error in errors:
            print(f"   • {error}")
        print()
    
    if warnings:
        print("⚠️  WARNINGS:")
        for warning in warnings:
            print(f"   • {warning}")
        print()
    
    if not errors and not warnings:
        print("✅ All checks passed!")
    elif not errors:
        print("✅ No critical errors found")
    
    return len(errors) == 0, errors + warnings


def main():
    project_path = sys.argv[1] if len(sys.argv) > 1 else "."
    
    success, messages = validate_extension(project_path)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
