# Resume instructions (for any Claude session / any account)

This repo holds an autonomous research project (full original brief: `BRIEF.md`).
If the user says "continue" (or similar):
1. Read `PROGRESS.md` top to bottom. The "NEXT ACTION" section says exactly what to do next.
2. Read the files it points to (journal_selection/*, experiments/protocol.md, etc.).
3. Continue from NEXT ACTION. Do not restart finished phases.
4. After EVERY completed step: update PROGRESS.md (phase, decisions + reasons, NEXT ACTION),
   then `git add -A && git commit && git push -u origin <current branch>`.
   The user may run out of usage at any moment; unsaved work is lost.
5. Integrity rules in BRIEF.md are absolute: never fabricate results, citations, dates, or journal data.
   Unverifiable items are marked UNVERIFIED.
