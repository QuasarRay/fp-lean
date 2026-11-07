#!/usr/bin/env python3
"""Generate a non-destructive ADHD companion from the official Verso HTML output.

The unmodified renderer output is the primary fidelity authority. Supplementary
HTML/Markdown are never substituted for it during verification.
"""
from __future__ import annotations

import argparse
import hashlib
import html as html_mod
import json
import re
import shutil
from pathlib import Path

from bs4 import BeautifulSoup, Tag
from markdownify import markdownify as html_to_md

CSS = """/* Opt-in reading layer; original pages live at ../original/ */
.adhd-guide { border: 2px solid #496c92; border-radius: .65rem;
  padding: 1rem; margin: 1.2rem 0; background: #f2f7fb; color: #18283a; }
.adhd-guide h2 { font-size: 1.12rem; margin: 0 0 .5rem; }
.adhd-guide p { margin: .35rem 0; }
.adhd-quick { border-left: 3px solid #496c92; padding: .35rem .9rem;
  margin: .75rem 0; background: #f8fafc; }
.adhd-quick summary { font-weight: 600; cursor: pointer; }
@media (prefers-color-scheme: dark) {
 .adhd-guide,.adhd-quick { background:#202a34; color:#eff4fa; }
}
"""


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pages(root: Path) -> list[Path]:
    return sorted(root.rglob('*.html'))


def content(soup: BeautifulSoup) -> Tag:
    target = soup.select_one('main, article, [role="main"]')
    if target is None:
        target = soup.body
    if target is None:
        raise ValueError('HTML has no <body> or main content')
    return target


def asset_inventory(root: Path) -> dict[str, dict[str, str]]:
    """Record assets including symlink targets, to detect scope reduction."""
    out: dict[str, dict[str, str]] = {}
    for path in sorted(root.rglob('*')):
        rel = path.relative_to(root).as_posix()
        if path.is_symlink():
            out[rel] = {'kind': 'link', 'target': str(path.readlink())}
        elif path.is_file():
            out[rel] = {'kind': 'file', 'sha256': digest(path)}
    return out


def source_snippets(node: Tag) -> list[str]:
    return [p.get_text() for p in node.select('pre')]


def source_headings(node: Tag) -> list[str]:
    return [h.get_text(' ', strip=True) for h in node.select('h1,h2,h3,h4,h5,h6')]


def meaningful_sentence(heading: Tag) -> str | None:
    """Use a *verbatim* short source passage, never invent a definition."""
    for sibling in heading.next_elements:
        if sibling is heading:
            continue
        if isinstance(sibling, Tag) and sibling.name in {'h1','h2','h3','h4','h5','h6'}:
            break
        if not isinstance(sibling, Tag) or sibling.name != 'p':
            continue
        raw = ' '.join(sibling.stripped_strings)
        if len(raw) < 28:
            continue
        found = re.search(r'(.{25,}?[.!?])(?:\s|$)', raw)
        sentence = (found.group(1) if found else raw).strip()
        # Do not truncate a sentence in the middle; a long one is better than an invented summary.
        return sentence if len(sentence) <= 380 else None
    return None


def inject_reading_aids(original_html: str) -> tuple[str, list[dict[str,str]], list[str]]:
    soup = BeautifulSoup(original_html, 'html.parser')
    page = content(soup)
    headings = list(page.select('h1,h2,h3,h4,h5,h6'))
    definitions: list[dict[str,str]] = []
    gaps: list[str] = []
    if not soup.head:
        raise ValueError('HTML has no <head>, cannot add stylesheet without losing structure')
    link = soup.new_tag('link', rel='stylesheet', href='__ADHD_STYLESHEET__')
    link['data-adhd-generated'] = '1'
    soup.head.append(link)
    guide = soup.new_tag('section', **{'class':'adhd-guide','data-adhd-generated':'1','aria-label':'Reading directions'})
    title = soup.new_tag('h2')
    title.string = 'Reading map — original content is unchanged'
    guide.append(title)
    goal = soup.new_tag('p')
    goal.string = 'Read one subsection. Run its original Lean examples. Attempt its exercises. Mark your progress before continuing.'
    guide.append(goal)
    details = soup.new_tag('p')
    details.string = 'Use the collapsible concept snapshots to recall the source explanation; they are excerpts, not replacement lessons.'
    guide.append(details)
    page.insert(0, guide)
    for heading in headings:
        name = heading.get_text(' ', strip=True)
        if not name:
            continue
        if name.lower().strip() in {'exercises','exercise','solutions','solution','summary','contents','acknowledgments'}:
            continue
        sentence = meaningful_sentence(heading)
        if not sentence:
            gaps.append(name)
            continue
        definitions.append({'heading':name,'source_excerpt':sentence})
        box = soup.new_tag('details', **{'class':'adhd-quick','data-adhd-generated':'1'})
        summary = soup.new_tag('summary')
        summary.string = 'Concept snapshot: ' + name
        box.append(summary)
        p = soup.new_tag('p')
        p.string = sentence
        box.append(p)
        heading.insert_after(box)
    return str(soup), definitions, gaps


def without_generated(soup: BeautifulSoup) -> BeautifulSoup:
    for x in soup.select('[data-adhd-generated="1"]'):
        x.decompose()
    return soup


def original_text(soup: BeautifulSoup) -> str:
    return content(soup).get_text()


def markdown_page(original: str, title: str, rel: Path,
                  definitions: list[dict[str,str]], gaps: list[str]) -> str:
    soup = BeautifulSoup(original, 'html.parser')
    node = content(soup)
    # Preserve all code *verbatim* by replacing pre blocks with opaque placeholders.
    snippets: list[str] = []
    for pre in list(node.select('pre')):
        n = len(snippets)
        snippets.append(pre.get_text())
        p = soup.new_tag('p')
        p.string = f'ADHDORIGINALCODEBLOCK{n:07d}END'
        pre.replace_with(p)
    body = html_to_md(str(node), heading_style='ATX', bullets='-', strip=['script','style']).strip()
    for n, source in enumerate(snippets):
        token = f'ADHDORIGINALCODEBLOCK{n:07d}END'
        if body.count(token) != 1:
            raise RuntimeError(f'Markdown placeholder lost or duplicated: {rel}: {token}')
        ticks = '`' * max(3, max([len(x) for x in re.findall(r'`+', source)] or [0])+1)
        fence = f'\n{ticks}lean\n{source.rstrip(chr(10))}\n{ticks}\n'
        body = body.replace(token, fence)
    lens = [f'- **{x["heading"]}** — {x["source_excerpt"]}' for x in definitions]
    if not lens:
        lens = ['- No source-derived concept snapshot was available on this page. Read the complete original explanation below.']
    # Chapter text is included in its entirety below, after the one-screen navigation.
    lines = [f'# Study guide: {title}', '',
             '> This page is a companion transcription. The authoritative, complete rendered book is in `site/original/`.',
             '> The ADHD website in `site/adhd/` retains every original rendered paragraph and code block.', '',
             '## Quick concept reference (source excerpts)', '', *lens, '',
             '## One-section checklist', '',
             '- [ ] Read one subsection of the full lesson.',
             '- [ ] Run all Lean examples, including examples that intentionally produce errors.',
             '- [ ] Attempt every original exercise.',
             '- [ ] Explain the main idea using one sentence.', '',
             '---', '', '## Complete source lesson', '', body, '']
    if gaps:
        lines += ['', '> **Review needed:** The following headings have no short source sentence: ' + ', '.join(gaps)]
    return '\n'.join(lines)


def manifest_path(output: Path) -> Path:
    return output / 'manifest.json'


def build(html_root: Path, output: Path, revision: str) -> dict:
    if not (html_root / 'index.html').is_file():
        raise SystemExit('Expected a full official HTML build with index.html')
    if output.resolve() == html_root.resolve() or html_root.resolve() in output.resolve().parents:
        raise SystemExit('Output must not be inside original HTML source tree')
    if output.exists():
        raise SystemExit('Refusing to overwrite an existing edition; choose a new output path')
    tmp = output.with_name(output.name + '.partial')
    if tmp.exists():
        raise SystemExit(f'Staging directory already exists: {tmp}')
    original_dir = tmp / 'site' / 'original'
    enhanced_dir = tmp / 'site' / 'adhd'
    original_paths = pages(html_root)
    if not original_paths:
        raise SystemExit('No HTML pages in the official book build')
    try:
        shutil.copytree(html_root, original_dir, symlinks=True)
        shutil.copytree(html_root, enhanced_dir, symlinks=True)
        (enhanced_dir/'_adhd.css').write_text(CSS, encoding='utf-8')
        entries = []
        for page in original_paths:
            rel = page.relative_to(html_root)
            text = page.read_text(encoding='utf-8')
            soup = BeautifulSoup(text, 'html.parser')
            body = content(soup)
            original_code = source_snippets(body)
            original_headers = source_headings(body)
            enhanced, notes, gaps = inject_reading_aids(text)
            relative_css = Path(*['..']*len(rel.parent.parts)) / '_adhd.css'
            enhanced = enhanced.replace('__ADHD_STYLESHEET__', relative_css.as_posix())
            enhanced_path = enhanced_dir / rel
            enhanced_path.write_text(enhanced, encoding='utf-8')
            # Require that no source content is deleted when the reading aids are added.
            clean = without_generated(BeautifulSoup(enhanced, 'html.parser'))
            if (source_snippets(content(clean)) != original_code
                or source_headings(content(clean)) != original_headers
                or original_text(clean) != original_text(soup)):
                raise RuntimeError(f'Enhanced HTML changed original content: {rel}')
            h1 = original_headers[0] if original_headers else rel.as_posix()
            md = markdown_page(text, h1, rel, notes, gaps)
            dest = tmp / 'markdown' / rel.with_suffix('.md')
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(md, encoding='utf-8')
            entries.append({'source_html':rel.as_posix(),'source_sha256':digest(page),
                 'code_blocks':len(original_code),'headings':len(original_headers),
                 'concept_snapshots':len(notes),'unresolved_headings':gaps,
                 'enhanced_sha256':digest(enhanced_path),'markdown_sha256':digest(dest)})
        (tmp / 'README.md').write_text(
             '# Complete Functional Programming in Lean — ADHD reading edition\n\n'
             'The complete, unmodified official HTML book is under `site/original/`.\n'
             'The ADHD-enhanced HTML retains all original text and code under `site/adhd/`.\n'
             'The `markdown/` tree provides a per-page Markdown transcription with concise source excerpts and checklists.\n'
             'Markdown is supplementary and may not reproduce all interactive Verso features.\n'
             'Read `manifest.json` and inspect any `unresolved_headings` before claiming all concepts have been explained.\n\n'
             'Original: David Thrane Christiansen; Microsoft Corporation / Lean FRO, LLC. CC BY 4.0.\n'
             'Source: https://github.com/leanprover/fp-lean\n', encoding='utf-8')
        manifest = {'status':'HTML_FULL_SOURCE_WITH_ADHD_SUPPLEMENTS',
             'original_repository':'https://github.com/leanprover/fp-lean',
             'book_source_revision':revision,'pages':entries,
             'page_count':len(entries),'original_code_blocks':sum(x['code_blocks'] for x in entries),
             'source_explanations':sum(x['concept_snapshots'] for x in entries),
             'original_asset_inventory':asset_inventory(original_dir),
             'unresolved_heading_count':sum(len(x['unresolved_headings']) for x in entries)}
        manifest_path(tmp).write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n', encoding='utf-8')
        verify(tmp)
        tmp.rename(output)
        return manifest
    except BaseException:
        shutil.rmtree(tmp,ignore_errors=True)
        raise


def verify(output: Path) -> dict:
    manifest = json.loads(manifest_path(output).read_text(encoding='utf-8'))
    original_root = output/'site'/'original'
    enhanced_root = output/'site'/'adhd'
    found = {p.relative_to(original_root).as_posix() for p in pages(original_root)}
    expected = {x['source_html'] for x in manifest['pages']}
    if manifest.get('original_asset_inventory') != asset_inventory(original_root):
        raise AssertionError('Original HTML assets removed or modified')
    if not expected or found != expected:
        raise AssertionError(f'HTML page inventory mismatch (missing={expected-found}, extra={found-expected})')
    total_code = 0
    total_notes = 0
    total_gaps = 0
    for entry in manifest['pages']:
        rel = Path(entry['source_html'])
        original = original_root/rel
        enhanced = enhanced_root/rel
        markdown = output/'markdown'/rel.with_suffix('.md')
        for f in (original,enhanced,markdown):
            if not f.is_file():
                raise AssertionError(f'Missing edition file: {f}')
        if digest(original)!=entry['source_sha256'] or digest(enhanced)!=entry['enhanced_sha256'] or digest(markdown)!=entry['markdown_sha256']:
            raise AssertionError(f'Content checksum mismatch: {rel}')
        source = BeautifulSoup(original.read_text(encoding='utf-8'),'html.parser')
        new = without_generated(BeautifulSoup(enhanced.read_text(encoding='utf-8'),'html.parser'))
        if (original_text(source)!=original_text(new) or
            source_snippets(content(source))!=source_snippets(content(new)) or
            source_headings(content(source))!=source_headings(content(new))):
            raise AssertionError(f'Fidelity mismatch: {rel}')
        code = source_snippets(content(source))
        # Markdown fenced blocks must preserve every literal code payload in order.
        md = markdown.read_text(encoding='utf-8')
        blocks = [m.group(2) for m in re.finditer(r'^(`{3,})lean\n(.*?)^\1\s*$',md,re.M|re.S)]
        if [s.rstrip('\n') for s in code] != [b.rstrip('\n') for b in blocks]:
            raise AssertionError(f'Markdown code mismatch: {rel}')
        if len(code)!=entry['code_blocks'] or len(source_headings(content(source)))!=entry['headings']:
            raise AssertionError(f'Incorrect source counts: {rel}')
        total_code += len(code)
        total_notes += entry['concept_snapshots']
        total_gaps += len(entry['unresolved_headings'])
    if (manifest['page_count']!=len(expected) or manifest['original_code_blocks']!=total_code or
        manifest['source_explanations']!=total_notes or manifest['unresolved_heading_count']!=total_gaps):
        raise AssertionError('Manifest global counts invalid')
    return manifest


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    sub=p.add_subparsers(dest='mode',required=True)
    b=sub.add_parser('build')
    b.add_argument('--html',type=Path,required=True)
    b.add_argument('--output',type=Path,required=True)
    b.add_argument('--revision',required=True)
    v=sub.add_parser('verify')
    v.add_argument('--output',type=Path,required=True)
    a=p.parse_args()
    result=build(a.html,a.output,a.revision) if a.mode=='build' else verify(a.output)
    print(json.dumps({k:result[k] for k in ['status','page_count','original_code_blocks','source_explanations','unresolved_heading_count']},indent=2))

if __name__=='__main__':
    main()
