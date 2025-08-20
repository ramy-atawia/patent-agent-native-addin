"""Utility functions for basic claim syntactic checks.

Provides lightweight heuristics used by unit tests and QA to detect
common problems: missing claim 1, absence of 'comprising' in claim 1,
numbering continuity when present, and simple antecedent/structure checks.
"""
from typing import List, Dict
import re


def _extract_leading_number(claim: str):
    m = re.match(r"^\s*(\d+)\s*[\.|\)]\s*(.*)$", claim)
    if m:
        return int(m.group(1)), m.group(2).strip()
    return None, claim.strip()


def check_claims_syntax(claims: List[str]) -> Dict[str, object]:
    """Perform basic syntactic checks on a list of claim strings.

    Returns dict: { ok: bool, issues: List[str], details: {...} }
    """
    issues = []
    details = {}

    if not claims:
        issues.append("No claims provided")
        return {"ok": False, "issues": issues, "details": details}

    # Check Claim 1 exists and has 'comprising'
    first = claims[0].strip()
    # Allow numbered or unnumbered; extract body
    num, body = _extract_leading_number(first)
    if 'comprising' not in body.lower():
        issues.append("Claim 1 missing required word 'comprising'")

    # Numbering continuity: if any claim has a leading number, expect sequential numbering
    nums = []
    for c in claims:
        n, _ = _extract_leading_number(c)
        if n is not None:
            nums.append(n)

    if nums:
        expected = list(range(1, len(nums) + 1))
        if nums != expected:
            issues.append(f"Claim numbering not continuous or not starting at 1: {nums}")
        details['numbers'] = nums

    # Minimum word length per claim
    short_claims = [i+1 for i,c in enumerate(claims) if len(c.split()) < 8]
    if short_claims:
        issues.append(f"Claims too short: {short_claims}")

    # Simple antecedent/structure check for dependent claims: look for 'wherein' or 'said' in dependent claims
    dep_issues = []
    for i, c in enumerate(claims[1:], start=2):
        low = c.lower()
        if 'wherein' not in low and 'said' not in low and 'the ' not in low:
            dep_issues.append(i)
    if dep_issues:
        issues.append(f"Dependent claims may lack antecedent basis or 'wherein' wording: {dep_issues}")

    ok = len(issues) == 0
    return {"ok": ok, "issues": issues, "details": details}


