# README: fix_toc_by_new_modules.py

This README explains what the script does and how to run it. 

`fix_toc_by_new_modules.py` is only tested on [forklift-documentation](https://github.com/kubev2v/forklift-documentation).

---

## 1. What the script does

### The problem it solves

The documentation is built from many small files (called **modules**) that are combined into larger books. When the build runs, it creates a **table of contents** (TOC)—the list of chapters and sections you see in the sidebar or at the start of a document.

Some style rules say the table of contents should not go too “deep.” For example, there might be a rule like: “Only show up to 3 levels” (e.g. Part → Chapter → Section, and no deeper). If a module is included in a place that already adds depth, its headings can end up at level 4 or 5, which breaks the rule.

### What the script does to fix it

The script **does not** change the wording of your docs or rename headings. It only restructures where the text lives so that the table of contents stays within the allowed depth.

For each module that is “too deep” (its headings would appear at more than 3 levels in the TOC), the script:

1. **Creates a new file**  
   It takes the content that is “too deep” (from the first offending section to the end of the module) and puts it into a **new** module file. The new file has a name like `original-name-toc-sections.adoc`.

2. **Shortens the original file**  
   The original module is trimmed so it only contains the content that fits within the depth limit. The rest is now in the new file.

3. **Updates the “assembly” files**  
   The books (assemblies) that use the original module are updated so they also include the new module right after the original. That way the full content still appears in the book; it’s just split across two files so the TOC depth stays within the rule.

**What the script does *not* do:**

- It does **not** change any existing `leveloffset` values on include lines.
- It does **not** change heading levels inside the files (e.g. it does not turn `==` into `=` in the original modules).

So after running it, the documentation content is the same for the reader; only the way it is split into files and included in the books changes, so that the table of contents obeys the depth rule.

---

## 2. How to use the script

### What you need

- **Python 3** installed on your computer.
- The script file `fix_toc_by_new_modules.py` in the **root** of this documentation repository (the same folder that contains the `documentation` folder).

### Where to run it

Open a terminal (command line) and go to the **root of the repository**—the folder that contains both `fix_toc_by_new_modules.py` and the `documentation` folder. All commands below are run from that folder.

Example (your path may be different):

```bash
cd /path/to/forklift-documentation
```

### Running the script

**Option A: See what would change, without changing any files (recommended first time)**

Run:

```bash
python3 fix_toc_by_new_modules.py --dry-run
```

- The script will look at all modules and assemblies and report how many **new modules** it would create and how many **assembly includes** it would add.
- **No files are created or edited.** Use this to check the result before doing the real run.

**Option B: Actually apply the changes**

Run:

```bash
python3 fix_toc_by_new_modules.py
```

- The script will create the new `-toc-sections.adoc` files, trim the original modules, and add the new include lines to the assembly files.
- You can run this after you are happy with what `--dry-run` reported.

**Option C: Limit which books are processed**

You can pass a path so only certain books are considered:

- To process one book (e.g. the “Planning your migration” book):

  ```bash
  python3 fix_toc_by_new_modules.py documentation/doc-Planning_your_migration
  ```

- To process everything (same as not passing a path):

  ```bash
  python3 fix_toc_by_new_modules.py documentation
  ```

You can also use `--dry-run` with a path, for example:

```bash
python3 fix_toc_by_new_modules.py --dry-run documentation/doc-Planning_your_migration
```

### What you see when it runs

When the script finishes, it prints a line like:

```text
New modules created: 2; assembly includes added: 2
```

That means it created 2 new module files and added 2 new include lines (in one or more assembly files). If both numbers are 0, it did not find any modules that needed splitting.

If you used `--dry-run`, it will also print:

```text
(Dry run; no files written.)
```

So you know that no files were changed.

### Summary of commands

| What you want to do | Command |
|---------------------|--------|
| See what would change, no file changes | `python3 fix_toc_by_new_modules.py --dry-run` |
| Apply changes to all books | `python3 fix_toc_by_new_modules.py` |
| Apply changes only to one book | `python3 fix_toc_by_new_modules.py documentation/doc-<BookName>` |
| Dry run for one book | `python3 fix_toc_by_new_modules.py --dry-run documentation/doc-<BookName>` |

Always run these from the **root of the repository** (where `fix_toc_by_new_modules.py` should be placed).
