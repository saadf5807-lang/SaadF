"""Render summaries/*.md to pdf/*.pdf via headless Chromium.
Usage: python3 tools/build_pdf.py   (requires: pip install markdown)"""
import glob, os, re, subprocess, sys, markdown

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROME = os.environ.get("CHROME", "/opt/pw-browsers/chromium-1194/chrome-linux/chrome")

CSS = """
@page { size: A4; margin: 14mm 12mm 16mm 12mm; }
body { font-family: 'DejaVu Sans', Arial, sans-serif; font-size: 10pt; line-height: 1.4; color: #1a1a1a; }
h1 { font-size: 19pt; color: #0b3d6b; border-bottom: 3px solid #0b3d6b; padding-bottom: 4px; }
h2 { font-size: 14pt; color: #fff; background: #0b3d6b; padding: 5px 8px; margin-top: 22px; page-break-after: avoid; }
h3 { font-size: 12pt; color: #0b3d6b; border-left: 4px solid #d9822b; padding-left: 6px; margin-top: 16px; page-break-after: avoid; }
table { border-collapse: collapse; width: 100%; margin: 6px 0 10px; font-size: 9pt; page-break-inside: auto; }
tr { page-break-inside: avoid; }
th { background: #dde8f3; color: #0b3d6b; text-align: left; }
th, td { border: 1px solid #9fb3c8; padding: 3px 5px; vertical-align: top; }
tr:nth-child(even) td { background: #f6f9fc; }
blockquote { background: #fff7e8; border-left: 5px solid #d9822b; margin: 12px 0; padding: 6px 10px; page-break-inside: avoid; }
blockquote p { margin: 4px 0; }
code, pre { font-family: 'DejaVu Sans Mono', monospace; font-size: 8.5pt; }
pre { background: #f2f2f2; padding: 6px; border-radius: 3px; }
strong { color: #7a1010; }
th strong { color: inherit; }
hr { border: 0; border-top: 1px solid #ccc; margin: 14px 0; }
ul, ol { margin: 4px 0 6px; padding-left: 20px; }
li { margin: 1px 0; }
.figrow { display: flex; gap: 8px; justify-content: center; align-items: flex-end; margin: 8px 0 12px; page-break-inside: avoid; }
.figrow figure { margin: 0; flex: 1 1 0; text-align: center; }
.figrow.n1 figure { max-width: 100%; }
figure img { max-width: 100%; max-height: 105mm; border: 1px solid #c9d3de; border-radius: 3px; }
figcaption { font-size: 8.3pt; color: #4a5a6a; font-style: italic; margin-top: 2px; }
"""

IMG = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)\)")

def figure_html(line):
    """A line holding only images becomes a figure row (side by side if several)."""
    imgs = IMG.findall(line)
    if not imgs or IMG.sub("", line).strip():
        return None
    cells = "".join(f'<figure><img src="{src}"><figcaption>{cap}</figcaption></figure>' for cap, src in imgs)
    return f'<div class="figrow n{len(imgs)}">{cells}</div>'

LIST = re.compile(r"^\s*([-*+]|\d+\.)\s")

def normalize(text):
    """Python-Markdown needs a blank line before tables/lists; split blockquote lines into paragraphs."""
    out, prev = [], ""
    for line in text.split("\n"):
        fig = figure_html(line)
        if fig:
            out += ["", fig, ""]
            prev = ""
            continue
        m = re.match(r"^( +)([-*+]|\d+\.)\s", line)
        if m:  # re-indent nested list items to 4 spaces per level
            line = "    " * ((len(m.group(1)) + 2) // 3) + line.lstrip()
        is_tbl, prev_tbl = line.startswith("|"), prev.startswith("|")
        is_list, prev_list = bool(LIST.match(line)), bool(LIST.match(prev)) or prev.startswith("  ")
        is_bq, prev_bq = line.startswith(">"), prev.startswith(">")
        if prev.strip() and ((is_tbl and not prev_tbl) or (is_list and not prev_list and not prev_tbl)):
            out.append("")
        if is_bq and prev_bq and line.strip() != ">" and prev.strip() != ">":
            out.append(">")
        out.append(line)
        prev = line
    return "\n".join(out)

def build(md_path):
    name = os.path.splitext(os.path.basename(md_path))[0]
    body = markdown.markdown(normalize(open(md_path, encoding="utf-8").read()),
                             extensions=["tables", "fenced_code", "sane_lists"])
    html_path = os.path.join(ROOT, "pdf", name + ".html")
    pdf_path = os.path.join(ROOT, "pdf", name + ".pdf")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(f"<!doctype html><html><head><meta charset='utf-8'><title>{name}</title>"
                f"<style>{CSS}</style></head><body>{body}</body></html>")
    subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu",
                    "--no-pdf-header-footer", f"--print-to-pdf={pdf_path}",
                    "file://" + html_path], check=True, capture_output=True)
    os.remove(html_path)
    print(pdf_path)

if __name__ == "__main__":
    os.makedirs(os.path.join(ROOT, "pdf"), exist_ok=True)
    for p in sys.argv[1:] or sorted(glob.glob(os.path.join(ROOT, "summaries", "*.md"))):
        build(p)
