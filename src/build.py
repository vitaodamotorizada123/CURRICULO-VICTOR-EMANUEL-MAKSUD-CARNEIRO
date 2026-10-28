"""Gera index.html (inglês) e pt/index.html (português) a partir de src/content.py.

Uso:  python3 src/build.py
"""
from html import escape
from pathlib import Path

from content import EN, PT, SITE_URL, EMAIL, LINKEDIN, GITHUB, PDF_FILE

ROOT = Path(__file__).resolve().parent.parent

FONTS = "https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400..800&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap"

ICON = {
    "download": '<path d="M12 3v12"/><path d="m7 10 5 5 5-5"/><path d="M5 21h14"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
    "out": '<path d="M7 17 17 7"/><path d="M8 7h9v9"/>',
    "pin": '<path d="M12 21s-7-6.2-7-12a7 7 0 0 1 14 0c0 5.8-7 12-7 12z"/><circle cx="12" cy="9" r="2.5"/>',
    "id": '<rect x="4" y="3" width="16" height="18" rx="2"/><circle cx="12" cy="10" r="3"/><path d="M8 17h8"/>',
    "cap": '<path d="m2 9 10-5 10 5-10 5z"/><path d="M6 11v5c0 1.5 2.7 3 6 3s6-1.5 6-3v-5"/>',
    "spark": '<path d="M12 3v4"/><path d="M12 17v4"/><path d="M3 12h4"/><path d="M17 12h4"/><path d="m6 6 2.5 2.5"/><path d="m15.5 15.5 2.5 2.5"/><path d="m6 18 2.5-2.5"/><path d="m15.5 8.5 2.5-2.5"/>',
}


def icon(name, size=16, stroke="currentColor"):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{stroke}" '
            f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICON[name]}</svg>')


def e(text):
    return escape(text, quote=True)


def section(sid, num, label, body, full=""):
    return f"""
<section class="section wrap" id="{sid}" aria-labelledby="{sid}-h">
<div class="section-grid">
<div class="section-label"><p class="num">{num}</p><h2 id="{sid}-h">{e(label)}</h2></div>
{body}{full}
</div>
</section>"""


def page(t, prefix, en_href, pt_href, canonical):
    is_en = t["html_lang"] == "en"
    nav = t["nav"]
    out_icon = icon("out", 14)

    chips = "".join(
        f'<span class="chip">{icon(i, 16, "#8EA8FF")}<span>{e(label)}</span></span>'
        for i, label in (("pin", t["chip_location"]), ("id", t["chip_visa"]), ("cap", t["chip_grad"]))
    )
    glance = "".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in t["glance"])

    open_to = "".join(f'<span class="pill-accent">{e(o)}</span>' for o in t["open_to"])
    profile = f"""<div class="section-body">
<p class="profile-lead">{e(t["profile1"])}</p>
<p class="profile-text">{e(t["profile2"])}</p>
<div class="open-to"><span class="eyebrow">{e(t["open_to_label"])}</span>{open_to}</div>
<p class="availability"><span class="dot"></span><span>{e(t["availability"])}</span></p>
</div>"""

    jobs = []
    for job in t["experience"]:
        bullets = "".join(f"<li>{e(b)}</li>" for b in job["bullets"])
        tags = "".join(f'<span class="tag">{e(x)}</span>' for x in job["tags"])
        jobs.append(f"""<article class="job">
<div class="row-between"><h3>{e(job["role"])}</h3><p class="dates">{e(job["dates"])}</p></div>
<p class="org">{e(job["org"])} <span>· {e(job["place"])}</span></p>
<p class="job-summary">{e(job["summary"])}</p>
<ul>{bullets}</ul>
<div class="tags">{tags}</div>
</article>""")
    experience = f'<div class="section-body jobs">{"".join(jobs)}</div>'

    cards = []
    for i, p in enumerate(t["projects"], start=1):
        tags = "".join(f'<span class="tag">{e(x)}</span>' for x in p["tags"])
        link = ""
        if p["url"]:
            label = t["open_app"] if p.get("app") else t["visit"]
            link = (f'<a class="card-link" href="{e(p["url"])}" target="_blank" rel="noopener">'
                    f'{e(label)}<span class="sr-only"> — {e(p["title"])}</span>{icon("out", 15)}</a>')
        cards.append(f"""<article class="card">
<div class="card-top"><span class="status status-{p["s"]}"><span class="dot"></span>{e(t["status"][p["s"]])}</span><span class="card-num">{i:02d}</span></div>
<div><h3>{e(p["title"])}</h3><p class="kind">{e(p["kind"])}</p></div>
<p class="card-desc">{e(p["desc"])}</p>
<div class="tags">{tags}</div>
{link}
</article>""")
    projects_intro = f'<div class="section-body"><p class="intro">{e(t["projects_intro"])}</p></div>'
    projects_full = f'\n<div class="section-full cards">{"".join(cards)}</div>'

    groups = "".join(
        f'<div class="skill-group"><h3>{e(title)}</h3><ul class="skill-list">{"".join(f"<li>{e(s)}</li>" for s in items)}</ul></div>'
        for title, items in t["skills"]
    )
    skills = f'<div class="section-body skill-groups">{groups}</div>'

    coursework = "".join(f"<li>{e(c)}</li>" for c in t["coursework"])
    highlights = "".join(f"<li>{icon('spark', 18, '#E2620F')}<span>{e(h)}</span></li>" for h in t["edu_highlights"])
    education = f"""<div class="section-body edu">
<article class="edu-card">
<div class="row-between" style="align-items:flex-start">
<div><h3>{e(t["degree"])}</h3><p class="edu-local" lang="pt-BR">Bacharelado em Sistemas de Informação</p></div>
<span class="badge">{e(t["grad_badge"])}</span>
</div>
<p class="edu-school"><strong>Centro Universitário de Belo Horizonte (UniBH)</strong> · {e(t["edu_place"])}</p>
<p class="edu-meta">{e(t["edu_meta"])}</p>
<div class="edu-block"><span class="eyebrow">{e(t["coursework_label"])}</span><ul class="coursework">{coursework}</ul></div>
<ul class="highlights edu-block">{highlights}</ul>
</article>
<article class="exchange">
<div><p class="title">{e(t["exchange_title"])}</p><p class="where">{e(t["exchange_where"])}</p></div>
<span class="dates">{e(t["exchange_dates"])}</span>
</article>
</div>"""

    certs = "".join(
        f"""<li><div class="cert-main"><p class="cert-name">{e(c["name"])}</p><p class="cert-issuer">{e(c["issuer"])}</p>{f'<p class="cert-id">{e(c["id"])}</p>' if c["id"] else ""}</div><span class="dates">{e(c["date"])}</span></li>"""
        for c in t["certs"]
    )
    certificates = f'<ol class="section-body certs">{certs}</ol>'

    langs = "".join(f'<div class="lang-row"><strong>{e(n)}</strong><span>{e(lv)}</span></div>' for n, lv in t["langs"])
    languages = f"""<div class="section-body duo">
<div class="box box-wide">{langs}</div>
<div class="box box-narrow"><p class="eyebrow" style="margin:0">{e(t["ref_label"])}</p><p class="box-strong">{e(t["ref_text"])}</p></div>
</div>"""

    pdf = f"{prefix}{PDF_FILE}"
    en_current = ' aria-current="page"' if is_en else ""
    pt_current = "" if is_en else ' aria-current="page"'

    return f"""<!doctype html>
<html lang="{t["html_lang"]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(t["title"])}</title>
<meta name="description" content="{e(t["meta_description"])}">
<meta name="theme-color" content="#0B1020">
<link rel="canonical" href="{canonical}">
<link rel="alternate" hreflang="en" href="{SITE_URL}/">
<link rel="alternate" hreflang="pt-BR" href="{SITE_URL}/pt/">
<link rel="alternate" hreflang="x-default" href="{SITE_URL}/">
<meta property="og:type" content="profile">
<meta property="og:title" content="{e(t["title"])}">
<meta property="og:description" content="{e(t["meta_description"])}">
<meta property="og:url" content="{canonical}">
<link rel="icon" href="{prefix}assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{e(FONTS)}">
<link rel="stylesheet" href="{prefix}assets/style.css">
</head>
<body>
<a class="skip" href="#main">{e(t["skip"])}</a>
<header class="hero" id="top">
<div class="wrap">
<nav class="nav" aria-label="Primary">
<div class="nav-top">
<a class="brand" href="#top">Victor Maksud</a>
<div class="nav-actions">
<div class="lang" role="group" aria-label="{e(t["lang_label"])}">
<a href="{en_href}" hreflang="en" lang="en"{en_current}>EN</a>
<a href="{pt_href}" hreflang="pt-BR" lang="pt-BR"{pt_current}>PT</a>
</div>
<a class="btn btn-light btn-sm" href="{pdf}" aria-label="{e(t["pdf_label"])}">{icon("download")}<span>{e(t["pdf_short"])}</span></a>
</div>
</div>
<div class="nav-links">
<a href="#profile">{e(nav["profile"])}</a>
<a href="#experience">{e(nav["experience"])}</a>
<a href="#projects">{e(nav["projects"])}</a>
<a href="#skills">{e(nav["skills"])}</a>
<a href="#education">{e(nav["education"])}</a>
<a href="#contact">{e(nav["contact"])}</a>
</div>
</nav>
<div class="hero-body">
<div class="hero-main">
<p class="eyebrow">{e(t["hero_eyebrow"])}</p>
<h1>Victor<br>Maksud</h1>
<p class="lead">{e(t["hero_lead"])}</p>
<div class="chips">{chips}</div>
<div class="cta">
<a class="btn btn-primary" href="{pdf}">{icon("download", 18)}<span>{e(t["cta_resume"])}</span></a>
<a class="btn btn-ghost" href="mailto:{EMAIL}">{icon("mail", 18)}<span>{e(t["cta_email"])}</span></a>
<div class="text-links">
<a class="text-link" href="{LINKEDIN}" target="_blank" rel="noopener">LinkedIn{out_icon}</a>
<a class="text-link" href="{GITHUB}" target="_blank" rel="noopener">GitHub{out_icon}</a>
</div>
</div>
</div>
<aside class="glance" aria-label="{e(t["glance_title"])}">
<div class="glance-head"><span class="eyebrow">{e(t["glance_title"])}</span><span class="coords"><span class="dot" style="background:#FF8A3D"></span>28.0° S · 153.4° E</span></div>
<div class="glance-route"><span>Belo Horizonte</span><svg width="56" height="14" viewBox="0 0 56 14" fill="none" aria-hidden="true"><path d="M2 12 C 18 0, 38 0, 54 12" stroke="#8EA8FF" stroke-width="1.5" stroke-dasharray="3 3"/><circle cx="54" cy="12" r="2" fill="#FF8A3D"/></svg><strong>Gold Coast</strong></div>
<dl>{glance}</dl>
</aside>
</div>
</div>
</header>

<main id="main">
{section("profile", "01", t["profile_label"], profile)}
{section("experience", "02", t["experience_label"], experience)}
{section("projects", "03", t["projects_label"], projects_intro, projects_full)}
{section("skills", "04", t["skills_label"], skills)}
{section("education", "05", t["education_label"], education)}
{section("certificates", "06", t["certs_label"], certificates)}
{section("languages", "07", t["langs_label"], languages)}
</main>

<footer class="footer" id="contact">
<div class="wrap">
<p class="eyebrow">{e(nav["contact"])}</p>
<h2>{e(t["contact_title"])}</h2>
<p class="footer-text">{e(t["contact_text"])}</p>
<div class="footer-actions">
<a class="btn btn-primary" href="mailto:{EMAIL}">{icon("mail", 18)}<span>{EMAIL}</span></a>
<a class="btn btn-ghost" href="{LINKEDIN}" target="_blank" rel="noopener">LinkedIn{icon("out", 15)}</a>
<a class="btn btn-ghost" href="{GITHUB}" target="_blank" rel="noopener">GitHub{icon("out", 15)}</a>
<a class="btn btn-ghost" href="{pdf}">{icon("download", 18)}<span>{e(t["pdf_short"])}</span></a>
</div>
<div class="footer-bottom"><span>© 2026 Victor Emanuel Maksud Carneiro</span><span>{e(t["footer_note"])}</span></div>
</div>
</footer>
</body>
</html>
"""


def main():
    (ROOT / "index.html").write_text(page(EN, "", "./", "pt/", f"{SITE_URL}/"), encoding="utf-8")
    (ROOT / "pt").mkdir(exist_ok=True)
    (ROOT / "pt" / "index.html").write_text(page(PT, "../", "../", "./", f"{SITE_URL}/pt/"), encoding="utf-8")
    print("ok: index.html, pt/index.html")


if __name__ == "__main__":
    main()
