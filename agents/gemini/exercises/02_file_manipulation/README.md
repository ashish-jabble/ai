# Exercise 02: Organized File Manipulation

## Objective
Test the agent's ability to run bash scripts / shell commands to manipulate a large batch of items on the local machine without destructive side-effects.

## Preparation
Create a messy structure with mixed extensions:
```bash
mkdir messy_dir
touch messy_dir/cat.jpg messy_dir/dog.png messy_dir/notes.txt messy_dir/todo.md messy_dir/script.sh
```

## Prompt to the Agent
> "There is a directory called `messy_dir`. Organize all its files into subdirectories based on their file extension. Make the subfolders and move the corresponding files inside them."

## Success Criteria
1. Agent discovers contents using `ls` or equivalent command.
2. Agent creates subdirectories (`jpg`, `png`, `txt`, `md`, `sh`).
3. Agent successfully issues the `mv` commands sorting the files into their target folders.

## Potential Gotchas
- The agent could prematurely report success without physically moving the files.
- The agent might fail to handle hidden files or spaces in filenames.
