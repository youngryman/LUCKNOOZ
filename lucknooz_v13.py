<<<<<<< HEAD
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LuckNooz V13</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="min-h-screen bg-gradient-to-br from-purple-50 to-blue-50 p-8">
    <div class="max-w-6xl mx-auto">
        <div class="text-center mb-8">
            <h1 class="text-4xl font-bold text-gray-800 mb-2">LuckNooz V13</h1>
            <p class="text-gray-600">Simplified First-Verb Detection</p>
        </div>

        <div class="bg-white rounded-lg shadow-lg p-6 mb-6">
            <button id="generateBtn" onclick="generateHeadlines()" class="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded-lg transition-colors">
                Generate New Headlines
            </button>
            <button id="fetchBtn" onclick="fetchLiveHeadlines()" class="w-full bg-green-600 hover:bg-green-700 text-white font-bold py-3 px-6 rounded-lg transition-colors mt-3">
                Try Fetching Live Headlines
            </button>
        </div>

        <div id="status" class="text-center text-gray-600 mb-4"></div>
        <div id="headlines" class="space-y-4"></div>
    </div>

    <script>
        // Sample headlines to use if feed fetching fails
        const sampleHeadlines = [
            "Scientists discover new species in Amazon rainforest",
            "Stock market reaches record high amid economic optimism",
            "City council approves funding for new public library",
            "Athletes prepare for upcoming championship game",
            "Tech company announces breakthrough in AI research",
            "Local restaurant wins prestigious culinary award",
            "Weather forecasters predict severe storms this weekend",
            "University researchers develop new cancer treatment",
            "Mayor unveils plan to reduce traffic congestion",
            "Art museum opens exhibition featuring local artists",
            "Schools implement new digital learning platform",
            "Community volunteers clean up neighborhood park",
            "Musicians perform at sold-out concert venue",
            "Business leaders discuss strategies for growth",
            "Astronomers observe rare celestial event tonight",
            "Activists rally for environmental protection measures",
            "Hospital staff celebrates life-saving medical advances",
            "Filmmakers premiere documentary about climate change",
            "Engineers design innovative solution for clean water",
            "Authors gather at annual book festival downtown",
            "Teams compete in regional robotics competition",
            "Voters head to polls for important referendum",
            "Chefs create menu inspired by seasonal ingredients",
            "Dancers rehearse for upcoming performance",
            "Historians uncover ancient artifacts at excavation site",
            "Entrepreneurs launch startup focused on sustainability",
            "Players celebrate victory in championship match",
            "Scientists warn about rising sea levels",
            "Teachers adopt new methods for student engagement",
            "Residents protest proposed development project"
        ];

        const commonVerbs = new Set([
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
            'replaces', 'replaced', 'replace', 'replacing',
            'discover', 'discovers', 'discovered', 'discovering',
            'predict', 'predicts', 'predicted', 'predicting',
            'approve', 'approves', 'approved', 'approving',
            'prepare', 'prepares', 'prepared', 'preparing',
            'unveil', 'unveils', 'unveiled', 'unveiling',
            'implement', 'implements', 'implemented', 'implementing',
            'clean', 'cleans', 'cleaned', 'cleaning',
            'perform', 'performs', 'performed', 'performing',
            'discuss', 'discusses', 'discussed', 'discussing',
            'observe', 'observes', 'observed', 'observing',
            'rally', 'rallies', 'rallied', 'rallying',
            'celebrate', 'celebrates', 'celebrated', 'celebrating',
            'premiere', 'premieres', 'premiered', 'premiering',
            'design', 'designs', 'designed', 'designing',
            'gather', 'gathers', 'gathered', 'gathering',
            'compete', 'competes', 'competed', 'competing',
            'head', 'heads', 'headed', 'heading',
            'rehearse', 'rehearses', 'rehearsed', 'rehearsing',
            'uncover', 'uncovers', 'uncovered', 'uncovering',
            'warn', 'warns', 'warned', 'warning',
            'adopt', 'adopts', 'adopted', 'adopting',
            'protest', 'protests', 'protested', 'protesting'
        ]);

        const skipWords = new Set([
            'the', 'a', 'an', 'this', 'that', 'these', 'those',
            'will', 'would', 'should', 'could', 'might', 'may', 'must', 'can',
            'to', 'for', 'of', 'in', 'on', 'at', 'by', 'with', 'from', 'about', 'as'
        ]);

        const neverVerbs = new Set([
            'news', 'report', 'update', 'story', 'article', 'poll', 'data',
            'study', 'research', 'analysis', 'review', 'survey'
        ]);

        function findFirstVerb(headline) {
            const words = headline.split(' ');
            
            for (let i = 1; i < words.length; i++) {
                const word = words[i];
                const wordLower = word.toLowerCase().replace(/[^a-z]/g, '');
                const prevWord = i > 0 ? words[i - 1].toLowerCase() : '';
                
                if (!wordLower) continue;
                if (skipWords.has(wordLower)) continue;
                if (neverVerbs.has(wordLower)) continue;
                if (skipWords.has(prevWord)) continue;
                if (word === word.toUpperCase() && word.length > 1) continue;
                
                if (commonVerbs.has(wordLower)) {
                    const subject = words.slice(0, i).join(' ');
                    const predicate = words.slice(i).join(' ');
                    return { subject, predicate, verb: word };
                }
                
                if ((wordLower.endsWith('ed') || wordLower.endsWith('ing')) && wordLower.length >= 5) {
                    const subject = words.slice(0, i).join(' ');
                    const predicate = words.slice(i).join(' ');
                    return { subject, predicate, verb: word };
                }
            }
            
            return null;
        }

        function conjugateVerb(verb, subjectIsPlural) {
            const verbLower = verb.toLowerCase();
            
            if (verbLower === 'is' || verbLower === 'are') {
                return subjectIsPlural ? 'are' : 'is';
            }
            if (verbLower === 'was' || verbLower === 'were') {
                return subjectIsPlural ? 'were' : 'was';
            }
            
            if (verbLower.endsWith('ed') || verbLower.endsWith('ing')) {
                return verb;
            }
            
            if (subjectIsPlural) {
                if (verbLower.endsWith('es')) {
                    return verb.slice(0, -2);
                }
                if (verbLower.endsWith('s') && !verbLower.endsWith('ss')) {
                    return verb.slice(0, -1);
                }
                return verb;
            }
            
            if (!subjectIsPlural) {
                if (!verbLower.endsWith('s')) {
                    if (verbLower.endsWith('ch') || verbLower.endsWith('sh') || 
                        verbLower.endsWith('x') || verbLower.endsWith('z') ||
                        verbLower.endsWith('o')) {
                        return verb + 'es';
                    }
                    if (verbLower.endsWith('y') && verbLower.length > 1 && !'aeiou'.includes(verbLower[verbLower.length - 2])) {
                        return verb.slice(0, -1) + 'ies';
                    }
                    return verb + 's';
                }
            }
            
            return verb;
        }

        function isPlural(subject) {
            const subjectLower = subject.toLowerCase().trim();
            
            if (subjectLower.includes(' and ')) return true;
            if (subjectLower.startsWith('several ')) return true;
            if (subjectLower.startsWith('many ')) return true;
            if (subjectLower.startsWith('both ')) return true;
            if (subjectLower.startsWith('all ')) return true;
            if (subjectLower.startsWith('some ')) return true;
            if (subjectLower.startsWith('most ')) return true;
            if (subjectLower.startsWith('few ')) return true;
            
            const words = subject.split(' ');
            const lastWord = words[words.length - 1].toLowerCase().replace(/[^a-z]/g, '');
            
            if (lastWord.endsWith('s') && !lastWord.endsWith('ss') && lastWord.length > 3) {
                return true;
            }
            
            return false;
        }

        function shuffle(array) {
            const newArray = [...array];
            for (let i = newArray.length - 1; i > 0; i--) {
                const j = Math.floor(Math.random() * (i + 1));
                [newArray[i], newArray[j]] = [newArray[j], newArray[i]];
            }
            return newArray;
        }

        function remixHeadlines(headlines) {
            const subjects = headlines.map(h => h.subject);
            const predicates = shuffle(headlines.map(h => h.predicate));
            
            return subjects.slice(0, 20).map((subject, i) => {
                const predicate = predicates[i];
                
                const verbMatch = predicate.match(/^(\S+)/);
                if (verbMatch) {
                    const verb = verbMatch[1];
                    const subjectIsPlural = isPlural(subject);
                    const conjugatedVerb = conjugateVerb(verb, subjectIsPlural);
                    const newPredicate = predicate.replace(/^(\S+)/, conjugatedVerb);
                    
                    return `${subject} ${newPredicate}`;
                }
                
                return `${subject} ${predicate}`;
            });
        }

        function displayHeadlines(headlines) {
            const container = document.getElementById('headlines');
            container.innerHTML = headlines.map(headline => 
                `<div class="bg-gray-50 p-4 rounded-lg border-l-4 border-blue-500">
                    <p class="text-lg text-gray-800">${headline}</p>
                </div>`
            ).join('');
        }

        function generateHeadlines() {
            const status = document.getElementById('status');
            
            status.textContent = '🔄 Parsing sample headlines...';
            status.className = 'text-center text-blue-600 mb-4 font-semibold';
            
            const parsed = sampleHeadlines
                .map(findFirstVerb)
                .filter(h => h !== null);
            
            if (parsed.length === 0) {
                status.textContent = '❌ Error parsing headlines';
                status.className = 'text-center text-red-600 mb-4';
                return;
            }
            
            const remixed = remixHeadlines(parsed);
            displayHeadlines(remixed);
            
            status.textContent = `✨ Generated ${remixed.length} LuckNooz headlines from sample data`;
            status.className = 'text-center text-green-600 mb-4 font-semibold';
        }

        async function fetchLiveHeadlines() {
            const status = document.getElementById('status');
            const button = document.getElementById('fetchBtn');
            
            button.disabled = true;
            button.classList.add('opacity-50', 'cursor-not-allowed');
            status.textContent = '🔄 Fetching live headlines from RSS feeds...';
            status.className = 'text-center text-blue-600 mb-4 font-semibold';
            
            const feeds = [
                'https://feeds.bbci.co.uk/news/world/rss.xml',
                'https://rss.nytimes.com/services/xml/rss/nyt/World.xml',
                'https://feeds.npr.org/1001/rss.xml',
                'https://www.theguardian.com/world/rss',
                'https://www.espn.com/espn/rss/news'
            ];
            
            const allHeadlines = [];
            
            try {
                for (const feed of feeds) {
                    try {
                        const response = await fetch(`https://api.rss2json.com/v1/api.json?rss_url=${encodeURIComponent(feed)}`);
                        const data = await response.json();
                        
                        if (data.items) {
                            data.items.forEach(item => {
                                const parsed = findFirstVerb(item.title);
                                if (parsed) {
                                    allHeadlines.push(parsed);
                                }
                            });
                        }
                    } catch (error) {
                        console.error('Error fetching feed:', feed, error);
                    }
                }
                
                if (allHeadlines.length === 0) {
                    status.textContent = '⚠️ Could not fetch live headlines. Using sample data instead.';
                    status.className = 'text-center text-yellow-600 mb-4';
                    generateHeadlines();
                } else {
                    const remixed = remixHeadlines(allHeadlines);
                    displayHeadlines(remixed);
                    status.textContent = `✨ Generated ${remixed.length} LuckNooz headlines from live feeds!`;
                    status.className = 'text-center text-green-600 mb-4 font-semibold';
                }
            } catch (error) {
                console.error('Error:', error);
                status.textContent = '⚠️ Error fetching live headlines. Using sample data.';
                status.className = 'text-center text-yellow-600 mb-4';
                generateHeadlines();
            } finally {
                button.disabled = false;
                button.classList.remove('opacity-50', 'cursor-not-allowed');
            }
        }

        window.onload = generateHeadlines;
    </script>
</body>
</html>


=======
#!/usr/bin/env python3
"""
LuckNooz V13.9 - Gerund Filtering Added
Skips gerunds (VBG) acting as nouns, not verbs
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
    
    # Prepositions that often follow adjectival participles or precede gerunds
    prep_indicators = {'with', 'by', 'in', 'for', 'of', 'from', 'to', 'at', 'on', 'over', 'after', 'about', 'without', 'before', 'through', 'during'}
    
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
                
                # ENHANCED CHECK FOR GERUNDS (VBG) USED AS NOUNS
                if token.tag_ == 'VBG':
                    # Check 1: Dependency indicates noun usage
                    if token.dep_ in ['pobj', 'dobj', 'nsubj', 'nsubjpass', 'attr', 'pcomp']:
                        # pobj = object of preposition, dobj = direct object
                        # These indicate the VBG is functioning as a noun
                        continue
                    
                    # Check 2: Preceded by preposition (common gerund pattern)
                    if i > 0:
                        prev_token = doc[i - 1]
                        if prev_token.text.lower() in prep_indicators:
                            # Pattern like "about giving", "by running" - gerund as noun
                            continue
                    
                    # Check 3: Preceded by adjective + preposition (e.g., "hesitant about giving")
                    if i > 1:
                        prev_token = doc[i - 1]
                        prev_prev_token = doc[i - 2]
                        if (prev_token.text.lower() in prep_indicators and 
                            prev_prev_token.pos_ == 'ADJ'):
                            # Pattern like "hesitant about giving" - gerund as noun
                            continue
                    
                    # Check 4: Following possessive (e.g., "his running")
                    if i > 0:
                        prev_token = doc[i - 1]
                        if prev_token.tag_ in ['PRP


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
    print("LuckNooz V13.9 - Gerund Filtering Added")
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
        'version': '13.9',
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
, 'POS']:  # Possessive pronouns/markers
                            # Pattern like "his giving", "country's opening" - gerund as noun
                            continue
                
                # ENHANCED CHECK FOR PAST PARTICIPLES (VBN) USED AS ADJECTIVES
                if token.tag_ == 'VBN':
                    # Check 1: Dependency is adjectival modifier
                    if token.dep_ in ['amod', 'acl', 'acomp']:
                        continue
                    
                    # Check 2: Followed by a preposition (common pattern for adjectival use)
                    if i < len(doc) - 1:
                        next_token = doc[i + 1]
                        if next_token.text.lower() in prep_indicators:
                            # This is likely "charged with", "banned from", etc. - adjectival
                            continue
                    
                    # Check 3: Previous token is a noun (pattern: "Noun + VBN + preposition")
                    if i > 0:
                        prev_token = doc[i - 1]
                        if prev_token.pos_ in ['NOUN', 'PROPN']:
                            # Check if next token is preposition
                            if i < len(doc) - 1:
                                next_token = doc[i + 1]
                                if next_token.text.lower() in prep_indicators:
                                    # Pattern like "adviser charged with" - skip
                                    continue
                    
                    # Check 4: Part of reduced relative clause
                    # Pattern: "Adjective/Determiner + Noun + VBN"
                    if i > 1:
                        prev_prev_token = doc[i - 2]
                        prev_token = doc[i - 1]
                        if (prev_prev_token.pos_ in ['ADJ', 'DET'] and 
                            prev_token.pos_ in ['NOUN', 'PROPN']):
                            # Pattern like "Former adviser charged" - likely adjectival
                            continue
                
                # Check for VBG/VBN participles modifying next noun (original check)
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
    print("LuckNooz V13.8 - Improved Past Participle Filtering")
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
        'version': '13.8',
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
>>>>>>> 6ecb2b2192f59895e0c0a1e5d530bd07eb7f4da1
