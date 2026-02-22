# Bridge: DesignArch to ImageGen

## Purpose
Define how DesignArch outputs feed ImageGen and ensure a clean, auditable handoff into the ideation stage while preserving private prompts/logs.

## Input / Output
- Input to Bridge: 3 SneakerPulse briefs produced by DesignArch (e.g., SneakerPulse_DesignA.md, B, C).
- Output from Bridge to ImageGen: 6 mood/visual directions per brief (rationale + palettes) plus brief mapping data.

## Handoff Steps
1) Validate inputs exist (3 briefs).
2) Enrich briefs with a concise brief-to-image mapping (three directions per brief).
3) Push to ImageGen (IGN-001) for mood-direction exploration.
4) Generate a simple internal note of the bridge for auditing.

## Gate Considerations
- Gate 1 remains after DesignArch; Bridge does not bypass Critic.
- All prompts and rationales stay private; only outputs flow to ImageGen.

## Logging / Retention
- Bridge activity logged in private memory, and branch results saved under memory/BridgeRun_DesignArch_ImageGen_2026-02-21.md.
