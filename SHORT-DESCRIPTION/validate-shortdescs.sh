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
#   DIRECTORY            Directory to scan recursively (default: current dir)
#
#   --attrs FILE         Additional AsciiDoc attributes file to parse.
#                        May be specified multiple times. Applied after the
#                        auto-discovered file, so these values take precedence.
#
#   --ifdef-tag TAG      When parsing attributes files, treat TAG as defined
#                        (include ifdef::TAG[] blocks, exclude ifndef::TAG[]).
#                        Can be specified multiple times.
#                        Example: --ifdef-tag mta  (for MTA documentation)
#                                 --ifdef-tag downstream
#
#   --no-auto-attrs      Disable automatic attributes file discovery.
#                        Useful when you want full control via --attrs.
#
# Attribute file auto-discovery
# ─────────────────────────────
# When DIRECTORY is inside a git repo, the script searches the repo root for
# the first matching file from the following list:
#
#   _attributes/common-attributes.adoc             openshift-docs (OADP, CNV)
#   documentation/modules/common-attributes.adoc   forklift-documentation (MTV)
#   docs/topics/templates/document-attributes.adoc mta-documentation (MTA)
#
# Attributes inside ifdef/ifndef/ifeval blocks in the file are skipped unless
# the matching tag is activated via --ifdef-tag.
#
# Dependencies: asciidoctor   gem install asciidoctor
#               xmllint       apt install libxml2-utils  |  brew install libxml2
# ==============================================================================

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

# --- Hardcoded fallback attributes --------------------------------------------
# These cover common OpenShift/Red Hat product names that may not be in every
# repo's attributes file. They are applied first; values from the auto-
# discovered or user-supplied attributes files override these.
# attribute-missing=drop causes undefined attributes to render as empty string
# rather than literal {name} text, keeping character counts accurate.
# i recommend updating 4.21 product-version to match whatever your current main working branch. 
ATTRS=(
    -a "attribute-missing=drop"
    -a experimental
    -a openshift-enterprise
    # OpenShift
    -a "product-title=OpenShift Container Platform"
    -a "product-version=4.21"
    -a "ocp-short=OCP"
    -a "oc-first=OpenShift CLI (oc)"
    # Virtualization
    -a "VirtProductName=OpenShift Virtualization"
    -a "VirtVersion=4.21"
    # OADP
    -a "oadp-short=OADP"
    -a "oadp-first=OpenShift API for Data Protection (OADP)"
    # MTV
    -a "project-short=MTV"
    -a "project-full=Migration Toolkit for Virtualization"
    # MTA
    -a "ProductShortName=MTA"
    -a "ProductName=migration toolkit for applications"
    # Cloud
    -a "aws-short=AWS"
    -a "ibm-name=IBM"
    -a "ibm-z-name=IBM Z"
    -a "ibm-linuxone-name=IBM LinuxONE"
    -a "ibm-cloud-title=IBM Cloud"
    # OS / platform
    -a "op-system-base=RHEL"
    -a "op-system-base-full=Red Hat Enterprise Linux"
    -a "op-system-first=Red Hat Enterprise Linux CoreOS (RHCOS)"
    -a "op-system=RHCOS"
    -a "sno=single-node OpenShift"
    # Storage / networking
    -a "rh-storage=OpenShift Data Foundation"
    -a "rh-storage-first=Red Hat OpenShift Data Foundation"
    # Other products
    -a "pipelines-shortname=Red Hat OpenShift Pipelines"
    -a "mtv-first=Migration Toolkit for Virtualization (MTV)"
    -a "rh-rhacm-first=Red Hat Advanced Cluster Management"
    -a "HCOCliKind=HyperConverged"
    -a "CNVNamespace=openshift-cnv"
)

# --- Known repo attributes file paths (relative to git root) ------------------
KNOWN_ATTR_PATHS=(
    "_attributes/common-attributes.adoc"             # openshift-docs (OADP, CNV)
    "documentation/modules/common-attributes.adoc"   # forklift-documentation (MTV)
    "docs/topics/templates/document-attributes.adoc" # mta-documentation (MTA)
)

# --- parse_attrs_file ---------------------------------------------------------
# Parses :name: value lines from an AsciiDoc attributes file.
#
# Handles ifdef/ifndef/ifeval conditional blocks:
#   - ifdef::TAG[]  blocks are included only if TAG is in IFDEF_TAGS
#   - ifndef::TAG[] blocks are included only if TAG is NOT in IFDEF_TAGS
#   - ifeval::[]    blocks are always excluded (expressions cannot be evaluated)
#   - Nesting is handled correctly via a stack
#
# Lines with cross-attribute references (e.g. :foo: {bar} value) are included
# as-is; asciidoctor resolves them at render time from the full attribute set.
parse_attrs_file() {
    local file="$1"
    [[ -f "$file" ]] || { echo "Warning: Attributes file '$file' not found." >&2; return; }
    echo "Loading attributes from: $file"

    local -a cond_stack=()  # each entry: 1 = include, 0 = skip
    local active=1           # 1 = currently including lines, 0 = skipping

    _tag_is_active() {
        local tag="$1"
        for t in "${IFDEF_TAGS[@]}"; do
            [[ "$t" == "$tag" ]] && return 0
        done
        return 1
    }

    _recalc_active() {
        active=1
        local s
        for s in "${cond_stack[@]}"; do
            [[ "$s" -eq 0 ]] && active=0 && return
        done
    }

    while IFS= read -r line; do
        # ifdef::TAG[]
        if [[ "$line" =~ ^ifdef::([^[]+)\[\] ]]; then
            local tag="${BASH_REMATCH[1]}"
            if _tag_is_active "$tag"; then
                cond_stack+=(1)
            else
                cond_stack+=(0)
            fi
            _recalc_active
            continue
        fi

        # ifndef::TAG[]
        if [[ "$line" =~ ^ifndef::([^[]+)\[\] ]]; then
            local tag="${BASH_REMATCH[1]}"
            if _tag_is_active "$tag"; then
                cond_stack+=(0)
            else
                cond_stack+=(1)
            fi
            _recalc_active
            continue
        fi

        # ifeval::[] — always excluded; we cannot evaluate arbitrary expressions
        if [[ "$line" =~ ^ifeval:: ]]; then
            cond_stack+=(0)
            _recalc_active
            continue
        fi

        # endif::[]
        if [[ "$line" =~ ^endif:: ]]; then
            if [[ ${#cond_stack[@]} -gt 0 ]]; then
                unset 'cond_stack[-1]'
            fi
            _recalc_active
            continue
        fi

        # Parse :name: value line if currently active
        if [[ $active -eq 1 ]] && \
           [[ "$line" =~ ^:([a-zA-Z][a-zA-Z0-9_-]*):([[:space:]]+(.*))? ]]; then
            local name="${BASH_REMATCH[1]}"
            local value="${BASH_REMATCH[3]:-}"
            ATTRS+=(-a "$name=$value")
        fi
    done < "$file"
}

# --- auto_discover_attrs ------------------------------------------------------
# Finds the repo root via git and loads the first matching known attributes file.
auto_discover_attrs() {
    local git_root
    git_root=$(git -C "$SEARCH_DIR" rev-parse --show-toplevel 2>/dev/null) || {
        echo "Warning: '$SEARCH_DIR' is not inside a git repo — skipping attribute auto-discovery." >&2
        return
    }

    local rel_path candidate
    for rel_path in "${KNOWN_ATTR_PATHS[@]}"; do
        candidate="$git_root/$rel_path"
        if [[ -f "$candidate" ]]; then
            parse_attrs_file "$candidate"
            return
        fi
    done

    echo "Warning: No known attributes file found under '$git_root'." >&2
    echo "         Use --attrs to specify one manually." >&2
}

# --- Load attributes ----------------------------------------------------------
# Auto-discovered file first, then user-specified files (which can override).
if [[ $AUTO_ATTRS -eq 1 ]]; then
    auto_discover_attrs
fi

for f in "${USER_ATTRS_FILES[@]}"; do
    parse_attrs_file "$f"
done

# --- Setup --------------------------------------------------------------------
DATE_TODAY=$(date +%Y-%m-%d)
REPORT_FILE="shortdesc-validation-report-${DATE_TODAY}.md"

total_files=0
no_abstract=0
ok_count=0
too_short_count=0
too_long_count=0
cond_count=0

tmp_short=$(mktemp)
tmp_long=$(mktemp)
tmp_cond=$(mktemp)
trap 'rm -f "$tmp_short" "$tmp_long" "$tmp_cond"' EXIT

# --- Scan ---------------------------------------------------------------------
echo "Scanning '$SEARCH_DIR'..."
total=$(find "$SEARCH_DIR" -type f -name "*.adoc" | wc -l | tr -d ' ')

if [[ "$total" -eq 0 ]]; then
    echo "No .adoc files found in '$SEARCH_DIR'." >&2
    exit 0
fi

while IFS= read -r file; do
    total_files=$(( total_files + 1 ))
    pct=$(( total_files * 100 / total ))
    printf "[%3d%%] %d/%d: %-55s\r" "$pct" "$total_files" "$total" "$(basename "$file")"

    # Single render per file — cache HTML to avoid calling asciidoctor twice.
    # -S safe allows local includes but prevents external file access.
    html=$(asciidoctor "${ATTRS[@]}" -S safe -o - "$file" 2>/dev/null)

    # Measure rendered abstract length via XPath on the HTML DOM.
    # Returns 0 if no [role="_abstract"] paragraph is present.
    length=$(printf '%s\n' "$html" | \
        xmllint --html \
                --xpath 'string-length(//div[contains(@class,"_abstract")][1]/p)' \
                - 2>/dev/null)

    if [[ -z "$length" || ! "$length" =~ ^[0-9]+(\.[0-9]+)?$ || "${length%.*}" -eq 0 ]]; then
        no_abstract=$(( no_abstract + 1 ))
        continue
    fi

    # Truncate any decimal from xmllint output (e.g. "143.0" → "143")
    length="${length%.*}"

    relpath="${file#"$SEARCH_DIR"/}"

    # Check raw source for conditional directives inside the abstract block.
    # These can cause the rendered length to vary across build targets.
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

done < <(find "$SEARCH_DIR" -type f -name "*.adoc" | sort)

printf '\n'

# --- Generate report ----------------------------------------------------------
files_with_abstract=$(( total_files - no_abstract ))
pct_of() { (( $2 > 0 )) && printf '%d' $(( $1 * 100 / $2 )) || printf '0'; }

{
cat << EOF
# Short Description Validation Report

**Date:** ${DATE_TODAY}
**Target directory:** \`${SEARCH_DIR}\`
**Files scanned:** ${total_files}
**Rules:**
1. \`[role="_abstract"]\` paragraph must be **50–300 characters** (measured on rendered HTML after attribute expansion — not raw source).
2. Abstract must not contain conditional syntax (\`ifdef::\`, \`ifndef::\`, \`ifeval::\`), which can cause the rendered length to vary across build targets.

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

---
EOF

if [[ -s "$tmp_cond" ]]; then
cat << EOF

## Contains Conditional Syntax — ${cond_count} file(s)

These abstracts contain \`ifdef::\`, \`ifndef::\`, or \`ifeval::\` directives.
The character count may be accurate for one build target but not others.
Review manually to confirm the length is within range for all variants.

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

} > "$REPORT_FILE"

# --- Terminal summary ---------------------------------------------------------
echo "Results:"
echo "  OK (50-300 chars) : ${ok_count}"
echo "  Too short (<50)   : ${too_short_count}"
echo "  Too long  (>300)  : ${too_long_count}"
echo "  Conditionals      : ${cond_count}"
echo "  No abstract       : ${no_abstract}"
echo ""
echo "Report: ${REPORT_FILE}"
