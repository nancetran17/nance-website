"""Render essay pages and writing.html for nance-website from posts.json.

Each post in posts.json has: slug, title, subtitle, date (YYYY-MM-DD), tag,
cover, substack, and either body (path to an HTML fragment) for a page we
render, or href for an essay that is its own standalone site.
Usage: python3 tools/render.py .
"""
import html, json, sys, datetime, pathlib

repo = pathlib.Path(sys.argv[1])
posts = json.loads((repo / "content" / "posts.json").read_text())
posts.sort(key=lambda p: p["date"], reverse=True)

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,300;0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400&family=Hanken+Grotesk:wght@400;500;600&family=IBM+Plex+Mono:wght@400&display=swap">\n'
         '  <link rel="stylesheet" href="css/writing.css">')

TOPBAR = '''<header class="topbar">
    <div class="topbar__inner">
      <a href="index.html" class="topbar__home">nance<span>.</span></a>
      <ul class="topbar__links">
        <li><a href="writing.html"{cur}>Writing</a></li>
        <li><a href="projects.html"{pcur}>Projects</a></li>
        <li><a href="/#work">Work with me</a></li>
        <li><a class="sub" href="https://overthinkerdiary.substack.com/subscribe" target="_blank" rel="noopener">Subscribe</a></li>
      </ul>
    </div>
  </header>'''

FOOT = '''<footer class="foot">
    <span>&copy; 2026 Nancy Tran</span>
    <a href="mailto:tuong.tran0117@gmail.com">Email</a>
    <a href="https://overthinkerdiary.substack.com" target="_blank" rel="noopener">Substack</a>
  </footer>'''

def fmt(d):
    d = datetime.date.fromisoformat(d)
    return d.strftime("%b ") + str(d.day) + d.strftime(", %Y")

def e(s):
    return html.escape(s, quote=True)

def href(p):
    return p.get("href") or f'{p["slug"]}.html'

for p in posts:
    if "body" not in p:
        continue
    body = (repo / "content" / p["body"]).read_text().strip()
    cover = (f'<figure class="essay__cover"><img src="{e(p["cover"])}" alt="{e(p.get("cover_alt", ""))}"></figure>'
             if p.get("cover") else "")
    page = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{e(p["title"])} | Nancy Tran</title>
  <meta name="description" content="{e(p["subtitle"])}">
  <meta property="og:title" content="{e(p["title"])}">
  <meta property="og:description" content="{e(p["subtitle"])}">
  {('<meta property="og:image" content="https://nancytuongtran.com/' + e(p["cover"]) + '">') if p.get("cover") else ""}
  {FONTS}
</head>
<body class="paper">
  {TOPBAR.format(cur="", pcur="")}

  <article class="essay">
    <a href="writing.html" class="essay__tag">{e(p["tag"])}</a>
    <h1 class="essay__title">{e(p["title"])}</h1>
    <p class="essay__subtitle">{e(p["subtitle"])}</p>
    <div class="byline"><b>Nancy Tran</b><time datetime="{p["date"]}">{fmt(p["date"])}</time><a href="{e(p["substack"])}" target="_blank" rel="noopener">Read on Substack</a></div>
    {cover}
    <div class="prose">
{body}
    </div>
    <nav class="essay__end"><a href="writing.html">&larr; All writing</a><a href="https://overthinkerdiary.substack.com/subscribe" target="_blank" rel="noopener">Get the next one by email &rarr;</a></nav>
  </article>

  {FOOT}
</body>
</html>
'''
    (repo / f'{p["slug"]}.html').write_text(page)

def archive(entries, title, eyebrow, lede, description, writing):
    items = []
    for p in entries:
        ext = ' target="_blank" rel="noopener"' if href(p).startswith("http") else ""
        thumb = f'<img class="post__thumb" src="{e(p["cover"])}" alt="" loading="lazy">' if p.get("cover") else f'<span class="post__thumb post__thumb--note" aria-hidden="true">{e(p.get("note", ""))}</span>'
        items.append(f'''      <li class="post">
        <a class="post__link" href="{e(href(p))}"{ext}>
          <div>
            <span class="post__tag">{e(p["tag"])}</span>
            <h2 class="post__title">{e(p["title"])}</h2>
            <p class="post__sub">{e(p["subtitle"])}</p>
            <p class="post__meta"><time datetime="{p["date"]}">{fmt(p["date"])}</time></p>
          </div>
          {thumb}
        </a>
      </li>''')
    cur = ' aria-current="page"'
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | Nancy Tran</title>
  <meta name="description" content="{description}">
  {FONTS}
</head>
<body class="paper">
  {TOPBAR.format(cur=cur if writing else "", pcur="" if writing else cur)}

  <main class="archive">
    <p class="archive__eyebrow">{eyebrow}</p>
    <h1 class="archive__title">{title}</h1>
    <p class="archive__lede">{lede}</p>
    <ul class="posts">
{chr(10).join(items)}
    </ul>
  </main>

  {FOOT}
</body>
</html>
'''

(repo / "writing.html").write_text(archive(
    posts, "Writing", "from the bookshelf",
    'I write to think, mostly about technology, civilization and why I\'m hopeful about where we\'re headed. Everything here also goes out on my <a href="https://overthinkerdiary.substack.com" target="_blank" rel="noopener">Substack</a>.',
    "Essays by Nancy Tran on technology, civilization and where we're headed, also published on Substack.", True))

projects = json.loads((repo / "content" / "projects.json").read_text())
(repo / "projects.html").write_text(archive(
    projects, "Projects", "open on the laptop",
    "Things I build to understand the world a little better.",
    "Projects by Nancy Tran: illustrated, interactive essays and things she builds.", False))

# The bookshelf panel on the studio homepage lists the same posts.
home = repo / "index.html"
if home.exists():
    shelf = []
    for p in posts:
        d = datetime.date.fromisoformat(p["date"])
        shelf.append(f'        <a class="piece" href="/{e(href(p).removesuffix(".html"))}" target="_blank" rel="noopener"><b>{e(p["title"])}</b><span class="date">{d.day} {d.strftime("%b %Y")}</span></a>')
    block = ('      <div class="series">\n' + "\n".join(shelf) + '\n      </div>\n'
             '      <p><a href="/writing" target="_blank" rel="noopener">All writing &rarr;</a></p>\n')
    h = home.read_text()
    a, b = "<!-- writing:start (generated by tools/render.py from content/posts.json) -->\n", "      <!-- writing:end -->"
    i, j = h.index(a) + len(a), h.index(b)
    home.write_text(h[:i] + block + h[j:])
    h = home.read_text()
    cards = []
    for p in projects:
        d = datetime.date.fromisoformat(p["date"])
        cards.append(f'        <a class="card" href="{e(p["href"])}" target="_blank" rel="noopener"><span class="date">{e(p["tag"])} · {d.year}</span><h3>{e(p["title"])}</h3><p>{e(p["short"])}</p></a>')
    block = ('      <div class="cards">\n' + "\n".join(cards) + '\n      </div>\n'
             '      <p><a href="/projects" target="_blank" rel="noopener">All projects &rarr;</a></p>\n')
    a, b = "<!-- projects:start (generated by tools/render.py from content/projects.json) -->\n", "      <!-- projects:end -->"
    i, j = h.index(a) + len(a), h.index(b)
    home.write_text(h[:i] + block + h[j:])
print("rendered", sum("body" in p for p in posts), "essays,", len(posts), "list items")
