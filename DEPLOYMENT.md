# Website deployment

## Current status — November 2, 2026

GitHub is synchronized with the published site. Cloudflare Pages is awaiting
authorization of its GitHub app for this repository. Until cutover is verified
here, https://coractive.co remains on Sites version 13, source commit
`3a50737d83ff8a158a401def78379c098fd837bf`. A GitHub push is not yet proof of a live release.

## Target configuration

| Setting | Value |
| --- | --- |
| Repository | `charlesamgmt-a11y/cor-active-website` |
| Pages project | `cor-active-website` (verify after creation) |
| Production branch | `main` |
| Preview branches | All non-production branches |
| Framework | None |
| Root directory | Repository root |
| Build command | `bash scripts/build-site.sh` |
| Output directory | `dist` |
| App secrets | None required |
| Canonical domain | `coractive.co` |
| Extra hostname | `www.coractive.co`, redirect to apex |

Cloudflare's GitHub integration builds after pushes and supplies branch/PR
previews and commit status checks. Both agents use the same repository; no
deployment token belongs in the source code.

## Change and release workflow

1. Fetch `origin`; start a branch from the latest `main`.
2. Edit source, run `bash scripts/build-site.sh`, and inspect relevant UI changes.
3. Commit source and generated pages; push the branch.
4. Review the Cloudflare preview for that exact commit.
5. When publication is authorized, merge to `main` to trigger production.
6. Verify a successful deployment for that commit, then check the live routes.

## Initial cutover

- [x] Latest site reconciled with GitHub, preserving both histories.
- [ ] Cloudflare GitHub app authorized for this repository only.
- [ ] Pages project created with the settings above.
- [ ] Successful build and pages.dev preview checked.
- [ ] Apex custom domain and HTTPS active on Pages.
- [ ] www configured and redirected to the apex.
- [ ] Main routes/assets, robots/sitemap and true 404 verified.
- [ ] A subsequent GitHub push verified to deploy automatically.
- [ ] This status and Notion updated to the verified result.

## Rollback

Use Pages' rollback to a previously successful production deployment, then
revert the offending Git commit and push the corrected source to keep GitHub and
hosting consistent.

The prior Sites project is retained during migration:
`appgprj_6ae2aaa1a36c8191a9adf4989b253526`, with `.openai/hosting.json` preserved.
Domain rollback requires restoring the verified prior DNS records and checking
HTTPS. Do not delete the old project during cutover.

Pre-cutover DNS observed on November 2: two apex A records, `172.66.3.26` and
`162.159.143.30`, both Proxied with Auto TTL. Preserve the existing verification
TXT records. No www or MX record was present; inbound email setup remains separate.

## References

- [Git integration](https://developers.cloudflare.com/pages/get-started/git-integration/)
- [Custom domains](https://developers.cloudflare.com/pages/configuration/custom-domains/)
- [Rollback](https://developers.cloudflare.com/pages/configuration/rollbacks/)
