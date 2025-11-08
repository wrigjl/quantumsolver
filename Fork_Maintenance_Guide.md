# 🧭 Fork Maintenance Guide

This is a **personal reference** to help keep my fork of this repository up to date with the original ("upstream") repository.  
These steps are meant for daily or regular maintenance and do **not** need to be merged back into the main project.

```
          ┌──────────────┐
          │  Upstream    │  ← Original project (main repo)
          │ (Main Repo)  │
          └──────┬───────┘
                 │ fetch / merge
                 ▼
          ┌──────────────┐
          │   My Fork    │  ← Your copy on GitHub (origin)
          └──────┬───────┘
                 │ push / pull
                 ▼
          ┌──────────────┐
          │   Local VS   │  ← Your local folder
          │     Code     │
          └──────────────┘
```

---

## Setup (Run Once)

1. Open this project in **VS Code**.
2. Open the **Terminal** (`Ctrl + \``) and verify the remotes:
   ```bash
   git remote -v
   ```
   You should see something like:
   ```
   origin   https://github.com/<my-username>/<repo-name>.git (fetch)
   upstream https://github.com/<original-owner>/<repo-name>.git (fetch)
   ```
3. If `upstream` is missing, add it:
   ```bash
   git remote add upstream https://github.com/<original-owner>/<repo-name>.git
   ```

---

## Daily Update Steps

Use these steps to keep your fork’s `main` branch synchronized with the upstream project.

### Fetch the Latest Updates
```bash
git fetch upstream
```

### Switch to the Main Branch
```bash
git checkout main
```

### Merge Upstream Changes
```bash
git merge upstream/main
```

If there are no merge conflicts, continue.  
If there *are* conflicts, resolve them using VS Code’s merge editor, then commit.

### Push to Your Fork
```bash
git push origin main
```

---

## Optional: Sync a Feature Branch

If you’re working on a branch (e.g., `my-feature`), you can rebase it after syncing `main`:

```bash
git checkout my-feature
git rebase main
```

Then push your branch:
```bash
git push origin my-feature
```

---

## Quick Commands Summary

| Task | Command |
|------|----------|
| Fetch upstream updates | `git fetch upstream` |
| Merge into main | `git merge upstream/main` |
| Push updates to your fork | `git push origin main` |
| Rebase feature branch | `git rebase main` |

---

## Notes

- Only **push to your fork** (`origin`) — not to `upstream`.  
- This file is for **personal reference** and should remain **only in this fork**.  
- You can safely edit or expand this file without affecting the main repository.

---


