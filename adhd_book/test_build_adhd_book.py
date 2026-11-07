"""Offline source-integrity tests for the Lean ADHD edition."""
import json
import tempfile
import unittest
from pathlib import Path
from build_adhd_book import build, verify

HTML = '''<!doctype html><html><head><title>FP Lean</title></head><body>
<nav>Navigation</nav><main><h1>Evaluating expressions</h1>
<p>Evaluation computes the value of a mathematical expression. The result is a value.</p>
<h2>Function application</h2><p>Function application places an argument after its function. Parentheses group arguments.</p>
<pre><code>#eval String.append "A" "B"\n#eval 1 + 2\n</code></pre>
<h2>Exercises</h2><p>Run the code above and verify its output.</p>
</main></body></html>'''

class EditionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.src = self.root / 'html'
        self.src.mkdir()
        (self.src/'index.html').write_text(HTML, encoding='utf8')
        (self.src/'asset.css').write_text('body{color:blue}', encoding='utf8')
        (self.src/'chapter').mkdir()
        (self.src/'chapter'/'index.html').write_text(HTML.replace('Evaluating expressions','Chapter'), encoding='utf8')
        self.out = self.root / 'edition'

    def tearDown(self):
        self.temp.cleanup()

    def run_build(self):
        return build(self.src, self.out, 'git-test-revision')

    def test_entire_original_html_preserved(self):
        m = self.run_build()
        self.assertEqual(m['page_count'],2)
        self.assertEqual(m['original_code_blocks'],2)
        self.assertEqual((self.out/'site/original/index.html').read_text(),HTML)
        verify(self.out)

    def test_original_exercises_and_code_in_markdown(self):
        self.run_build()
        md = (self.out/'markdown/index.md').read_text()
        self.assertIn('Run the code above',md)
        self.assertIn('#eval 1 + 2',md)

    def test_missing_original_page_fails(self):
        self.run_build()
        (self.out/'site/original/chapter/index.html').unlink()
        with self.assertRaises(AssertionError): verify(self.out)

    def test_missing_asset_fails(self):
        self.run_build()
        (self.out/'site/original/asset.css').unlink()
        with self.assertRaises(AssertionError): verify(self.out)

    def test_modified_code_fails(self):
        self.run_build()
        p=self.out/'site/adhd/index.html'
        p.write_text(p.read_text().replace('#eval 1 + 2','#eval 9 + 9'))
        with self.assertRaises(AssertionError): verify(self.out)

    def test_missing_markdown_fails(self):
        self.run_build()
        (self.out/'markdown/index.md').unlink()
        with self.assertRaises(AssertionError): verify(self.out)

    def test_manifest_tamper_fails(self):
        self.run_build()
        p=self.out/'manifest.json'
        m=json.loads(p.read_text());m['original_code_blocks']+=100
        p.write_text(json.dumps(m))
        with self.assertRaises(AssertionError): verify(self.out)

    def test_refuse_overwrite(self):
        self.run_build()
        with self.assertRaises(SystemExit): self.run_build()
        verify(self.out)

    def test_source_missing_causes_atomic_abort(self):
        (self.src/'index.html').unlink()
        with self.assertRaises(SystemExit): self.run_build()
        self.assertFalse(self.out.exists())

    def test_symlinks_preserved(self):
        (self.src/'link.css').symlink_to('asset.css')
        self.run_build()
        self.assertTrue((self.out/'site/original/link.css').is_symlink())
        verify(self.out)

if __name__ == '__main__':
    unittest.main()
