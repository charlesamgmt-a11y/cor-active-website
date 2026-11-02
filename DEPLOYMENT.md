# Website deployment

## Current status — November 2, 2026

GitHub → Cloudflare Pages is live at https://coractive.co. The custom domain is
Active with SSL enabled. The GitHub app has access to this repository only.
Both Codex and Claude can use this workflow when their own GitHub connection has
write access to the repository. No Codex session or local server needs to stay open.

The initial end-to-end test created a branch preview for commit `6590cab`, then
merged [PR #1](https://github.com/charlesamgmt-a11y/cor-active-website/pull/1).
Cloudflare automatically built production commit
`a29b8fb18292ec3c997481b9d828ad28211e3185`; the live domain's `/deployment.json`
returned that exact SHA. This is the migration test, not a permanently fixed
latest version. Check `/deployment.json` and the dashboard for the current release.

## Active configuration

| Setting | Value |
| --- | --- |
| Repository | `charlesamgmt-a11y/cor-active-website` |
| Pages project | `cor-active-website` |
| Production branch | `main` |
| Preview branches | All non-production branches |
| Framework | None |
| Root directory | Repository root |
| Build command | `bash scripts/build-site.sh` |
| Output directory | `dist` |
| App secrets | None required |
| Canonical domain | `coractive.co` |
| Extra hostname | `www.coractive.co`, redirect to apex |

Project dashboard:
https://dash.cloudflare.com/54d323b3a1eea9541fa44367dd6e25ff/pages/view/cor-active-website

Production fallback URL: https://cor-active-website.pages.dev/

Cloudflare's GitHub integration builds after pushes and supplies branch/PR
previews and commit status checks. Both agents use the same repository; no
deployment token belongs in the source code.

## Change and release workflow

1. Fetch `origin`; start a branch from the latest `main`.
2. Edit source, run `bash scripts/build-site.sh`, and inspect relevant UI changes.
3. Commit source and generated pages; push the branch.
4. Review the Cloudflare preview for that exact commit.
5. When publication is authorized, merge to `main` to trigger production.
6. Verify a successful deployment for that commit, compare `/deployment.json`
   with the full Git SHA, then check the live affected routes.

The build generates `dist/deployment.json`; it is intentionally ignored by Git.
Previews are public, so never put secrets or private data in a preview.
Publication approval is a workflow instruction, not an enforced GitHub branch
protection rule: a direct push to `main` also deploys.

Suggested request for either agent: “Use charlesamgmt-a11y/cor-active-website.
Read AGENTS.md and DEPLOYMENT.md, make the change on a branch, and show me the
Cloudflare preview before merging.” When ready, authorize merging to publish.

## Initial cutover

- [x] Latest site reconciled with GitHub, preserving both histories.
- [x] Cloudflare GitHub app authorized for this repository only.
- [x] Pages project created with the settings above.
- [x] Successful build and branch preview checked.
- [x] Apex custom domain and HTTPS active on Pages.
- [x] www configured and redirected to the apex.
- [x] Main routes/assets, robots/sitemap and true 404 verified.
- [x] A subsequent GitHub change verified to deploy automatically through PR #1.
- [x] This status and Notion updated to the verified result.

Validation covered six HTML pages, 112 local references, unique IDs and 73
deployable files. Eleven public routes/assets were checked on both hosts;
Pages output matched source bytes. The custom domain applies Cloudflare's
existing email obfuscation/security scripts to HTML. Its page headings,
static assets, HTTPS and real 404 behavior passed. This migration does not
constitute a full accessibility audit or complete the disabled Brevo waitlist.

## Domain routing

- Proxied apex CNAME → `cor-active-website.pages.dev`, TTL Auto.
- Proxied `www` A record → `192.0.2.1`, TTL Auto, used only for edge redirects.
- Single Redirect rule “Redirect www to coractive.co”: `*://www.coractive.co/*`
  → `https://coractive.co/${2}`, 301, preserve query string enabled.
- HTTP and HTTPS www requests preserve paths and query strings while redirecting
  to the HTTPS apex. Apex HTTP also redirects to HTTPS.
- Existing verification TXT records were preserved. No MX/email setup changed.

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
