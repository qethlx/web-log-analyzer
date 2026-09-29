#!/usr/bin/env python3
import argparse
import re
import json
from collections import Counter
from typing import Dict, Any, Optional

# Regex for default Nginx/Apache log format
LOG_PATTERN = re.compile(
    r'(?P<ip>\S+) \S+ \S+ \[.*?\] "(?P<method>\S+) (?P<url>\S+) \S+" (?P<status>\d{3}) (?P<size>\S+)'
)

def parse_log_file(file_path: str) -> Optional[Dict[str, Counter]]:
    """Reads the log file and extracts IP, URL, and Status Code statistics."""
    stats = {
        'ips': Counter(),
        'urls': Counter(),
        'statuses': Counter()
    }
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                match = LOG_PATTERN.search(line)
                if match:
                    data = match.groupdict()
                    stats['ips'][data['ip']] += 1
                    stats['urls'][data['url']] += 1
                    stats['statuses'][data['status']] += 1
                    
        return stats
    except FileNotFoundError:
        print(f"Error: '{file_path}' not found. Please check the file path.")
        return None
    except PermissionError:
        print(f"Error: Permission denied to read '{file_path}'.")
        return None

def print_report(stats: Dict[str, Counter], limit: int = 5) -> None:
    """Prints the extracted statistics to the terminal in a formatted way."""
    print("\n" + "="*40)
    print(" 📊 WEB SERVER LOG ANALYSIS REPORT")
    print("="*40)
    
    print(f"\n📍 Top {limit} Requesting IP Addresses:")
    for ip, count in stats['ips'].most_common(limit):
        print(f"   - {ip:<15} : {count} requests")
        
    print(f"\n🔗 Top {limit} Most Visited URLs:")
    for url, count in stats['urls'].most_common(limit):
        print(f"   - {url:<30} : {count} times")
        
    print("\n🚦 HTTP Status Codes Distribution:")
    for status, count in stats['statuses'].most_common():
        status_type = "✅ (Success)" if status.startswith('2') else "❌ (Error)" if status.startswith(('4', '5')) else "ℹ️ (Info/Redirect)"
        print(f"   - HTTP {status} : {count} ({status_type})")
    
    print("\n" + "="*40 + "\n")

def export_to_json(stats: Dict[str, Counter], output_file: str) -> None:
    """Exports the parsed statistics to a JSON file, ordered by frequency."""
    # Convert Counters to standard dicts ordered by frequency for JSON
    serializable_stats = {
        'ips': dict(stats['ips'].most_common()),
        'urls': dict(stats['urls'].most_common()),
        'statuses': dict(stats['statuses'].most_common())
    }
    
    try:
        with open(output_file, 'w', encoding='utf-8') as json_file:
            json.dump(serializable_stats, json_file, indent=4)
        print(f"💾 Results successfully exported to JSON: {output_file}\n")
    except Exception as e:
        print(f"❌ Error exporting to JSON: {e}\n")

def main():
    parser = argparse.ArgumentParser(description="A simple and fast web log analysis tool.")
    parser.add_argument("logfile", help="Path to the log file to be analyzed (e.g., access.log)")
    parser.add_argument("-n", "--number", type=int, default=5, help="Number of top records to display (default: 5)")
    parser.add_argument("-j", "--json", type=str, help="Export results to a JSON file (e.g., report.json)", default=None)
    
    args = parser.parse_args()
    
    print(f"Analyzing: {args.logfile}...")
    stats = parse_log_file(args.logfile)
    
    if stats:
        print_report(stats, limit=args.number)
        
        if args.json:
            export_to_json(stats, args.json)

if __name__ == "__main__":
    main()
