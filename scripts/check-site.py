"""Check deployable output without dependencies or network access."""
from collections import Counter
import hashlib
from html.parser import HTMLParser
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1] / "dist"


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.refs = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.ids.append(attrs["id"])
        for key in ("href", "src", "poster"):
            if attrs.get(key):
                self.refs.append(attrs[key])
        if attrs.get("srcset") and not attrs["srcset"].startswith("data:"):
            self.refs.extend(item.strip().split()[0]
                             for item in attrs["srcset"].split(",") if item.strip())


def main():
    pages = {}
    errors = []
    for file in ROOT.rglob("*.html"):
        page = Page()
        page.feed(file.read_text())
        pages[file] = page
    for suffix in ("*.html", "*.css", "*.js", "*.svg"):
        for file in ROOT.rglob(suffix):
            text = file.read_text()
            if "CŌR" in text or "CO\u0304R" in text:
                errors.append(f"{file.relative_to(ROOT)}: use COR without a macron")
    for name in ("index.html", "404.html", "robots.txt", "sitemap.xml"):
        if not (ROOT / name).is_file():
            errors.append(f"Missing required output: {name}")
    refs = []
    for file, page in pages.items():
        for ident, count in Counter(page.ids).items():
            if count > 1:
                errors.append(f"{file.relative_to(ROOT)}: duplicate id {ident}")
        refs.extend((file, ref) for ref in page.refs)
    for css in ROOT.rglob("*.css"):
        for match in re.finditer(r"url\(\s*(['\"]?)(.*?)\1\s*\)", css.read_text()):
            ref = match.group(2)
            if not ref.startswith("#"):
                refs.append((css, ref))
    checked = 0
    for file, ref in refs:
        url = urlsplit(ref)
        if url.scheme or url.netloc:
            continue
        target = (ROOT / unquote(url.path).lstrip("/")) if url.path.startswith("/") else (
            file.parent / unquote(url.path) if url.path else file)
        if target.is_dir():
            target /= "index.html"
        target = target.resolve()
        checked += 1
        if not target.is_file():
            errors.append(f"{file.relative_to(ROOT)}: missing {ref}")
        elif url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
            errors.append(f"{file.relative_to(ROOT)}: missing anchor {ref}")
    # Guard the exact Apple source artwork and all three on-page placements.
    frame_path = "/assets/brand/iphone-18-pro-max-glacier-apple.png"
    frame = ROOT / frame_path.lstrip("/")
    expected_sha = "f6edfdf4f4b84170d79e34b21df4d4b3ab300e738b64d54bdf8297788e32c6af"
    if not frame.is_file() or hashlib.sha256(frame.read_bytes()).hexdigest() != expected_sha:
        errors.append("Official Apple device artwork is missing or modified")
    home = pages.get(ROOT / "index.html")
    if home and sum(ref == frame_path for ref in home.refs) != 3:
        errors.append("Hero, walkthrough and showcase must use the official device artwork")
    if "iphone-18-pro-max-glacier.webp" in (ROOT / "index.html").read_text():
        errors.append("The old third-party phone illustration is still referenced")
    files = [path for path in ROOT.rglob("*") if path.is_file()]
    if len(files) > 20000:
        errors.append("Output exceeds Cloudflare Pages' 20,000-file free-plan limit")
    for file in files:
        if file.stat().st_size > 25 * 1024 * 1024:
            errors.append(f"Asset exceeds 25 MiB: {file.relative_to(ROOT)}")
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"Validated {len(pages)} HTML pages, {checked} local references, unique IDs, "
          f"and {len(files)} deployable files.")


if __name__ == "__main__":
    main()
