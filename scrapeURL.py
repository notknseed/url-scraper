import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
from collections import deque
import re

class WebsiteScraper:
    def __init__(self, base_url, max_depth=2, delay=1, include_external=False):
        self.base_url = base_url
        self.domain = urlparse(base_url).netloc
        self.max_depth = max_depth
        self.delay = delay
        self.include_external = include_external
        self.visited_urls = set()
        self.internal_urls = set()
        self.external_urls = set()
        
    def is_valid_url(self, url):
        """Check if URL is valid"""
        parsed = urlparse(url)
        return (
            parsed.scheme in ['http', 'https'] and
            parsed.netloc and  # Must have domain
            not url.endswith(('.pdf', '.jpg', '.png', '.gif', '.zip', '.exe', '.doc', '.docx', '.mp4', '.mp3')) and
            '#' not in url and  # Skip anchor links
            'javascript:' not in url.lower() and
            'mailto:' not in url.lower() and
            'tel:' not in url.lower()
        )
    
    def is_internal_url(self, url):
        """Check if URL belongs to the same domain"""
        parsed = urlparse(url)
        return parsed.netloc == self.domain
    
    def categorize_external_url(self, url):
        """Categorize external URLs by type"""
        domain = urlparse(url).netloc.lower()
        
        # Social Media
        social_platforms = {
            'facebook.com': 'Facebook',
            'twitter.com': 'Twitter', 
            'x.com': 'X (Twitter)',
            'instagram.com': 'Instagram',
            'linkedin.com': 'LinkedIn',
            'youtube.com': 'YouTube',
            'tiktok.com': 'TikTok',
            'github.com': 'GitHub',
            'gitlab.com': 'GitLab',
            'discord.com': 'Discord',
            'telegram.org': 'Telegram',
            'whatsapp.com': 'WhatsApp'
        }
        
        # Development/Tech
        tech_platforms = {
            'stackoverflow.com': 'Stack Overflow',
            'medium.com': 'Medium',
            'dev.to': 'Dev.to',
            'hackernoon.com': 'HackerNoon',
            'reddit.com': 'Reddit',
            'npm.org': 'NPM',
            'pypi.org': 'PyPI'
        }
        
        # Check social media
        for platform, name in social_platforms.items():
            if platform in domain:
                return f"Social Media - {name}"
        
        # Check tech platforms  
        for platform, name in tech_platforms.items():
            if platform in domain:
                return f"Tech Platform - {name}"
        
        # Government/Official
        if domain.endswith('.gov') or domain.endswith('.edu'):
            return "Official/Government"
        
        # Default
        return "External Website"
    
    def get_page_links(self, url):
        """Extract all links from a single page"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            internal_links = set()
            external_links = set()
            
            # Find all anchor tags with href attributes
            for link in soup.find_all('a', href=True):
                absolute_url = urljoin(url, link['href'])
                
                if self.is_valid_url(absolute_url):
                    if self.is_internal_url(absolute_url):
                        internal_links.add(absolute_url)
                    elif self.include_external:
                        external_links.add(absolute_url)
            
            return internal_links, external_links
            
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return set(), set()
    
    def scrape_breadth_first(self):
        """Scrape using breadth-first search approach"""
        print(f"Starting BFS scraping of {self.base_url}")
        
        queue = deque([(self.base_url, 0)])  # (url, depth)
        
        while queue:
            current_url, depth = queue.popleft()
            
            if current_url in self.visited_urls or depth > self.max_depth:
                continue
                
            print(f"Scraping (depth {depth}): {current_url}")
            self.visited_urls.add(current_url)
            self.internal_urls.add(current_url)
            
            # Get links from current page
            internal_links, external_links = self.get_page_links(current_url)
            
            # Add internal links to queue for next depth level
            for link in internal_links:
                if link not in self.visited_urls:
                    queue.append((link, depth + 1))
                    self.internal_urls.add(link)
            
            # Add external links (won't be crawled further)
            self.external_urls.update(external_links)
            
            # Be respectful to the server
            time.sleep(self.delay)
        
        return {
            'internal': sorted(self.internal_urls),
            'external': sorted(self.external_urls)
        }

def method_1_comprehensive_scraper(url, max_depth=2, include_external=False):
    """Method 1: Comprehensive scraper with depth control"""
    scraper = WebsiteScraper(url, max_depth=max_depth, include_external=include_external)
    return scraper.scrape_breadth_first()

def method_2_simple_scraper(url, include_external=False):
    """Method 2: Simple single-page scraper"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        domain = urlparse(url).netloc
        internal_urls = set([url])  # Include the base URL
        external_urls = set()
        
        for link in soup.find_all('a', href=True):
            absolute_url = urljoin(url, link['href'])
            parsed = urlparse(absolute_url)
            
            # Validate URL
            if (parsed.scheme in ['http', 'https'] and 
                parsed.netloc and
                not absolute_url.endswith(('.pdf', '.jpg', '.png', '.gif', '.zip', '.exe')) and
                '#' not in absolute_url and
                'javascript:' not in absolute_url.lower() and
                'mailto:' not in absolute_url.lower()):
                
                if parsed.netloc == domain:
                    internal_urls.add(absolute_url)
                elif include_external:
                    external_urls.add(absolute_url)
        
        return {
            'internal': sorted(internal_urls),
            'external': sorted(external_urls)
        }
        
    except Exception as e:
        print(f"Error: {e}")
        return {'internal': [], 'external': []}

def method_3_sitemap_scraper(url, include_external=False):
    """Method 3: Try to find and parse sitemap.xml"""
    sitemap_urls = [
        urljoin(url, '/sitemap.xml'),
        urljoin(url, '/sitemap_index.xml'),
        urljoin(url, '/robots.txt')  # Check robots.txt for sitemap location
    ]
    
    internal_urls = set([url])
    external_urls = set()
    domain = urlparse(url).netloc
    
    for sitemap_url in sitemap_urls:
        try:
            response = requests.get(sitemap_url, timeout=10)
            if response.status_code == 200:
                if 'sitemap' in sitemap_url:
                    # Parse XML sitemap
                    soup = BeautifulSoup(response.content, 'xml')
                    for loc in soup.find_all('loc'):
                        if loc.text:
                            parsed = urlparse(loc.text)
                            if parsed.netloc == domain:
                                internal_urls.add(loc.text)
                            elif include_external:
                                external_urls.add(loc.text)
                elif 'robots.txt' in sitemap_url:
                    # Look for sitemap in robots.txt
                    for line in response.text.split('\n'):
                        if line.lower().startswith('sitemap:'):
                            sitemap_found = line.split(':', 1)[1].strip()
                            # Recursively get sitemap
                            sitemap_urls.append(sitemap_found)
        except:
            continue
    
    return {
        'internal': sorted(internal_urls),
        'external': sorted(external_urls)
    }

def method_4_selenium_alternative():
    """Method 4: Using requests-html (lightweight alternative to Selenium)"""
    try:
        from requests_html import HTMLSession
        
        def scrape_with_js(url):
            session = HTMLSession()
            r = session.get(url)
            r.html.render(timeout=20)  # Execute JavaScript
            
            urls = set([url])
            domain = urlparse(url).netloc
            
            for link in r.html.absolute_links:
                parsed = urlparse(link)
                if parsed.netloc == domain:
                    urls.add(link)
            
            session.close()
            return sorted(urls)
            
        return scrape_with_js
        
    except ImportError:
        print("requests-html not installed. Install with: pip install requests-html")
        return None

def analyze_external_urls(external_urls, scraper_instance):
    """Analyze and categorize external URLs"""
    if not external_urls:
        return {}
    
    categorized = {}
    for url in external_urls:
        category = scraper_instance.categorize_external_url(url)
        if category not in categorized:
            categorized[category] = []
        categorized[category].append(url)
    
    return categorized

# Main execution with user choice
def main():
    target_url = input("Masukkan URL website (default: https://catenalabs.com/): ").strip()
    if not target_url:
        target_url = "https://catenalabs.com/"
    
    include_external = input("Scrape external URLs juga? (y/N): ").strip().lower() == 'y'
    
    print("\nPilih method yang ingin digunakan:")
    print("1. Comprehensive Scraper (Recommended - crawl dengan kedalaman)")
    print("2. Simple Scraper (Hanya halaman utama)")
    print("3. Sitemap Scraper (Cari sitemap.xml)")
    print("4. Jalankan semua method")
    
    choice = input("\nPilihan Anda (1-4): ").strip()
    
    if choice == "1":
        max_depth = input("Max depth (default: 2): ").strip()
        max_depth = int(max_depth) if max_depth.isdigit() else 2
        
        print(f"\n=== Method 1: Comprehensive Scraper (depth: {max_depth}) ===")
        result = method_1_comprehensive_scraper(target_url, max_depth=max_depth, include_external=include_external)
        scraper_instance = WebsiteScraper(target_url, include_external=include_external)
        print_enhanced_results(result, "Method 1", scraper_instance)
        
    elif choice == "2":
        print("\n=== Method 2: Simple Scraper ===")
        result = method_2_simple_scraper(target_url, include_external=include_external)
        scraper_instance = WebsiteScraper(target_url, include_external=include_external)
        print_enhanced_results(result, "Method 2", scraper_instance)
        
    elif choice == "3":
        print("\n=== Method 3: Sitemap Scraper ===")
        result = method_3_sitemap_scraper(target_url, include_external=include_external)
        scraper_instance = WebsiteScraper(target_url, include_external=include_external)
        print_enhanced_results(result, "Method 3", scraper_instance)
        
    elif choice == "4":
        print("\n=== Menjalankan Semua Method ===")
        scraper_instance = WebsiteScraper(target_url, include_external=include_external)
        
        print("\n--- Method 1: Comprehensive Scraper ---")
        result1 = method_1_comprehensive_scraper(target_url, max_depth=2, include_external=include_external)
        print_enhanced_results(result1, "Method 1", scraper_instance)
        
        print("\n--- Method 2: Simple Scraper ---")
        result2 = method_2_simple_scraper(target_url, include_external=include_external)
        print_enhanced_results(result2, "Method 2", scraper_instance)
        
        print("\n--- Method 3: Sitemap Scraper ---")
        result3 = method_3_sitemap_scraper(target_url, include_external=include_external)
        print_enhanced_results(result3, "Method 3", scraper_instance)
        
        # Gabungkan semua hasil
        all_internal = set(result1['internal'] + result2['internal'] + result3['internal'])
        all_external = set(result1['external'] + result2['external'] + result3['external'])
        
        combined_result = {
            'internal': sorted(all_internal),
            'external': sorted(all_external)
        }
        
        print(f"\n=== HASIL GABUNGAN SEMUA METHOD ===")
        print_enhanced_results(combined_result, "Gabungan", scraper_instance)
        
    else:
        print("Pilihan tidak valid!")

def print_enhanced_results(result, method_name, scraper_instance):
    """Enhanced function to print results with categorization"""
    if isinstance(result, dict):
        internal_urls = result.get('internal', [])
        external_urls = result.get('external', [])
        
        # Print internal URLs
        if internal_urls:
            print(f"\n🏠 INTERNAL URLs ({len(internal_urls)}):")
            for url in internal_urls:
                print(url)
        
        # Print external URLs with categorization
        if external_urls:
            print(f"\n🌐 EXTERNAL URLs ({len(external_urls)}):")
            categorized = analyze_external_urls(external_urls, scraper_instance)
            
            for category, urls in categorized.items():
                print(f"\n📂 {category} ({len(urls)}):")
                for url in urls:
                    print(f" {url}")
        
        total_urls = len(internal_urls) + len(external_urls)
        print(f"\n✅ {method_name} menemukan {total_urls} URLs total ({len(internal_urls)} internal, {len(external_urls)} external)")
        
    else:
        # Backward compatibility for old format
        if result:
            for url in result:
                print(url)
            print(f"\n✅ {method_name} menemukan {len(result)} URLs")
        else:
            print(f"❌ {method_name} tidak menemukan URL")

def print_results(urls, method_name):
    """Legacy function - kept for backward compatibility"""
    if urls:
        for url in urls:
            print(url)
        print(f"\n✅ {method_name} menemukan {len(urls)} URLs")
    else:
        print(f"❌ {method_name} tidak menemukan URL")

# Quick usage functions (untuk dipanggil langsung dari code)
def quick_scrape_comprehensive(url, max_depth=2, include_external=False):
    """Quick function untuk method 1"""
    return method_1_comprehensive_scraper(url, max_depth, include_external)

def quick_scrape_simple(url, include_external=False):
    """Quick function untuk method 2"""
    return method_2_simple_scraper(url, include_external)

def quick_scrape_sitemap(url, include_external=False):
    """Quick function untuk method 3"""
    return method_3_sitemap_scraper(url, include_external)

def export_results_to_file(result, filename="scraped_urls.txt"):
    """Export results to text file"""
    with open(filename, 'w', encoding='utf-8') as f:
        if isinstance(result, dict):
            f.write("=== INTERNAL URLs ===\n")
            for url in result.get('internal', []):
                f.write(f"{url}\n")
            
            f.write(f"\n=== EXTERNAL URLs ===\n")
            for url in result.get('external', []):
                f.write(f"{url}\n")
        else:
            for url in result:
                f.write(f"{url}\n")
    
    print(f"📄 Results exported to {filename}")

if __name__ == "__main__":
    main()

# Requirements untuk menjalankan script ini:
# pip install requests beautifulsoup4 lxml
# 
# Optional untuk Method 4:
# pip install requests-html