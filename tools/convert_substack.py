"""Convert a Substack export post body into clean HTML for content/essays/.

Strips subscribe widgets and Substack chrome, turns images into captioned
<figure>s with the files saved under images/writing/<slug>/, and maps
pull quotes and dividers to the essay stylesheet's elements.
Needs beautifulsoup4 and Pillow.
Usage: python3 tools/convert_substack.py <export.html> . <slug>
"""
import io, json, re, pathlib, sys, urllib.request
from PIL import Image
from bs4 import BeautifulSoup

src, repo, slug = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]), sys.argv[3]
soup = BeautifulSoup(src.read_text(), "html.parser")
img_dir = repo / "images" / "writing" / slug
n = 0

def save(url):
    global n
    n += 1
    img_dir.mkdir(parents=True, exist_ok=True)
    out = img_dir / f"{n:02d}.jpg"
    if not out.exists():
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        im = Image.open(io.BytesIO(urllib.request.urlopen(req).read())).convert("RGB")
        im.thumbnail((1600, 1600))
        im.save(out, "JPEG", quality=82, optimize=True, progressive=True)
    return f"images/writing/{slug}/{out.name}"

def figure(src_url, caption, alt):
    fig = soup.new_tag("figure")
    fig.append(soup.new_tag("img", src=save(src_url), alt=alt or "", loading="lazy"))
    if caption:
        cap = soup.new_tag("figcaption")
        cap.append(BeautifulSoup(caption, "html.parser"))
        fig.append(cap)
    return fig

for el in soup.select(".subscription-widget-wrap-editor, .button-wrapper"):
    el.decompose()

for box in soup.select(".captioned-image-container"):
    img = box.find("img")
    cap = box.find("figcaption")
    attrs = json.loads(img.get("data-attrs") or "{}")
    url = attrs.get("src") or img["src"]
    box.replace_with(figure(url, cap.decode_contents() if cap else "", img.get("alt") or attrs.get("alt")))

for box in soup.select(".image-gallery-embed"):
    g = json.loads(box["data-attrs"])["gallery"]
    last = len(g["images"]) - 1
    for k, i in enumerate(g["images"]):
        box.insert_before(figure(i["src"], g.get("caption") if k == last else "", g.get("alt")))
    box.decompose()

for q in soup.select("div.pullquote"):
    q.name = "blockquote"
    q["class"] = "pull"

for d in soup.find_all("div"):
    if d.find("hr") and len(d.contents) == 1:
        d.replace_with(soup.new_tag("hr"))

for c in soup.select("pre code code"):
    c.unwrap()
for c in soup.select("pre code"):
    c.string = re.sub(r"\n\s*\n", "\n", c.get_text())

for tag in soup.find_all(["p", "h2", "h3", "h4"]):
    if not tag.get_text(strip=True) and not tag.find("img"):
        tag.decompose()

html = str(soup)
for t in ("p", "h2", "h3", "h4", "ul", "ol", "blockquote", "figure", "pre", "hr"):
    html = html.replace(f"</{t}><", f"</{t}>\n<")
html = html.replace("<hr/><", "<hr/>\n<")
out = repo / "content" / "essays" / f"{slug}.html"
out.write_text(html.strip() + "\n")
print(slug, f"({n} images)")
