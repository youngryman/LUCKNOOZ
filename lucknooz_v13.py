#!/usr/bin/env python3
"""
LuckNooz V13.3 - NLTK-Based Verb Detection
Fetches news headlines, splits at first verb using NLTK POS tagging, and creates remixed headlines
"""

import feedparser
import json
import random
from datetime import datetime
import nltk

# Download required NLTK data (will only download if not present)
try:
    nltk.data.find('taggers/averaged_perceptron_tagger')
except LookupError:
    nltk.download('averaged_perceptron_tagger', quiet=True)

# RSS Feeds to scrape with display names
FEEDS = [
    {'url': 'https://feeds.bbci.co.uk/news/world/rss.xml', 'name': 'BBC News'},
    {'url': 'https://rss.nytimes.com/services/xml/rss/nyt/World.xml', 'name': 'The New York Times'},
    {'url': 'https://feeds.npr.org/1001/rss.xml', 'name': 'NPR'},
    {'url': 'https://www.theguardian.com/world/rss', 'name': 'The Guardian'},
    {'url': 'https://www.espn.com/espn/rss/news', 'name': 'ESPN'},
    {'url': 'https://www.rollingstone.com/feed/', 'name': 'Rolling Stone'},
    {'url': 'https://feeds.arstechnica.com/arstechnica/index', 'name': 'Ars Technica'}
]

# Question words that indicate headlines to skip
QUESTION_WORDS = {'why', 'what', 'when', 'where', 'who', 'how', 'which'}

# Words to always skip as potential verbs
SKIP_WORDS = {
    'the', 'a', 'an', 'this', 'that', 'these', 'those',
    'will', 'would', 'should', 'could', 'might', 'may', 'must', 'can',
    'to', 'for', 'of', 'in', 'on', 'at', 'by', 'with', 'from', 'about', 'as'
}

# Never treat these as verbs (even if NLTK tags them as such)
NEVER_VERBS = {
    'news', 'report', 'update', 'story', 'article', 'poll', 'data',
    'study', 'research', 'analysis', 'review', 'survey'
}

# Common nouns that might follow -ing/-ed adjectives
COMMON_NOUNS = {
    'palestinians', 'singer', 'officer', 'artist', 'player', 'athletes',
    'leader', 'minister', 'president', 'official', 'expert', 'officials',
    'scientist', 'researcher', 'student', 'teacher', 'doctor', 'scientists',
    'people', 'man', 'woman', 'child', 'person', 'group', 'members',
    'victims', 'survivors', 'residents', 'citizens', 'voters', 'workers'
}


def find_first_verb(headline):
    """Find the first verb in a headline using NLTK POS tagging."""
    words = headline.split()
    
    # Skip question headlines
    if words and words[0].lower().rstrip(',:;?!') in QUESTION_WORDS:
        return None
    
    # Use NLTK to tag parts of speech
    try:
        tagged = nltk.pos_tag(words)
    except Exception as e:
        print(f"Error tagging headline: {headline[:50]}... - {e}")
        return None
    
    # Look for first verb (start from index 1 to ensure subject has at least 1 word)
    for i in range(1, len(tagged)):
        word, pos = tagged[i]
        word_lower = ''.join(c for c in word.lower() if c.isalpha())
        prev_word = words[i - 1].lower() if i > 0 else ''
        
        # Skip if empty after cleanup
        if not word_lower:
            continue
        
        # Skip determiners and function words
        if word_lower in SKIP_WORDS:
            continue
        
        # Skip never-verbs
        if word_lower in NEVER_VERBS:
            continue
        
        # Skip if previous word is a skip word (likely not a verb)
        if prev_word in SKIP_WORDS:
            continue
        
        # Skip if all caps (likely acronym)
        if word.isupper() and len(word) > 1:
            continue
        
        # Skip if word is part of a hyphenated compound
        if i > 0 and words[i - 1].endswith('-'):
            continue
        
        # Check if this is a verb according to NLTK
        # VB = verb base form, VBD = past tense, VBG = gerund/present participle
        # VBN = past participle, VBP = present tense, VBZ = 3rd person singular present
        if pos.startswith('VB'):
            # Additional check: if it's VBG or VBN (participles), make sure it's not an adjective
            if pos in ['VBG', 'VBN']:
                # Check if followed by a noun (which would make this an adjective)
                if i < len(tagged) - 1:
                    next_word, next_pos = tagged[i + 1]
                    next_word_lower = ''.join(c for c in next_word.lower() if c.isalpha())
                    
                    # If next word is a noun or in our common nouns list, skip this verb
                    if next_pos.startswith('NN') or next_word_lower in COMMON_NOUNS:
                        continue
            
            # Found a valid verb!
            subject = ' '.join(words[:i])
            predicate = ' '.join(words[i:])
            return {
                'subject': subject,
                'predicate': predicate,
                'verb': word
            }
    
    return None


def is_plural(subject):
    """Determine if a subject is plural."""
    subject_lower = subject.lower().strip()
    
    # Check for plural indicators
    if ' and ' in subject_lower:
        return True
    
    plural_indicators = ['several', 'many', 'both', 'all', 'some', 'most', 'few']
    for indicator in plural_indicators:
        if subject_lower.startswith(indicator + ' '):
            return True
    
    # Use NLTK to check if last word is plural noun
    words = subject.split()
    if not words:
        return False
    
    try:
        tagged = nltk.pos_tag(words)
        last_word, last_pos = tagged[-1]
        
        # NNS = plural noun, NNPS = plural proper noun
        if last_pos in ['NNS', 'NNPS']:
            return True
    except:
        pass
    
    # Fallback to simple check
    last_word = ''.join(c for c in words[-1].lower() if c.isalpha())
    if last_word.endswith('s') and not last_word.endswith('ss') and len(last_word) > 3:
        return True
    
    return False


def conjugate_verb(verb, subject_is_plural):
    """Conjugate a verb to match subject number."""
    verb_lower = verb.lower()
    
    # Handle "to be" specially
    if verb_lower in ['is', 'are']:
        return 'are' if subject_is_plural else 'is'
    if verb_lower in ['was', 'were']:
        return 'were' if subject_is_plural else 'was'
    
    # Don't conjugate past tense or progressive forms
    if verb_lower.endswith('ed') or verb_lower.endswith('ing'):
        return verb
    
    # If plural, remove -s/-es
    if subject_is_plural:
        if verb_lower.endswith('ies'):
            return verb[:-3] + 'y'
        if verb_lower.endswith('es'):
            return verb[:-2]
        if verb_lower.endswith('s') and not verb_lower.endswith('ss'):
            return verb[:-1]
        return verb
    
    # If singular, add -s/-es
    if not subject_is_plural:
        if not verb_lower.endswith('s'):
            if verb_lower.endswith(('ch', 'sh', 'x', 'z', 'o')):
                return verb + 'es'
            if verb_lower.endswith('y') and len(verb_lower) > 1:
                if verb_lower[-2] not in 'aeiou':
                    return verb[:-1] + 'ies'
            return verb + 's'
    
    return verb


def fetch_headlines():
    """Fetch headlines from RSS feeds with source tracking."""
    all_headlines = []
    
    for feed_info in FEEDS:
        feed_url = feed_info['url']
        feed_name = feed_info['name']
        
        try:
            print(f"Fetching {feed_name}...")
            feed = feedparser.parse(feed_url)
            
            for entry in feed.entries:
                title = entry.get('title', '').strip()
                link = entry.get('link', '')
                
                if title:
                    parsed = find_first_verb(title)
                    if parsed:
                        parsed['original_headline'] = title
                        parsed['source'] = feed_name
                        parsed['link'] = link
                        all_headlines.append(parsed)
        except Exception as e:
            print(f"Error fetching {feed_name}: {e}")
    
    return all_headlines


def remix_headlines(headlines, count=50):
    """Create remixed headlines by swapping subjects and predicates."""
    if len(headlines) < 2:
        return []
    
    subjects = headlines.copy()
    predicates = headlines.copy()
    random.shuffle(predicates)
    
    # Ensure no headline is paired with itself
    for i in range(len(subjects)):
        if i < len(predicates) and subjects[i]['original_headline'] == predicates[i]['original_headline']:
            # Swap with next one (or previous if at end)
            swap_idx = (i + 1) if i < len(predicates) - 1 else (i - 1)
            if swap_idx >= 0 and swap_idx < len(predicates):
                predicates[i], predicates[swap_idx] = predicates[swap_idx], predicates[i]
    
    remixed = []
    
    for i in range(min(count, len(subjects))):
        subject_obj = subjects[i]
        predicate_obj = predicates[i]
        
        # Double-check we didn't pair with self
        if subject_obj['original_headline'] == predicate_obj['original_headline']:
            continue
        
        subject = subject_obj['subject']
        predicate = predicate_obj['predicate']
        
        # Extract verb from predicate (first word)
        pred_words = predicate.split()
        if pred_words:
            verb = pred_words[0]
            subject_is_plural = is_plural(subject)
            conjugated_verb = conjugate_verb(verb, subject_is_plural)
            
            # Replace verb in predicate
            new_predicate = ' '.join([conjugated_verb] + pred_words[1:])
            remixed_headline = f"{subject} {new_predicate}"
        else:
            remixed_headline = f"{subject} {predicate}"
        
        remixed.append({
            'headline': remixed_headline,
            'subject_source': {
                'original': subject_obj['original_headline'],
                'source': subject_obj['source'],
                'link': subject_obj['link']
            },
            'predicate_source': {
                'original': predicate_obj['original_headline'],
                'source': predicate_obj['source'],
                'link': predicate_obj['link']
            }
        })
    
    return remixed


def main():
    """Main function to fetch, process, and save headlines."""
    print("LuckNooz V13.3 - NLTK-Based Verb Detection")
    print("=" * 50)
    
    # Fetch headlines
    print("\nFetching headlines from RSS feeds...")
    headlines = fetch_headlines()
    print(f"Found {len(headlines)} parseable headlines")
    
    if len(headlines) < 2:
        print("Not enough headlines found. Exiting.")
        return
    
    # Create remixed headlines
    print("\nRemixing headlines...")
    remixed = remix_headlines(headlines, count=50)
    
    # Prepare output
    output = {
        'generated_at': datetime.now().isoformat(),
        'version': '13.3',
        'count': len(remixed),
        'headlines': remixed
    }
    
    # Save to JSON
    output_file = 'lucknooz-headlines.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"\nSaved {len(remixed)} remixed headlines to {output_file}")
    
    # Print sample
    print("\nSample headlines:")
    for i, item in enumerate(remixed[:10], 1):
        print(f"{i}. {item['headline']}")


if __name__ == '__main__':
    main()
