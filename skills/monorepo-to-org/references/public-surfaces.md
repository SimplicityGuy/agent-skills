# Branding, profile, Astro Pages, and DNS

## Canonical brand and profile

Keep editable sources under `infra/brand`: design tokens, SVG templates/source artwork, deterministic rendering, logo variants, light/dark assets, avatar, favicon/application sizes, social banners, default Open Graph image, and regeneration/usage documentation. Rendered assets must be reproducible from those sources. Promote copies into profile, site, apps and docs; do not create independently editable logo copies. Use relevant branding skills when assets need creation or auditing.

Prepare `.github` privately, with `profile/README.md` and `profile/assets/` at its repository root. Explain the organization, link primary products/docs, and use the rendered banner. Add shared community-health files only after verifying GitHub's current inheritance behavior. This repository does not automatically control organization settings or avatar; manage supported settings in OpenTofu and explicitly identify owner-only/manual branding actions.

Review content, history, license obligations and exposure before requesting the separate approved public transition. Keep the intended public exception visible in infra without enabling it prematurely.

## Astro organization site

Verify current official [Astro GitHub deployment guidance](https://docs.astro.build/en/guides/deploy/github/) and [GitHub Pages guidance](https://docs.github.com/pages) before implementation. Create `<ORG>/<ORG>.github.io` initially private. Plan capability checks, content exposure review, public transition and Pages enablement as explicit gates.

Use static Astro output and `site: "https://<ORG>.github.io"` or the approved custom domain. A root organization site has no repository base path. Commit the package-manager lockfile and pinned tooling. Provide local dev, build and preview commands through the repository's developer interface.

Include accessible navigation, semantic HTML, metadata/canonical URLs, Open Graph image, sitemap where appropriate, robots.txt, manifest, favicon, and a 404 page. Promote assets from infra's brand sources. No secret-dependent runtime behavior.

Use the current official Astro/Pages Actions deployment approach, pinned actions, a Pages environment and deployment concurrency. Minimal deployment permissions normally are:

```yaml
permissions:
  contents: read
  pages: write
  id-token: write
```

Configure Pages for GitHub Actions after approval. Verify the deployed URL, internal links, assets, 404 behavior and responsive layout. Do not claim deployment success from a local build alone.

For a custom domain, inspect current DNS/service usage; prepare declarative records where practical, custom-domain configuration, verification and rollback. Obtain approval before changing live DNS. Verify DNS resolution, domain ownership requirements and HTTPS before declaring it healthy. Record manual owner actions or certificate propagation as pending when not yet verified.
