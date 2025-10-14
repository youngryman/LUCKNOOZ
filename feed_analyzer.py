#!/usr/bin/env python3
"""
RSS Feed Analyzer for LUCKNOOZ
Tests RSS feeds and reports statistics to help select the best feeds
"""

import feedparser
import re
from collections import defaultdict
import statistics

# Test feeds - your current ones plus potential new ones
TEST_FEEDS = {
    # Current feeds
    'NY Times': 'https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml',
    'BBC World': 'https://feeds.bbci.co.uk/news/world/rss.xml',
    'WSJ World': 'https://feeds.a.dj.com/rss/RSSWorldNews.xml',
    'Guardian': 'https://www.theguardian.com/world/rss',
    'Nature': 'https://www.nature.com/nature.rss',
    'Variety': 'https://variety.com/feed/',
    'NPR': 'https://feeds.npr.org/1001/rss.xml',
    
    # User-requested additions
    'AlterNet': 'https://www.alternet.org/feeds/feed.rss',
    'HuffPost': 'https://chaski.huffpost.com/us/auto/vertical/world-news',

    'Japan Times': 'https://www.japantimes.co.jp/feed/',
    'Fox News': 'https://moxie.foxnews.com/google-publisher/latest.xml',
    'CNN': 'http://rss.cnn.com/rss/edition.rss',
    
    # Potential new feeds - News
    'BBC UK': 'https://feeds.bbci.co.uk/news/uk/rss.xml',
    'Al Jazeera': 'https://www.aljazeera.com/xml/rss/all.xml',
    'Reuters (alt)': 'http://feeds.reuters.com/Reuters/worldNews',
    'AP News': 'https://apnews.com/rss',
    'USA Today': 'https://rssfeeds.usatoday.com/usatoday-NewsTopStories',
    'CBS News': 'https://www.cbsnews.com/latest/rss/main',
    'Politico': 'https://www.politico.com/rss/politicopicks.xml',
    
    # Tech (often terse)
    'TechCrunch': 'https://techcrunch.com/feed/',
    'The Verge': 'https://www.theverge.com/rss/index.xml',
    'Ars Technica': 'https://feeds.arstechnica.com/arstechnica/index',
    'Wired': 'https://www.wired.com/feed/rss',
    'CNET': 'https://www.cnet.com/rss/news/',
    'Engadget': 'https://www.engadget.com/rss.xml',
    
    # Sports (very terse, active verbs)
    'ESPN': 'https://www.espn.com/espn/rss/news',
    'ESPN NFL': 'https://www.espn.com/espn/rss/nfl/news',
    'ESPN NBA': 'https://www.espn.com/espn/rss/nba/news',
    'BBC Sport': 'https://feeds.bbci.co.uk/sport/rss.xml',
    'Sky Sports': 'https://www.skysports.com/rss/12040',
    
    # Entertainment (dramatic language)
    'Hollywood Reporter': 'https://www.hollywoodreporter.com/feed/',
    'Rolling Stone': 'https://www.rollingstone.com/feed/',
    'Deadline': 'https://deadline.com/feed/',
    
    # Business
    'Forbes': 'https://www.forbes.com/real-time/feed2/',
    'Business Insider': 'https://www.businessinsider.com/rss',
    'MarketWatch': 'https://www.marketwatch.com/rss/topstories',
    
    # Science
    'Science Daily': 'https://www.sciencedaily.com/rss/all.xml',
    'New Scientist': 'https://www.newscientist.com/feed/home',
}

def find_first_verb(title):
    """
    Simplified verb detection (same logic as your generator script)
    Returns the position of the first verb, or -1 if none found
    """
    words = title.split()
    
    # Skip questions
    question_words = {'who', 'what', 'where', 'when', 'why', 'how', 'which', 'whose'}
    if words and words[0].lower() in question_words:
        return -1
    
    # Look for verb patterns
    verb_indicators = [
        'ing ', 'ed ', 'es ', 's ', 'will ', 'can ', 'could ',
        'may ', 'might ', 'must ', 'should ', 'would '
    ]
    
    for i, word in enumerate(words):
        # Skip first word if it's a gerund
        if i == 0 and word.lower().endswith('ing'):
            continue
            
        # Skip if preceded by "the", "a", "an"
        if i > 0 and words[i-1].lower() in ['the', 'a', 'an']:
            continue
            
        word_lower = word.lower()
        
        # Check for common verb forms
        if any(word_lower.endswith(ind.strip()) for ind in verb_indicators):
            return i
            
        # Check for auxiliary verbs
        if word_lower in ['is', 'are', 'was', 'were', 'has', 'have', 'had', 
                          'will', 'would', 'can', 'could', 'may', 'might']:
            return i
    
    return -1

def analyze_feed(feed_url, feed_name):
    """
    Analyze a single feed and return statistics
    """
    try:
        print(f"Testing {feed_name}...", end=' ')
        feed = feedparser.parse(feed_url)
        
        if not feed.entries:
            print("❌ No entries found")
            return None
            
        headlines = []
        word_counts = []
        parseable = 0
        
        for entry in feed.entries[:30]:  # Test first 30 headlines
            title = entry.get('title', '').strip()
            if not title:
                continue
                
            # Clean title
            title = re.sub(r'<[^>]+>', '', title)  # Remove HTML
            title = re.sub(r'\s+', ' ', title).strip()  # Normalize whitespace
            
            headlines.append(title)
            word_count = len(title.split())
            word_counts.append(word_count)
            
            # Check if parseable (has a verb we can detect)
            verb_pos = find_first_verb(title)
            if verb_pos > 0:  # Need at least one word before the verb
                parseable += 1
        
        if not headlines:
            print("❌ No valid headlines")
            return None
            
        total = len(headlines)
        avg_words = statistics.mean(word_counts)
        parse_rate = (parseable / total) * 100
        
        print(f"✅ {total} headlines")
        
        return {
            'name': feed_name,
            'url': feed_url,
            'total_headlines': total,
            'avg_words': avg_words,
            'min_words': min(word_counts),
            'max_words': max(word_counts),
            'parseable': parseable,
            'parse_rate': parse_rate,
            'sample_headlines': headlines[:5]
        }
        
    except Exception as e:
        print(f"❌ Error: {str(e)[:50]}")
        return None

def main():
    print("=" * 80)
    print("LUCKNOOZ RSS Feed Analyzer")
    print("=" * 80)
    print()
    
    results = []
    
    # Test all feeds
    for feed_name, feed_url in TEST_FEEDS.items():
        result = analyze_feed(feed_url, feed_name)
        if result:
            results.append(result)
    
    print()
    print("=" * 80)
    print("ANALYSIS RESULTS")
    print("=" * 80)
    print()
    
    if not results:
        print("No feeds successfully analyzed.")
        return
    
    # Sort by parse rate (best first)
    results.sort(key=lambda x: x['parse_rate'], reverse=True)
    
    # Display detailed results
    print(f"{'Feed Name':<25} {'Avg Words':<12} {'Parse Rate':<12} {'Total':<8}")
    print("-" * 80)
    
    for r in results:
        print(f"{r['name']:<25} {r['avg_words']:>6.1f} words   {r['parse_rate']:>5.1f}%       {r['total_headlines']:>4}")
    
    print()
    print("=" * 80)
    print("RANKINGS")
    print("=" * 80)
    print()
    
    # Rank by terseness (shorter = better)
    print("🏆 MOST TERSE (Shortest Headlines):")
    terse = sorted(results, key=lambda x: x['avg_words'])[:10]
    for i, r in enumerate(terse, 1):
        print(f"{i:2}. {r['name']:<25} {r['avg_words']:>6.1f} words")
    
    print()
    print("🎯 BEST PARSE RATE (Most Parseable):")
    best_parse = sorted(results, key=lambda x: x['parse_rate'], reverse=True)[:10]
    for i, r in enumerate(best_parse, 1):
        print(f"{i:2}. {r['name']:<25} {r['parse_rate']:>5.1f}%")
    
    print()
    print("⭐ RECOMMENDED FEEDS (Terse + High Parse Rate):")
    # Calculate composite score: prefer shorter headlines with high parse rates
    for r in results:
        # Normalize scores (lower word count is better, higher parse rate is better)
        word_score = 100 - (r['avg_words'] * 5)  # Penalize long headlines
        parse_score = r['parse_rate']
        r['composite_score'] = (word_score + parse_score) / 2
    
    recommended = sorted(results, key=lambda x: x['composite_score'], reverse=True)[:15]
    for i, r in enumerate(recommended, 1):
        print(f"{i:2}. {r['name']:<25} {r['avg_words']:>6.1f} words, {r['parse_rate']:>5.1f}% parse")
    
    print()
    print("=" * 80)
    print("SAMPLE HEADLINES")
    print("=" * 80)
    print()
    
    # Show samples from top 3 recommended feeds
    for r in recommended[:3]:
        print(f"\n{r['name']} (avg {r['avg_words']:.1f} words):")
        print("-" * 60)
        for headline in r['sample_headlines']:
            verb_pos = find_first_verb(headline)
            if verb_pos > 0:
                words = headline.split()
                subject = ' '.join(words[:verb_pos])
                predicate = ' '.join(words[verb_pos:])
                print(f"  ✓ [{subject}] | [{predicate}]")
            else:
                print(f"  ✗ {headline}")
    
    print()
    print("=" * 80)
    print("STATISTICS SUMMARY")
    print("=" * 80)
    print()
    
    all_avg_words = [r['avg_words'] for r in results]
    all_parse_rates = [r['parse_rate'] for r in results]
    
    print(f"Total feeds analyzed: {len(results)}")
    print(f"Average headline length: {statistics.mean(all_avg_words):.1f} words")
    print(f"Average parse rate: {statistics.mean(all_parse_rates):.1f}%")
    print(f"Shortest avg headlines: {min(all_avg_words):.1f} words ({[r['name'] for r in results if r['avg_words'] == min(all_avg_words)][0]})")
    print(f"Longest avg headlines: {max(all_avg_words):.1f} words ({[r['name'] for r in results if r['avg_words'] == max(all_avg_words)][0]})")
    print()

if __name__ == "__main__":
    main()