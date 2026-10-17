#!/usr/bin/env python3
"""Structural traceability check for the project documentation.

Run from anywhere: python3 scripts/trace_check.py [--root DIR] [--strict]

Checks:
- every RF/RNF/RN/PRN/UI/D/P/SPEC/CA identifier cited in Markdown is defined
  in its owner document (CA criteria are scoped as SPEC-NNN/CA-NN);
- identifiers defined only in plans/ are reported as proposals, not definitions;
- local Markdown links resolve to existing files;
- every English .md not listed in scripts/mirror-exclusions.txt has a mirror in
  espanol/ with the same heading structure and the same identifier set.

Exit status is 1 when errors were found (or warnings with --strict), else 0.
These are structural checks only; they do not prove correct translation,
permission consistency, diagram balancing, or complete requirement coverage. xd
"""

import argparse
import os
import re
import sys
import unicodedata
from collections import defaultdict
from urllib.parse import unquote

# Owner document per identifier namespace; an ID is defined only there. xd
OWNERS = {
    "D": "docs/00-context.md",
    "P": "docs/00-context.md",
    "RF": "docs/02-requirements.md",
    "RNF": "docs/02-requirements.md",
    "RN": "docs/03-business-rules.md",
    "PRN": "docs/03-business-rules.md",
    "UI": "docs/04-view-design.md",
}
SPEC_DIR = "specs"
PLAN_DIR = "plans"
MIRROR_DIR = "espanol"
EXCLUSIONS_FILE = "scripts/mirror-exclusions.txt"
DEFAULT_EXCLUSIONS = ["espanol/", "contexto/", ".claude/", ".agents/", ".codex/",
                      "AGENTS.md", "CLAUDE.md", "SKILLS.md"]
# Directories and root files never scanned at all (local agent configuration). xd
SKIP_DIRS = {".git", ".claude", ".agents", ".codex", "node_modules", "contexto"}
SKIP_FILES = {"AGENTS.md", "CLAUDE.md", "SKILLS.md"}

ID_PATTERN = r"(RF|RNF|RN|PRN|UI|D|P|SPEC|CA)-([A-Z]?\d{2,3})"
ID_RE = re.compile(r"\b" + ID_PATTERN + r"\b")
# "RN-01/02/03" cites several IDs of the same prefix. xd
SHORTHAND_RE = re.compile(r"(?:/(\d{2,3}))+")
# "D-01–D-09" or "D-01-D-09" is an inclusive range of the same prefix. xd
RANGE_RE = re.compile(r"\b" + ID_PATTERN + r"\s*[–-]\s*" + ID_PATTERN + r"\b")
DEF_RES = [
    re.compile(r"^\|\s*" + ID_PATTERN + r"\s*\|"),          # first cell of a table row xd
    re.compile(r"^#{1,6}\s+" + ID_PATTERN + r"\b"),          # heading xd
    re.compile(r"^(?:[-*]\s+)?\*\*" + ID_PATTERN + r"\b"),   # bold list item or paragraph xd
    re.compile(r"^[-*]\s+" + ID_PATTERN + r"\s*[:—–-]"),       # list item "- CA-01: ..." as in specs/template.md xd
]
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
SPEC_FILE_RE = re.compile(r"^(\d{3})-[a-z0-9-]+\.md$")


class Report:
    def __init__(self):
        self.errors, self.warnings, self.infos = [], [], []

    def error(self, msg):
        self.errors.append(msg)

    def warn(self, msg):
        self.warnings.append(msg)

    def info(self, msg):
        self.infos.append(msg)


def read_exclusions(root):
    path = os.path.join(root, EXCLUSIONS_FILE)
    if not os.path.isfile(path):
        return list(DEFAULT_EXCLUSIONS)
    entries = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.split("#", 1)[0].strip()
            if line:
                entries.append(line)
    return entries


def is_excluded(rel, exclusions):
    for entry in exclusions:
        if entry.endswith("/"):
            if rel.startswith(entry):
                return True
        elif rel == entry:
            return True
    return False


def list_markdown(root):
    files = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)
        for name in sorted(filenames):
            if not name.lower().endswith(".md"):
                continue
            rel = os.path.relpath(os.path.join(dirpath, name), root).replace(os.sep, "/")
            if rel in SKIP_FILES:
                continue
            files.append(rel)
    return files


def read_lines(root, rel):
    with open(os.path.join(root, rel), encoding="utf-8") as fh:
        return fh.read().splitlines()


def fenced_mask(lines):
    """Return a list of booleans: True when the line is inside a fenced code block. xd"""
    mask, inside, fence = [], False, None
    for line in lines:
        stripped = line.strip()
        if not inside and (stripped.startswith("```") or stripped.startswith("~~~")):
            inside, fence = True, stripped[:3]
            mask.append(True)
            continue
        if inside and stripped.startswith(fence):
            inside = False
            mask.append(True)
            continue
        mask.append(inside)
    return mask


def spec_number(rel):
    """SPEC number owned by a spec file, in specs/ or its mirror, else None. xd"""
    parts = rel.split("/")
    if parts[0] == MIRROR_DIR:
        parts = parts[1:]
    if len(parts) == 2 and parts[0] == SPEC_DIR:
        match = SPEC_FILE_RE.match(parts[1])
        if match:
            return match.group(1)
    return None


def canonical(prefix, num, line, spec):
    """Full identifier; CA criteria are scoped to a SPEC named on the line or owning the file. xd"""
    if prefix != "CA":
        return f"{prefix}-{num}"
    specs_on_line = re.findall(r"\bSPEC-(\d{3})\b", line)
    scope = specs_on_line[-1] if specs_on_line else spec
    return f"SPEC-{scope}/CA-{num}" if scope else f"CA-{num}"


def extract_ids(line, spec):
    """All identifiers cited on a line, including shorthand lists and ranges. xd"""
    found = []
    for match in ID_RE.finditer(line):
        prefix, num = match.group(1), match.group(2)
        found.append(canonical(prefix, num, line, spec))
        tail = SHORTHAND_RE.match(line, match.end())
        if tail:
            for extra in re.findall(r"/(\d{2,3})", tail.group(0)):
                found.append(canonical(prefix, extra, line, spec))
    for match in RANGE_RE.finditer(line):
        p1, n1, p2, n2 = match.groups()
        if p1 == p2 and n1.isdigit() and n2.isdigit() and int(n1) < int(n2):
            width = len(n1)
            for n in range(int(n1) + 1, int(n2)):
                found.append(canonical(p1, str(n).zfill(width), line, spec))
    return found


def definitions_on(line, spec):
    for regex in DEF_RES:
        match = regex.match(line)
        if match:
            return canonical(match.group(1), match.group(2), line, spec)
    return None


def scan_file(root, rel):
    """Collect definitions, references, headings and links of one Markdown file. xd"""
    lines = read_lines(root, rel)
    mask = fenced_mask(lines)
    spec = spec_number(rel)
    is_plan = rel.startswith(PLAN_DIR + "/") or rel.startswith(f"{MIRROR_DIR}/{PLAN_DIR}/")
    is_template = os.path.basename(rel) == "template.md"
    data = {"defs": {}, "refs": [], "headings": [], "links": [], "spec": spec,
            "is_plan": is_plan, "is_template": is_template, "first_heading": None}
    for number, line in enumerate(lines, 1):
        if not mask[number - 1]:
            heading = HEADING_RE.match(line)
            if heading:
                data["headings"].append((len(heading.group(1)), heading.group(2).strip(), number))
                if data["first_heading"] is None:
                    data["first_heading"] = heading.group(2).strip()
            for link in LINK_RE.finditer(line):
                data["links"].append((link.group(1), number))
        if is_template:
            continue
        if not mask[number - 1]:
            defined = definitions_on(line, spec)
            if defined:
                data["defs"].setdefault(defined, []).append(number)
        for ident in extract_ids(line, spec):
            data["refs"].append((ident, number))
    return data


def owner_of(ident):
    if ident.startswith("SPEC-"):
        return "spec"
    return OWNERS.get(ident.split("-", 1)[0])


def check_links(root, rel, data, report):
    base = os.path.dirname(os.path.join(root, rel))
    for target, number in data["links"]:
        if "://" in target or target.startswith(("#", "mailto:")):
            continue
        path = unquote(target.split("#", 1)[0])
        if not path:
            continue
        candidate = os.path.normpath(os.path.join(base, path))
        exists = os.path.exists(candidate)
        if not exists:
            for form in ("NFC", "NFD"):
                if os.path.exists(unicodedata.normalize(form, candidate)):
                    exists = True
                    break
        if not exists:
            report.error(f"{rel}:{number}: link target not found: {target}")


def main():
    parser = argparse.ArgumentParser(description="Structural traceability check.")
    parser.add_argument("--root", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    parser.add_argument("--strict", action="store_true", help="treat warnings as errors")
    args = parser.parse_args()
    root = os.path.abspath(args.root)
    report = Report()
    exclusions = read_exclusions(root)

    files = list_markdown(root)
    scanned = {rel: scan_file(root, rel) for rel in files}
    sources = [rel for rel in files if not rel.startswith(MIRROR_DIR + "/")]
    mirrors = [rel for rel in files if rel.startswith(MIRROR_DIR + "/")]

    # 1. Definitions: owner documents and spec files define; plans only propose. xd
    defined, proposed = {}, defaultdict(set)
    for rel in sources:
        data = scanned[rel]
        for ident, numbers in data["defs"].items():
            owner = owner_of(ident)
            if data["is_plan"]:
                proposed[ident].add(rel)
                continue
            owns = (owner == "spec" and data["spec"] is not None) or owner == rel \
                or (ident.startswith(f"SPEC-{data['spec']}/CA-") if data["spec"] else False)
            if not owns:
                continue
            if len(numbers) > 1:
                report.error(f"{rel}: {ident} is defined more than once (lines {numbers})")
            if ident in defined:
                report.error(f"{rel}:{numbers[0]}: {ident} is already defined in {defined[ident]}")
            defined[ident] = rel
        if data["spec"]:
            expected = f"SPEC-{data['spec']}"
            if not (data["first_heading"] or "").startswith(expected):
                report.error(f"{rel}: first heading must start with {expected}")
            elif expected not in defined and not data["is_plan"]:
                defined[expected] = rel

    # 2. References must resolve to a definition. xd
    plan_only = defaultdict(set)
    for rel in sources:
        data = scanned[rel]
        for ident, number in data["refs"]:
            if ident in defined:
                continue
            if ident.startswith("CA-"):
                report.warn(f"{rel}:{number}: {ident} is not scoped to a SPEC; cite it as SPEC-NNN/{ident}")
                continue
            if data["is_plan"]:
                plan_only[ident].add(rel)
                continue
            if ident in proposed:
                report.warn(f"{rel}:{number}: {ident} exists only as a proposal in {', '.join(sorted(proposed[ident]))}")
            else:
                owner = owner_of(ident)
                where = f"in {owner}" if owner and owner != "spec" else "anywhere"
                report.error(f"{rel}:{number}: {ident} is not defined {where}")
    pending = sorted(set(proposed) | set(plan_only), key=lambda s: (s.split("-")[0], s))
    if pending:
        report.info("identifiers that exist only in plans/ (proposals, not decisions): " + ", ".join(pending))

    # 3. Local links. xd
    for rel in files:
        check_links(root, rel, scanned[rel], report)

    # 4. Mirrors: existence, heading structure, identifier sets. xd
    mirrored = 0
    for rel in sources:
        if is_excluded(rel, exclusions):
            continue
        mirror = f"{MIRROR_DIR}/{rel}"
        if mirror not in scanned:
            report.error(f"{rel}: missing Spanish mirror {mirror}")
            continue
        mirrored += 1
        src, mir = scanned[rel], scanned[mirror]
        src_levels = [h[0] for h in src["headings"]]
        mir_levels = [h[0] for h in mir["headings"]]
        if src_levels != mir_levels:
            index = next((i for i, pair in enumerate(zip(src_levels, mir_levels)) if pair[0] != pair[1]),
                         min(len(src_levels), len(mir_levels)))
            src_desc = f"line {src['headings'][index][2]} '{src['headings'][index][1]}'" if index < len(src_levels) else "end of file"
            mir_desc = f"line {mir['headings'][index][2]} '{mir['headings'][index][1]}'" if index < len(mir_levels) else "end of file"
            report.error(f"{rel}: heading structure differs from {mirror} "
                         f"({len(src_levels)} vs {len(mir_levels)} headings; first difference at {src_desc} vs {mir_desc})")
        if not src["is_template"]:
            src_ids = {i for i, _ in src["refs"]} | set(src["defs"])
            mir_ids = {i for i, _ in mir["refs"]} | set(mir["defs"])
            missing, extra = sorted(src_ids - mir_ids), sorted(mir_ids - src_ids)
            if missing:
                report.error(f"{mirror}: identifiers missing from mirror: {', '.join(missing)}")
            if extra:
                report.error(f"{mirror}: identifiers not in the English source: {', '.join(extra)}")
    for mirror in mirrors:
        rel = mirror[len(MIRROR_DIR) + 1:]
        if is_excluded(rel, exclusions):
            report.warn(f"{mirror}: mirror of an excluded path; it is not kept in sync and can be removed")
        elif not os.path.exists(os.path.join(root, rel)):
            report.warn(f"{mirror}: orphan mirror; no English source {rel}")

    for msg in report.errors:
        print(f"ERROR {msg}")
    for msg in report.warnings:
        print(f"WARN  {msg}")
    for msg in report.infos:
        print(f"INFO  {msg}")
    refs = sum(len(scanned[r]["refs"]) for r in sources)
    print(f"INFO  checked {len(sources)} English files, {mirrored} mirrors, {len(defined)} definitions, {refs} references: "
          f"{len(report.errors)} errors, {len(report.warnings)} warnings")
    failed = bool(report.errors) or (args.strict and bool(report.warnings))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
