#!/bin/bash

# ==============================================================================
# AsciiDoc Short Description Validator
# ==============================================================================
# Checks that [role="_abstract"] paragraphs in AsciiDoc files are between
# 50 and 300 characters, measured on rendered HTML output after attribute
# expansion — not raw source text.
#
# Usage: ./validate-shortdescs.sh [DIRECTORY] [OPTIONS]
#
#   DIRECTORY            Directory to scan (default: current dir).
#                        All .adoc files under DIRECTORY are the primary set.
#                        Any modules referenced via include:: from those files
#                        are automatically added to the scan — so only modules
#                        used by the target product area are checked.
#
#   --attrs FILE         Additional AsciiDoc attributes file to parse.
#                        May be specified multiple times.
#
#   --ifdef-tag TAG      When parsing attributes files, treat TAG as defined
#                        (include ifdef::TAG[] blocks, exclude ifndef::TAG[]).
#                        Can be specified multiple times.
#                        Example: --ifdef-tag mta
#
#   --no-auto-attrs      Disable automatic attributes file discovery.
#
# Include resolution:
#   openshift-docs resolves include:: paths relative to the git repo root.
#   For example, include::modules/oadp-foo.adoc in an assembly under
#   backup_and_restore/ resolves to {repo_root}/modules/oadp-foo.adoc.
#   The script tries this git-root-relative resolution first, then falls back
#   to file-relative resolution for other repos.
#
# Attribute file auto-discovery:
#   Searches the git repo root for known attributes files:
#     _attributes/common-attributes.adoc             openshift-docs (OADP, CNV)
#     documentation/modules/common-attributes.adoc    forklift (MTV)
#     docs/topics/templates/document-attributes.adoc  mta-documentation (MTA)
#
# Dependencies: asciidoctor   gem install asciidoctor
#               xmllint       apt install libxml2-utils  |  brew install libxml2
# ==============================================================================

set -euo pipefail

# --- Dependency checks --------------------------------------------------------
for cmd in asciidoctor xmllint git; do
    if ! command -v "$cmd" &>/dev/null; then
        echo "Error: '$cmd' is required but not found." >&2
        case "$cmd" in
            asciidoctor) echo "  Install: gem install asciidoctor" >&2 ;;
            xmllint)     echo "  Install: apt install libxml2-utils  OR  brew install libxml2" >&2 ;;
            git)         echo "  Install: https://git-scm.com" >&2 ;;
        esac
        exit 1
    fi
done

# --- Argument parsing ---------------------------------------------------------
SEARCH_DIR="."
USER_ATTRS_FILES=()
IFDEF_TAGS=()
AUTO_ATTRS=1

while [[ $# -gt 0 ]]; do
    case "$1" in
        --attrs)         USER_ATTRS_FILES+=("$2"); shift 2 ;;
        --ifdef-tag)     IFDEF_TAGS+=("$2"); shift 2 ;;
        --no-auto-attrs) AUTO_ATTRS=0; shift ;;
        -*)              echo "Error: Unknown option '$1'" >&2; exit 1 ;;
        *)               SEARCH_DIR="$1"; shift ;;
    esac
done

if [[ ! -d "$SEARCH_DIR" ]]; then
    echo "Error: Directory '$SEARCH_DIR' not found." >&2
    exit 1
fi

SEARCH_DIR=$(cd "$SEARCH_DIR" && pwd)

# --- Git repo root ------------------------------------------------------------
# Used for:
#   (a) include:: path resolution (openshift-docs resolves from repo root)
#   (b) clean relative paths in report output
#   (c) attributes file auto-discovery
GIT_ROOT=$(git -C "$SEARCH_DIR" rev-parse --show-toplevel 2>/dev/null) || GIT_ROOT=""

# --- Hardcoded fallback attributes --------------------------------------------
# Applied first; values from auto-discovered / --attrs files take precedence.
# attribute-missing=drop causes undefined attributes to render as empty string.
ATTRS=(
    -a "attribute-missing=drop"
    -a experimental
    -a openshift-enterprise
    -a "product-title=OpenShift Container Platform"
    -a "product-version=4.17"
    -a "ocp-short=OCP"
    -a "oc-first=OpenShift CLI (oc)"
    -a "VirtProductName=OpenShift Virtualization"
    -a "VirtVersion=4.17"
    -a "oadp-short=OADP"
    -a "oadp-first=OpenShift API for Data Protection (OADP)"
    -a "project-short=MTV"
    -a "project-full=Migration Toolkit for Virtualization"
    -a "ProductShortName=MTA"
    -a "ProductName=migration toolkit for applications"
    -a "aws-short=AWS"
    -a "ibm-name=IBM"
    -a "ibm-z-name=IBM Z"
    -a "ibm-linuxone-name=IBM LinuxONE"
    -a "ibm-cloud-title=IBM Cloud"
    -a "op-system-base=RHEL"
    -a "op-system-base-full=Red Hat Enterprise Linux"
    -a "op-system-first=Red Hat Enterprise Linux CoreOS (RHCOS)"
    -a "op-system=RHCOS"
    -a "sno=single-node OpenShift"
    -a "rh-storage=OpenShift Data Foundation"
    -a "rh-storage-first=Red Hat OpenShift Data Foundation"
    -a "pipelines-shortname=Red Hat OpenShift Pipelines"
    -a "mtv-first=Migration Toolkit for Virtualization (MTV)"
    -a "rh-rhacm-first=Red Hat Advanced Cluster Management"
    -a "HCOCliKind=HyperConverged"
    -a "CNVNamespace=openshift-cnv"
)

# --- Known repo attributes file paths (relative to git root) ------------------
KNOWN_ATTR_PATHS=(
    "_attributes/common-attributes.adoc"             # openshift-docs (OADP, CNV)
    "documentation/modules/common-attributes.adoc"   # forklift (MTV)
    "docs/topics/templates/document-attributes.adoc" # mta-documentation (MTA)
)

# --- parse_attrs_file ---------------------------------------------------------
# Parses :name: value lines from an AsciiDoc attributes file.
# Handles ifdef/ifndef/ifeval conditional blocks via a stack; only includes
# blocks whose guard tag is listed in IFDEF_TAGS. ifeval blocks are always
# excluded (expressions cannot be evaluated statically).
parse_attrs_file() {
    local file="$1"
    [[ -f "$file" ]] || { echo "Warning: Attributes file '$file' not found." >&2; return; }
    echo "Loading attributes from: $file"

    local -a cond_stack=()
    local active=1

    _tag_active() {
        local t
        for t in "${IFDEF_TAGS[@]}"; do
            if [[ "$t" == "$1" ]]; then return 0; fi
        done
        return 1
    }

    _recalc() {
        active=1
        local s
        for s in "${cond_stack[@]}"; do
            if [[ $s -eq 0 ]]; then active=0; return; fi
        done
    }

    while IFS= read -r line; do
        if [[ "$line" =~ ^ifdef::([^[]+)\[\] ]]; then
            _tag_active "${BASH_REMATCH[1]}" && cond_stack+=(1) || cond_stack+=(0)
            _recalc; continue
        fi
        if [[ "$line" =~ ^ifndef::([^[]+)\[\] ]]; then
            _tag_active "${BASH_REMATCH[1]}" && cond_stack+=(0) || cond_stack+=(1)
            _recalc; continue
        fi
        if [[ "$line" =~ ^ifeval:: ]]; then
            cond_stack+=(0); _recalc; continue
        fi
        if [[ "$line" =~ ^endif:: ]]; then
            [[ ${#cond_stack[@]} -gt 0 ]] && unset 'cond_stack[-1]'
            _recalc; continue
        fi
        if [[ $active -eq 1 ]] && \
           [[ "$line" =~ ^:([a-zA-Z][a-zA-Z0-9_-]*):([[:space:]]+(.*))? ]]; then
            ATTRS+=(-a "${BASH_REMATCH[1]}=${BASH_REMATCH[3]:-}")
        fi
    done < "$file"
}

# --- auto_discover_attrs ------------------------------------------------------
auto_discover_attrs() {
    [[ -z "$GIT_ROOT" ]] && {
        echo "Warning: Not inside a git repo — skipping attribute auto-discovery." >&2
        return
    }
    local rel candidate
    for rel in "${KNOWN_ATTR_PATHS[@]}"; do
        candidate="$GIT_ROOT/$rel"
        if [[ -f "$candidate" ]]; then
            parse_attrs_file "$candidate"
            return
        fi
    done
    echo "Warning: No known attributes file found under '$GIT_ROOT'. Use --attrs to specify one." >&2
}

# --- Load attributes ----------------------------------------------------------
[[ $AUTO_ATTRS -eq 1 ]] && auto_discover_attrs
for f in "${USER_ATTRS_FILES[@]}"; do parse_attrs_file "$f"; done

# --- collect_scan_files -------------------------------------------------------
# Returns the list of files to scan:
#   1. All .adoc files found directly under SEARCH_DIR (primary set).
#   2. Files discovered by following include:: directives recursively.
#      The BFS terminates naturally because leaf nodes (modules, snippets) do
#      not include other modules. Depth in practice: 1–3 levels.
#
# Include path resolution (two-step):
#   Step 1 — git-root-relative: try $GIT_ROOT/$inc_path first.
#             openshift-docs resolves include::modules/foo.adoc relative to
#             the repo root, not the including file's directory.
#   Step 2 — file-relative: fallback for repos like forklift / mta-documentation
#             that use standard AsciiDoc path resolution.
#
# Sets globals: primary_count, module_count
primary_count=0
module_count=0

collect_scan_files() {
    local -A seen=()
    local -a queue=()

    # --- Primary files --------------------------------------------------------
    while IFS= read -r f; do
        seen["$f"]=1
        queue+=("$f")
    done < <(find "$SEARCH_DIR" -type f -name "*.adoc" | sort)

    primary_count=${#queue[@]}

    # --- Follow includes (BFS) ------------------------------------------------
    # i=$(( )) is always exit-0; avoids set -e pitfall of (( i++ )) when i=0.
    # [[ ]] comparison likewise safe under set -e.
    local f dir inc_path resolved abs
    local i=0

    while [[ $i -lt ${#queue[@]} ]]; do
        f="${queue[$i]}"
        dir=$(dirname "$f")
        i=$(( i + 1 ))

        while IFS= read -r inc_path; do
            # Skip unresolved attribute references
            [[ "$inc_path" == *"{"* ]] && continue

            resolved=""

            # Step 1: git-root-relative (openshift-docs convention)
            if [[ -n "$GIT_ROOT" && -f "$GIT_ROOT/$inc_path" ]]; then
                resolved="$GIT_ROOT/$inc_path"
            fi

            # Step 2: file-relative (standard AsciiDoc — forklift, mta-documentation)
            if [[ -z "$resolved" ]]; then
                abs=$(cd "$dir" 2>/dev/null && \
                      cd "$(dirname "$inc_path")" 2>/dev/null && \
                      echo "$(pwd)/$(basename "$inc_path")") 2>/dev/null || true
                [[ -n "$abs" && -f "$abs" ]] && resolved="$abs"
            fi

            [[ -z "$resolved" ]] && continue
            [[ -n "${seen[$resolved]+_}" ]] && continue

            seen["$resolved"]=1
            queue+=("$resolved")

        done < <(grep -oE 'include::([^[]+\.adoc)\[' "$f" 2>/dev/null \
                     | sed 's/include:://;s/\[.*//')
    done

    module_count=$(( ${#queue[@]} - primary_count ))
    printf '%s\n' "${queue[@]}" | sort
}

# --- relpath helper -----------------------------------------------------------
# Returns a clean repo-relative path for display. Falls back to SEARCH_DIR-
# relative, then absolute if the file is somehow outside both.
display_path() {
    local file="$1"
    if [[ -n "$GIT_ROOT" && "$file" == "$GIT_ROOT"/* ]]; then
        echo "${file#"$GIT_ROOT"/}"
    elif [[ "$file" == "$SEARCH_DIR"/* ]]; then
        echo "${file#"$SEARCH_DIR"/}"
    else
        echo "$file"
    fi
}

# --- Setup --------------------------------------------------------------------
DATE_TODAY=$(date +%Y-%m-%d)
REPORT_FILE="shortdesc-validation-report-${DATE_TODAY}.md"

total_files=0
no_abstract=0
ok_count=0
too_short_count=0
too_long_count=0
cond_count=0
colon_count=0
selfref_count=0

tmp_short=$(mktemp)
tmp_long=$(mktemp)
tmp_cond=$(mktemp)
tmp_colon=$(mktemp)
tmp_selfref=$(mktemp)
tmp_filelist=$(mktemp)
trap 'rm -f "$tmp_short" "$tmp_long" "$tmp_cond" "$tmp_colon" "$tmp_selfref" "$tmp_filelist"' EXIT

# --- Collect files ------------------------------------------------------------
echo "Collecting files from '$(display_path "$SEARCH_DIR")' (following include:: directives)..."
collect_scan_files > "$tmp_filelist"
total=$(wc -l < "$tmp_filelist" | tr -d ' ')

if [[ "$total" -eq 0 ]]; then
    echo "No .adoc files found in '$SEARCH_DIR'." >&2
    exit 0
fi

echo "Scope: ${primary_count} files in target directory + ${module_count} included modules = ${total} total"

# --- Scan ---------------------------------------------------------------------
echo "Scanning..."

set +e   # disable exit-on-error for the scan loop; errors are non-fatal per file

while IFS= read -r file; do
    total_files=$(( total_files + 1 ))
    pct=$(( total_files * 100 / total ))
    printf "[%3d%%] %d/%d: %-55s\r" "$pct" "$total_files" "$total" "$(basename "$file")"

    # Single render per file. -S safe allows local includes.
    html=$(asciidoctor "${ATTRS[@]}" -S safe -o - "$file" 2>/dev/null)

    # Extract rendered abstract text via XPath (normalize-space strips leading/trailing
    # whitespace and collapses internal runs; used for both length and content checks).
    text=$(printf '%s\n' "$html" | \
        xmllint --html \
                --xpath 'normalize-space(//div[contains(@class,"_abstract")][1]/p)' \
                - 2>/dev/null)

    if [[ -z "$text" ]]; then
        no_abstract=$(( no_abstract + 1 ))
        continue
    fi

    length=${#text}
    relpath=$(display_path "$file")

    # Check for conditional directives inside the abstract block.
    raw_abstract=$(awk '
        /\[role="_abstract"\]/ { flag=1; next }
        flag && /^[[:space:]]*$/ { exit }
        flag { print }
    ' "$file")

    if printf '%s\n' "$raw_abstract" | grep -qE '(ifdef|ifndef|ifeval|endif)::'; then
        cond_count=$(( cond_count + 1 ))
        printf '| `%s` | Conditional syntax — length may vary by build target |\n' \
            "$relpath" >> "$tmp_cond"
    fi

    if (( length < 50 )); then
        too_short_count=$(( too_short_count + 1 ))
        printf '| %d | `%s` |\n' "$length" "$relpath" >> "$tmp_short"
    elif (( length > 300 )); then
        too_long_count=$(( too_long_count + 1 ))
        printf '| %d | `%s` |\n' "$length" "$relpath" >> "$tmp_long"
    else
        ok_count=$(( ok_count + 1 ))
    fi

    # Check: abstract ends with a colon (introductory fragment, not a description).
    if [[ "$text" =~ :[[:space:]]*$ ]]; then
        colon_count=$(( colon_count + 1 ))
        printf '| `%s` | `%s` |\n' "$relpath" "${text:0:120}" >> "$tmp_colon"
    fi

    # Check: self-referential or introductory opening ("This topic…", "The following table…").
    if printf '%s' "$text" | grep -qiE \
        '^(This (topic|section|module|document|chapter|guide|page|procedure|reference|concept|assembly|book|content|article|information|table|list|figure|example)|The following )'; then
        selfref_count=$(( selfref_count + 1 ))
        printf '| `%s` | `%s` |\n' "$relpath" "${text:0:120}" >> "$tmp_selfref"
    fi

done < "$tmp_filelist"

printf '\n'
set -e

# --- Generate report ----------------------------------------------------------
files_with_abstract=$(( total_files - no_abstract ))
pct_of() { (( $2 > 0 )) && printf '%d' $(( $1 * 100 / $2 )) || printf '0'; }

{
cat << EOF
# Short Description Validation Report

**Date:** ${DATE_TODAY}
**Target directory:** \`$(display_path "$SEARCH_DIR")\`
**Files scanned:** ${total_files} (${primary_count} in target directory + ${module_count} included modules)
**Rules:**
1. \`[role="_abstract"]\` paragraph must be **50–300 characters** (measured on rendered HTML after attribute expansion).
2. Abstract must not contain conditional syntax (\`ifdef::\`, \`ifndef::\`, \`ifeval::\`), which can cause the rendered length to vary across build targets.
3. Abstract must not end with a colon (indicates a leading fragment, not a description).
4. Abstract must not open with self-referential or introductory language (\`This topic…\`, \`The following table…\`, etc.).

---

## Summary

| Result | Count | % of files with abstract |
|--------|-------|--------------------------|
| Files checked | ${total_files} | — |
| No \`[role="_abstract"]\` (skipped) | ${no_abstract} | — |
| Files with abstract | ${files_with_abstract} | 100% |
| **OK (50–300 chars)** | **${ok_count}** | **$(pct_of $ok_count $files_with_abstract)%** |
| **Too short (<50 chars)** | **${too_short_count}** | **$(pct_of $too_short_count $files_with_abstract)%** |
| **Too long (>300 chars)** | **${too_long_count}** | **$(pct_of $too_long_count $files_with_abstract)%** |
| **Contains conditionals** | **${cond_count}** | — |
| **Ends with colon** | **${colon_count}** | — |
| **Self-referential / introductory** | **${selfref_count}** | — |

---
EOF

if [[ -s "$tmp_cond" ]]; then
cat << EOF

## Contains Conditional Syntax — ${cond_count} file(s)

These abstracts contain \`ifdef::\`, \`ifndef::\`, or \`ifeval::\` directives.
Review manually to confirm the length is within range for all build targets.

| File | Note |
|------|------|
EOF
    cat "$tmp_cond"
    printf '\n---\n'
fi

if [[ -s "$tmp_short" ]]; then
cat << EOF

## Too Short (<50 characters) — ${too_short_count} file(s)

Sorted shortest first.

| Chars (rendered) | File |
|------------------|------|
EOF
    sort -t'|' -k2 -n "$tmp_short"
    printf '\n---\n'
fi

if [[ -s "$tmp_long" ]]; then
cat << EOF

## Too Long (>300 characters) — ${too_long_count} file(s)

Sorted longest first.

| Chars (rendered) | File |
|------------------|------|
EOF
    sort -t'|' -k2 -rn "$tmp_long"
    printf '\n---\n'
fi

if [[ -s "$tmp_colon" ]]; then
cat << EOF

## Ends with Colon — ${colon_count} file(s)

These abstracts end with \`:\`, which indicates an introductory fragment rather than a
standalone description. Rewrite as a complete sentence that summarises the content.

| File | Abstract (first 120 chars) |
|------|---------------------------|
EOF
    cat "$tmp_colon"
    printf '\n---\n'
fi

if [[ -s "$tmp_selfref" ]]; then
cat << EOF

## Self-Referential / Introductory Language — ${selfref_count} file(s)

These abstracts open with phrases such as "This topic describes…" or "The following
table shows…", which describe the content structure rather than the content itself.
Rewrite to describe what the reader will learn or accomplish.

| File | Abstract (first 120 chars) |
|------|---------------------------|
EOF
    cat "$tmp_selfref"
    printf '\n---\n'
fi

} > "$REPORT_FILE"

# --- Terminal summary ---------------------------------------------------------
echo "Results:"
echo "  OK (50-300 chars) : ${ok_count}"
echo "  Too short (<50)   : ${too_short_count}"
echo "  Too long  (>300)  : ${too_long_count}"
echo "  Conditionals      : ${cond_count}"
echo "  Ends with colon   : ${colon_count}"
echo "  Self-referential  : ${selfref_count}"
echo "  No abstract       : ${no_abstract}"
echo ""
echo "Report: ${REPORT_FILE}"
