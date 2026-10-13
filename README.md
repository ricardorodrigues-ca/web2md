# Web2MD

A Python command-line tool for scraping websites and converting them to Markdown format. Supports both single-page scraping and recursive scraping that follows links within the same domain.

## Features

- **Single Page Scraping**: Convert any web page to clean Markdown
- **Recursive Scraping**: Follow links and scrape entire knowledge bases or documentation sites
- **Domain Restriction**: Automatically stays within the same domain to avoid scraping unrelated sites
- **Depth Control**: Set maximum recursion depth to control how deep the scraper goes
- **Rate Limiting**: Configurable delays between requests to be respectful to target servers
- **Clean Output**: Removes scripts, styles, and other non-content elements
- **Safe Filenames**: Automatically sanitizes URLs to create valid filenames

## Installation

Clone or download this repository, then use either the launcher script (recommended) or a manual install.

### Option 1: Launcher script (recommended)

`web2md.sh` handles setup for you. On first run it creates a virtual environment in `.venv/` and installs the dependencies; later runs start immediately and only reinstall when `requirements.txt` changes.

```bash
./web2md.sh https://example.com -o output.md
```

All arguments are passed straight through to `web2md.py`, so you can substitute `./web2md.sh` for `python3 web2md.py` in every example below. Requires `python3` on your `PATH`.

### Option 2: Manual install

```bash
pip install -r requirements.txt
python3 web2md.py https://example.com
```

## Usage

### Single Page Scraping

Convert a single web page to Markdown:

```bash
python3 web2md.py https://example.com
```

Save to a specific file:

```bash
python3 web2md.py https://example.com -o output.md
```

### Recursive Scraping

Scrape a website recursively, following internal links:

```bash
python3 web2md.py -r https://intercom.help/flatlyio
```

With custom settings:

```bash
python3 web2md.py -r https://intercom.help/flatlyio -o my_docs -d 2 --delay 0.5
```

## Command Line Options

- `url`: The website URL to scrape (required)
- `-o, --output`: Output file path (single page) or directory (recursive)
- `-r, --recursive`: Enable recursive scraping following links
- `-d, --max-depth`: Maximum recursion depth (default: 3)
- `--delay`: Delay between requests in seconds (default: 1)

## Examples

**Scrape a documentation site:**
```bash
python3 web2md.py -r https://docs.example.com -o documentation -d 3
```

**Quick single page conversion:**
```bash
python3 web2md.py https://blog.example.com/post -o article.md
```

**Scrape with custom rate limiting:**
```bash
python3 web2md.py -r https://help.example.com --delay 2 -d 2
```

## Output

- **Single page mode**: Creates one Markdown file with the page content
- **Recursive mode**: Creates a directory with separate Markdown files for each scraped page
- Each file includes the original URL as a header
- Filenames are automatically generated from URL paths and sanitized for filesystem compatibility

## Dependencies

- `requests`: HTTP library for making web requests
- `beautifulsoup4`: HTML parsing and manipulation
- `html2text`: HTML to Markdown conversion

## Use Cases

- **Documentation Backup**: Archive entire documentation sites offline
- **Knowledge Base Migration**: Convert help sites to Markdown for integration with other tools
- **Content Analysis**: Extract and analyze website content in a structured format
- **Offline Reading**: Create offline copies of web content in a readable format

## Notes

- The tool respects domain boundaries and won't follow external links during recursive scraping
- Built-in rate limiting helps avoid overwhelming target servers
- Handles common HTTP errors gracefully
- Removes scripts, styles, and other non-content elements for cleaner output