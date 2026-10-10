# Repo profile: `<repo>`

Save as `.bughunt/profile.md` in the repo, so it travels with the code and the skill
itself stays generic.

## Parameters

| Parameter | Value |
|---|---|
| STACK | |
| TRACKER | |
| VERIFIER_MODEL | |
| MAX_AGENTS | 16 |
| MAX_PASSES | 10 |
| CHECKPOINT_EVERY | 3 |

## Slicing plan

One line per slice: name, then paths. Every source file in exactly one slice.

## Lens emphases

Repo-specific patterns worth naming in finder prompts, by lens. Lenses to skip, lenses
to add.

## Tracker quirks

CLI oddities, shadowed aliases, JSON shapes, required sync steps.

## Environment quirks

Agent types that fail to spawn, spend limits, anything else that bit a previous hunt.

## Hunt history

One entry per hunt: date, LABEL, rounds and the operator's decision at each gate,
per-round candidates -> confirmed -> filed, novelty rate, severity mix, corpus size
before/after.

## Un-swept ground

Lenses never run, areas never sliced. These go first next time.
