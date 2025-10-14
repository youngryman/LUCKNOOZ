#!/usr/bin/env python3
"""
LuckNooz V13 - Simplified First Verb Detection
Fetches news headlines, splits at first verb, and creates remixed headlines
"""

import feedparser
import json
import random
from datetime import datetime

# RSS Feeds to scrape
FEEDS = [
    'https://feeds.bbci.co.uk/news/world/rss.xml',
    'https://rss.nytimes.com/services/xml/rss/nyt/World.xml',
    'https://feeds.npr.org/1001/rss.xml',
    'https://www.theguardian.com/world/rss',
    'https://www.espn.com/espn/rss/news',
    'https://www.rollingstone.com/feed/',
    'https://feeds.arstechnica.com/arstechnica/index'
]

# Common verbs for detection
COMMON_VERBS = {
    'is', 'are', 'was', 'were', 'be', 'been', 'being',
    'has', 'have', 'had', 'having',
    'says', 'said', 'say', 'saying',
    'gets', 'got', 'get', 'getting',
    'makes', 'made', 'make', 'making',
    'takes', 'took', 'take', 'taking',
    'comes', 'came', 'come', 'coming',
    'goes', 'went', 'go', 'going',
    'wants', 'wanted', 'want', 'wanting',
    'gives', 'gave', 'give', 'giving',
    'finds', 'found', 'find', 'finding',
    'tells', 'told', 'tell', 'telling',
    'asks', 'asked', 'ask', 'asking',
    'works', 'worked', 'work', 'working',
    'seems', 'seemed', 'seem', 'seeming',
    'feels', 'felt', 'feel', 'feeling',
    'tries', 'tried', 'try', 'trying',
    'leaves', 'left', 'leave', 'leaving',
    'calls', 'called', 'call', 'calling',
    'announces', 'announced', 'announce', 'announcing',
    'wins', 'won', 'win', 'winning',
    'loses', 'lost', 'lose', 'losing',
    'reveals', 'revealed', 'reveal', 'revealing',
    'shows', 'showed', 'shown', 'show', 'showing',
    'faces', 'faced', 'face', 'facing',
    'reaches', 'reached', 'reach', 'reaching',
    'breaks', 'broke', 'broken', 'break', 'breaking',
    'plans', 'planned', 'plan', 'planning',
    'launches', 'launched', 'launch', 'launching',
    'opens', 'opened', 'open', 'opening',
    'closes', 'closed', 'close', 'closing',
    'begins', 'began', 'begun', 'begin', 'beginning',
    'ends', 'ended', 'end', 'ending',
    'continues', 'continued', 'continue', 'continuing',
    'becomes', 'became', 'become', 'becoming',
    'remains', 'remained', 'remain', 'remaining',
    'appears', 'appeared', 'appear', 'appearing',
    'leads', 'led', 'lead', 'leading',
    'follows', 'followed', 'follow', 'following',
    'brings', 'brought', 'bring', 'bringing',
    'keeps', 'kept', 'keep', 'keeping',
    'holds', 'held', 'hold', 'holding',
    'turns', 'turned', 'turn', 'turning',
    'starts', 'started', 'start', 'starting',
    'stops', 'stopped', 'stop', 'stopping',
    'helps', 'helped', 'help', 'helping',
    'moves', 'moved', 'move', 'moving',
    'plays', 'played', 'play', 'playing',
    'runs', 'ran', 'run', 'running',
    'stands', 'stood', 'stand', 'standing',
    'falls', 'fell', 'fallen', 'fall', 'falling',
    'rises', 'rose', 'risen', 'rise', 'rising',
    'sets', 'set', 'setting',
    'meets', 'met', 'meet', 'meeting',
    'includes', 'included', 'include', 'including',
    'suggests', 'suggested', 'suggest', 'suggesting',
    'considers', 'considered', 'consider', 'considering',
    'reports', 'reported', 'report', 'reporting',
    'claims', 'claimed', 'claim', 'claiming',
    'argues', 'argued', 'argue', 'arguing',
    'believes', 'believed', 'believe', 'believing',
    'thinks', 'thought', 'think', 'thinking',
    'knows', 'knew', 'known', 'know', 'knowing',
    'sees', 'saw', 'seen', 'see', 'seeing',
    'looks', 'looked', 'look', 'looking',
    'sounds', 'sounded', 'sound', 'sounding',
    'means', 'meant', 'mean', 'meaning',
    'offers', 'offered', 'offer', 'offering',
    'provides', 'provided', 'provide', 'providing',
    'serves', 'served', 'serve', 'serving',
    'uses', 'used', 'use', 'using',
    'needs', 'needed', 'need', 'needing',
    'requires', 'required', 'require', 'requiring',
    'expects', 'expected', 'expect', 'expecting',
    'hopes', 'hoped', 'hope', 'hoping',
    'wishes', 'wished', 'wish', 'wishing',
    'decides', 'decided', 'decide', 'deciding',
    'chooses', 'chose', 'chosen', 'choose', 'choosing',
    'picks', 'picked', 'pick', 'picking',
    'selects', 'selected', 'select', 'selecting',
    'votes', 'voted', 'vote', 'voting',
    'elects', 'elected', 'elect', 'electing',
    'defeats', 'defeated', 'defeat', 'defeating',
    'beats', 'beat', 'beaten', 'beating',
    'scores', 'scored', 'score', 'scoring',
    'ties', 'tied', 'tie', 'tying',
    'fails', 'failed', 'fail', 'failing',
    'passes', 'passed', 'pass', 'passing',
    'joins', 'joined', 'join', 'joining',
    'quits', 'quit', 'quitting',
    'resigns', 'resigned', 'resign', 'resigning',
    'retires', 'retired', 'retire', 'retiring',
    'dies', 'died', 'die', 'dying',
    'kills', 'killed', 'kill', 'killing',
    'saves', 'saved', 'save', 'saving',
    'protects', 'protected', 'protect', 'protecting',
    'attacks', 'attacked', 'attack', 'attacking',
    'defends', 'defended', 'defend', 'defending',
    'fights', 'fought', 'fight', 'fighting',
    'struggles', 'struggled', 'struggle', 'struggling',
    'suffers', 'suffered', 'suffer', 'suffering',
    'enjoys', 'enjoyed', 'enjoy', 'enjoying',
    'loves', 'loved', 'love', 'loving',
    'hates', 'hated', 'hate', 'hating',
    'fears', 'feared', 'fear', 'fearing',
    'worries', 'worried', 'worry', 'worrying',
    'cares', 'cared', 'care', 'caring',
    'matters', 'mattered', 'matter', 'mattering',
    'changes', 'changed', 'change', 'changing',
    'grows', 'grew', 'grown', 'grow', 'growing',
    'develops', 'developed', 'develop', 'developing',
    'improves', 'improved', 'improve', 'improving',
    'increases', 'increased', 'increase', 'increasing',
    'decreases', 'decreased', 'decrease', 'decreasing',
    'reduces', 'reduced', 'reduce', 'reducing',
    'cuts', 'cut', 'cutting',
    'adds', 'added', 'add', 'adding',
    'removes', 'removed', 'remove', 'removing',
    'creates', 'created', 'create', 'creating',
    'builds', 'built', 'build', 'building',
    'destroys', 'destroyed', 'destroy', 'destroying',
    'damages', 'damaged', 'damage', 'damaging',
    'fixes', 'fixed', 'fix', 'fixing',
    'repairs', 'repaired', 'repair', 'repairing',
    'replaces', 'replaced', 'replace', 'replacing'
}

# Words to always skip
SKIP_WORDS = {
    'the', 'a', 'an', 'this', 'that', 'these', 'those',
    'will', 'would', 'should', 'could', 'might', 'may', 'must', 'can',
    'to', 'for', 'of', 'in', 'on', 'at', 'by', 'with', 'from', 'about', 'as'
}

# Never treat these as verbs
NEVER_VERBS = {
    'news', 'report', 'update', 'story', 'article', 'poll', 'data',
    'study', 'research', 'analysis', 'review', 'survey'
}


def find_first_verb(headline):
    """Find the first verb in a headline and split it there."""
    words = headline.split()
    
    # Start from word 1 to ensure subject has at least 1 word
    for i in range(1, len(words)):
        word = words[i]
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
        
        # Skip if previous word is a skip word
        if prev_word in SKIP_WORDS:
            continue
        
        # Skip if all caps (likely acronym)
        if word.isupper() and len(word) > 1:
            continue
        
        # Check if it's a known verb
        if word_lower in COMMON_VERBS:
            subject = ' '.join(words[:i])
            predicate = ' '.join(words[i:])
            return {
                'subject': subject,
                'predicate': predicate,
                'verb': word
            }
        
        # Check for -ed, -ing endings
        if (word_lower.endswith('ed') or word_lower.endswith('ing')) and len(word_lower) >= 5:
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
    
    # Get last significant word
    words = subject.split()
    if not words:
        return False
    
    last_word = ''.join(c for c in words[-1].lower() if c.isalpha())
    
    # Check if last word ends in 's'
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
    """Fetch headlines from RSS feeds."""
    all_headlines = []
    
    for feed_url in FEEDS:
        try:
            print(f"Fetching {feed_url}...")
            feed = feedparser.parse(feed_url)
            
            for entry in feed.entries:
                title = entry.get('title', '').strip()
                if title:
                    parsed = find_first_verb(title)
                    if parsed:
                        all_headlines.append(parsed)
        except Exception as e:
            print(f"Error fetching {feed_url}: {e}")
    
    return all_headlines


def remix_headlines(headlines, count=50):
    """Create remixed headlines by swapping subjects and predicates."""
    if len(headlines) < 2:
        return []
    
    subjects = [h['subject'] for h in headlines]
    predicates = headlines.copy()
    random.shuffle(predicates)
    
    remixed = []
    
    for i in range(min(count, len(subjects))):
        subject = subjects[i]
        predicate_obj = predicates[i]
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
        
        remixed.append(remixed_headline)
    
    return remixed


def main():
    """Main function to fetch, process, and save headlines."""
    print("LuckNooz V13 - Simplified First Verb Detection")
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
        'version': '13',
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
    for i, headline in enumerate(remixed[:10], 1):
        print(f"{i}. {headline}")


if __name__ == '__main__':
    main()
