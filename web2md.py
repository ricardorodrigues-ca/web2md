#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import html2text
import argparse
import sys
import os
import time
from urllib.parse import urljoin, urlparse, urlunparse
import re
from collections import deque

def get_links_from_page(soup, base_url, same_domain_only=True):
    links = set()
    base_domain = urlparse(base_url).netloc
    
    for link in soup.find_all('a', href=True):
        href = link['href'].strip()
        if not href or href.startswith('#') or href.startswith('mailto:') or href.startswith('tel:'):
            continue
            
        absolute_url = urljoin(base_url, href)
        parsed_url = urlparse(absolute_url)
        
        if same_domain_only and parsed_url.netloc != base_domain:
            continue
            
        clean_url = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, '', '', ''))
        links.add(clean_url)
    
    return links

def sanitize_filename(url):
    parsed = urlparse(url)
    filename = parsed.path.strip('/')
    if not filename:
        filename = 'index'
    
    filename = re.sub(r'[^\w\-_./]', '_', filename)
    filename = filename.replace('/', '_')
    
    if not filename.endswith('.md'):
        filename += '.md'
    
    return filename

def scrape_single_page(url, headers):
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        for script in soup(["script", "style"]):
            script.decompose()
        
        h = html2text.HTML2Text()
        h.ignore_links = False
        h.ignore_images = False
        h.body_width = 0
        h.unicode_snob = True
        h.mark_code = True
        
        markdown_content = h.handle(str(soup))
        
        return markdown_content, soup
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}", file=sys.stderr)
        return None, None
    except Exception as e:
        print(f"Error processing {url}: {e}", file=sys.stderr)
        return None, None

def scrape_website_recursive(start_url, output_dir=None, max_depth=3, delay=1):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    visited = set()
    to_visit = deque([(start_url, 0)])
    scraped_content = {}
    
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    
    while to_visit:
        current_url, depth = to_visit.popleft()
        
        if current_url in visited or depth > max_depth:
            continue
            
        print(f"Scraping (depth {depth}): {current_url}")
        visited.add(current_url)
        
        markdown_content, soup = scrape_single_page(current_url, headers)
        
        if markdown_content:
            scraped_content[current_url] = markdown_content
            
            if output_dir:
                filename = sanitize_filename(current_url)
                filepath = os.path.join(output_dir, filename)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(f"# {current_url}\n\n{markdown_content}")
                print(f"Saved: {filepath}")
            
            if depth < max_depth:
                links = get_links_from_page(soup, current_url)
                for link in links:
                    if link not in visited:
                        to_visit.append((link, depth + 1))
        
        if delay > 0:
            time.sleep(delay)
    
    return scraped_content

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    markdown_content, _ = scrape_single_page(url, headers)
    
    if markdown_content:
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            print(f"Markdown saved to: {output_file}")
        else:
            print(markdown_content)
            
    return markdown_content

def main():
    parser = argparse.ArgumentParser(description='Convert website content to Markdown')
    parser.add_argument('url', help='Website URL to scrape')
    parser.add_argument('-o', '--output', help='Output file path (single page) or directory (recursive)')
    parser.add_argument('-r', '--recursive', action='store_true', help='Scrape recursively following links')
    parser.add_argument('-d', '--max-depth', type=int, default=3, help='Maximum recursion depth (default: 3)')
    parser.add_argument('--delay', type=float, default=1, help='Delay between requests in seconds (default: 1)')
    
    args = parser.parse_args()
    
    if not args.url.startswith(('http://', 'https://')):
        args.url = 'https://' + args.url
    
    if args.recursive:
        if args.output and not os.path.isdir(args.output):
            os.makedirs(args.output, exist_ok=True)
        
        output_dir = args.output or 'scraped_content'
        print(f"Starting recursive scrape of {args.url} (max depth: {args.max_depth})")
        scraped_content = scrape_website_recursive(args.url, output_dir, args.max_depth, args.delay)
        print(f"\nScraping complete! Scraped {len(scraped_content)} pages.")
        print(f"Content saved to directory: {output_dir}")
    else:
        scrape_website_to_markdown(args.url, args.output)

if __name__ == '__main__':
    main()