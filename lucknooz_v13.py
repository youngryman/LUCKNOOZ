#!/usr/bin/env python3
"""
LuckNooz V13.7 - Tense Matching Improvement
Matches predicate verb tense to subject verb tense for grammatical consistency
"""

import feedparser
import json
import random
from datetime import datetime
import spacy
import subprocess
import sys

# Download spaCy model if not present
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Downloading spaCy English model...")
    subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

# Import LemmInflect and add to spaCy pipeline
try:
    import lemminflect
except ImportError:
    print("Installing lemminflect...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "lemminflect"])
    import lemminflect

# RSS Feeds to scrape with display names
# 6 feeds with cleanest headline structure
FEEDS = [
    {'url': 'https://feeds.bbci.co.uk/news/world/rss.xml', 'name': 'BBC News'},
    {'url': 'https://feeds.npr.org/1001/rss.xml', 'name': 'NPR'},
    {'url': 'https://www.theguardian.com/world/rss', 'name': 'The Guardian'},
    {'url': 'http://feeds.reuters.com/Reuters/worldNews', 'name': 'Reuters'},
    {'url': 'https://www.aljazeera.com/xml/rss/all.xml', 'name': 'Al Jazeera'},
    {'url': 'http://rss.cnn.com/rss/edition.rss', 'name': 'CNN'}
]

# Question words that indicate headlines to skip
QUESTION_WORDS = {'why', 'what', 'when', 'where', 'who', 'how', 'which', 'whose'}

# Never treat these as verbs
NEVER_VERBS = {
    'news', 'report', 'update', 'story', 'article', 'poll', 'data',
    'study', 'research', 'analysis', 'review', 'survey', 'alert',
    'wins', 'calls', 'wounded', 'targeted', 'attached'
}


def find_first_verb(headline):
    """Find the first verb using spaCy structure + LemmInflect verification."""
    
    # Skip question headlines
    first_word = headline.split()[0] if headline.split() else ''
    if first_word.lower().rstrip(',:;?!') in QUESTION_WORDS:
        return None
    
    words = headline.split()
    
    # Skip if headline ends with common verb (creates nonsense)
    if len(words) > 0:
        last_word_lower = words[-1].lower().rstrip(',.!?;:')
        common_ending_verbs = {'say', 'says', 'said', 'attached', 'included', 'reported'}
        if last_word_lower in common_ending_verbs:
            return None
    
    # Process with spaCy
    try:
        doc = nlp(headline)
    except Exception as e:
        print(f"Error processing headline: {headline[:50]}... - {e}")
        return None
    
    # Look for first verb (start from token 1 to ensure subject has at least 1 word)
    for i in range(1, len(doc)):
        token = doc[i]
        word = token.text
        word_lower = word.lower().rstrip(',.!?;:')
        
        # Skip never-verbs
        if word_lower in NEVER_VERBS:
            continue
        
        # Skip if this is "to" + infinitive
        if i > 0 and doc[i-1].text.lower() == "to":
            continue
        
        # Check if this is actually a verb using LemmInflect
        from lemminflect import getLemma
        
        # Try to get lemma as a VERB
        lemmas = getLemma(word, upos='VERB')
        
        # If LemmInflect recognizes it as a verb, it's likely a verb
        if lemmas and len(lemmas) > 0:
            # Additional check: skip if it's clearly an adjective modifying a noun
            if token.pos_ in ["VERB"] or token.tag_.startswith('VB'):
                # Check if it's a participle modifying the next noun
                if token.tag_ in ["VBG", "VBN"] and i < len(doc) - 1:
                    next_token = doc[i + 1]
                    if next_token.pos_ in ["NOUN", "PROPN"] and token.dep_ == "amod":
                        continue
                
                # Found a valid verb!
                subject_tokens = doc[:i]
                predicate_tokens = doc[i:]
                
                subject = " ".join([t.text for t in subject_tokens])
                predicate = " ".join([t.text for t in predicate_tokens])
                
                return {
                    'subject': subject,
                    'predicate': predicate,
                    'verb': word,
                    'verb_lemma': lemmas[0],
                    'verb_tag': token.tag_
                }
    
    return None


def is_plural(subject):
    """Determine if a subject is plural using spaCy."""
    try:
        doc = nlp(subject)
        
        # Find the root noun (usually the last significant noun)
        root_noun = None
        for token in reversed(doc):
            if token.pos_ in ["NOUN", "PROPN"]:
                root_noun = token
                break
        
        if root_noun:
            # Check if it's tagged as plural
            if root_noun.tag_ in ["NNS", "NNPS"]:
                return True
            # Check for compound subjects with "and"
            if " and " in subject.lower():
                return True
    except:
        pass
    
    # Fallback: check for plural indicators
    subject_lower = subject.lower().strip()
    plural_indicators = ['several', 'many', 'both', 'all', 'some', 'most', 'few', 'these', 'those']
    for indicator in plural_indicators:
        if subject_lower.startswith(indicator + ' '):
            return True
    
    return False


def conjugate_verb(predicate_verb, predicate_verb_lemma, predicate_verb_tag, 
                   subject_verb_tag, new_subject_is_plural):
    """
    Conjugate predicate verb to match subject verb's tense and new subject's number.
    
    Args:
        predicate_verb: The original predicate verb word
        predicate_verb_lemma: Lemma of predicate verb
        predicate_verb_tag: Original tag of predicate verb
        subject_verb_tag: Tag of the subject verb (to match tense)
        new_subject_is_plural: Whether the new subject is plural
    
    Returns:
        Conjugated verb matching subject tense and new subject number
    """
    from lemminflect import getInflection
    
    # Map verb tags to tense categories
    # VB = base form, VBD = past, VBG = gerund, VBN = past participle
    # VBP = present non-3rd, VBZ = present 3rd singular
    
    # Determine target tense from SUBJECT verb
    target_tense = None
    
    if subject_verb_tag in ['VBD', 'VBN']:
        # Subject is past tense → predicate should be past tense
        target_tense = 'past'
    elif subject_verb_tag in ['VBZ', 'VBP', 'VB']:
        # Subject is present tense → predicate should be present tense
        target_tense = 'present'
    elif subject_verb_tag == 'VBG':
        # Subject is gerund → keep predicate as gerund
        target_tense = 'gerund'
    else:
        # Default to present
        target_tense = 'present'
    
    # Special handling for "to be"
    if predicate_verb_lemma in ['be', 'is', 'are', 'was', 'were', 'am']:
        if target_tense == 'past':
            return 'were' if new_subject_is_plural else 'was'
        elif target_tense == 'present':
            return 'are' if new_subject_is_plural else 'is'
    
    # Determine target tag based on tense and number
    target_tag = None
    
    if target_tense == 'past':
        # Past tense (same for singular and plural)
        target_tag = 'VBD'
    elif target_tense == 'gerund':
        # Keep as gerund
        return predicate_verb
    elif target_tense == 'present':
        # Present tense - adjust for number
        if new_subject_is_plural:
            target_tag = 'VBP'  # Present non-3rd person (base form for plural)
        else:
            target_tag = 'VBZ'  # Present 3rd person singular
    
    # Use LemmInflect to get the correct conjugation
    if target_tag:
        inflections = getInflection(predicate_verb_lemma, tag=target_tag)
        if inflections and len(inflections) > 0:
            return inflections[0]
    
    # Fallback: return original verb
    return predicate_verb


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
        
        # Get subject verb info (for tense matching)
        subject_verb_tag = subject_obj['verb_tag']
        
        # Get predicate verb info
        predicate_verb = predicate_obj['verb']
        predicate_verb_lemma = predicate_obj['verb_lemma']
        predicate_verb_tag = predicate_obj['verb_tag']
        
        # Determine if new subject is plural
        new_subject_is_plural = is_plural(subject)
        
        # Conjugate predicate verb to match SUBJECT VERB TENSE and NEW SUBJECT NUMBER
        conjugated_verb = conjugate_verb(
            predicate_verb, 
            predicate_verb_lemma, 
            predicate_verb_tag,
            subject_verb_tag,  # NEW: Pass subject verb tag for tense matching
            new_subject_is_plural
        )
        
        # Replace first word of predicate (the verb) with conjugated version
        pred_words = predicate.split()
        if pred_words:
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
    print("LuckNooz V13.7 - Tense Matching Improvement")
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
        'version': '13.7',
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
