# Broken link checker for virt AsciiDoc

`check_broken_links.py` checks AsciiDoc files under `openshift-docs/virt/` for broken **xrefs**, **includes**, and (optionally) **external links**.

## Requirements

- **Python 3.9+** (no extra packages required)
- For `--check-urls`: standard library only (`urllib.request`)

Run from the **openshift-docs** repository root, or set `--repo-root` to that directory.

## Usage

```bash
# From openshift-docs repo root: scan all of virt/
python3 virt/check_broken_links.py

# Scan a specific subdirectory
python3 virt/check_broken_links.py virt/about_virt
python3 virt/check_broken_links.py virt/nodes

# From inside virt/: scan current directory (virt/) or a subdir
cd virt && python3 check_broken_links.py
cd virt && python3 check_broken_links.py about_virt
```

**PATH** is the directory to scan. It can be:

- The whole **virt/** tree (default when you omit PATH)
- Any **subdirectory** (e.g. `virt/about_virt`, `virt/nodes`, or `about_virt` when run from `virt/`)

Paths are resolved relative to the current working directory.

## Options

| Option | Description |
|--------|-------------|
| `--repo-root DIR` | Repository root (default: auto-detect by walking up for `modules/` or `_attributes/`) |
| `--validate-against URL` | **Validate xrefs against published docs.** Resolves each xref to the corresponding page URL and checks it with HTTP GET. **Red Hat OCP virtualization:** `https://docs.redhat.com/en/documentation/openshift_container_platform/4.21/html-single/virtualization` — **OKD docs:** `https://docs.okd.io/latest` |
| `--check-urls` | Validate external `link:https?://...` URLs with a HEAD request |
| `--no-xref` | Skip xref validation |
| `--no-include` | Skip `include::` validation |
| `-q`, `--quiet` | Only print a one-line summary (e.g. `N issue(s) in M file(s)`) |

## What it checks

1. **xrefs** (`xref:path#anchor[text]`)
   - **With `--validate-against URL`** (recommended for virt): Resolves each xref to the published page URL and checks it with HTTP GET. Reports non-2xx responses (e.g. 404). Use **Red Hat OCP virtualization** (`https://docs.redhat.com/en/documentation/openshift_container_platform/4.21/html-single/virtualization`) or **OKD docs** (`https://docs.okd.io/latest`).
   - **Without `--validate-against`**: Resolves `path` relative to the current file and repo root; verifies the target `.adoc` exists and the `#anchor` appears as `[id="..."]` in the source (can yield false positives due to build-generated IDs).

2. **Includes** (`include::path[options]`)
   - Resolves `path` relative to the current file, then relative to the repo root (so `modules/` and `_attributes/` at repo root work).
   - Verifies the included file exists.

3. **External links** (`link:https?://...`) — only with `--check-urls`
   - Sends a HEAD request to each URL.
   - Reports non-2xx/3xx responses or connection errors.

## Exit codes

- **0** — No issues (or no `.adoc` files under PATH).
- **1** — One or more broken xrefs, includes, or links.
- **2** — Invalid arguments (e.g. path does not exist or is not a directory).

## Anchor matching and false positives

Xref anchor checking looks for a literal `[id="..."]` (or `[id='...']`) in the target file. The AsciiDoc build may generate different IDs from section titles, so some reported xref issues can be **false positives** if the build resolves anchors differently. Review the listed target file and IDs to confirm.

## Examples

```bash
# Full virt tree, xrefs and includes only
python3 virt/check_broken_links.py

# One subdirectory, with URL checking
python3 virt/check_broken_links.py --check-urls virt/about_virt

# Pin repo root and scan virt
python3 virt/check_broken_links.py --repo-root /path/to/openshift-docs virt

# Validate xrefs against Red Hat OCP virtualization docs
python3 virt/check_broken_links.py --validate-against "https://docs.redhat.com/en/documentation/openshift_container_platform/4.21/html-single/virtualization" virt/about_virt

# Validate xrefs against OKD docs (latest)
python3 virt/check_broken_links.py --validate-against https://docs.okd.io/latest virt/about_virt

# Only check includes (e.g. after moving modules)
python3 virt/check_broken_links.py --no-xref virt

# Quiet run for scripts
python3 virt/check_broken_links.py -q virt/about_virt
```
