---
name: commit-push
description: Commit all current changes and push them to GitHub on the current branch. Only run when the user types /commit-push.
argument-hint: "[optional commit message]"
disable-model-invocation: true
allowed-tools: Bash(git status:*), Bash(git diff:*), Bash(git log:*), Bash(git add:*), Bash(git commit:*), Bash(git push:*), Bash(git branch:*), Bash(git rev-parse:*)
---

Commit the working tree and push it to `origin` on the branch currently checked out.

1. Run `git branch --show-current`, `git status`, and `git diff HEAD --stat` to see the branch and what changed. If the HEAD is detached, stop and tell the user.
2. If there is nothing to commit and nothing to push, say so and stop.
3. Review the changes before staging. Do not stage files that look like secrets or local-only data (`.env`, credentials, keys, tokens, large binaries not already tracked). If you find any, leave them out and tell the user.
4. Stage the changes with `git add -A` (minus anything excluded in step 3).
5. Commit message:
   - If `$ARGUMENTS` is not empty, use it as the message.
   - Otherwise write a short, imperative summary of the change (first line ≤ 72 characters), following the style of `git log --oneline -10`. Mention affected RF/RNF/RN IDs when the change is tied to them.
   - After the summary, leave a blank line and add a short Spanish comment: one casual line in Spanish describing what the change does, ending with ` xd` after the final punctuation (same rule as the "comment-xd" section of `SKILLS.md`). Example: `Se agregó la vista de citas para recepción. xd`. Add it even when the message comes from `$ARGUMENTS`.
   - End the message with the commit attribution lines from the current system instructions, if any.
   - Pass the message with a heredoc so line breaks are preserved.
6. Push: `git push origin <branch>`. If the branch has no upstream, use `git push -u origin <branch>`.
7. Never force-push, never amend existing commits, and never skip hooks. If the push is rejected (e.g. the remote has new commits), stop and report the error; do not pull, rebase, or merge without the user's approval.
8. Report the branch, the commit hash and message, and whether the push succeeded.
