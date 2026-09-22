# Updating this repo

This repo is yours for the whole term -- Weeks 3 through 12 all build on
it. Each week I add new files to the original template: new tasks, a
new stub function, sometimes a fix to something that was broken. This is
how you pull those into your own copy without losing your own work.

## One-time setup

Add the template as a second remote. Do this once, the first time you
need to pull an update:

```bash
git remote add upstream https://github.com/machine-learning-applications-and-tools/comp840-f26-agent.git
```

## Every week

Commit your own work first, so nothing is lost if a step below goes
wrong:

```bash
git add -A
git commit -m "my week N work"
```

Then fetch the update:

```bash
git fetch upstream
```

**Do not run `git merge upstream/main`.** Your repo and the template
were created independently by GitHub Classroom, so they share no git
history -- a merge has no common ancestor to compare against, and it
will report every single file that exists on both sides as a conflict,
including files you never touched. This was tested, not assumed: even
`agent/cli.py`, which nobody is supposed to edit, conflicts under a
plain merge.

Instead, pull only the specific files that changed, by name -- that
week's own `weekNN-README.md` gives you the exact list:

```bash
git checkout upstream/main -- <file1> <file2> <file3>
git add -A
git commit -m "Pull Week N update"
```

`git checkout upstream/main -- <path>` takes that one file's content
from the template and stages it, without touching anything else in your
working tree. Run it once with every filename that week's update
touches, listed together.

## Which files to pull, and which to never pull

Every week's new files (new labs, new demos, new task lists) are always
safe to pull this way -- there is nothing of yours to lose in a file
that did not exist in your repo before. Each week's instructions and
output file are named `weekNN-README.md` and `weekNN-OUTPUT.md`, not
shared filenames reused every week, so both always fall into this safe,
brand-new-file category too -- pulling `week05-README.md` next week will
never touch `week04-README.md`, and every past week's instructions and
answers stay sitting right there in your working tree, not buried in git
history.

For files that already existed in your repo: only pull the ones the
week's instructions explicitly say changed (for example, `README.md` and
`agent/cli.py` when a new flag is added). **Never pull `agent/loop.py`,
`agent/tools.py`, or any other file a previous week's lab asked you to
write yourself**, even if I also ship a copy of it in the template -- my
copy is a reference, not something meant to replace your own working
code. Pulling it would silently revert your own completed work back to
that week's stub.

If you are ever unsure whether a file is safe to pull, ask before
running the checkout command, rather than guessing.

## Why Week 4 also adds `week03-README.md`

This naming started with Week 4, so your current `README.md` is still
Week 3's instructions. Week 4 replaces it with the new stable index, and
adds `week03-README.md` alongside it so Week 3's instructions aren't
lost in the swap. One-time only -- every later week already has its own
uniquely-named file from the start.

## If something goes wrong

`git checkout upstream/main -- <path>` only ever stages that one path --
if you pulled the wrong file by mistake and have not committed yet,
`git checkout HEAD -- <path>` restores your previous version. If you
already committed a bad pull, stop and message me before doing anything
else -- do not force-push or reset to "fix" it yourself.
