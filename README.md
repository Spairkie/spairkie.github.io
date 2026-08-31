# spairkie.github.io

Personal portfolio for Hans Sai - Systems Administrator building toward security engineering.

**Live site: [spairkie.github.io](https://spairkie.github.io)**

## What it is

A single-file, hand-built portfolio: Active Directory / IT operations background, a terminal-style hero with a live three.js particle network, real projects (with test counts and MITRE ATT&CK mappings where relevant), and certifications with linked proof.

No framework, no build step, no bundler. `index.html` is the entire site - HTML, CSS, and JS inline, plus one CDN script (three.js) for the hero visualization.

## Structure

```
index.html          the site (everything lives here)
404.html             custom 404 page (served automatically by GitHub Pages)
manifest.json        web app manifest (icons, theme color)
favicon.ico          favicon
icons/               favicon/apple-touch-icon/manifest icon set
certs/               certification PDFs linked from the Education section
resume/              resume PDF linked from the hero
files/               vCard (not currently linked from the live site)
```

## Local preview

Nothing to install - open `index.html` directly in a browser, or serve the folder with any static server:

```bash
python3 -m http.server 8000
```

## Deploying

Push to `main`. GitHub Pages serves it directly, no build step.
