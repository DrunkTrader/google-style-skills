# Testing, source, and license record

Official sections: [Use the right per-codebase test framework](https://google.github.io/styleguide/rustguide.html#Use_the_right_per-codebase_test_framework), plus the upstream source record in this file's companion skill documentation.

## Use the right per-codebase test framework

Use the test framework and build/test command selected by the repository. A Cargo project may use `cargo test`, while Chromium, Fuchsia, Android, or another monorepo may require a wrapper, target label, or test shard. Do not add a framework or claim a test passed because a generic Cargo command exists. Inspect CI and build documentation, run the narrowest relevant test first, then report the exact command and result.

## Source record

- Official discovery index: <https://google.github.io/styleguide/>
- Official guide: <https://google.github.io/styleguide/rustguide.html>
- Upstream repository: <https://github.com/google/styleguide>
- Retrieved: 2026-10-24
- Upstream snapshot: `c775c0c2f73c110613243520c001577cdbc0034d` (`Automated export from internal guides`, committed 2026-10-23)
- Source license: guide prose is CC BY 3.0; source code samples are Apache 2.0. See <https://github.com/google/styleguide#licensing>.
- This is an independently maintained adaptation, not an official Google product. See the repository `NOTICE.md` and `LICENSE` for the mixed licensing of adaptations and code.
