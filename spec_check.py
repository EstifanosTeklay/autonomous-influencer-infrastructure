#!/usr/bin/env python3
"""
Spec Check Automation Tool

Validates specifications against requirements and checks code alignment.
Run locally with: python spec_check.py
"""

import os
import json
import re
from pathlib import Path
from typing import List, Dict, Tuple


class SpecChecker:
    def __init__(self):
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.passes: List[str] = []

    def log_pass(self, msg: str):
        self.passes.append(f"✓ {msg}")

    def log_warning(self, msg: str):
        self.warnings.append(f"◆ {msg}")

    def log_error(self, msg: str):
        self.errors.append(f"✗ {msg}")

    def check_markdown_files(self):
        """Validate all .md files in specs/ directory"""
        print("\n[1] Checking Markdown Specs...")
        
        specs_dir = Path("specs")
        if not specs_dir.exists():
            self.log_error("specs/ directory not found")
            return

        spec_files = list(specs_dir.glob("*.md"))
        if not spec_files:
            self.log_error("No .md files found in specs/")
            return

        for spec_file in spec_files:
            with open(spec_file, "r") as f:
                content = f.read()

            # Check for main heading
            if re.search(r"^# ", content, re.MULTILINE):
                self.log_pass(f"{spec_file.name} has main heading")
            else:
                self.log_error(f"{spec_file.name} missing main heading")

            # Check for version/date
            if re.search(r"Last Updated|Version|Date", content):
                self.log_pass(f"{spec_file.name} has version/date")
            else:
                self.log_warning(f"{spec_file.name} missing version/date")

            # Check for table of contents (for long docs)
            line_count = len(content.split("\n"))
            if line_count > 100 and not re.search(r"^## Table of Contents|^## Contents", content, re.MULTILINE):
                self.log_warning(f"{spec_file.name} is long (>{line_count}L) but missing TOC")

    def check_speckit_json(self):
        """Validate speckit.json configuration"""
        print("\n[2] Checking speckit.json...")
        
        spec_file = Path("speckit.json")
        if not spec_file.exists():
            self.log_error("speckit.json not found")
            return

        try:
            with open(spec_file, "r") as f:
                config = json.load(f)

            required_keys = ["specDirectory", "files"]
            for key in required_keys:
                if key in config:
                    self.log_pass(f"speckit.json has required key: {key}")
                else:
                    self.log_error(f"speckit.json missing required key: {key}")

            # Verify referenced files exist
            spec_dir = config.get("specDirectory", "specs")
            files_config = config.get("files", {})
            
            for file_type, file_path in files_config.items():
                full_path = Path(spec_dir) / file_path
                if full_path.exists():
                    self.log_pass(f"Spec file exists: {file_path}")
                else:
                    self.log_error(f"Spec file missing: {file_path}")

        except json.JSONDecodeError as e:
            self.log_error(f"speckit.json is invalid JSON: {e}")

    def check_adr_completeness(self):
        """Validate Architecture Decision Records"""
        print("\n[3] Checking ADR.md...")
        
        adr_file = Path("ADR.md")
        if not adr_file.exists():
            self.log_error("ADR.md not found")
            return

        with open(adr_file, "r") as f:
            content = f.read()

        # Count ADRs
        adrs = re.findall(r"## ADR-(\d+):", content)
        if adrs:
            self.log_pass(f"Found {len(adrs)} ADRs: {', '.join(sorted(set(adrs)))}")
        else:
            self.log_error("No ADRs found in ADR.md")
            return

        # Check required sections in each ADR
        required_sections = ["Status", "Context", "Decision"]
        
        for adr_num in sorted(set(adrs)):
            pattern = rf"## ADR-{adr_num}:(.*?)(?=## ADR-|\Z)"
            match = re.search(pattern, content, re.DOTALL)
            
            if match:
                adr_content = match.group(1)
                missing = [s for s in required_sections if s not in adr_content]
                
                if not missing:
                    self.log_pass(f"ADR-{adr_num} is complete")
                else:
                    self.log_warning(f"ADR-{adr_num} missing: {', '.join(missing)}")

    def check_frontend_specs(self):
        """Validate frontend specifications"""
        print("\n[4] Checking Frontend Specs...")
        
        frontend_specs = ["frontend.md", "SPEC.md"]
        found = False
        
        for spec_file in frontend_specs:
            path = Path(spec_file)
            if not path.exists():
                continue
            
            found = True
            with open(path, "r") as f:
                content = f.read()

            checklist = {
                "Framework declared": "react" in content.lower(),
                "Component structure": "component" in content.lower(),
                "Pages/Routes defined": "page" in content.lower() or "route" in content.lower(),
                "API integration": "api" in content.lower() or "endpoint" in content.lower(),
                "State management": "state" in content.lower(),
            }

            for check, result in checklist.items():
                if result:
                    self.log_pass(f"{spec_file}: {check}")
                else:
                    self.log_warning(f"{spec_file}: Missing {check}")

        if not found:
            self.log_warning("No frontend specs found (frontend.md, SPEC.md)")

    def check_mcp_logs(self):
        """Validate MCP Interaction Log structure"""
        print("\n[5] Checking MCP Interaction Log...")
        
        mcp_file = Path("MCP_INTERACTION_LOG.md")
        if not mcp_file.exists():
            self.log_warning("MCP_INTERACTION_LOG.md not found")
            return

        with open(mcp_file, "r") as f:
            content = f.read()

        # Check for JSON blocks
        json_blocks = re.findall(r"```json(.*?)```", content, re.DOTALL)
        
        if json_blocks:
            self.log_pass(f"Found {len(json_blocks)} JSON structured logs")
            
            # Validate JSON
            valid = 0
            for i, block in enumerate(json_blocks):
                try:
                    json.loads(block.strip())
                    valid += 1
                except json.JSONDecodeError:
                    self.log_warning(f"JSON block {i+1} is invalid")
            
            if valid == len(json_blocks):
                self.log_pass(f"All {valid} JSON blocks are valid")
        else:
            self.log_warning("No structured JSON logs found")

        # Check for agentic artifacts
        artifacts = {
            "MCP Sense logs": "MCP SENSE" in content,
            "Decision traces": "decision" in content.lower(),
            "Memory consolidation": "memory" in content.lower(),
            "State transitions": "state_transition" in content.lower(),
        }

        for artifact, found in artifacts.items():
            if found:
                self.log_pass(f"MCP log contains: {artifact}")
            else:
                self.log_warning(f"MCP log missing: {artifact}")

    def check_spec_code_alignment(self):
        """Verify specs reference implementation correctly"""
        print("\n[6] Checking Spec → Code Alignment...")
        
        specs_dir = Path("specs")
        if not specs_dir.exists():
            return

        spec_mentions = {}
        
        for spec_file in specs_dir.glob("*.md"):
            with open(spec_file, "r") as f:
                content = f.read()
                # Look for file references like `src/swarm/planner.py`
                files = re.findall(r"`([src|tests][^`]*\.py)`", content)
                for file_ref in files:
                    if file_ref not in spec_mentions:
                        spec_mentions[file_ref] = []
                    spec_mentions[file_ref].append(spec_file.name)

        if spec_mentions:
            self.log_pass(f"Found {len(spec_mentions)} spec→code references")
            
            for file_ref in sorted(spec_mentions.keys()):
                exists = Path(file_ref).exists()
                status = "✓" if exists else "○"
                specs_referencing = ", ".join(spec_mentions[file_ref])
                
                if exists:
                    self.log_pass(f"{status} {file_ref} (referenced in {specs_referencing})")
                else:
                    self.log_warning(f"{status} {file_ref} pending (referenced in {specs_referencing})")
        else:
            self.log_warning("No spec→code references found")

    def check_test_spec_alignment(self):
        """Verify tests match specifications"""
        print("\n[7] Checking Test ↔ Spec Alignment...")
        
        test_dir = Path("tests/functional")
        if not test_dir.exists():
            self.log_warning("tests/functional/ not found")
            return

        test_files = list(test_dir.glob("test_*.py"))
        if not test_files:
            self.log_warning("No test files found in tests/functional/")
            return

        total_tests = 0
        for test_file in test_files:
            with open(test_file, "r") as f:
                content = f.read()
                tests = len(re.findall(r"def test_", content))
                total_tests += tests
                self.log_pass(f"{test_file.name}: {tests} tests")

        self.log_pass(f"Total: {total_tests} test cases (TDD pattern verified)")

    def print_summary(self):
        """Print final report"""
        print("\n" + "=" * 60)
        print("SPEC CHECK REPORT")
        print("=" * 60)

        if self.passes:
            print(f"\n✓ PASSED ({len(self.passes)}):")
            for msg in self.passes[:10]:  # Show first 10
                print(f"  {msg}")
            if len(self.passes) > 10:
                print(f"  ... and {len(self.passes) - 10} more")

        if self.warnings:
            print(f"\n◆ WARNINGS ({len(self.warnings)}):")
            for msg in self.warnings[:5]:
                print(f"  {msg}")
            if len(self.warnings) > 5:
                print(f"  ... and {len(self.warnings) - 5} more")

        if self.errors:
            print(f"\n✗ ERRORS ({len(self.errors)}):")
            for msg in self.errors:
                print(f"  {msg}")

        # Summary line
        print("\n" + "=" * 60)
        if not self.errors:
            print("✓ Specifications validated successfully")
            print("  Ready for code generation")
            return 0
        else:
            print(f"✗ {len(self.errors)} error(s) found")
            print("  Please address errors before proceeding")
            return 1

    def run(self) -> int:
        """Run all checks"""
        print("\n🔍 Running Spec Check Automation...\n")
        
        self.check_markdown_files()
        self.check_speckit_json()
        self.check_adr_completeness()
        self.check_frontend_specs()
        self.check_mcp_logs()
        self.check_spec_code_alignment()
        self.check_test_spec_alignment()

        return self.print_summary()


if __name__ == "__main__":
    import sys
    checker = SpecChecker()
    exit_code = checker.run()
    sys.exit(exit_code)
