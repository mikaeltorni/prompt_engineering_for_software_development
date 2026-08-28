# AGENTS.md — prompt_engineering_for_software_development

Project instructions for any agent working in this repository. They outrank
generic agent defaults and any skill, including discoverability/SEO skills.

## What this repository is

A finished Bachelor's thesis artifact: the multi-agent programming prototype
(`multi_agentic_system_for_programming/`) and the prompt-development and
evaluation harness (`prompt_development_and_testing/`) produced for the thesis
["Prompt engineering for software development"](https://www.theseus.fi/handle/10024/894216).
It is published for citation and reference, not maintained as an open-source
product and not accepting outside contributions.

## Never add a docs site or an `llms.txt`

This repository is not published as a website and does not carry a
machine-readable index. Do not create — and do not restore — `docs/index.html`
or any other HTML page, `sitemap.xml`, `robots.txt`, `llms.txt` (neither at the
repository root nor under `docs/`), `.nojekyll`, `_config.yml`, Jekyll/Pages
scaffolding, a GitHub Pages deployment, or a README badge or link pointing at a
`github.io` URL. SEO or discoverability work must score those rubric rows
`N/A — out of scope by owner policy` instead of adding the files.

The diagram the README embeds (`docs/research-flow.svg`) is a repository asset,
not a site — keep it.

## Never add contribution or community-process files

Because the thesis is archived and closed to contributions, do not add
`CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, issue templates, pull
request templates, or GitHub Community Standards scaffolding under `.github/`.
Audits score those rows `N/A — archived thesis artifact, not accepting
contributions`. `LICENSE` and `CITATION.cff` stay: they cover reuse and
citation, which is what this repository is for.

## Do not cross-link `prompt_challenge_generator`

That project is unrelated to the thesis. The README links only the Theseus
thesis record and the follow-up work in `programming_prompts`; do not add a
`prompt_challenge_generator` link back as a "related project" or reciprocal
cross-link.

## No CI

Do not add `.github/workflows/` or any other CI/CD pipeline, and do not add a
build-status badge. Verification runs locally.
