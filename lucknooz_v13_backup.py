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


