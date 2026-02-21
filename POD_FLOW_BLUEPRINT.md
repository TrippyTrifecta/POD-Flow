# POD Flow — Central Blueprint

> **Last updated:** 2026-02-21
> **Workspace root:** `C:\Users\Axiom\Documents\Git-Projects`
> **Project folder:** `POD Flow`

---

## 1. Overview

POD Flow is a structured, multi-agent pipeline that turns high-level product briefs into finished designs, mockups, optimized listings, and social content — all with built-in quality gates, audit trails, and cost controls.

The guiding philosophy: decompose creative work into specialized stages, evaluate rigorously at each checkpoint, and only advance work that meets a rising quality bar. Humans stay in the loop for heavy decisions; AI handles the grunt work within defined guardrails.

---

## 2. Agents & Roles

### TEAM_LEAD (Orchestrator)
- Routes tasks to the right agent based on the request.
- Decomposes high-level briefs into stage-specific tasks.
- Enforces guardrails: no auto-publishing, pre-flight approval for expensive operations, generation quotas.
- Maintains central logs and coordinates handoffs between agents.

### IdeaGen (IGR-001)
- Brainstorms design concepts, themes, and slogans.
- Researches trends, cultural context, and market gaps.
- Outputs: 6 design concepts per cycle with short rationales, initial color palettes, and creative angles.

### DesignArch (DA-002)
- Translates raw concepts into concrete, production-ready design briefs.
- Personality: a free-thinking genius savant with deep knowledge of apparel design, the psychology of what sells, and a finger on the pulse of emerging trends. Carries a healthy distrust of the establishment and a fascination with high strangeness.
- Outputs: 3+ detailed briefs per concept including variant prompts, asset lists, color palettes, product fit notes, feasibility assessments, and acceptance criteria.

### Critic (Standalone Agent)
- An independent evaluator that gates progression through the pipeline.
- Uses a 10-point scale per criterion to score designs at three checkpoints.
- Does NOT generate or edit designs — only evaluates, scores, and provides actionable feedback.
- Full details in `POD Flow\Critic\SOUL.md`.

#### Critic Scoring Rubric (10-point scale per criterion)

| # | Criterion | What It Measures |
|---|-----------|-----------------|
| 1 | Market Appeal | Would this catch a buyer's eye? Does it tap into current demand or an emerging trend? |
| 2 | Originality | Is this fresh, or does it feel like something already saturating the market? |
| 3 | Visual Impact | Does the design pop? Strong contrast, composition, and focal point? |
| 4 | Print/Production Fit | How well will this translate to the target product? Considers ink behavior, color accuracy on different substrates, detail loss at print scale. |
| 5 | Brand Alignment | Does it fit the brand identity and tone? |
| 6 | Emotional Hook | Does it provoke a reaction — humor, curiosity, nostalgia, edge? |
| 7 | Versatility | Can this work across multiple product types, or is it a one-trick design? |
| 8 | Color & Contrast | Will the palette hold up in CMYK and on dark/light garments? |
| 9 | Target Audience Fit | Does this speak to the intended demographic? |
| 10 | Trend Longevity | Is this a flash-in-the-pan or does it have staying power? |

**Overall score** = average of all 10 criteria, expressed as a percentage.

### MockupMaestro (MM-003)
- Generates POD-ready mockups (product-on-model, lifestyle scenes, flat lays) from approved design briefs.
- Outputs: 1–4 high-quality mockups per brief with notes on pose, lighting, and composition, plus export-ready files.

### ImageRefiner (IR-004)
- Polishes visuals: color correction, CMYK gamut fixes, consistency checks, upscaling, and prompt refinement for fidelity.
- Outputs: refined final asset sets ready for production and marketing use.

### SEOListing (SEO-005)
- Crafts SEO-optimized titles, bullet points, descriptions, and tags for each SKU.
- Suggests pricing and margin targets.
- Outputs: complete product listings (typically 19–30+ per cycle).

### SocialContent (SC-006)
- Develops social media content briefs, captions, hooks, and posting schedules aligned to the new designs.
- Covers TikTok/Reels, Instagram carousels, Twitter threads, and Pinterest pins.
- Outputs: content calendars, caption copy, asset requirements, and a 14-day launch schedule.

---

## 3. Workflow & Data Flow

The pipeline runs in sequence with Critic gates inserted after three key stages:

```
IdeaGen
   ↓
DesignArch → CRITIC GATE 1 (75% threshold)
   ↓ (pass)                ↑ (fail — return with notes, up to 3 tries)
MockupMaestro → CRITIC GATE 2 (82% threshold)
   ↓ (pass)                ↑ (fail — return with notes, up to 2 tries)
ImageRefiner → CRITIC GATE 3 (87% threshold)
   ↓ (pass)                ↑ (fail — return with notes, up to 2 tries)
SEOListing
   ↓
SocialContent
   ↓
Final Output / Review
```

### Gate Details

**Gate 1 — After DesignArch (75%)**
- Critic scores each brief on the 10-point rubric.
- Pass (≥75%): brief advances to MockupMaestro.
- Fail (<75%): Critic returns the brief to DesignArch with a short description of what needs improvement. DesignArch revises and resubmits.
- Max iterations: 3. After the third failure, the brief is put on hold for human review.

**Gate 2 — After MockupMaestro (82%)**
- Critic scores each mockup set on the same rubric, with additional weight on print/production fit and visual impact.
- Pass (≥82%): mockups advance to ImageRefiner.
- Fail (<82%): Critic returns feedback to MockupMaestro for revision.
- Max iterations: 2. After the second failure, the mockups are paused and backed up for later review.

**Gate 3 — After ImageRefiner (87%)**
- Critic scores final refined assets.
- Pass (≥87%): assets advance to SEOListing and SocialContent.
- Fail (<87%): Critic returns feedback to ImageRefiner for a final polish pass.
- Max iterations: 2. After the second failure, the assets are paused and backed up for later review.

### What Happens When a Design Is Paused
- The design and all its iterations are backed up to `POD Flow\Output\paused\` with timestamps and score history.
- The human is notified so they can review and decide whether to revive, rework manually, or retire the concept.
- Nothing paused is deleted — it's always available for later review.

---

## 4. Governance

### Approval Rules
- No auto-publishing. Every heavy action (batch renders, final exports, listing uploads) requires explicit human approval.
- Pre-flight checks for token-heavy tasks: the Critic and TEAM_LEAD flag expensive operations before they run.
- Generation quotas: max 2 rounds of 4 images/videos before mandatory review.

### Iteration Limits (per design, per gate)
| Gate | Max Iterations Before Pause |
|------|-----------------------------|
| After DesignArch | 3 |
| After MockupMaestro | 2 |
| After ImageRefiner | 2 |

### Token-Saving Strategies
- Reuse and cache: previous outputs, prompts, and partial work are reused wherever possible.
- Batch processing: work in defined batches with review checkpoints, not one-at-a-time.
- Lightweight steps first: use human review, templates, and simple checks before spinning up AI-heavy generation.
- Critic feedback is concise: short, actionable notes — not essays.
- Minimize redundant passes: if a design clearly won't pass, flag it early rather than burning tokens on iterations.

### Communication Rules
- All human-facing communication is in plain English. No JSON, no structured data formats in chat.
- Internal agent-to-agent data (scores, prompts, schemas) stays in private files and logs — never surfaced raw to the user.

---

## 5. Retention & Artifacts

### File Structure
```
POD Flow\
 ├─ TEAM_LEAD\           ← orchestration prompts, central logs
 ├─ IdeaGen\             ← concept outputs
 ├─ DesignArch\          ← design briefs, variant prompts, feasibility
 ├─ Critic\              ← scoring rubric, evaluation logs, feedback history
 │    ├─ SOUL.md         ← Critic personality and rules
 │    ├─ Prompts.md      ← prompts skeleton
 │    └─ evaluations\    ← per-design score logs
 ├─ MockupMaestro\       ← mockup specs and assets
 ├─ ImageRefiner\        ← refined assets, color correction logs
 ├─ SEOListing\          ← product listings, tags, pricing
 ├─ SocialContent\       ← content calendars, captions, hooks
 ├─ 001\                 ← current product batch (SneakerPulse designs)
 │    ├─ SneakerPulse_DesignA.md
 │    ├─ SneakerPulse_DesignB.md
 │    └─ SneakerPulse_DesignC.md
 ├─ Output\              ← final assembled outputs and exports
 │    └─ paused\         ← designs that didn't pass gates, backed up for review
 ├─ Results\             ← aggregated results and performance data
 └─ POD_FLOW_BLUEPRINT.md  ← this document
```

### What Gets Logged
- Every Critic evaluation: score per criterion, overall percentage, pass/fail, feedback notes, timestamps.
- Every iteration: which agent revised, what changed, before/after scores.
- Handoff records: what was passed from one agent to the next, with task IDs.
- Pause/backup events: which design was paused, why, where it's stored.

### Backup Rules
- Paused designs go to `POD Flow\Output\paused\` with full iteration history.
- Nothing is deleted without explicit human approval.
- Logs are append-only (no overwriting history).

---

## 6. Current Cycle State

| Cycle | Agent | Status | Notes |
|-------|-------|--------|-------|
| IGR-001 | IdeaGen | Completed | 6 design concepts generated. |
| DA-002 | DesignArch | Completed | 6 themes → 12 variant briefs. |
| MM-003 | MockupMaestro | Completed | 20 mockup specs across all themes. |
| IR-004 | ImageRefiner | Completed | Color corrections, quality checklists, final assets. |
| SEO-005 | SEOListing | Completed | 19 product listings with SEO optimization. |
| SC-006 | SocialContent | Completed | 10 content pieces with 14-day launch calendar. |

**Next up:** 3 new SneakerPulse designs in folder 001 — wire through the full pipeline with Critic gates active.

---

## 7. Quick Reference

- **Pass thresholds:** 75% → 82% → 87%
- **Max retries per gate:** 3 → 2 → 2
- **Critic rubric:** 10 criteria, 10-point scale each
- **Paused designs:** backed up to `Output\paused\`, human notified
- **No auto-publish.** Ever.
- **Talk to John in plain English.** Always.
