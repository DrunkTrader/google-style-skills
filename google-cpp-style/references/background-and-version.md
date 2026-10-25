# Background and C++ version

Official sections: [Background](https://google.github.io/styleguide/cppguide.html#Background), [Goals of the Style Guide](https://google.github.io/styleguide/cppguide.html#Goals), and [C++ Version](https://google.github.io/styleguide/cppguide.html#C++_Version).

## What “style” means here

The guide treats style as readability and maintainability conventions, not merely whitespace. Use it to reason about APIs, ownership, language-feature selection, headers, and long-term maintenance as well as formatting.

The guide's goals are:

- Make every rule pay for its cognitive cost.
- Optimize for the reader, maintainer, and debugger rather than the original writer.
- Prefer consistency with nearby code and with the broader C++ community when that does not conflict with project needs.
- Avoid surprising, dangerous, or unusually difficult constructs.
- Be mindful of large-scale codebase effects such as namespace pollution and refactoring/tooling cost.
- Concede to measured optimization when a real performance requirement justifies it.

These goals are decision criteria, not a license to impose a personal interpretation. A review should cite the concrete rule or risk rather than saying that code “doesn't feel Google-ish.”

## Applying the guide

The official examples are illustrative and are not necessarily complete production templates. In particular, examples may omit comments or technical details that real submitted code needs.

When this skill is used outside a Google-originated project:

1. Confirm the repository's own C++ version, ABI and portability targets.
2. Treat project instructions and established local conventions as higher priority.
3. Use the Google rule when it is compatible; record a narrow, reasoned exception when it is not.
4. Keep correctness, security, ABI, performance, and build findings distinct from style findings.

## C++ Version

The current upstream guide targets **C++20** and says not to use C++23 features. Check the repository's actual compiler/toolchain before using a C++20 feature. The guide also says to consider portability to other environments before using C++17/C++20 features.

Do not use non-standard extensions. If the project has an explicitly documented extension boundary, identify that boundary and do not generalize it to portable code.

## Practical review checklist

- What language standard is configured in the build, and does the proposed code require a newer standard?
- Is a clever feature being used because it materially improves the API or performance, or merely because it is available?
- Does the proposed change leave a useful trace for a future reader (ownership transfer, lifetime, unusual control flow, or a deliberate exception)?
- Does it preserve local formatting and include organization instead of triggering an unrelated repository-wide reformat?
