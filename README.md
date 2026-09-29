# Simple Web Log Analyzer

A lightweight, dependency-free command line tool built with Python to parse and analyze Nginx/Apache access logs. It extracts meaningful statistics such as top visiting IP addresses, most requested URLs, and HTTP status code distributions.

## Features
- **Zero Dependencies:** Built entirely with Python Standard Library (`re`, `collections`, `argparse`).
- **Fast Regex Parsing:** Efficiently parses standard combined log formats.
- **CLI Support:** Easy to use from the terminal with customizable output limits.

## 🛠️ Usage

You can run the script directly from your terminal. Just provide the path to your log file.

```bash
# Basic usage
python log_analyzer.py access.log

# Show top 10 results instead of the default 5
python log_analyzer.py access.log -n 10

# Show help menu
python log_analyzer.py --help
