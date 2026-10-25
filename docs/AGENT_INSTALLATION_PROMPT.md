# Agent-driven installation prompt

Copy the following instruction into a coding agent when you want it to install this pack without granting it permission to replace existing files or alter unrelated configuration:

```text
Install one or more Google Style Guide Agent Skills from this repository, but do
not install software, modify shell startup files, alter unrelated configuration,
or replace existing skills without my explicit approval.

1. Inspect the operating system, current working directory, and available coding
   agents. Check for Claude Code, OpenAI Codex, OpenCode, Cursor, and Gemini CLI
   using documented commands/paths rather than guessing.
2. Read README.md and docs/INSTALLATION.md in this repository. Use the paths and
   scope rules documented there. If the requested agent is not verified, stop and
   ask me for its documented skills directory or an explicit destination.
3. Run the repository installer in list mode:

   python3 scripts/install.py list

   Show me the four skill names and the destinations that apply to the selected
   agent and user-global/project-local scope.
4. Ask which language skills to install, unless I already selected them. Never
   assume that “all” means replace existing skills.
5. Run a dry run with the exact selected skill(s), agent(s), scope, and destination:

   python3 scripts/install.py install ... --dry-run

   Inspect every resolved source and destination. Report conflicts and permissions
   before making changes. If the destination is ambiguous, stop and ask me for an
   explicit path.
6. After I approve the dry-run plan, run the same command without --dry-run. Do
   not add --replace unless I explicitly authorize replacement for named skill(s).
7. Verify each copied directory contains SKILL.md and its references/ files, and
   run:

   python3 scripts/validate.py

   Also inspect the target path and use the selected agent's own skill-list or
   discovery command when one is available. If the agent requires a restart or
   reload, tell me instead of changing unrelated configuration.
8. Report the exact installed paths, selected skills, scope, conflict handling,
   validator result, agent-discovery result, commands actually run, and any manual
   step still required. Say explicitly if live discovery could not be tested.

If an install or verification step fails, do not retry blindly. Read the error,
leave existing files untouched, explain the recovery path, and ask before any
destructive cleanup.
```
