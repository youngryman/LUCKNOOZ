#!/usr/bin/env python3
"""
LuckNooz V15.0 - Complete Interactive Headline Remixer
Features: Three-part remixing, User submissions, Voting system
"""

import random
import json
import os
import re
from datetime import datetime
from collections import defaultdict


class HeadlineSplitter:
    """Handles three-part headline splitting with prepositional phrase extraction"""
    
    PREPOSITIONS = [
        'in', 'on', 'at', 'with', 'for', 'about', 'after', 'before',
        'during', 'from', 'to', 'over', 'under', 'between', 'among',
        'through', 'across', 'along', 'around', 'near', 'by', 'of'
    ]
    
    @staticmethod
    def split_three_parts(headline):
        """Split headline into [subject] [connector] [context]"""
        words = headline.split()
        
        # Find prepositional phrases
        for i, word in enumerate(words):
            if word.lower() in HeadlineSplitter.PREPOSITIONS:
                before = ' '.join(words[:i])
                prep = word
                after = ' '.join(words[i+1:])
                
                if before and after and len(words[:i]) >= 2 and len(words[i+1:]) >= 2:
                    return [before, prep, after]
        
        # Fallback: split at midpoint with 'and'
        mid = len(words) // 2
        for offset in range(-2, 3):
            idx = mid + offset
            if 0 < idx < len(words) - 1:
                word = words[idx]
                if any(word.lower().endswith(end) for end in ['s', 'ed', 'ing']):
                    return [' '.join(words[:idx+1]), 'and', ' '.join(words[idx+1:])]
        
        return [' '.join(words[:mid]), 'and', ' '.join(words[mid:])]
    
    @staticmethod
    def remix_three_parts(headlines, count=10):
        """Generate remixed headlines from three-part combinations"""
        if len(headlines) < 2:
            return headlines
        
        split_headlines = [HeadlineSplitter.split_three_parts(h) for h in headlines]
        remixed = []
        
        for _ in range(count):
            parts_pool = list(range(len(split_headlines)))
            random.shuffle(parts_pool)
            
            if len(parts_pool) >= 3:
                part1 = split_headlines[parts_pool[0]][0]
                part2 = split_headlines[parts_pool[1]][1]
                part3 = split_headlines[parts_pool[2]][2]
            else:
                idx = random.choice(parts_pool)
                parts = split_headlines[idx]
                part1 = parts[0]
                part2 = random.choice([p[1] for p in split_headlines])
                part3 = random.choice([p[2] for p in split_headlines if p != parts])
            
            remixed_headline = f"{part1} {part2} {part3}"
            remixed.append(remixed_headline)
        
        return remixed


class HeadlineDatabase:
    """Manages headlines with voting and user submissions"""
    
    def __init__(self, filename='lucknooz_data.json'):
        self.filename = filename
        self.headlines = []
        self.remixed_headlines = []
        self.votes = defaultdict(int)  # headline -> vote count
        self.user_submissions = []
        self.load_data()
    
    def load_data(self):
        """Load all data from JSON file"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    data = json.load(f)
                    self.headlines = data.get('headlines', [])
                    self.remixed_headlines = data.get('remixed', [])
                    self.votes = defaultdict(int, data.get('votes', {}))
                    self.user_submissions = data.get('user_submissions', [])
                print(f"✓ Loaded {len(self.headlines)} headlines, {len(self.remixed_headlines)} remixes")
            except Exception as e:
                print(f"⚠ Error loading data: {e}")
    
    def save_data(self):
        """Save all data to JSON file"""
        data = {
            'headlines': self.headlines,
            'remixed': self.remixed_headlines,
            'votes': dict(self.votes),
            'user_submissions': self.user_submissions,
            'last_updated': datetime.now().isoformat()
        }
        
        try:
            with open(self.filename, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"✓ Saved to {self.filename}")
        except Exception as e:
            print(f"⚠ Error saving: {e}")
    
    def add_headline(self, headline, source='manual'):
        """Add a headline (original or user submission)"""
        if headline not in self.headlines:
            self.headlines.append(headline)
            if source == 'user':
                self.user_submissions.append({
                    'headline': headline,
                    'timestamp': datetime.now().isoformat()
                })
            return True
        return False
    
    def vote(self, headline, value=1):
        """Vote on a remixed headline"""
        self.votes[headline] += value
    
    def get_top_remixes(self, n=10):
        """Get top voted remixes"""
        sorted_remixes = sorted(
            self.remixed_headlines,
            key=lambda h: self.votes.get(h, 0),
            reverse=True
        )
        return sorted_remixes[:n]


class LuckNoozApp:
    """Main application controller"""
    
    def __init__(self):
        self.db = HeadlineDatabase()
        self.current_remixes = []
    
    def add_headline_interactive(self):
        """Interactive headline input"""
        print("\n" + "="*70)
        print("ADD HEADLINE")
        print("="*70)
        headline = input("\nEnter headline (or 'cancel' to abort): ").strip()
        
        if headline.lower() == 'cancel':
            print("Cancelled.")
            return
        
        if not headline:
            print("⚠ Empty headline!")
            return
        
        source = input("Is this from (1) news or (2) your imagination? [1/2]: ").strip()
        source_type = 'user' if source == '2' else 'manual'
        
        if self.db.add_headline(headline, source_type):
            print(f"✓ Added: {headline}")
            if source_type == 'user':
                print("  (Marked as user submission)")
        else:
            print("⚠ Headline already exists!")
    
    def view_headlines(self):
        """Display all headlines"""
        print("\n" + "="*70)
        print(f"HEADLINE LIBRARY ({len(self.db.headlines)} total)")
        print("="*70)
        
        if not self.db.headlines:
            print("\n⚠ No headlines yet! Add some first.")
            return
        
        for i, headline in enumerate(self.db.headlines, 1):
            marker = "👤" if any(s['headline'] == headline for s in self.db.user_submissions) else "📰"
            print(f"{i}. {marker} {headline}")
    
    def remix_and_vote(self):
        """Generate remixes and allow voting"""
        if len(self.db.headlines) < 2:
            print("\n⚠ Need at least 2 headlines to remix!")
            return
        
        print("\n" + "="*70)
        print("REMIXED HEADLINES - VOTE FOR YOUR FAVORITES!")
        print("="*70)
        
        # Generate new remixes
        self.current_remixes = HeadlineSplitter.remix_three_parts(self.db.headlines, count=10)
        
        # Add to database
        for remix in self.current_remixes:
            if remix not in self.db.remixed_headlines:
                self.db.remixed_headlines.append(remix)
        
        # Display with voting
        print()
        for i, headline in enumerate(self.current_remixes, 1):
            votes = self.db.votes.get(headline, 0)
            vote_display = f"[{votes:+d}]" if votes != 0 else "[ 0]"
            print(f"{i}. {vote_display} {headline}")
        
        print("\n" + "="*70)
        print("Enter headline numbers to upvote (e.g., '1 3 7')")
        print("Or enter 'all' to see top-rated remixes from all time")
        print("Or press Enter to skip")
        print("="*70)
        
        choice = input("\nYour choice: ").strip().lower()
        
        if choice == 'all':
            self.show_top_remixes()
        elif choice:
            try:
                numbers = [int(x) for x in choice.split()]
                for num in numbers:
                    if 1 <= num <= len(self.current_remixes):
                        headline = self.current_remixes[num - 1]
                        self.db.vote(headline, 1)
                        print(f"✓ Upvoted: {headline}")
                print(f"\n👍 Voted for {len(numbers)} headlines!")
            except ValueError:
                print("⚠ Invalid input!")
    
    def show_top_remixes(self):
        """Display all-time top remixes"""
        print("\n" + "="*70)
        print("🏆 TOP REMIXES OF ALL TIME")
        print("="*70)
        
        top = self.db.get_top_remixes(20)
        
        if not top:
            print("\n⚠ No remixes yet!")
            return
        
        print()
        for i, headline in enumerate(top, 1):
            votes = self.db.votes.get(headline, 0)
            print(f"{i}. [{votes:+d}] {headline}")
    
    def show_stats(self):
        """Display statistics"""
        print("\n" + "="*70)
        print("📊 LUCKNOOZ STATISTICS")
        print("="*70)
        
        print(f"\n📰 Total headlines: {len(self.db.headlines)}")
        print(f"👤 User submissions: {len(self.db.user_submissions)}")
        print(f"🎲 Total remixes generated: {len(self.db.remixed_headlines)}")
        print(f"🗳️  Total votes cast: {sum(self.db.votes.values())}")
        
        if self.db.votes:
            top_headline = max(self.db.remixed_headlines, key=lambda h: self.db.votes.get(h, 0))
            top_votes = self.db.votes.get(top_headline, 0)
            print(f"\n🏆 Top remix ({top_votes:+d} votes):")
            print(f"   {top_headline}")
        
        if self.db.user_submissions:
            print(f"\n👤 Recent user submissions:")
            for submission in self.db.user_submissions[-3:]:
                print(f"   • {submission['headline']}")
    
    def run(self):
        """Main application loop"""
        print("\n" + "="*70)
        print("🍀 LUCKNOOZ V15.0 - Interactive Headline Remixer")
        print("="*70)
        print("Three-part remixing • User submissions • Community voting")
        
        while True:
            print("\n" + "="*70)
            print("MAIN MENU")
            print("="*70)
            print("1. Add headline")
            print("2. View all headlines")
            print("3. Generate remixes & vote")
            print("4. View top remixes")
            print("5. View statistics")
            print("6. Save & exit")
            
            choice = input("\nEnter your choice (1-6): ").strip()
            
            if choice == '1':
                self.add_headline_interactive()
            elif choice == '2':
                self.view_headlines()
            elif choice == '3':
                self.remix_and_vote()
            elif choice == '4':
                self.show_top_remixes()
            elif choice == '5':
                self.show_stats()
            elif choice == '6':
                self.db.save_data()
                print("\n👋 Thanks for using LuckNooz!")
                break
            else:
                print("⚠ Invalid choice!")


if __name__ == "__main__":
    app = LuckNoozApp()
    app.run()