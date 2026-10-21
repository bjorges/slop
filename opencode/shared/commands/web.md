---
description: Open the current repo in the browser with optional view specifier
argument-hint: "[prs|prs ready|prs mine|issues|actions|branches|releases|settings]"
---

You are being asked to open the current git repository in the browser.

**Task:**
1. Run `git remote get-url origin` to get the remote URL
2. Parse the URL:
   - If it's an SSH URL like `git@github.com:user/repo.git`, convert it to `https://github.com/user/repo`
   - If it's already HTTPS, use it as-is (remove `.git` suffix if present)
   - Extract the base repository URL without `.git`
3. Based on the argument provided in `$ARGUMENTS`, append the appropriate path:
   - No arguments or empty: Use the base repo URL (homepage)
   - `pr` or `prs`: Append `/pulls`
   - `pr ready`, `prs ready`, or `prs ready for review`: Append `/pulls?q=is:pr+is:open+review:required`
   - `pr mine` or `my prs`: Append `/pulls?q=is:pr+is:open+author:@me`
   - `issues`: Append `/issues`
   - `actions` or `ci`: Append `/actions`
   - `branches`: Append `/branches`
   - `releases`: Append `/releases`
   - `settings`: Append `/settings`
   - Any other text: Treat as a best-effort URL construction (e.g., `/search?q=<text>` or `/blob/main/<text>`)
4. Use the bash tool to run `open "<url>"` to open the URL in the default browser

**Example scenarios:**
- `/web` → opens `https://github.com/user/repo`
- `/web prs` → opens `https://github.com/user/repo/pulls`
- `/web prs ready` → opens `https://github.com/user/repo/pulls?q=is:pr+is:open+review:required`
- `/web issues` → opens `https://github.com/user/repo/issues`
- `/web settings` → opens `https://github.com/user/repo/settings`

Execute this task with clarity and precision.
