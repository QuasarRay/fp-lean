# ADHD-friendly complete edition of Functional Programming in Lean

This branch leaves the authoritative Lean/Verso book and its examples unchanged.

## How to get the complete book

1. Open the Actions tab for the QuasarRay/fp-lean repository.
2. Run (or locate the push-triggered run of) the workflow named "Complete ADHD book (official Lean/Verso renderer)".
3. Download the artifact "complete-fp-lean-adhd-book".
4. Unzip and open ADHD_BOOK/site/adhd/index.html through a local HTTP server, or browse ADHD_BOOK/markdown for the complete Markdown chapter transcriptions.

The workflow builds the full book with the official Lake / Verso pipeline. The output contains unchanged original HTML (site/original), an additive ADHD reading layer (site/adhd), Markdown transcripts (markdown/), an integrity manifest, and full static assets. On successful branch runs, the Markdown files and manifest are also committed to this branch automatically.

## Reproduce locally

Install the project's Lean toolchains as described in the upstream README, plus Python 3.10+ and the two Python dependencies (beautifulsoup4 4.14.3, markdownify 1.2.2). Build the examples and book using the existing project instructions. Then run:

    python adhd_book/build_adhd_book.py build --html book/_out/html-multi --output ADHD_BOOK --revision "$(git rev-parse HEAD)"
    python adhd_book/build_adhd_book.py verify --output ADHD_BOOK

The generator source is supplied initially as a reproducible gzip bootstrap; the successful workflow writes the readable Python source to the branch and removes the bootstrap.

## Fidelity and limitations

The full original HTML and assets remain byte-identical in site/original. The ADHD HTML retains the same original headings, text and preformatted code blocks, adding collapsible source-derived concept excerpts and bounded reading actions. The Markdown transcriptions preserve the preformatted code payloads; dynamic Verso interactions and visual formatting should be read in the HTML edition.

A source-derived snapshot for a section is not a verified pedagogical paraphrase. The manifest records any headings with no concise source excerpt. This pipeline is NOT a certificate that every independently named concept has a human-reviewed concise definition.

Copyright and attribution: Functional Programming in Lean by David Thrane Christiansen, Microsoft Corporation (2023) and Lean FRO, LLC (2023-2026), CC BY 4.0. The authoritative upstream is https://github.com/leanprover/fp-lean .
