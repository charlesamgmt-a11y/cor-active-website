# Shared instructions for Codex and Claude

Follow the user's current instructions and publication scope.

## Editing

- Shared Git remote: `charlesamgmt-a11y/cor-active-website` on GitHub.
- Fetch first. Work on a branch, or a separate worktree when another agent is
  editing. Preserve unrelated changes and reconcile history without force pushes.
- Read `DEPLOYMENT.md` for the actual hosting state before publishing.
- Edit page markup/metadata in `build.py`, copy in `reference-data.json`, styles
  in `dist/style.css`/`dist/fonts.css`, and behavior in `dist/app.js`.
- Never delete the whole `dist` directory: it contains source assets too.
- Run `bash scripts/build-site.sh`; commit generated HTML with its source.
- Preview UI changes in a browser, including relevant narrow layouts and keyboard
  interactions. State any verification that was not possible.

## Product constraints

- Preserve the black/ivory/glass style and approved logo proportions.
- Business/tab name: COR Active. In-page app name: CŌR.
- App is coming soon. Do not invent download links, dates, prices, trials,
  feature support, or database marketing claims.
- Preserve legal draft labels and the disabled waitlist until actually ready.
- App captures use illustrative records; concept device renders do not prove
  device compatibility. Do not present sample records as customer data.
- Never expose credentials, subscriber/health data or home addresses in this
  public repository or generated website.

## Publishing

- Branches are for development/previews; merging to `main` releases production
  once Cloudflare Git integration is active. Honor the user's publication scope.
- After an authorized release, verify the exact commit's successful deployment
  and the live affected pages. A push or local build alone is not a deployment.
- Keep `.openai/hosting.json` as the legacy Sites configuration. After cutover,
  do not switch the domain or use the old host unless performing an authorized rollback.
- Keep meaningful release status and unfinished launch work in the existing
  Notion task when requested; do not mark waitlist/legal work done prematurely.
