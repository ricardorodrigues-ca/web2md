# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python-based web scraping tool that converts website content to Markdown format. The tool supports both single-page scraping and recursive scraping that follows links within the same domain.

## Core Architecture

The application is built around several key functions:

- `scrape_single_page()`: Handles HTTP requests and HTML parsing for individual pages
- `get_links_from_page()`: Extracts and filters links from HTML content, respecting domain boundaries
- `scrape_website_recursive()`: Implements breadth-first traversal with depth limiting and visited URL tracking
- `sanitize_filename()`: Converts URLs to safe filesystem paths for output files

The recursive scraping uses a deque-based queue system to manage URLs to visit, with built-in safeguards against infinite loops and domain restrictions to prevent scraping external sites.

## Dependencies and Setup

Install dependencies with:
```bash
pip install -r requirements.txt
```

Required packages:
- `requests` for HTTP requests
- `beautifulsoup4` for HTML parsing  
- `html2text` for HTML to Markdown conversion

## Usage Commands

**Single page scraping:**
```bash
python3 web2md.py <url> [-o output_file.md]
```

**Recursive scraping:**
```bash
python3 web2md.py -r <url> [-o output_directory] [-d max_depth] [--delay seconds]
```

Key options:
- `-r, --recursive`: Enable recursive link following
- `-d, --max-depth`: Control recursion depth (default: 3)
- `--delay`: Set delay between requests (default: 1 second)
- `-o, --output`: Output file (single page) or directory (recursive)

## Output Structure

- Single page mode: Creates one markdown file
- Recursive mode: Creates a directory with separate markdown files for each scraped page
- Filenames are sanitized versions of the URL paths
- Each file includes the original URL as a header

## Testing

The script can be tested with knowledge base sites like `https://intercom.help/flatlyio` which contain multiple linked pages within the same domain. The `mydocs/` directory contains example output from such a scraping operation.