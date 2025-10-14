#!/usr/bin/env python3
"""
LUCKNOOZ Headline Generator - Version 12
Pre-generates fully conjugated headline combinations
"""

import feedparser
import json
import re
from datetime import datetime
import random
import spacy

# Load spaCy English model
print("Loading spaCy model...")
nlp = spacy.load('en_core_web_sm')
print("✓ spaCy loaded\n")

# RSS feeds
FEEDS = [
    'https://variety.com/feed/',
    'https://feeds.arstechnica.com/arstechnica/index',
    'https://feeds.bbci.co.uk/news/world/rss.xml',
    'https://feeds.npr.org/1001/rss.xml',
    'https://www.aljazeera.com/xml/rss/all.xml',
    'https://www.rollingstone.com/feed/',
    'https://www.japantimes.co.jp/feed/',
    'https://www.wired.com/feed/rss',
    'https://www.newscientist.com/feed/home',
    'https://moxie.foxnews.com/google-publisher/latest.xml',
    'https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml',
    'https://www.theguardian.com/world/rss',
    'https://www.nature.com/nature.rss',
    'http://rss.cnn.com/rss/edition.rss',
    'https://www.sciencedaily.com/rss/all.xml'
]

QUESTION_WORDS = {'who', 'what', 'where', 'when', 'why', 'how', 'which', 'whose'}

# Irregular verbs
IRREGULAR_VERBS = {
    'is': {'singular': 'is', 'plural': 'are', 'past': 'was'},
    'are': {'singular': 'is', 'plural': 'are', 'past': 'were'},
    'was': {'singular': 'was', 'plural': 'were', 'past': 'was'},
    'were': {'singular': 'was', 'plural': 'were', 'past': 'were'},
    'has': {'singular': 'has', 'plural': 'have', 'past': 'had'},
    'have': {'singular': 'has', 'plural': 'have', 'past': 'had'},
    'had': {'singular': 'had', 'plural': 'had', 'past': 'had'},
    'does': {'singular': 'does', 'plural': 'do', 'past': 'did'},
    'do': {'singular': 'does', 'plural': 'do', 'past': 'did'},
    'did': {'singular': 'did', 'plural': 'did', 'past': 'did'},
    'goes': {'singular': 'goes', 'plural': 'go', 'past': 'went'},
    'go': {'singular': 'goes', 'plural': 'go', 'past': 'went'},
    'went': {'singular': 'went', 'plural': 'went', 'past': 'went'},
    'says': {'singular': 'says', 'plural': 'say', 'past': 'said'},
    'say': {'singular': 'says', 'plural': 'say', 'past': 'said'},
    'said': {'singular': 'said', 'plural': 'said', 'past': 'said'}
}

def clean_headline(text):
    """Clean and normalize headline text"""
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.strip('"\'')
    return text.strip()

def is_subject_singular(subject_doc):
    """Use spaCy to determine if subject is singular or plural"""
    nouns = [token for token in subject_doc if token.pos_ in ['NOUN', 'PROPN', 'PRON']]
    
    if not nouns:
        return True
    
    # Compound subjects with "and" are plural
    if any(token.text.lower() == 'and' for token in subject_doc):
        return False
    
    head_noun = nouns[-1]
    
    # Check spaCy's morphology
    if head_noun.morph.get('Number'):
        number = head_noun.morph.get('Number')[0]
        if number == 'Plur':
            return False
        elif number == 'Sing':
            return True
    
    # Plural determiners
    plural_determiners = {'these', 'those', 'many', 'several', 'few', 'both'}
    if any(token.text.lower() in plural_determiners for token in subject_doc):
        return False
    
    # Check ending
    head_text = head_noun.text.lower()
    if head_text.endswith('s') and not head_text.endswith('ss'):
        if head_noun.pos_ == 'PROPN':
            return True
        return False
    
    return True

def get_verb_tense(verb_token):
    """Determine the tense of a verb"""
    if verb_token.tag_ in ['VBD', 'VBN']:
        return 'past'
    elif verb_token.tag_ in ['VBP', 'VBZ']:
        return 'present'
    elif verb_token.tag_ == 'VB':
        return 'base'
    
    if verb_token.text.lower() in ['was', 'were', 'had', 'did', 'went', 'said'] or verb_token.text.endswith('ed'):
        return 'past'
    
    return 'present'

def conjugate_verb(verb_text, is_singular, target_tense='present'):
    """Conjugate verb to match subject and tense"""
    verb_lower = verb_text.lower()
    
    # Handle irregular verbs
    if verb_lower in IRREGULAR_VERBS:
        if target_tense == 'past':
            return IRREGULAR_VERBS[verb_lower]['past']
        elif is_singular:
            return IRREGULAR_VERBS[verb_lower]['singular']
        else:
            return IRREGULAR_VERBS[verb_lower]['plural']
    
    # Regular verbs
    if target_tense == 'past':
        if not verb_text.endswith('ed'):
            return verb_text + 'ed'
        return verb_text
    
    # Present tense
    if is_singular:
        if verb_lower.endswith(('s', 'x', 'z', 'ch', 'sh', 'o')):
            return verb_text + 'es'
        elif verb_lower.endswith('y') and len(verb_lower) > 1 and verb_lower[-2] not in 'aeiou':
            return verb_text[:-1] + 'ies'
        elif not verb_lower.endswith('s'):
            return verb_text + 's'
        return verb_text
    else:
        # Plural: remove -s/-es
        if verb_lower.endswith('ies'):
            return verb_lower[:-3] + 'y'
        elif verb_lower.endswith('es'):
            if verb_lower.endswith(('shes', 'ches', 'xes', 'zes', 'oes')):
                return verb_lower[:-2]
            return verb_lower[:-1]
        elif verb_lower.endswith('s') and not verb_lower.endswith('ss'):
            return verb_lower[:-1]
        return verb_text

def conjugate_predicate_for_subject(predicate_doc, subject_doc, original_verb_token):
    """
    Conjugate predicate to match a NEW subject
    This is the KEY function that makes combinations grammatical
    """
    if len(predicate_doc) == 0:
        return ""
    
    # Determine if NEW subject is singular
    is_singular = is_subject_singular(subject_doc)
    
    # Get original verb tense
    original_tense = get_verb_tense(original_verb_token)
    
    # Find verbs in predicate
    verbs = [token for token in predicate_doc if token.pos_ == 'VERB' or token.pos_ == 'AUX']
    
    if not verbs:
        return predicate_doc.text
    
    main_verb = verbs[0]
    
    # Conjugate to match new subject, preserving tense
    conjugated = conjugate_verb(main_verb.text, is_singular, original_tense)
    
    # Rebuild predicate
    result_parts = []
    for token in predicate_doc:
        if token.i == main_verb.i:
            result_parts.append(conjugated)
        else:
            result_parts.append(token.text_with_ws.strip())
    
    return ' '.join(result_parts)

def find_root_verb(doc):
    """Find the ROOT verb using spaCy"""
    for token in doc:
        if token.dep_ == 'ROOT' and token.pos_ == 'VERB':
            return token
    
    for token in doc:
        if token.pos_ == 'VERB':
            if token.text[0].isupper() and token.i > 0:
                continue
            return token
    
    return None

def parse_headline(title, source):
    """Parse headline into subject and predicate components"""
    title = clean_headline(title)
    
    if len(title.split()) < 4:
        return None
    
    doc = nlp(title)
    
    # Reject problematic patterns
    if doc[0].text.lower() in QUESTION_WORDS:
        return None
    
    if len(doc) >= 2 and doc[0].text.lower() == 'how' and doc[1].text.lower() == 'to':
        return None
    
    if doc[0].pos_ == 'VERB' and doc[0].tag_ == 'VBG':
        return None
    
    root_verb = find_root_verb(doc)
    
    if not root_verb:
        return None
    
    verb_idx = root_verb.i
    
    if verb_idx < 1:
        return None
    
    subject_doc = doc[:verb_idx]
    predicate_doc = doc[verb_idx:]
    
    if len(subject_doc) < 2 or len(subject_doc) > 15:
        return None
    
    subject_content = [t for t in subject_doc if t.pos_ in ['NOUN', 'PROPN', 'PRON', 'NUM']]
    if len(subject_content) == 0:
        return None
    
    return {
        'subject_doc': subject_doc,
        'subject_text': subject_doc.text,
        'predicate_doc': predicate_doc,
        'predicate_text': predicate_doc.text,
        'verb_token': root_verb,
        'original': title,
        'source': source
    }

def fetch_headlines():
    """Fetch and parse headlines from all RSS feeds"""
    parsed_headlines = []
    
    print("Fetching headlines from feeds...")
    
    for feed_url in FEEDS:
        try:
            print(f"  Fetching from {feed_url}...")
            feed = feedparser.parse(feed_url)
            source = feed.feed.get('title', feed_url)
            
            feed_count = 0
            for entry in feed.entries[:30]:
                title = entry.get('title', '')
                if title:
                    parsed = parse_headline(title, source)
                    if parsed:
                        parsed_headlines.append(parsed)
                        feed_count += 1
            
            print(f"    Found {feed_count} parseable headlines")
        
        except Exception as e:
            print(f"    Error fetching {feed_url}: {str(e)}")
    
    return parsed_headlines

def generate_combinations(parsed_headlines, num_combinations=120):
    """
    Generate headline combinations with proper conjugation
    THIS IS WHERE THE MAGIC HAPPENS
    """
    if len(parsed_headlines) < 2:
        return []
    
    combinations = []
    attempts = 0
    max_attempts = num_combinations * 10
    
    print(f"\nGenerating {num_combinations} combinations with proper conjugation...")
    
    while len(combinations) < num_combinations and attempts < max_attempts:
        attempts += 1
        
        # Pick random subject and predicate sources
        subj_parsed = random.choice(parsed_headlines)
        pred_parsed = random.choice(parsed_headlines)
        
        # CRITICAL: Ensure different originals
        if subj_parsed['original'] == pred_parsed['original']:
            continue
        
        # Get the NEW subject and predicate
        subject_doc = subj_parsed['subject_doc']
        subject_text = subj_parsed['subject_text']
        
        predicate_doc = pred_parsed['predicate_doc']
        verb_token = pred_parsed['verb_token']
        
        # CONJUGATE predicate to match the NEW subject
        conjugated_predicate = conjugate_predicate_for_subject(
            predicate_doc, 
            subject_doc, 
            verb_token
        )
        
        # Create combined headline
        combined_headline = f"{subject_text} {conjugated_predicate}"
        
        # Check for duplicates
        if any(c['headline'] == combined_headline for c in combinations):
            continue
        
        combinations.append({
            'headline': combined_headline,
            'subject': {
                'text': subject_text,
                'original': subj_parsed['original'],
                'source': subj_parsed['source']
            },
            'predicate': {
                'text': conjugated_predicate,
                'original': pred_parsed['original'],
                'source': pred_parsed['source']
            }
        })
    
    print(f"✓ Generated {len(combinations)} unique, grammatical combinations")
    return combinations

def main():
    print("=" * 60)
    print("LUCKNOOZ Headline Generator v12")
    print("Pre-combined with proper conjugation")
    print("=" * 60)
    print()
    
    # Fetch and parse headlines
    parsed_headlines = fetch_headlines()
    
    if not parsed_headlines:
        print("ERROR: No headlines parsed successfully")
        return
    
    print(f"\nSuccessfully parsed {len(parsed_headlines)} headlines")
    
    # Generate combinations
    combinations = generate_combinations(parsed_headlines, num_combinations=120)
    
    if not combinations:
        print("ERROR: Could not generate any combinations")
        return
    
    # Prepare output
    output = {
        'headlines': combinations,
        'generated': datetime.now().isoformat(),
        'total_headlines': len(combinations)
    }
    
    # Save to file
    filename = 'headline-components.json'
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print()
    print(f"✅ Saved {len(combinations)} headlines to {filename}")
    print()
    print("Sample headlines:")
    for combo in combinations[:8]:
        print(f"  • {combo['headline']}")
    print()
    print("Upload headline-components.json to GitHub to update your site!")

if __name__ == "__main__":
    main()