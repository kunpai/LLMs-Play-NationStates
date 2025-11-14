"""
NationStates Decision Analytics
--------------------------------
Analyze historical decisions from choices.ndjson to provide insights
into decision-making patterns, AI performance, and issue trends.
"""

import json
from collections import Counter, defaultdict
from datetime import datetime
import sys


def load_decisions(filepath="choices.ndjson"):
    """Load all decisions from the NDJSON file."""
    decisions = []
    try:
        with open(filepath, 'r') as f:
            for line in f:
                if line.strip():
                    decisions.append(json.loads(line))
    except FileNotFoundError:
        print(f"Error: {filepath} not found")
        return []
    return decisions


def analyze_decisions(decisions):
    """Analyze decision patterns and generate statistics."""
    if not decisions:
        print("No decisions to analyze.")
        return
    
    total_decisions = len(decisions)
    methods = Counter(d.get('method', 'unknown') for d in decisions)
    
    # Calculate date range
    timestamps = [d['timestamp'] for d in decisions if 'timestamp' in d]
    if timestamps:
        start_date = datetime.fromtimestamp(min(timestamps))
        end_date = datetime.fromtimestamp(max(timestamps))
        date_range = (end_date - start_date).days
    else:
        start_date = end_date = None
        date_range = 0
    
    # Analyze issue types (extract first few words of title as category)
    issue_categories = Counter()
    for d in decisions:
        title = d.get('title', '')
        # Use first 2-3 words as rough category
        words = title.split()[:2]
        if words:
            category = ' '.join(words)
            issue_categories[category] += 1
    
    # Print analysis
    print("=" * 60)
    print("NATIONSTATES DECISION ANALYTICS")
    print("=" * 60)
    print(f"\nTotal Decisions Made: {total_decisions}")
    
    if start_date and end_date:
        print(f"Date Range: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
        print(f"Duration: {date_range} days")
        if date_range > 0:
            print(f"Average Decisions per Day: {total_decisions / date_range:.2f}")
    
    print("\n" + "-" * 60)
    print("DECISION METHOD BREAKDOWN")
    print("-" * 60)
    for method, count in methods.most_common():
        percentage = (count / total_decisions) * 100
        print(f"{method.upper()}: {count} ({percentage:.1f}%)")
    
    print("\n" + "-" * 60)
    print("TOP 10 ISSUE CATEGORIES")
    print("-" * 60)
    for category, count in issue_categories.most_common(10):
        print(f"{category}: {count}")
    
    # AI effectiveness (if we can measure it)
    ai_decisions = [d for d in decisions if d.get('method') == 'AI']
    random_decisions = [d for d in decisions if d.get('method') == 'random']
    
    print("\n" + "-" * 60)
    print("DECISION STATISTICS")
    print("-" * 60)
    print(f"AI Decisions: {len(ai_decisions)}")
    print(f"Random Fallback Decisions: {len(random_decisions)}")
    if ai_decisions and total_decisions > 0:
        print(f"AI Success Rate: {(len(ai_decisions) / total_decisions) * 100:.1f}%")
    
    print("\n" + "=" * 60)


def show_recent_decisions(decisions, count=5):
    """Display the most recent decisions."""
    if not decisions:
        return
    
    print(f"\nRECENT DECISIONS (Last {count})")
    print("=" * 60)
    
    # Sort by timestamp, most recent first
    sorted_decisions = sorted(decisions, key=lambda x: x.get('timestamp', 0), reverse=True)
    
    for i, decision in enumerate(sorted_decisions[:count], 1):
        timestamp = datetime.fromtimestamp(decision['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
        title = decision.get('title', 'Unknown')
        method = decision.get('method', 'unknown')
        option_text = decision.get('chosen_option_text', '')[:60] + '...' if len(decision.get('chosen_option_text', '')) > 60 else decision.get('chosen_option_text', '')
        
        print(f"\n{i}. {title}")
        print(f"   Date: {timestamp}")
        print(f"   Method: {method.upper()}")
        print(f"   Choice: {option_text}")


def main():
    """Main entry point for analytics script."""
    filepath = "choices.ndjson"
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
    
    decisions = load_decisions(filepath)
    
    if decisions:
        analyze_decisions(decisions)
        show_recent_decisions(decisions)
    else:
        print("No decisions found to analyze.")
        print(f"Make sure {filepath} exists and contains decision data.")


if __name__ == "__main__":
    main()
