# Website URL Scraper

A comprehensive Python-based web scraping tool that extracts and categorizes URLs from websites using multiple scraping methods.

## 📖 Overview

This tool provides 4 different methods to scrape URLs from websites:

1. **Comprehensive Scraper** - Breadth-first crawling with depth control
2. **Simple Scraper** - Single-page URL extraction  
3. **Sitemap Scraper** - Parses sitemap.xml and robots.txt
4. **All Methods** - Combines results from all approaches

## ✨ Features

- **Multi-method scraping** for comprehensive URL discovery
- **URL categorization** (internal vs external)
- **External link classification** (social media, tech platforms, government)
- **Depth control** for crawling (prevents infinite loops)
- **Rate limiting** to be respectful to target servers
- **Export functionality** to save results to files
- **Interactive CLI** with user-friendly prompts

## 🚀 Quick Start

### Windows

clone repository

```bash
git clone https://github.com/notknseed/url-scraper.git
``` 

#### For 64-bit Windows:
1. Open url-scraper folder
2. Right-click `installer_windows_64_bit.bat` → "Run as administrator"
   this will install python (if not installed yet) and all the requirements
4. Wait for installation to complete
5. Double-click `run_scraper.bat` to start scraping

#### For 32-bit Windows:
1. Download url-scraper folder
2. Right-click `installer_windows_32_bit.bat` → "Run as administrator"
   this will install python (if not installed yet) and all the requirements  
4. Wait for installation to complete
5. Double-click `run_scraper.bat` to start scraping

### macOS

1. **Install Python** (if not already installed):
   ```bash
   # Using Homebrew (recommended)
   brew install python
   
   # Or download from https://python.org/downloads/
   ```

2. **Install dependencies**:
   ```bash
   pip3 install requests beautifulsoup4 lxml
   ```

3. **Run the scraper**:
   ```bash
   python3 scrapeURL.py
   ```

### Linux (Ubuntu/Debian)

1. **Install Python and pip**:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip
   ```

2. **Install dependencies**:
   ```bash
   pip3 install requests beautifulsoup4 lxml
   ```

3. **Run the scraper**:
   ```bash
   python3 scrapeURL.py
   ```

### Linux (CentOS/RHEL/Fedora)

1. **Install Python and pip**:
   ```bash
   # CentOS/RHEL
   sudo yum install python3 python3-pip
   
   # Fedora
   sudo dnf install python3 python3-pip
   ```

2. **Install dependencies**:
   ```bash
   pip3 install requests beautifulsoup4 lxml
   ```

3. **Run the scraper**:
   ```bash
   python3 scrapeURL.py
   ```

## 📋 Requirements

- **Python 3.7+**
- **Required packages:**
  - `requests` - HTTP requests
  - `beautifulsoup4` - HTML parsing
  - `lxml` - XML parsing
- **Optional packages:**
  - `requests-html` - JavaScript rendering (for Method 4)

## 🎯 Usage

### Interactive Mode

Run the script and follow the prompts:

```bash
python scrapeURL.py
```

1. Enter target URL (default: https://catenalabs.com/)
2. Choose whether to include external URLs (y/N)
3. Select scraping method (1-4)
4. View categorized results

### Method Details

#### Method 1: Comprehensive Scraper
- **Best for:** Complete website analysis
- **Features:** Breadth-first crawling, depth control
- **Use case:** When you need all internal pages

#### Method 2: Simple Scraper  
- **Best for:** Quick single-page analysis
- **Features:** Fast, lightweight
- **Use case:** When you only need links from homepage

#### Method 3: Sitemap Scraper
- **Best for:** Well-structured websites
- **Features:** Uses sitemap.xml, robots.txt
- **Use case:** When website has proper sitemaps

#### Method 4: All Methods
- **Best for:** Maximum coverage
- **Features:** Combines all approaches
- **Use case:** When you want comprehensive results

### Quick Functions

You can also use the scraper programmatically:

```python
from scrapeURL import quick_scrape_comprehensive, quick_scrape_simple

# Comprehensive scraping
result = quick_scrape_comprehensive("https://example.com", max_depth=2)

# Simple scraping  
result = quick_scrape_simple("https://example.com")

print(result['internal'])  # Internal URLs
print(result['external'])  # External URLs
```

## 📊 Output Format

Results are categorized as:

### Internal URLs
- URLs from the same domain
- Sorted alphabetically

### External URLs (if enabled)
- **Social Media**: Facebook, Twitter, Instagram, LinkedIn, etc.
- **Tech Platforms**: GitHub, Stack Overflow, Medium, etc.
- **Official/Government**: .gov, .edu domains
- **External Websites**: Other domains

**Please ensure you:**
- Respect robots.txt
- Don't overload servers
- Follow website terms of service
- Use appropriate delays between requests

## 🔧 Troubleshooting

### Windows Issues

**Installer not working:**
- Run as Administrator
- Disable antivirus temporarily
- Check Windows execution policy

**Python not found:**
- Restart command prompt
- Reboot computer
- Manually add Python to PATH

### macOS/Linux Issues

**Permission denied:**
```bash
sudo python3 scrapeURL.py
```

**Package installation fails:**
```bash
python3 -m pip install --user requests beautifulsoup4 lxml
```

**Command not found:**
- Use `python3` instead of `python`
- Use `pip3` instead of `pip`

## 📁 File Structure

```
scrapeURL/
├── scrapeURL.py                    # Main scraper script
├── requirements.txt                # Python dependencies
├── installer_windows_64_bit.bat    # Windows 64-bit installer
├── installer_windows_32_bit.bat    # Windows 32-bit installer
├── run_scraper.bat                 # Windows launcher
└── README.md                       # This file
```

## 🤝 Contributing

Feel free to contribute by:
- Adding new scraping methods
- Improving error handling
- Adding support for more platforms
- Enhancing URL categorization

## 📄 License

This project is open source. Use responsibly and ethically.
