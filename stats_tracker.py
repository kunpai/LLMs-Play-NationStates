"""
NationStates Statistics Tracker
--------------------------------
Track nation statistics over time to observe how decisions impact your nation.
"""

import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

BASE = "https://www.nationstates.net/cgi-bin/api.cgi"
USER_AGENT = os.getenv("USER_AGENT")
NATION = os.getenv("NATION")


def fetch_nation_stats():
    """Fetch current nation statistics from NationStates API."""
    headers = {"User-Agent": USER_AGENT}
    params = {
        "nation": NATION,
        "q": "category+freedom+region+population+gdp+income+tax+government+deaths"
    }
    
    try:
        r = requests.get(BASE, params=params, headers=headers, timeout=30)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, "xml")
            
            # Extract statistics
            stats = {
                "timestamp": time.time(),
                "date": datetime.now().isoformat(),
                "category": soup.find("CATEGORY").text if soup.find("CATEGORY") else None,
                "region": soup.find("REGION").text if soup.find("REGION") else None,
                "population": int(soup.find("POPULATION").text) if soup.find("POPULATION") else None,
                "gdp": int(soup.find("GDP").text) if soup.find("GDP") else None,
                "income": int(soup.find("INCOME").text) if soup.find("INCOME") else None,
                "tax": float(soup.find("TAX").text) if soup.find("TAX") else None,
            }
            
            # Extract freedom scores
            freedom = soup.find("FREEDOM")
            if freedom:
                stats["civil_rights"] = freedom.find("CIVILRIGHTS").text if freedom.find("CIVILRIGHTS") else None
                stats["economy"] = freedom.find("ECONOMY").text if freedom.find("ECONOMY") else None
                stats["political_freedom"] = freedom.find("POLITICALFREEDOM").text if freedom.find("POLITICALFREEDOM") else None
            
            # Extract government spending
            govt = soup.find("GOVT")
            if govt:
                stats["govt_administration"] = float(govt.find("ADMINISTRATION").text) if govt.find("ADMINISTRATION") else None
                stats["govt_defence"] = float(govt.find("DEFENCE").text) if govt.find("DEFENCE") else None
                stats["govt_education"] = float(govt.find("EDUCATION").text) if govt.find("EDUCATION") else None
                stats["govt_environment"] = float(govt.find("ENVIRONMENT").text) if govt.find("ENVIRONMENT") else None
                stats["govt_healthcare"] = float(govt.find("HEALTHCARE").text) if govt.find("HEALTHCARE") else None
                stats["govt_commerce"] = float(govt.find("COMMERCE").text) if govt.find("COMMERCE") else None
                stats["govt_international_aid"] = float(govt.find("INTERNATIONALAID").text) if govt.find("INTERNATIONALAID") else None
                stats["govt_law_and_order"] = float(govt.find("LAWANDORDER").text) if govt.find("LAWANDORDER") else None
                stats["govt_public_transport"] = float(govt.find("PUBLICTRANSPORT").text) if govt.find("PUBLICTRANSPORT") else None
                stats["govt_social_equality"] = float(govt.find("SOCIALEQUALITY").text) if govt.find("SOCIALEQUALITY") else None
                stats["govt_spirituality"] = float(govt.find("SPIRITUALITY").text) if govt.find("SPIRITUALITY") else None
                stats["govt_welfare"] = float(govt.find("WELFARE").text) if govt.find("WELFARE") else None
            
            # Extract cause of death statistics
            deaths = soup.find("DEATHS")
            if deaths:
                causes = {}
                for cause in deaths.find_all("CAUSE"):
                    cause_type = cause.get("type")
                    percentage = float(cause.text)
                    causes[cause_type] = percentage
                stats["causes_of_death"] = causes
            
            return stats
        else:
            print(f"[!] Failed to fetch stats: HTTP {r.status_code}")
            return None
    except Exception as e:
        print(f"[!] Error fetching stats: {e}")
        return None


def save_stats(stats, filepath="nation_stats.ndjson"):
    """Save nation statistics to NDJSON file."""
    if stats:
        with open(filepath, "a") as f:
            f.write(json.dumps(stats) + "\n")
        print(f"✓ Statistics saved to {filepath}")
        return True
    return False


def load_all_stats(filepath="nation_stats.ndjson"):
    """Load all historical statistics."""
    stats_list = []
    try:
        with open(filepath, 'r') as f:
            for line in f:
                if line.strip():
                    stats_list.append(json.loads(line))
    except FileNotFoundError:
        return []
    return stats_list


def compare_stats(old_stats, new_stats):
    """Compare two stat snapshots and show changes."""
    if not old_stats or not new_stats:
        return
    
    print("\n" + "=" * 60)
    print("NATION STATISTICS COMPARISON")
    print("=" * 60)
    
    # Population change
    if old_stats.get("population") and new_stats.get("population"):
        pop_change = new_stats["population"] - old_stats["population"]
        print(f"Population: {old_stats['population']} → {new_stats['population']} ({pop_change:+d})")
    
    # GDP change
    if old_stats.get("gdp") and new_stats.get("gdp"):
        gdp_change = new_stats["gdp"] - old_stats["gdp"]
        print(f"GDP: {old_stats['gdp']} → {new_stats['gdp']} ({gdp_change:+d})")
    
    # Freedom changes
    freedom_categories = ["civil_rights", "economy", "political_freedom"]
    for cat in freedom_categories:
        if old_stats.get(cat) and new_stats.get(cat):
            if old_stats[cat] != new_stats[cat]:
                print(f"{cat.replace('_', ' ').title()}: {old_stats[cat]} → {new_stats[cat]}")
    
    # Tax change
    if old_stats.get("tax") is not None and new_stats.get("tax") is not None:
        tax_change = new_stats["tax"] - old_stats["tax"]
        if abs(tax_change) > 0.1:
            print(f"Tax Rate: {old_stats['tax']:.1f}% → {new_stats['tax']:.1f}% ({tax_change:+.1f}%)")


def display_current_stats(stats):
    """Display current nation statistics in a readable format."""
    if not stats:
        print("No statistics available.")
        return
    
    print("\n" + "=" * 60)
    print(f"NATION STATISTICS FOR {NATION.upper()}")
    print("=" * 60)
    print(f"Date: {stats.get('date', 'Unknown')}")
    print(f"Category: {stats.get('category', 'Unknown')}")
    print(f"Region: {stats.get('region', 'Unknown')}")
    print(f"Population: {stats.get('population', 'Unknown'):,}")
    
    if stats.get("gdp"):
        print(f"GDP: ${stats['gdp']:,}")
    if stats.get("income"):
        print(f"Average Income: ${stats['income']:,}")
    if stats.get("tax") is not None:
        print(f"Tax Rate: {stats['tax']:.1f}%")
    
    print("\n" + "-" * 60)
    print("FREEDOMS")
    print("-" * 60)
    if stats.get("civil_rights"):
        print(f"Civil Rights: {stats['civil_rights']}")
    if stats.get("economy"):
        print(f"Economy: {stats['economy']}")
    if stats.get("political_freedom"):
        print(f"Political Freedom: {stats['political_freedom']}")
    
    print("\n" + "=" * 60)


def main():
    """Main entry point for stats tracker."""
    print("Fetching nation statistics...")
    stats = fetch_nation_stats()
    
    if stats:
        display_current_stats(stats)
        
        # Check for previous stats to compare
        all_stats = load_all_stats()
        if all_stats:
            compare_stats(all_stats[-1], stats)
        
        # Save current stats
        save_stats(stats)
        
        # Respect rate limits
        print("\nWaiting 10 seconds to respect API rate limits...")
        time.sleep(10)
    else:
        print("Failed to fetch statistics.")


if __name__ == "__main__":
    main()
