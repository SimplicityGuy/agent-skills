# Private infra, secrets, and declarative GitHub management

## Bootstrap

Verify current upstream documentation and provider schemas before implementing commands, version pins, or feature claims. Required sources include [age-plugin-se](https://github.com/remko/age-plugin-se), [SOPS](https://github.com/getsops/sops), OpenTofu documentation, the GitHub provider documentation, and GitHub's current plan/feature documentation. Record consulted versions and dates; do not freeze guessed versions in the skill.

After design approval and explicit creation authorization, confirm `gh auth status`, organization-owner permissions, and the existing organization's identity. Create `infra` manually as private with no generated README. If it exists, inspect and adopt rather than overwrite. Prepare:

```text
infra/
├── .github/workflows/
├── brand/
│   ├── assets/
│   ├── templates/
│   ├── tokens.json
│   ├── render.mjs
│   └── README.md
├── docs/design/
├── manifests/
├── scripts/
├── secrets/
├── tofu/
├── .gitignore
├── .mise.toml
├── .sops.yaml
├── Justfile
└── README.md
```

Pin applicable OpenTofu, SOPS, age, age-plugin-se, just, gh, jq, and scripting runtime versions in `.mise.toml`. Ignore state and backups, secret-bearing plans, private identities, credentials, generated auth files, decrypted intermediates, and local configuration. Commit `.terraform.lock.hcl`, not state or the `.terraform` directory.

The default Justfile recipe lists commands. Include `doctor`, `check`, `init`, `plan`, `apply`, `secrets-edit`, `secrets-check`, and `brand`. `check` runs formatting checks, `tofu init -backend=false -input=false`, and `tofu validate` without touching live state; use an isolated validation directory if existing local state/backend configuration makes that uncertain. `plan` and `apply` obtain `GITHUB_TOKEN` from `gh auth token` at runtime and use noninteractive flags. Noninteractive execution does not remove the operator's approval gate; do not use an automatically approved apply until the complete reviewed plan is explicitly authorized. Protect any saved plan locally and never commit it.

Initially use local, untracked state unless a secure remote-state design is already approved. Explain that provider secret inputs can appear in state even when read from encrypted source files. Document secure storage, backups, operator access, and recovery. Declare the manually bootstrapped `infra` repository in OpenTofu and import it rather than recreate it. Inspect the import plan for unintended changes before applying.

## Secure Enclave and SOPS

On a compatible Mac, inspect `age-plugin-se keygen --help` and current upstream behavior. Use an explicit access-control mode matching the operator's chosen Touch ID and password/passcode fallback policy. Do not guess flags or silently fall back to a weaker software identity. If incompatible, present alternatives and leave this part pending.

Create a project-specific identity outside all repositories, for example `~/.config/age/<ORG>-infra.txt`, with mode `0600`. Never display or commit its payload. Only the public `age1se...` recipient belongs in `.sops.yaml`. Explain:

- Decryption follows the selected biometric/password policy.
- The identity is machine-bound; copying its file does not make a replacement Mac usable.
- Add a separate recovery recipient or protected offline recovery mechanism before depending on it for long-lived secrets. Test that recovery path with dummy data.
- A passphrase-protected software recovery identity, if desired, is separate from the Secure Enclave identity and stays outside repositories.

Limit anchored SOPS creation rules to `secrets/*.sops.yaml`, `secrets/*.sops.json`, and `secrets/*.sops.env` (escape dots and match only intended paths). Set `SOPS_AGE_KEY_FILE` through `.mise.toml` or a documented local environment mechanism containing only the path. Add an encrypted dummy example, prove decryption without logging plaintext, and check tracked files for plaintext. `secrets-check` decrypts each encrypted file directly to `/dev/null`, propagating any failure. When recipients change, run `sops updatekeys` on every encrypted file; never commit an unencrypted intermediate.

## Canonical resource map

Use version-constrained providers and commit the lockfile. One canonical repository map must show identity, initial/intended visibility, and explicit public exceptions; defaults are private. Share defaults with documented overrides. Manage supported resources:

- teams, maintainer memberships, team access, and repository creation;
- description, homepage, topics, issues/projects/wiki/discussions;
- merge methods, automatic branch deletion, labels, rulesets;
- Actions variables/secrets sourced from SOPS;
- Pages and optional DNS, using appropriate providers where applicable.

Every new IaC-managed repository is empty with `auto_init = false`. Keep intended public state separate from approved current state so an early apply cannot expose content. Choose merge policy from the actual landing protocol; do not impose squash-only on preserved-merge workflows. Detect plan support before defining private rulesets/protection or private Pages. Document unsupported protection honestly and identify manual/owner-only settings.

Infra CI initially performs formatting, backend-disabled initialization, validation, and leak checks that do not decrypt real secrets. Real plan/apply stays operator-local until CI identity, decryption, state storage, and approval controls are explicitly designed and approved. Secure Enclave operator identities are not a portable CI key.

Run `tofu fmt`, backend-disabled validation, then a real `tofu plan` locally with protected output. Review the complete plan and obtain explicit approval before apply. Verify an empty post-apply plan. If drift or feature limitations remain, record them rather than claiming convergence.
