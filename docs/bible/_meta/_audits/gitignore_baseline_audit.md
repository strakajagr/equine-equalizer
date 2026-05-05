# .gitignore Baseline Audit

**Document:** gitignore_baseline_audit
**Phase:** 0 exit prerequisite (per META_PLAN v6 § 7.14)
**Date:** 2026-05-04
**Author:** QB
**Status:** AUDIT COMPLETE

---

## 1. Purpose

Per META_PLAN v6 § 7.14: "QB performs a quick (~15-minute) audit pass comparing all deploy script artifact-writes (verified locations include `scripts/deploy-backend.sh:229,243,262`) against `.gitignore`. Any gaps are added in one sweep."

This audit establishes a clean commit-hygiene baseline before Tony performs the pre-Phase-1 baseline commit (META_PLAN v6 § 3.1.1).

## 2. Method

1. Read current `.gitignore` at repo root.
2. Read both deploy scripts (`scripts/deploy-backend.sh` + `scripts/deploy-frontend.sh`).
3. Enumerate every artifact-write location (lines that write to the local working tree).
4. Compare each artifact-write target against `.gitignore` patterns.
5. Document any gaps for one-sweep remediation.

## 3. Deploy script artifact-writes enumerated

### scripts/deploy-backend.sh

| Line | Artifact write target | Trigger condition |
|---|---|---|
| 168 | `cdk-outputs.json` (repo root) | single-stack deploy (`--stack` flag) |
| 175 | `cdk-outputs.json` (repo root) | full deploy (`cdk deploy --all`) |
| 233-234 | `frontend/.env.production` | API URL extraction succeeds |
| 249-250 | `.frontend-bucket` (repo root) | S3 bucket extraction succeeds |
| 269 | `.cf-distribution-id` (repo root) | CloudFront distribution ID extraction succeeds |

### scripts/deploy-frontend.sh

| Line | Artifact write target | Trigger condition |
|---|---|---|
| 196 | `frontend/.env.production` | `.env.production` doesn't already exist (fallback creation) |

### Unique artifact set

Five write-statements across both scripts produce four unique artifacts (frontend/.env.production written from two locations, but same target):

1. `cdk-outputs.json` (repo root)
2. `frontend/.env.production`
3. `.frontend-bucket` (repo root)
4. `.cf-distribution-id` (repo root)

## 4. Comparison against current .gitignore

Current `.gitignore` "Deployment artifacts (machine-specific)" section reads verbatim:

```
# Deployment artifacts (machine-specific)
.frontend-bucket
.cf-distribution-id
cdk-outputs.json
frontend/.env.production
```

| Artifact (from § 3) | Matched .gitignore pattern | Coverage |
|---|---|---|
| `cdk-outputs.json` | `cdk-outputs.json` | ✓ covered |
| `frontend/.env.production` | `frontend/.env.production` | ✓ covered |
| `.frontend-bucket` | `.frontend-bucket` | ✓ covered |
| `.cf-distribution-id` | `.cf-distribution-id` | ✓ covered |

**Result: all 4 unique deploy artifacts gitignored. Zero gaps.**

## 5. Findings

**Zero gaps.** Current `.gitignore` covers all artifacts written by both deploy scripts. No remediation required.

This audit ratifies the v3-cycle reframing of META_PLAN's Q4 (per META_PLAN v6 § 7.14): the v2-audit-claimed gap was already closed; the prerequisite remained valid as a forensic sweep, and the sweep confirms zero gaps as predicted.

## 6. Going-forward rule

Per META_PLAN v6 § 7.14: "any new deploy script that writes a machine-specific artifact must update `.gitignore` in the same commit. This is repository-hygiene discipline parallel to (not a sub-rule of) § 7.1's bible-update discipline; both share the principle 'every change is captured in the commit that produces it.'"

The discipline is operative from this audit forward. New deploy artifacts → `.gitignore` update in the same commit.

## 7. Phase 0 exit prerequisite status

This audit completes Phase 0 exit prerequisite #4 (per META_PLAN v6 § 11):

> [ ] `.gitignore` baseline audit performed; findings documented at `_audits/gitignore_baseline_audit.md` (§ 7.14)

Status: ✓ COMPLETE. Findings documented at this file location.

---

**End of gitignore_baseline_audit.md**
