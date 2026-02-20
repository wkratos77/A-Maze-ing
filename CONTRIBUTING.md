# Contributing to A-Maze-ing

Welcome! This guide explains how to collaborate on this repository with a friend.

---

## Option 1: Add Your Friend as a Collaborator (Recommended for small teams)

This lets your friend push changes directly to your repository.

1. Go to your repository on GitHub: `https://github.com/wkratos77/A-Maze-ing`
2. Click **Settings** (top navigation bar).
3. In the left sidebar, click **Collaborators** (under "Access").
4. Click **Add people** and enter your friend's GitHub username or email address.
5. Choose the **Write** role and click **Add**.
6. Your friend will receive an email invitation — they need to accept it to gain access.

---

## Option 2: Fork & Pull Request Workflow (Recommended for open-source style contributions)

This is the standard GitHub collaboration workflow and works even without adding someone as a collaborator.

### Your friend's steps:

1. **Fork the repository**
   - Go to `https://github.com/wkratos77/A-Maze-ing`
   - Click the **Fork** button (top right corner).
   - This creates a personal copy of the repository under your friend's account.

2. **Clone their fork locally**
   ```bash
   git clone https://github.com/<friends-username>/A-Maze-ing.git
   cd A-Maze-ing
   ```

3. **Add the original repository as an upstream remote** (to stay in sync)
   ```bash
   git remote add upstream https://github.com/wkratos77/A-Maze-ing.git
   ```

4. **Create a new branch for their changes**
   ```bash
   git checkout -b feature/my-feature
   ```

5. **Make changes, then commit them**
   ```bash
   git add .
   git commit -m "Describe the change"
   ```

6. **Push the branch to their fork**
   ```bash
   git push origin feature/my-feature
   ```

7. **Open a Pull Request**
   - Go to `https://github.com/wkratos77/A-Maze-ing`
   - Click **Compare & pull request** (GitHub will prompt this automatically).
   - Add a title and description, then click **Create pull request**.

8. **You review and merge** the pull request from the repository's **Pull requests** tab.

---

## Keeping Your Local Copy Up to Date

If using the fork workflow, run these commands before starting new work:

```bash
git fetch upstream
git checkout main
git merge upstream/main
```

---

## Working Together Directly (Collaborator workflow)

If you've added your friend as a collaborator (Option 1), they can clone the repository directly:

```bash
git clone https://github.com/wkratos77/A-Maze-ing.git
cd A-Maze-ing
```

Then follow good branch practices:

```bash
# Create a branch for your work
git checkout -b feature/my-feature

# Make changes and commit
git add .
git commit -m "Describe the change"

# Push the branch
git push origin feature/my-feature
```

Then open a Pull Request on GitHub to merge changes into `main`.

---

## Tips for Smooth Collaboration

- **Always work on a branch**, not directly on `main`.
- **Pull the latest changes** before starting new work.
- **Write clear commit messages** so your collaborator understands what changed.
- **Use Pull Requests** even between collaborators — it allows for code review and discussion.
