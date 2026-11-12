#!/usr/bin/env python3
"""
Bundle linter for earthmover_edfi_bundles.

Validates that an assessment bundle meets structural and convention requirements
before merge. Designed to run in CI (GitHub Actions) or locally.

Usage:
    python lint_bundle.py <path_to_bundle>
    python lint_bundle.py assessments/MAP_Growth

Exit codes:
    0 — all checks passed (warnings may still be present)
    1 — one or more ERROR-level checks failed
"""

import csv
import io
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Optional

import yaml


# ---------------------------------------------------------------------------
# Result types
# ---------------------------------------------------------------------------

class Severity(Enum):
    ERROR = "ERROR"
    WARNING = "WARNING"


@dataclass
class CheckResult:
    rule_id: str
    severity: Severity
    message: str
    passed: bool

    def __str__(self):
        icon = "PASS" if self.passed else self.severity.value
        return f"  [{icon}] {self.rule_id}: {self.message}"


@dataclass
class LintReport:
    bundle_path: str
    results: list[CheckResult] = field(default_factory=list)

    def add(self, rule_id: str, severity: Severity, message: str, passed: bool):
        self.results.append(CheckResult(rule_id, severity, message, passed))

    @property
    def errors(self):
        return [r for r in self.results if not r.passed and r.severity == Severity.ERROR]

    @property
    def warnings(self):
        return [r for r in self.results if not r.passed and r.severity == Severity.WARNING]

    @property
    def passed(self):
        return [r for r in self.results if r.passed]

    @property
    def has_errors(self):
        return len(self.errors) > 0

    def print_report(self):
        print(f"\n{'=' * 60}")
        print(f"  Bundle Lint Report: {self.bundle_path}")
        print(f"{'=' * 60}")

        if self.errors:
            print(f"\n  ERRORS ({len(self.errors)}):")
            for r in self.errors:
                print(f"    {r}")

        if self.warnings:
            print(f"\n  WARNINGS ({len(self.warnings)}):")
            for r in self.warnings:
                print(f"    {r}")

        if self.passed:
            print(f"\n  PASSED ({len(self.passed)}):")
            for r in self.passed:
                print(f"    {r}")

        print(f"\n{'=' * 60}")
        total = len(self.results)
        print(f"  {len(self.passed)}/{total} passed, "
              f"{len(self.errors)} errors, {len(self.warnings)} warnings")
        if self.has_errors:
            print("  RESULT: FAIL")
        else:
            print("  RESULT: PASS")
        print(f"{'=' * 60}\n")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_yaml_safe(path: Path) -> Optional[dict]:
    """Load a YAML file, returning None if it fails."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except Exception:
        return None


def load_earthmover_yaml(path: Path) -> Optional[dict]:
    """Load an earthmover YAML file that may contain Jinja2 and ${} syntax.

    Earthmover configs often contain Jinja2 macros and ${VAR} references that
    break yaml.safe_load. Strategy:
    1. Try standard YAML parsing
    2. Fall back to regex-based field extraction for the fields we need
    """
    result = load_yaml_safe(path)
    if result is not None:
        return result

    # Regex-based extraction of key fields
    try:
        text = path.read_text(encoding="utf-8")
        return _extract_earthmover_fields(text)
    except Exception:
        return None


def _extract_earthmover_fields(text: str) -> dict:
    """Extract key fields from earthmover YAML using regex when YAML parsing fails."""
    result = {}

    # Version
    m = re.search(r'^version:\s*(\d+)', text, re.MULTILINE)
    if m:
        result["version"] = int(m.group(1))

    # Parameter defaults
    param_defaults = {}
    pd_section = re.search(r'parameter_defaults:\s*\n((?:\s+\S.*\n)*)', text)
    if pd_section:
        pd_text = pd_section.group(1)
        for pm in re.finditer(r'(\w+):\s*[\'"]?([^\s\'"\n#]+)', pd_text):
            param_defaults[pm.group(1)] = pm.group(2)
    if param_defaults:
        result.setdefault("config", {})["parameter_defaults"] = param_defaults

    # Transformations — check for input transformation
    input_section = re.search(
        r'transformations:\s*\n\s+input:\s*\n\s+source:\s*(\S+)\s*\n\s+operations:\s*\[\s*\]',
        text
    )
    if input_section:
        result.setdefault("transformations", {})["input"] = {
            "source": input_section.group(1),
            "operations": []
        }
    else:
        # Check if input exists but with different structure
        input_basic = re.search(
            r'transformations:\s*\n\s+input:\s*\n\s+source:\s*(\S+)',
            text
        )
        if input_basic:
            result.setdefault("transformations", {})["input"] = {
                "source": input_basic.group(1),
                "operations": "UNKNOWN"  # can't parse further
            }

    # Sources — extract file references
    sources = {}
    for m in re.finditer(r'(\w+):\s*\n\s+file:\s*(\S+)', text):
        sources[m.group(1)] = {"file": m.group(2)}
    if sources:
        result["sources"] = sources

    # Destinations — extract template references
    destinations = {}
    for m in re.finditer(r'(\w+):\s*\n\s+source:.*\n\s+template:\s*(\S+)', text):
        destinations[m.group(1)] = {"template": m.group(2)}
    if destinations:
        result["destinations"] = destinations

    return result if result else None


def read_csv_headers(path: Path) -> Optional[list[str]]:
    """Read just the header row of a CSV file."""
    try:
        with open(path, "r", encoding="utf-8-sig", newline="") as f:
            reader = csv.reader(f)
            return next(reader)
    except Exception:
        return None


def count_csv_rows(path: Path) -> Optional[int]:
    """Count data rows in a CSV (excluding header)."""
    try:
        with open(path, "r", encoding="utf-8-sig", newline="") as f:
            reader = csv.reader(f)
            next(reader)  # skip header
            return sum(1 for _ in reader)
    except Exception:
        return None


def read_csv_column(path: Path, column: str) -> Optional[list[str]]:
    """Read all values from a specific column in a CSV."""
    try:
        with open(path, "r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            return [row[column] for row in reader if column in row]
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Section 1: File Structure
# ---------------------------------------------------------------------------

def check_file_structure(bundle: Path, report: LintReport):
    """Rules 1.1 - 1.15: Check required files and directories."""

    # 1.1 - earthmover.yaml
    report.add("1.1", Severity.ERROR,
               "earthmover.yaml exists",
               (bundle / "earthmover.yaml").is_file())

    # 1.2 - lightbeam.yaml
    report.add("1.2", Severity.ERROR,
               "lightbeam.yaml exists",
               (bundle / "lightbeam.yaml").is_file())

    # 1.3 - README.md
    report.add("1.3", Severity.ERROR,
               "README.md exists",
               (bundle / "README.md").is_file())

    # 1.4 - _metadata.yaml
    report.add("1.4", Severity.ERROR,
               "_metadata.yaml exists",
               (bundle / "_metadata.yaml").is_file())

    # 1.5 - seeds/ with at least one CSV
    seeds_dir = bundle / "seeds"
    has_seeds = seeds_dir.is_dir() and any(seeds_dir.glob("*.csv"))
    report.add("1.5", Severity.ERROR,
               "seeds/ directory exists with at least one .csv file",
               has_seeds)

    # 1.6 - templates/ with at least one .jsont
    templates_dir = bundle / "templates"
    has_templates = templates_dir.is_dir() and any(templates_dir.glob("*.jsont"))
    report.add("1.6", Severity.ERROR,
               "templates/ directory exists with at least one .jsont file",
               has_templates)

    # 1.7 - data/ with at least one sample file
    data_dir = bundle / "data"
    has_data = data_dir.is_dir() and any(
        f for f in data_dir.iterdir()
        if f.name != ".gitkeep" and not f.name.startswith(".")
    )
    report.add("1.7", Severity.ERROR,
               "data/ directory exists with at least one sample file",
               has_data)

    # 1.8 - Only one earthmover*.yaml
    em_yamls = list(bundle.glob("earthmover*.yaml"))
    # Exclude compiled files
    em_yamls = [f for f in em_yamls if "_compiled" not in f.name]
    report.add("1.8", Severity.WARNING,
               f"Single earthmover config file (found {len(em_yamls)})",
               len(em_yamls) <= 1)

    # 1.9 - Only one lightbeam*.yaml
    lb_yamls = list(bundle.glob("lightbeam*.yaml"))
    report.add("1.9", Severity.WARNING,
               f"Single lightbeam config file (found {len(lb_yamls)})",
               len(lb_yamls) <= 1)

    # 1.10 - .gitignore
    report.add("1.10", Severity.WARNING,
               ".gitignore exists",
               (bundle / ".gitignore").is_file())

    # 1.11 - No .jsonl output files
    jsonl_files = list(bundle.rglob("*.jsonl"))
    report.add("1.11", Severity.ERROR,
               f"No .jsonl output files committed (found {len(jsonl_files)})",
               len(jsonl_files) == 0)

    # 1.12 - No runs.csv / state files
    runs_files = list(bundle.glob("runs*.csv"))
    report.add("1.12", Severity.ERROR,
               f"No runs.csv state files committed (found {len(runs_files)})",
               len(runs_files) == 0)

    # 1.13 - No compiled yaml
    compiled_files = list(bundle.glob("*_compiled.yaml"))
    report.add("1.13", Severity.ERROR,
               f"No *_compiled.yaml files committed (found {len(compiled_files)})",
               len(compiled_files) == 0)

    # 1.14 - No bundle_metadata.json
    report.add("1.14", Severity.WARNING,
               "No bundle_metadata.json (wrong format; use _metadata.yaml)",
               not (bundle / "bundle_metadata.json").is_file())


# ---------------------------------------------------------------------------
# Section 2: Sample Data
# ---------------------------------------------------------------------------

def check_sample_data(bundle: Path, report: LintReport):
    """Rules 2.1 - 2.3: Check sample data files."""
    data_dir = bundle / "data"

    if not data_dir.is_dir():
        report.add("2.1", Severity.ERROR, "data/ directory missing", False)
        return

    sample_files = [
        f for f in data_dir.iterdir()
        if f.is_file() and f.name != ".gitkeep" and not f.name.startswith(".")
    ]

    # 2.1 - Sample files exist
    report.add("2.1", Severity.ERROR,
               f"Sample data file(s) exist ({len(sample_files)} found)",
               len(sample_files) > 0)

    # 2.2 - Row count check (5-10 rows recommended)
    for sf in sample_files:
        if sf.suffix.lower() in ('.csv', '.tsv', '.txt'):
            row_count = count_csv_rows(sf)
            if row_count is not None:
                ok = row_count <= 15  # allow some slack above 10
                report.add("2.2", Severity.WARNING,
                           f"Sample file {sf.name} has {row_count} data rows (target: 5-10)",
                           ok)

    # 2.3 - Heuristic check for fake-looking data
    for sf in sample_files:
        if sf.suffix.lower() in ('.csv', '.tsv'):
            try:
                with open(sf, "r", encoding="utf-8") as f:
                    content = f.read(4096).lower()  # first 4KB
                has_fake_markers = any(
                    marker in content
                    for marker in ["fake", "test_", "sample", "anonymous", "anonymized",
                                   "xxx", "placeholder", "demo"]
                )
                report.add("2.3", Severity.WARNING,
                           f"Sample file {sf.name} appears to use fake/anonymized identifiers",
                           has_fake_markers)
            except Exception:
                pass


# ---------------------------------------------------------------------------
# Section 3: earthmover.yaml Configuration
# ---------------------------------------------------------------------------

def check_earthmover_yaml(bundle: Path, report: LintReport) -> Optional[dict]:
    """Rules 3.1 - 3.9: Validate earthmover.yaml configuration."""
    em_path = bundle / "earthmover.yaml"

    if not em_path.is_file():
        return None

    em = load_earthmover_yaml(em_path)
    if em is None:
        report.add("3.0", Severity.ERROR, "earthmover.yaml could not be parsed", False)
        return None

    # 3.1 - Version 2
    report.add("3.1", Severity.ERROR,
               "earthmover.yaml has version: 2",
               em.get("version") == 2)

    # Get parameter_defaults
    config = em.get("config", {}) or {}
    param_defaults = config.get("parameter_defaults", {}) or {}

    # 3.2 - STUDENT_ID_NAME
    sid = param_defaults.get("STUDENT_ID_NAME", "")
    # Strip quotes that may be in the YAML string
    sid_clean = str(sid).strip("'\"")
    report.add("3.2", Severity.ERROR,
               "STUDENT_ID_NAME defaults to 'edFi_studentUniqueID'",
               sid_clean == "edFi_studentUniqueID")

    # 3.3 - DESCRIPTOR_NAMESPACE
    dns = param_defaults.get("DESCRIPTOR_NAMESPACE", "")
    dns_clean = str(dns).strip("'\"")
    report.add("3.3", Severity.ERROR,
               "DESCRIPTOR_NAMESPACE defaults to 'uri://ed-fi.org'",
               dns_clean == "uri://ed-fi.org")

    # 3.4 - Empty input transformation
    transformations = em.get("transformations", {}) or {}
    input_transform = transformations.get("input", {}) or {}
    has_correct_source = input_transform.get("source") == "$sources.input"
    has_empty_ops = input_transform.get("operations") == [] or input_transform.get("operations") is None
    # Some bundles use operations: [] and some omit it; both are acceptable if source is correct
    report.add("3.4", Severity.ERROR,
               "First transformation is empty input (source: $sources.input, operations: [])",
               has_correct_source and (input_transform.get("operations", []) == []))

    # 3.5 - Relative paths (no $BUNDLE_DIR or absolute paths)
    em_text = em_path.read_text(encoding="utf-8")
    has_bundle_dir = "$BUNDLE_DIR" in em_text or "${BUNDLE_DIR}" in em_text
    # Check for absolute paths in file: references (but allow parameter references like ${INPUT_FILE})
    abs_path_pattern = re.compile(r'file:\s*/[a-zA-Z]')
    has_abs_paths = bool(abs_path_pattern.search(em_text))
    report.add("3.5", Severity.ERROR,
               "All paths are relative (no $BUNDLE_DIR or absolute paths)",
               not has_bundle_dir and not has_abs_paths)

    # 3.6 - POSSIBLE_STUDENT_ID_COLUMNS
    report.add("3.6", Severity.WARNING,
               "POSSIBLE_STUDENT_ID_COLUMNS is configured",
               "POSSIBLE_STUDENT_ID_COLUMNS" in param_defaults)

    # 3.7 - All referenced seed files exist
    sources = em.get("sources", {}) or {}
    missing_seeds = []
    for source_name, source_def in sources.items():
        if isinstance(source_def, dict):
            file_ref = source_def.get("file", "")
            if isinstance(file_ref, str) and file_ref.startswith("./seeds/"):
                seed_path = bundle / file_ref.lstrip("./")
                if not seed_path.is_file():
                    missing_seeds.append(file_ref)
    if missing_seeds:
        report.add("3.7", Severity.ERROR,
                   f"Referenced seed files missing: {', '.join(missing_seeds)}",
                   False)
    else:
        report.add("3.7", Severity.ERROR,
                   "All referenced seed files exist on disk",
                   True)

    # 3.8 - All referenced template files exist
    destinations = em.get("destinations", {}) or {}
    missing_templates = []
    for dest_name, dest_def in destinations.items():
        if isinstance(dest_def, dict):
            tmpl_ref = dest_def.get("template", "")
            if isinstance(tmpl_ref, str) and tmpl_ref.startswith("./templates/"):
                tmpl_path = bundle / tmpl_ref.lstrip("./")
                if not tmpl_path.is_file():
                    missing_templates.append(tmpl_ref)
    if missing_templates:
        report.add("3.8", Severity.ERROR,
                   f"Referenced template files missing: {', '.join(missing_templates)}",
                   False)
    else:
        report.add("3.8", Severity.ERROR,
                   "All referenced template files exist on disk",
                   True)

    return em


# ---------------------------------------------------------------------------
# Section 4: lightbeam.yaml Configuration
# ---------------------------------------------------------------------------

def check_lightbeam_yaml(bundle: Path, report: LintReport):
    """Rules 4.1 - 4.3: Validate lightbeam.yaml parameterization."""
    lb_path = bundle / "lightbeam.yaml"

    if not lb_path.is_file():
        return

    lb_text = lb_path.read_text(encoding="utf-8")
    lb = load_yaml_safe(lb_path)

    if lb is None:
        report.add("4.0", Severity.ERROR, "lightbeam.yaml is valid YAML", False)
        return

    # 4.1 - data_dir parameterized
    data_dir = str(lb.get("data_dir", ""))
    report.add("4.1", Severity.ERROR,
               "data_dir is parameterized (not hardcoded)",
               "${" in data_dir or data_dir == "")

    # 4.2 - state_dir parameterized if present
    if "state_dir" in lb:
        state_dir = str(lb.get("state_dir", ""))
        report.add("4.2", Severity.ERROR,
                   "state_dir is parameterized (not hardcoded)",
                   "${" in state_dir)

    # 4.3 - No hardcoded credentials
    has_hardcoded_creds = False
    edfi_api = lb.get("edfi_api", {}) or {}
    for key in ("client_id", "client_secret"):
        val = str(edfi_api.get(key, ""))
        if val and "${" not in val:
            has_hardcoded_creds = True
    report.add("4.3", Severity.ERROR,
               "API credentials are parameterized (no hardcoded secrets)",
               not has_hardcoded_creds)


# ---------------------------------------------------------------------------
# Section 5: _metadata.yaml
# ---------------------------------------------------------------------------

def check_metadata_yaml(bundle: Path, report: LintReport) -> Optional[dict]:
    """Rules 5.1 - 5.10: Validate _metadata.yaml."""
    meta_path = bundle / "_metadata.yaml"

    if not meta_path.is_file():
        return None

    meta = load_yaml_safe(meta_path)
    if meta is None:
        report.add("5.0", Severity.ERROR, "_metadata.yaml is valid YAML", False)
        return None

    # 5.1 - display_name
    report.add("5.1", Severity.ERROR,
               "display_name field exists",
               bool(meta.get("display_name")))

    # 5.2 - path field matches actual bundle path
    meta_path_val = meta.get("path", "")
    # The path should be like "assessments/BundleName"
    expected_path = f"assessments/{bundle.name}"
    path_matches = meta_path_val == expected_path
    report.add("5.2", Severity.ERROR,
               f"path field matches bundle location (expected '{expected_path}', got '{meta_path_val}')",
               path_matches)

    # 5.3 - input_files list
    input_files = meta.get("input_files", [])
    report.add("5.3", Severity.ERROR,
               "input_files list exists with at least one entry",
               isinstance(input_files, list) and len(input_files) > 0)

    # 5.4 - Each input_file has required fields
    if isinstance(input_files, list):
        for i, inf in enumerate(input_files):
            if isinstance(inf, dict):
                required_fields = ["env_var", "is_required", "file_type"]
                missing = [f for f in required_fields if f not in inf]
                report.add("5.4", Severity.ERROR,
                           f"input_files[{i}] has required fields ({', '.join(required_fields)})"
                           + (f" — missing: {', '.join(missing)}" if missing else ""),
                           len(missing) == 0)

    # 5.5 - env_vars correspond to earthmover.yaml parameters
    em_path = bundle / "earthmover.yaml"
    if em_path.is_file():
        em = load_yaml_safe(em_path)
        if em and isinstance(input_files, list):
            em_text = em_path.read_text(encoding="utf-8")
            for inf in input_files:
                if isinstance(inf, dict):
                    env_var = inf.get("env_var", "")
                    if env_var:
                        # Check if the env_var appears anywhere in the earthmover config
                        found = env_var in em_text
                        report.add("5.5", Severity.WARNING,
                                   f"input_files env_var '{env_var}' referenced in earthmover.yaml",
                                   found)

    # 5.6 - descriptor_mapping_files exist in seeds/
    desc_files = meta.get("descriptor_mapping_files", [])
    if isinstance(desc_files, list) and len(desc_files) > 0:
        seeds_dir = bundle / "seeds"
        for df in desc_files:
            exists = (seeds_dir / df).is_file()
            report.add("5.6", Severity.ERROR,
                       f"descriptor_mapping_files: seeds/{df} exists",
                       exists)

            # 5.7 - edfi_descriptor column exists
            if exists:
                headers = read_csv_headers(seeds_dir / df)
                has_col = headers is not None and "edfi_descriptor" in headers
                report.add("5.7", Severity.ERROR,
                           f"seeds/{df} contains 'edfi_descriptor' column",
                           has_col)

                # 5.8 - edfi_descriptor values follow URI format
                if has_col:
                    values = read_csv_column(seeds_dir / df, "edfi_descriptor")
                    uri_pattern = re.compile(r'^uri://[^/]+/.+#.+$')
                    if values:
                        bad_values = [v for v in values if not uri_pattern.match(v)]
                        report.add("5.8", Severity.WARNING,
                                   f"seeds/{df} edfi_descriptor values follow URI format"
                                   + (f" — invalid: {bad_values[:3]}" if bad_values else ""),
                                   len(bad_values) == 0)

    # 5.9 - valid_edfi field
    report.add("5.9", Severity.WARNING,
               "valid_edfi field exists",
               "valid_edfi" in meta)

    # 5.10 - report_resources field
    report.add("5.10", Severity.WARNING,
               "report_resources field exists",
               "report_resources" in meta)

    return meta


# ---------------------------------------------------------------------------
# Section 6: Template Files
# ---------------------------------------------------------------------------

def check_templates(bundle: Path, report: LintReport, em: Optional[dict]):
    """Rules 6.1 - 6.5: Validate .jsont template files."""
    templates_dir = bundle / "templates"

    if not templates_dir.is_dir():
        return

    jsont_files = list(templates_dir.glob("*.jsont"))
    if not jsont_files:
        return

    # 6.1 - No hardcoded uri:// in templates
    # We allow ${DESCRIPTOR_NAMESPACE} references and Jinja variable references like {{namespace}}
    uri_pattern = re.compile(r'(?<!\$\{DESCRIPTOR_NAMESPACE\})uri://[^\s"\'}{]+')
    # More precise: find literal uri:// strings that aren't part of a ${DESCRIPTOR_NAMESPACE} expansion
    for tmpl_file in jsont_files:
        content = tmpl_file.read_text(encoding="utf-8")
        # Remove ${DESCRIPTOR_NAMESPACE}/... patterns — these are OK
        cleaned = re.sub(r'\$\{DESCRIPTOR_NAMESPACE\}/[^\s"\']*', '', content)
        # Remove Jinja variable references like {{namespace}}/... — these are OK
        cleaned = re.sub(r'\{\{[^}]+\}\}/[^\s"\']*', '', cleaned)
        # Remove full Jinja expressions like {{edfi_descriptor}} — these are OK
        cleaned = re.sub(r'\{\{[^}]+\}\}', '', cleaned)
        # Now check for remaining hardcoded URIs
        hardcoded = re.findall(r'uri://[^\s"\']+', cleaned)
        if hardcoded:
            report.add("6.1", Severity.WARNING,
                       f"{tmpl_file.name}: hardcoded namespace URIs found: {hardcoded[:3]}",
                       False)
        else:
            report.add("6.1", Severity.WARNING,
                       f"{tmpl_file.name}: no hardcoded namespace URIs",
                       True)

    # 6.2 - resultDatatypeTypeDescriptor uses ${DESCRIPTOR_NAMESPACE}
    for tmpl_file in jsont_files:
        content = tmpl_file.read_text(encoding="utf-8")
        if "resultDatatypeTypeDescriptor" in content or "resultDataTypeDescriptor" in content:
            uses_param = "${DESCRIPTOR_NAMESPACE}" in content
            report.add("6.2", Severity.ERROR,
                       f"{tmpl_file.name}: resultDatatypeTypeDescriptor uses ${{DESCRIPTOR_NAMESPACE}}",
                       uses_param)

    # 6.3 - Heuristic JSON validity check
    # Look for obvious structural issues in templates.
    # NOTE: Most templates use Jinja loop constructs to handle trailing commas,
    # so we only flag trailing commas in sections WITHOUT Jinja loop control.
    for tmpl_file in jsont_files:
        content = tmpl_file.read_text(encoding="utf-8")
        issues = []

        # Only check for trailing commas if the template has NO Jinja loop logic
        # (templates with loops almost always use Jinja for comma control)
        has_jinja_loops = "loop.last" in content or "loop.index" in content
        if not has_jinja_loops:
            stripped = re.sub(r'\{%.*?%\}', '', content, flags=re.DOTALL)
            stripped = re.sub(r'\{\{.*?\}\}', '""', stripped)
            if re.search(r',\s*[\]}]', stripped):
                issues.append("possible trailing comma before } or ]")

        # Check for unclosed braces (rough check)
        stripped_all = re.sub(r'\{[%{].*?[%}]\}', '', content, flags=re.DOTALL)
        open_braces = stripped_all.count('{') - stripped_all.count('}')
        if abs(open_braces) > 1:  # allow 1 off for template wrapper
            issues.append(f"mismatched braces (diff: {open_braces})")

        if issues:
            report.add("6.3", Severity.WARNING,
                       f"{tmpl_file.name}: potential JSON issues: {'; '.join(issues)}",
                       False)

    # 6.4 - Score null-filtering pattern in studentAssessment templates
    sa_templates = [f for f in jsont_files
                    if "studentassessment" in f.name.lower() and "objective" not in f.name.lower()]
    for tmpl_file in sa_templates:
        content = tmpl_file.read_text(encoding="utf-8")
        if "scoreResults" in content or "score_results" in content:
            # Look for the null-filter pattern: checking for none/length before including scores
            has_null_check = ("is not none" in content or "!= ''" in content
                              or "| length" in content or "is not none" in content.lower())
            report.add("6.4", Severity.WARNING,
                       f"{tmpl_file.name}: score results include null/empty filtering",
                       has_null_check)

    # 6.5 - Single shared descriptors.jsont
    if em:
        destinations = em.get("destinations", {}) or {}
        descriptor_templates = set()
        for dest_name, dest_def in destinations.items():
            if isinstance(dest_def, dict) and "descriptor" in dest_name.lower():
                tmpl = dest_def.get("template", "")
                if tmpl:
                    descriptor_templates.add(tmpl)
        if len(descriptor_templates) > 1:
            report.add("6.5", Severity.WARNING,
                       f"Multiple descriptor templates used: {descriptor_templates} (prefer single descriptors.jsont)",
                       False)
        elif len(descriptor_templates) == 1:
            report.add("6.5", Severity.WARNING,
                       "Single shared descriptor template used",
                       True)


# ---------------------------------------------------------------------------
# Section 7: Seed Files
# ---------------------------------------------------------------------------

def check_seed_files(bundle: Path, report: LintReport, em: Optional[dict]):
    """Rules 7.1 - 7.7: Validate seed CSV files."""
    seeds_dir = bundle / "seeds"

    if not seeds_dir.is_dir():
        return

    # 7.1 - assessments.csv exists with required columns
    # Accept common variants: assessmentIdentifier/assessment_identifier, namespace/assessmentNamespace
    assessments_csv = seeds_dir / "assessments.csv"
    assess_id_col = None  # track which variant is used for cross-referencing
    if assessments_csv.is_file():
        headers = read_csv_headers(assessments_csv)
        if headers:
            header_set = set(h.strip() for h in headers)
            has_id = "assessmentIdentifier" in header_set or "assessment_identifier" in header_set
            has_ns = "namespace" in header_set or "assessmentNamespace" in header_set
            if "assessmentIdentifier" in header_set:
                assess_id_col = "assessmentIdentifier"
            elif "assessment_identifier" in header_set:
                assess_id_col = "assessment_identifier"
            missing_parts = []
            if not has_id:
                missing_parts.append("assessmentIdentifier (or assessment_identifier)")
            if not has_ns:
                missing_parts.append("namespace (or assessmentNamespace)")
            report.add("7.1", Severity.ERROR,
                       "assessments.csv contains assessment ID and namespace columns"
                       + (f" — missing: {', '.join(missing_parts)}" if missing_parts else ""),
                       has_id and has_ns)
        else:
            report.add("7.1", Severity.ERROR, "assessments.csv could not be read", False)
    else:
        report.add("7.1", Severity.ERROR, "assessments.csv exists in seeds/", False)

    # 7.2 - Assessment identifiers should not contain vendor names
    known_vendors = [
        "nwea", "collegeboard", "renaissance", "pearson", "ets",
        "act_inc", "curriculum_associates", "houghton", "mcgraw",
        "datarecognition", "measured_progress", "questar"
    ]
    if assessments_csv.is_file() and assess_id_col:
        ids = read_csv_column(assessments_csv, assess_id_col)
        if ids:
            suspicious = []
            for aid in ids:
                aid_lower = aid.lower().replace(" ", "_").replace("-", "_")
                for vendor in known_vendors:
                    if vendor in aid_lower:
                        suspicious.append((aid, vendor))
            if suspicious:
                report.add("7.2", Severity.WARNING,
                           f"Assessment IDs may contain vendor names: {suspicious[:3]}",
                           False)
            else:
                report.add("7.2", Severity.WARNING,
                           "Assessment identifiers do not contain known vendor names",
                           True)

    # 7.4 - Descriptor seed files have standard columns
    descriptor_seeds = list(seeds_dir.glob("*Descriptors.csv"))
    # Only check assessment-specific descriptor seeds (reporting method, performance level)
    for ds in descriptor_seeds:
        name_lower = ds.name.lower()
        # Skip descriptor mapping files (gradeLevelDescriptors, academicSubjectDescriptors, etc.)
        # — those follow a different schema with edfi_descriptor column
        if any(skip in name_lower for skip in ["gradelevel", "academicsubject",
                                                 "assessmentcategory", "language",
                                                 "platformtype"]):
            continue
        headers = read_csv_headers(ds)
        if headers:
            header_set = set(h.strip() for h in headers)
            expected = {"codeValue", "namespace", "description", "shortDescription"}
            missing = expected - header_set
            report.add("7.4", Severity.ERROR,
                       f"{ds.name} has standard descriptor columns (codeValue, namespace, description, shortDescription)"
                       + (f" — missing: {missing}" if missing else ""),
                       len(missing) == 0)

    # 7.5 - Assessment-specific descriptor namespaces should use vendor URI
    for ds in descriptor_seeds:
        name_lower = ds.name.lower()
        if any(skip in name_lower for skip in ["gradelevel", "academicsubject",
                                                 "assessmentcategory", "language",
                                                 "platformtype"]):
            continue
        namespaces = read_csv_column(ds, "namespace")
        if namespaces:
            edfi_ns = [ns for ns in namespaces if "ed-fi.org" in ns]
            if edfi_ns:
                report.add("7.5", Severity.WARNING,
                           f"{ds.name}: assessment-specific descriptors use ed-fi.org namespace "
                           f"(should use vendor namespace): {edfi_ns[:3]}",
                           False)
            else:
                report.add("7.5", Severity.WARNING,
                           f"{ds.name}: uses vendor-specific namespace",
                           True)

    # 7.6 - Non-assessment descriptor seeds should use Ed-Fi namespace
    for ds in descriptor_seeds:
        name_lower = ds.name.lower()
        if not any(check in name_lower for check in ["gradelevel", "academicsubject",
                                                       "assessmentcategory"]):
            continue
        # These files may use edfi_descriptor column format (full URI) or namespace column
        headers = read_csv_headers(ds)
        if headers and "edfi_descriptor" in headers:
            values = read_csv_column(ds, "edfi_descriptor")
            if values:
                non_edfi = [v for v in values if "ed-fi.org" not in v]
                if non_edfi:
                    report.add("7.6", Severity.WARNING,
                               f"{ds.name}: non-assessment descriptors use non-Ed-Fi namespace: {non_edfi[:3]}",
                               False)
                else:
                    report.add("7.6", Severity.WARNING,
                               f"{ds.name}: defaults to Ed-Fi namespace",
                               True)
        elif headers and "namespace" in headers:
            namespaces = read_csv_column(ds, "namespace")
            if namespaces:
                non_edfi = [ns for ns in namespaces if "ed-fi.org" not in ns]
                if non_edfi:
                    report.add("7.6", Severity.WARNING,
                               f"{ds.name}: non-assessment descriptors use non-Ed-Fi namespace: {non_edfi[:3]}",
                               False)
                else:
                    report.add("7.6", Severity.WARNING,
                               f"{ds.name}: defaults to Ed-Fi namespace",
                               True)

    # 7.7 - Consistent assessment identifiers across seed files
    if assessments_csv.is_file() and assess_id_col:
        master_ids = read_csv_column(assessments_csv, assess_id_col)
        if master_ids:
            master_set = set(master_ids)
            for seed_file in seeds_dir.glob("*.csv"):
                if seed_file.name == "assessments.csv":
                    continue
                headers = read_csv_headers(seed_file)
                if headers:
                    # Look for either column name variant
                    id_col = None
                    if "assessmentIdentifier" in headers:
                        id_col = "assessmentIdentifier"
                    elif "assessment_identifier" in headers:
                        id_col = "assessment_identifier"
                    seed_ids = None
                    if id_col:
                        seed_ids = read_csv_column(seed_file, id_col)
                    if seed_ids:
                        seed_set = set(seed_ids)
                        # Check if seed file references IDs not in assessments.csv
                        extra = seed_set - master_set
                        if extra:
                            report.add("7.7", Severity.ERROR,
                                       f"{seed_file.name} references assessment IDs not in assessments.csv: {extra}",
                                       False)

            # Only report once if all consistent
            if not any(r.rule_id == "7.7" and not r.passed for r in report.results):
                report.add("7.7", Severity.ERROR,
                           "Assessment identifiers are consistent across seed files",
                           True)


# ---------------------------------------------------------------------------
# Section 8: README
# ---------------------------------------------------------------------------

def check_readme(bundle: Path, report: LintReport) -> Optional[str]:
    """Rules 8.1 - 8.3: Validate README.md content."""
    readme_path = bundle / "README.md"

    if not readme_path.is_file():
        return None

    content = readme_path.read_text(encoding="utf-8")

    # 8.1 - Contains earthmover run command
    has_em_cmd = "earthmover run" in content
    report.add("8.1", Severity.ERROR,
               "README contains a sample 'earthmover run' command",
               has_em_cmd)

    # 8.2 - Command references data/ sample file
    has_data_ref = "data/" in content or "data\\" in content
    report.add("8.2", Severity.WARNING,
               "README command references a file in data/",
               has_data_ref)

    # 8.3 - Extract and validate JSON params from command
    params_str = None
    # Try to find -p '{...}' or -p "{...}" patterns
    # Match single-quoted or double-quoted JSON blocks after -p
    p_patterns = [
        re.compile(r"-p\s+'(\{.*?\})'", re.DOTALL),
        re.compile(r'-p\s+"(\{.*?\})"', re.DOTALL),
        re.compile(r"-p\s+'(\{.*?\})'\s", re.DOTALL),
    ]
    for pat in p_patterns:
        m = pat.search(content)
        if m:
            params_str = m.group(1)
            break

    if params_str:
        try:
            json.loads(params_str)
            report.add("8.3", Severity.WARNING,
                       "README earthmover command parameters are valid JSON",
                       True)
        except json.JSONDecodeError as e:
            report.add("8.3", Severity.WARNING,
                       f"README earthmover command parameters are not valid JSON: {e}",
                       False)

    return params_str


# ---------------------------------------------------------------------------
# Section 9: Earthmover Compilation
# ---------------------------------------------------------------------------

def check_compilation(bundle: Path, report: LintReport, params_str: Optional[str]):
    """Rule 9.1: Attempt earthmover compile."""
    em_path = bundle / "earthmover.yaml"

    if not em_path.is_file():
        return

    if params_str is None:
        report.add("9.1", Severity.WARNING,
                   "earthmover compile skipped (could not extract params from README)",
                   True)  # Don't fail; we just can't run this check
        return

    # Run earthmover compile
    cmd = f"earthmover compile -c {em_path} -p '{params_str}'"
    try:
        result = subprocess.run(
            ["bash", "-c", cmd],
            capture_output=True,
            text=True,
            timeout=60,
            cwd=str(bundle)
        )
        passed = result.returncode == 0
        msg = "earthmover compile succeeds"
        if not passed:
            stderr = result.stderr.strip()[:200] if result.stderr else ""
            stdout = result.stdout.strip()[:200] if result.stdout else ""
            msg += f"\n      stderr: {stderr}" if stderr else ""
            msg += f"\n      stdout: {stdout}" if stdout else ""
        report.add("9.1", Severity.ERROR, msg, passed)
    except FileNotFoundError:
        report.add("9.1", Severity.WARNING,
                   "earthmover compile skipped (earthmover not installed)",
                   True)
    except subprocess.TimeoutExpired:
        report.add("9.1", Severity.WARNING,
                   "earthmover compile timed out after 60s",
                   False)
    finally:
        # Clean up compiled file
        compiled = bundle / "earthmover_compiled.yaml"
        if compiled.is_file():
            compiled.unlink()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def lint_bundle(bundle_path: str) -> LintReport:
    """Run all lint checks on a bundle directory."""
    bundle = Path(bundle_path).resolve()
    report = LintReport(bundle_path)

    if not bundle.is_dir():
        report.add("0.0", Severity.ERROR, f"Bundle directory does not exist: {bundle}", False)
        return report

    # Skip the template bundle
    if bundle.name == "_template_bundle":
        print(f"Skipping _template_bundle (reference only)")
        return report

    # Run all checks
    check_file_structure(bundle, report)
    check_sample_data(bundle, report)
    em = check_earthmover_yaml(bundle, report)
    check_lightbeam_yaml(bundle, report)
    meta = check_metadata_yaml(bundle, report)
    check_templates(bundle, report, em)
    check_seed_files(bundle, report, em)
    params_str = check_readme(bundle, report)
    check_compilation(bundle, report, params_str)

    return report


def main():
    if len(sys.argv) < 2:
        print("Usage: python lint_bundle.py <path_to_bundle> [<path_to_bundle2> ...]")
        print("       python lint_bundle.py assessments/MAP_Growth")
        print("       python lint_bundle.py --all  (lint all bundles under assessments/)")
        sys.exit(1)

    bundles = []
    if sys.argv[1] == "--all":
        assessments_dir = Path("assessments")
        if not assessments_dir.is_dir():
            print("ERROR: assessments/ directory not found in current directory")
            sys.exit(1)
        bundles = sorted([
            str(d) for d in assessments_dir.iterdir()
            if d.is_dir() and d.name != "_template_bundle"
        ])
    else:
        bundles = sys.argv[1:]

    any_errors = False
    for bundle_path in bundles:
        report = lint_bundle(bundle_path)
        report.print_report()
        if report.has_errors:
            any_errors = True

    sys.exit(1 if any_errors else 0)


if __name__ == "__main__":
    main()
