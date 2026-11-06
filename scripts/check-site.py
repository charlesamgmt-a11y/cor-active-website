"""Check deployable output without dependencies or network access."""
from collections import Counter
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
