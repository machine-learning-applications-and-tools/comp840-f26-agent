# Updating this repo

This repo is yours for the whole term. Weeks 3 through 12 all build on
it. Each week I add new files to the original template: new tasks, a
new stub function, sometimes a fix. This page shows how to pull those
into your copy without losing your own work.

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

**Do not run `git merge upstream/main`.** Your repo was made from the
template, not cloned from it, so the two share no git history. A merge
reports every file that exists on both sides as a conflict, including
files you never touched, even `agent/cli.py`.

Instead, pull only the files that changed, by name. Each week's
`weekNN-README.md` gives you the exact list:

```bash
git checkout upstream/main -- <file1> <file2> <file3>
git add -A
git commit -m "Pull Week N update"
```

`git checkout upstream/main -- <path>` copies that one file from the
template and stages it. Nothing else in your folder changes. List every
file from that week's update in one command.

## Which files to pull, and which never to pull

New files are always safe to pull: new labs, new demos, new task lists.
There is nothing of yours in a file you did not have before. Each week's
instructions and output file have their own names, `weekNN-README.md`
and `weekNN-OUTPUT.md`, so they are always new files too. Pulling
`week05-README.md` never touches `week04-README.md`, and every past
week's instructions and answers stay in your folder.

For files you already have, only pull the ones that week's instructions
say changed, for example `README.md`, or `agent/cli.py` when a new flag
is added. **Never pull `agent/loop.py`, `agent/tools.py`, or any other
file a previous week's lab asked you to write.** The template's copy is
a reference. Pulling it would replace your finished work with that
week's stub.

If you are not sure whether a file is safe to pull, ask before you run
the command.

## Why Week 4 also adds `week03-README.md`

The weekNN naming started in Week 4, so before that your `README.md`
held Week 3's instructions. Week 4 replaces it with the index you see
now, and adds `week03-README.md` so Week 3's instructions are kept. This
happens once. Every later week has its own file from the start.

## If something goes wrong

`git checkout upstream/main -- <path>` only stages that one file. If
you pulled the wrong file and have not committed yet,
`git checkout HEAD -- <path>` restores your previous version. If you
already committed a bad pull, message me before doing anything else. Do
not force-push or reset it yourself.
