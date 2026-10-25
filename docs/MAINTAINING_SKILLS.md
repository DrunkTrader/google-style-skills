# Maintaining the skills

The skills are a reviewed adaptation, not an automatic mirror. Update them when the official guides change or when an Agent Skills host changes its discovery contract.

## Update workflow

1. **Re-fetch the discovery entry point.** Open <https://google.github.io/styleguide/> and verify the four destination URLs, redirects, page titles, and licensing text. Do not assume a link or filename is unchanged.
2. **Capture upstream state.** Record the retrieval date, repository commit/tag when identifiable, page URLs, and any material page notes in each `source-and-license.md` and `NOTICE.md`.
3. **Retrieve the complete guides.** Prefer the official repository checkout for large HTML/Markdown documents, then compare the rendered official pages. Extract headings and inspect sections, examples, exceptions, and linked tooling recommendations—not only the introduction or table of contents.
4. **Diff the outline.** Compare new, removed, renamed, and moved headings with `docs/SOURCE_MAPPING.md`. Mark any uncertain mapping as **Not yet covered** during the work; do not silently map it to a vaguely similar topic.
5. **Update references.** Preserve the distinction between mandatory rules, recommendations, exceptions, rationale, generated-code/tool-specific boundaries, and version-dependent guidance. Prefer concise paraphrasing and original examples over copying large passages.
6. **Review attribution/licensing.** Re-check Google's license statement. Keep CC BY attribution for guide prose and Apache 2.0 notices for any derived code examples. Update `NOTICE.md` if the source terms or upstream assets change.
7. **Update skill metadata only when needed.** Keep names compliant and descriptions trigger-focused. Do not add agent-specific frontmatter that breaks the open specification unless it is explicitly optional and documented.
8. **Run checks.** Execute `python3 scripts/validate.py`, `python3 -m unittest discover -s tests -v`, and any available `skills-ref validate` command. Use temporary destinations for installer tests.
9. **Review language-model behavior.** Run representative prompts from `tests/fixtures/style-scenarios.json` through the supported agents when available. Record this separately from deterministic validation; passing structural tests does not prove an LLM will follow every rule.
10. **Report source changes.** Summarize added/removed/changed sections, rule-strength changes, codebase marker changes, tool recommendations, and any source change that could not be mapped confidently.

## Suggested source-diff commands

```bash
git clone --depth 1 https://github.com/google/styleguide.git /tmp/google-styleguide-source
git -C /tmp/google-styleguide-source show -s --format='%H %aI %s' HEAD
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
```

For a historical update, fetch the previous commit separately and compare only the four source files. Do not add other Google language guides to this pack unless the project scope is intentionally changed.

## Quality gates for a source update

- Every new substantive heading has a row in `SOURCE_MAPPING.md`.
- Every row has a local reference or an explicit documented exclusion.
- The skill body remains concise enough for progressive disclosure.
- Upstream links and local relative links resolve.
- The installer still installs one language independently.
- No source example is copied at length without the required license treatment.
- Project precedence and “do not blindly reformat” guidance remain intact.
