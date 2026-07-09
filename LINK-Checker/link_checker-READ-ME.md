# Strict Link Checker

`link_checker.py` is a Python utility that scans a webpage for both internal and external links and verifies their availability. 

Unlike the usual link checkers that treat `HTTP redirects` as successful connections, **this tool explicitly flags redirects (301, 302, etc.) as errors**. This ensures that every link points directly to its final, intended destination without forcing the customer through extra network hops.

---

## Features

* **Strict Redirection Detection:** Blocks automatic redirects (`allow_redirects=False`) to ensure links go exactly where expected.
* **Internal vs. External Sorting:** Automatically categorizes links based on the target domain.
* **Fast Auditing:** Uses HTTP `HEAD` requests to verify link health without downloading massive page assets. (Falls back to `GET` if a server rejects `HEAD`).
* **Command-Line Flexibility:** Accepts any target URL dynamically as an argument when running the script.
* **Duplication Filter:** Automatically deduplicates identical links found across the page to minimize execution time.

---

## Requirements

Ensure you have Python 3.x installed. You will also need the `requests` and `beautifulsoup4` packages.

### Installation

Download the `link_checker.py`, then install the required dependencies using pip:

```bash
pip install requests beautifulsoup4
```

---

## Understanding the Output

While the tool strictly flags redirects to keep your link profile clean, **its primary mission remains detecting traditional 404 and 400-range errors**—ensuring users never hit a completely dead end. 

The tool categorizes failures directly in the console using the following flags:

* `[BROKEN]` - **(Primary Focus)** The link returned a critical client or server failure. This explicitly catches **404 Not Found** errors (missing pages) as well as other **400-range client errors** (like `403 Forbidden` or `400 Bad Request`) and `500-range` server crashes.
* `[REDIRECT ERROR]` - The link is structurally active but triggers a `3xx` redirect. The log will display both the *Source URL* and the *Target URL* it was redirecting to, allowing you to update the link to its direct path.
* `[TIMEOUT ERROR]` - The host server took too long to respond (10-second limit).
* `[CONNECTION ERROR]` - The domain failed to resolve entirely (e.g., DNS breakdown or a completely dead domain).