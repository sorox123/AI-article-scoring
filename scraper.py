import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import time
import json
import re
from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor, as_completed

class AINewsScraper:
    def __init__(self, urls_file='urls.txt'):
        self.urls = self._load_urls(urls_file)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.results = []
        
    def _load_urls(self, filename):
        """Load URLs from file"""
        with open(filename, 'r') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    def fetch_title(self, url):
        """Fetch title from a single URL"""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Try multiple methods to get title
            title = None
            
            # Method 1: meta og:title
            og_title = soup.find('meta', property='og:title')
            if og_title and og_title.get('content'):
                title = og_title['content']
            
            # Method 2: meta twitter:title
            if not title:
                twitter_title = soup.find('meta', attrs={'name': 'twitter:title'})
                if twitter_title and twitter_title.get('content'):
                    title = twitter_title['content']
            
            # Method 3: h1 tag
            if not title:
                h1 = soup.find('h1')
                if h1:
                    title = h1.get_text(strip=True)
            
            # Method 4: title tag
            if not title:
                title_tag = soup.find('title')
                if title_tag:
                    title = title_tag.get_text(strip=True)
            
            if title:
                # Clean up title
                title = re.sub(r'\s+', ' ', title).strip()
                return {'url': url, 'title': title, 'status': 'success'}
            else:
                return {'url': url, 'title': None, 'status': 'no_title'}
                
        except requests.exceptions.Timeout:
            return {'url': url, 'title': None, 'status': 'timeout'}
        except requests.exceptions.RequestException as e:
            return {'url': url, 'title': None, 'status': f'error: {str(e)[:50]}'}
        except Exception as e:
            return {'url': url, 'title': None, 'status': f'parse_error: {str(e)[:50]}'}
    
    def scrape_all(self, max_workers=5):
        """Scrape all URLs with parallel processing"""
        print(f"Starting to scrape {len(self.urls)} URLs...")
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(self.fetch_title, url): url for url in self.urls}
            
            for i, future in enumerate(as_completed(futures), 1):
                result = future.result()
                self.results.append(result)
                
                if result['status'] == 'success':
                    print(f"[{i}/{len(self.urls)}] ✓ {result['title'][:80]}")
                else:
                    print(f"[{i}/{len(self.urls)}] ✗ {result['status']} - {result['url'][:60]}")
                
                # Small delay to be respectful
                time.sleep(0.1)
        
        return self.results
    
    def categorize_source_credibility(self, url):
        """Categorize source credibility level"""
        domain = urlparse(url).netloc.lower()
        
        # High credibility - established tech/academic outlets
        high_credibility = [
            'technologyreview.com', 'spectrum.ieee.org', 'techcrunch.com',
            'venturebeat.com', 'fortune.com', 'cnbc.com', 'theverge.com',
            'nature.com', 'sciencemag.org', 'acm.org', 'ai.meta.com',
            'blog.google', 'anthropic.com', 'openai.com', 'deepmind.google',
            'blog.ml.cmu.edu', 'karpathy.ai', 'lilianweng.github.io',
            'ben-evans.com', 'stratechery.com', 'deeplearning.ai'
        ]
        
        # Medium credibility - established blogs, some Medium, newsletters
        medium_credibility = [
            'towardsai.net', 'analyticsvidhya.com', 'hackernoon.com',
            'kdnuggets.com', 'sebastianraschka.com', 'alignmentforum.org',
            'lesswrong.com', 'oneusefulthing.org', 'jack-clark.net',
            'situational-awareness.ai'
        ]
        
        # Low-medium credibility - general Medium posts, aggregators
        low_medium_credibility = [
            'medium.com', 'towardsdatascience.com', 'substack.com'
        ]
        
        # Low credibility - questionable sources, sensational sites
        low_credibility = [
            'machine.news', 'ts2.tech', 'penbrief.com', 'rollingstone.com',
            'threadreaderapp.com', 'twitter.com', 'x.com'
        ]
        
        for source in high_credibility:
            if source in domain:
                return 'HIGH'
        for source in medium_credibility:
            if source in domain:
                return 'MEDIUM'
        for source in low_medium_credibility:
            if source in domain:
                return 'MEDIUM-LOW'
        for source in low_credibility:
            if source in domain:
                return 'LOW'
        
        return 'UNKNOWN'
    
    def analyze_truth_level(self, title, url):
        """Estimate how true/verifiable a claim sounds"""
        credibility = self.categorize_source_credibility(url)
        
        # Patterns that suggest actual verifiable facts
        verifiable_patterns = [
            r'announces?', r'launches?', r'releases?', r'unveils?',
            r'raises? \$\d+', r'funding', r'acquired?',
            r'study shows?', r'research finds?', r'report'
        ]
        
        # Patterns that suggest speculation/prediction
        speculation_patterns = [
            r'predicts?', r'will be', r'could be', r'might',
            r'forecasts?', r'expects?', r'by \d{4}',
            r'next', r'future', r'soon'
        ]
        
        # Patterns that suggest extreme/unlikely claims
        extreme_patterns = [
            r'living viruses', r'please die', r'apocalypse',
            r'end of (?:the world|humanity|everything)',
            r'superintelligence', r'AGI by', r'crushes',
            r'changed everything', r'biggest.*ever'
        ]
        
        verifiable_count = sum(1 for p in verifiable_patterns if re.search(p, title, re.IGNORECASE))
        speculation_count = sum(1 for p in speculation_patterns if re.search(p, title, re.IGNORECASE))
        extreme_count = sum(1 for p in extreme_patterns if re.search(p, title, re.IGNORECASE))
        
        # Determine truth level
        if extreme_count >= 2:
            truth_level = 'EXTREME_CLAIM'
        elif extreme_count >= 1 and credibility in ['LOW', 'UNKNOWN']:
            truth_level = 'LIKELY_FALSE'
        elif extreme_count >= 1 and credibility in ['HIGH', 'MEDIUM']:
            truth_level = 'SHOCKING_BUT_TRUE'
        elif speculation_count > verifiable_count:
            truth_level = 'SPECULATION'
        elif verifiable_count > 0:
            truth_level = 'LIKELY_TRUE'
        else:
            truth_level = 'UNCERTAIN'
        
        return truth_level
    
    def analyze_titles(self):
        """Analyze titles to find ones that sound fake but might be true"""
        
        # Keywords and patterns that make titles sound sensational/fake
        sensational_patterns = [
            r'breakthrough',
            r'shock',
            r'revolutionar',
            r'biggest',
            r'changed everything',
            r'crushes',
            r'doom',
            r'frightening',
            r'apocal',
            r'\d+\s*(million|billion)',
            r'AGI',
            r'superintelligence',
            r'living viruses',
            r'deceive',
            r'faking',
            r'please die',
            r'\$\d+',
            r'more.*than people',
            r'end of',
            r'beginning of the end',
            r'beat.*gpt',
            r'better than',
            r'top \d+',
            r'best.*ever',
            r'what.*looks like',
            r'2027',
            r'2030',
            r'alignment faking',
            r'astonishing',
            r'ultimate',
            r'definitive',
            r'threatening',
        ]
        
        analyzed = []
        for result in self.results:
            if result['status'] == 'success' and result['title']:
                title = result['title']
                url = result['url']
                score = 0
                matched_patterns = []
                
                for pattern in sensational_patterns:
                    if re.search(pattern, title, re.IGNORECASE):
                        score += 1
                        matched_patterns.append(pattern)
                
                # Additional scoring for specific characteristics
                if any(word in title.lower() for word in ['shocking', 'unbelievable', 'insane', 'crazy']):
                    score += 2
                
                if re.search(r'\d+', title):  # Contains numbers
                    score += 0.5
                
                if len(title) > 60:  # Long sensational titles
                    score += 0.5
                
                # Get credibility and truth level
                credibility = self.categorize_source_credibility(url)
                truth_level = self.analyze_truth_level(title, url)
                
                analyzed.append({
                    'title': title,
                    'url': url,
                    'score': score,
                    'patterns': matched_patterns,
                    'credibility': credibility,
                    'truth_level': truth_level
                })
        
        # Sort by score
        analyzed.sort(key=lambda x: x['score'], reverse=True)
        return analyzed
    
    def save_results(self, filename='results.json'):
        """Save all results to JSON"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        print(f"\nAll results saved to {filename}")
    
    def save_fake_sounding_titles(self, analyzed, filename='fake_sounding_titles.json', min_count=25):
        """Save the most fake-sounding titles from diverse credibility sources"""
        # Group by credibility first
        by_credibility = {
            'HIGH': [],
            'MEDIUM': [],
            'MEDIUM-LOW': [],
            'LOW': [],
            'UNKNOWN': []
        }
        
        for item in analyzed:
            if item['score'] > 0:  # Only sensational titles
                by_credibility[item['credibility']].append(item)
        
        # Sort each credibility group by how fake-sounding they are (score)
        for cred in by_credibility:
            by_credibility[cred].sort(key=lambda x: x['score'], reverse=True)
        
        # Take the MOST fake-sounding from each credibility level
        # This ensures we get a diverse range of sources
        diverse_titles = []
        diverse_titles.extend(by_credibility['HIGH'][:12])      # Top 12 from high-cred sources
        diverse_titles.extend(by_credibility['MEDIUM'][:8])     # Top 8 from medium-cred
        diverse_titles.extend(by_credibility['MEDIUM-LOW'][:8]) # Top 8 from medium-low
        diverse_titles.extend(by_credibility['LOW'][:8])        # Top 8 from low-cred
        diverse_titles.extend(by_credibility['UNKNOWN'][:4])    # Top 4 from unknown
        
        # Sort final list by fake-sounding score (but we've already ensured diversity)
        diverse_titles.sort(key=lambda x: x['score'], reverse=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(diverse_titles, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Saved {len(diverse_titles)} fake-sounding titles from diverse sources to {filename}")
        
        # Show what we got from each credibility level
        cred_counts = {}
        for item in diverse_titles:
            cred_counts[item['credibility']] = cred_counts.get(item['credibility'], 0) + 1
        
        print("\n  Distribution by source credibility:")
        for cred in ['HIGH', 'MEDIUM', 'MEDIUM-LOW', 'LOW', 'UNKNOWN']:
            if cred in cred_counts:
                print(f"    {cred}: {cred_counts[cred]} articles (most fake-sounding from this tier)")
        
        return diverse_titles

def main():
    scraper = AINewsScraper()
    
    # Scrape all URLs
    results = scraper.scrape_all(max_workers=8)
    
    # Save all results
    scraper.save_results()
    
    # Analyze and find fake-sounding titles
    print("\n" + "="*80)
    print("ANALYZING TITLES FOR SENSATIONAL/FAKE-SOUNDING CONTENT")
    print("="*80)
    
    analyzed = scraper.analyze_titles()
    top_titles = scraper.save_fake_sounding_titles(analyzed)
    
    # Display results grouped by credibility
    print("\n" + "="*80)
    print("FAKE-SOUNDING ARTICLES FROM DIVERSE SOURCES")
    print("="*80)
    print("\nShowing the MOST fake-sounding articles from each credibility tier:")
    print("(This ensures you get diverse sources, not just clickbait sites)\n")
    
    # Group by credibility for display
    by_cred = {}
    for item in top_titles:
        if item['credibility'] not in by_cred:
            by_cred[item['credibility']] = []
        by_cred[item['credibility']].append(item)
    
    # Display each credibility tier
    tier_order = ['HIGH', 'MEDIUM', 'MEDIUM-LOW', 'LOW', 'UNKNOWN']
    overall_count = 1
    
    for tier in tier_order:
        if tier in by_cred and by_cred[tier]:
            print(f"\n{'='*80}")
            print(f"📊 {tier} CREDIBILITY SOURCES ({len(by_cred[tier])} articles)")
            print(f"{'='*80}\n")
            
            for item in by_cred[tier]:
                print(f"{overall_count}. [Score: {item['score']:.1f}] {item['title']}")
                domain = urlparse(item['url']).netloc
                print(f"   Source: {domain}")
                print(f"   URL: {item['url']}")
                if item['patterns']:
                    print(f"   Why it sounds fake: {', '.join(item['patterns'][:4])}")
                print()
                overall_count += 1
    
    # Summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"✓ Successfully scraped {len([r for r in results if r['status'] == 'success'])} articles")
    print(f"✓ Found {len(top_titles)} fake-sounding articles across all credibility levels")
    print(f"✓ Distribution ensures diverse sources (not just clickbait)")
    
    cred_counts = {}
    for item in top_titles:
        cred_counts[item['credibility']] = cred_counts.get(item['credibility'], 0) + 1
    
    print("\n  Articles per credibility tier:")
    for tier in tier_order:
        if tier in cred_counts:
            print(f"    {tier}: {cred_counts[tier]}")

if __name__ == '__main__':
    main()
