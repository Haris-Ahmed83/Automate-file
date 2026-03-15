"""
====================================================
  Daily Auto GitHub Project Generator - Project 1
  Runs at 5:30 PM Pakistan Time (12:30 PM UTC)
  Uses Google Gemini API (FREE)
====================================================
"""

import os
import re
import time
import base64
import requests
from datetime import datetime
from google import genai

GITHUB_TOKEN = os.environ.get("PERSONAL_TOKEN", "")
GITHUB_USER  = "HarisAhmed83"
GEMINI_KEY   = os.environ.get("GEMINI_API_KEY", "")

HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

# ── Validate token ──────────────────────────────────────────
print("\nValidating GitHub token...")
r = requests.get("https://api.github.com/user", headers=HEADERS)
if r.status_code != 200:
    print(f"  [ERROR] Token invalid! HTTP {r.status_code}")
    exit(1)
scopes = r.headers.get("X-OAuth-Scopes", "")
if "repo" not in scopes:
    print(f"  [ERROR] Token missing 'repo' scope! Scopes: {scopes}")
    exit(1)
print(f"  [OK]  Token valid | Scopes: {scopes}\n")

MODELS = [
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",  # Faster fallback
    "gemini-2.0-flash",           # Final fallback
]

TOPICS = [
    "Bank Account System using OOP with savings checking and transaction history",
    "Student Management System OOP with GPA calculator and report card generator",
    "Employee Payroll System OOP with salary tax deduction and payslip generator",
    "Hospital Patient Management OOP with appointments prescriptions and billing",
    "School Timetable Generator OOP with teacher subject and room assignment",
    "Online Shopping Cart OOP with products discount coupon and checkout",
    "Hotel Room Booking System OOP with availability calendar and invoice",
    "Parking Lot Management OOP with vehicle types hourly rates and receipt",
    "Restaurant Order System OOP with menu items total bill and kitchen queue",
    "Gym Membership Manager OOP with plans attendance and payment tracking",
    "Automated File Backup Script with timestamp versioning and restore option",
    "Portfolio Website Generator creating HTML CSS from user input data",
    "Database Schema Visualizer reading SQLite and printing table relationships",
    "API Rate Limiter simulation with token bucket algorithm and logging",
    "Automated Report Generator from CSV data with summary in terminal",
    "Email Template Generator with placeholders and batch personalization",
    "Config File Manager supporting INI JSON formats with validation",
    "Directory Tree Visualizer with file sizes dates and search filter",
    "Automated Test Runner for Python functions with pass fail summary",
    "Simple Task Automation Scheduler with cron-like syntax",
    "Personal Diary App with date entries search and password protection",
    "Recipe Manager with ingredients steps category search and shopping list",
    "Habit Tracker with daily streaks completion rate and progress bar",
    "Budget Planner with income expense savings goal and monthly report",
    "Flashcard Study App with spaced repetition and score tracking",
    "Travel Packing List Manager with categories checklist and trip profiles",
    "Movie Watchlist Manager with ratings reviews genre filter and stats",
    "Workout Log Tracker with exercises sets reps weight and progress chart",
    "Book Reading Tracker with progress notes rating and reading speed",
    "Music Playlist Manager with songs artist genre shuffle and export",
    "Student Survey Analyzer reading CSV calculating stats and generating report",
    "Sales Data Dashboard showing revenue by product region and time period",
    "Text Sentiment Analyzer using keyword scoring positive negative neutral",
    "Phone Number Formatter and Validator for international formats",
    "Email Address Validator and Cleaner with domain check and deduplication",
    "Data Cleaning Script for CSV removing duplicates nulls and formatting",
    "Grade Distribution Analyzer with histogram in terminal and statistics",
    "Sports League Table Generator from match results with sorting",
    "Election Results Analyzer with vote percentage bar chart and winner",
    "Weather Data Analyzer from CSV with monthly averages and trend",
    "Multi-threaded File Downloader with progress bar and retry logic",
    "Simple REST API Client with GET POST PUT DELETE and response formatter",
    "Web Scraper for job listings with title company location and export",
    "ZIP File Manager with compress extract list and password protection",
    "SQLite Todo App with priorities deadlines tags and completion stats",
    "Simple Chat Bot with pattern matching responses and conversation log",
    "Snake Game using curses library with score levels and high score",
    "Tetris Clone text-based with scoring levels and game over screen",
    "Cron Job Simulator running scheduled Python tasks with logging",
    "Plugin System demonstrating dynamic loading of Python modules",
    "ASCII Art Generator converting text to large ASCII font styles",
    "Random Story Generator with characters settings plot and twist",
    "Morse Code Encoder and Decoder with audio description output",
    "Number to Words Converter supporting up to trillions in English",
    "Joke of the Day App with categories ratings and local joke database",
    "Color Palette Generator showing RGB HEX HSL values with named colors",
    "Star Pattern Printer generating 10 different star patterns by size",
    "Calendar Printer with highlighted today events and navigation",
    "Simple Cipher Collection with 5 encryption methods encode decode",
    "Math Magic Tricks App demonstrating 10 number magic tricks with explanation",
]

day_of_year = datetime.now().timetuple().tm_yday
topic_index = (day_of_year - 1) % len(TOPICS)
topic       = TOPICS[topic_index]
today       = datetime.now().strftime("%Y-%m-%d")

_stop = {"with","that","and","for","the","a","an","of","to","in","by","on","using","from"}
_words = [w for w in topic.lower().split() if w not in _stop][:3]
repo_name = "-".join(_words).replace(",","").replace("(","").replace(")","").replace("/","-")

print(f"{'='*60}")
print(f"  PROJECT 2  —  6:00 PM PKT")
print(f"  Date    : {today}")
print(f"  Topic   : {topic}")
print(f"  Project : {topic_index + 1} of {len(TOPICS)}")
print(f"  Repo    : {repo_name}")
print(f"{'='*60}\n")

# ── Gemini ──────────────────────────────────────────────────
def gemini_generate(client, prompt):
    for model in MODELS:
        print(f"  [Model] Trying {model} ...")
        for attempt in range(1, 3):
            try:
                resp = client.models.generate_content(model=model, contents=prompt)
                print(f"  [OK]    {model} succeeded.")
                return resp.text.strip()
            except Exception as e:
                err = str(e)
                if "429" in err or "RESOURCE_EXHAUSTED" in err:
                    if attempt == 1:
                        print(f"  [Wait]  {model} — retrying in 65s...")
                        time.sleep(65)
                    else:
                        print(f"  [Skip]  {model} exhausted.")
                        break
                else:
                    raise
    raise RuntimeError("All Gemini models exhausted.")

def strip_fences(text, lang=""):
    text = re.sub(rf"^```{lang}\n?", "", text.strip())
    text = re.sub(r"\n?```$", "", text.strip())
    return text.strip()

# ── Generate files ───────────────────────────────────────────
print("Generating files with Gemini...\n")
client = genai.Client(api_key=GEMINI_KEY)

print("  [1/3] src/main.py ...")
code = strip_fences(gemini_generate(client,
    f"Write a professional, complete Python script for: {topic}\n\n"
    f"REQUIREMENTS:\n"
    f"1. Module docstring: title, description, author HarisAhmed83\n"
    f"2. Every function must have a docstring\n"
    f"3. Full input validation on ALL user inputs\n"
    f"4. try/except error handling throughout\n"
    f"5. Clean terminal UI with dividers and clear prompts\n"
    f"6. Main menu with numbered options and exit option\n"
    f"7. if __name__ == '__main__': block at bottom\n\n"
    f"Return ONLY raw Python code. No markdown. No backticks."
), "python")
if len(code) < 200:
    print(f"  [ERROR] Code too short. Aborting.")
    exit(1)
print(f"  [OK]    {len(code)} chars\n")
time.sleep(15)

print("  [2/3] README.md ...")
readme = strip_fences(gemini_generate(client,
    f"Write a professional GitHub README.md for: {topic}\n\n"
    f"Sections: # Title with emoji, ## Description, ## Features, "
    f"## Project Structure, ## Requirements, ## Installation, "
    f"## How to Run, ## Example Output, ## Author (HarisAhmed83 - https://github.com/HarisAhmed83)\n\n"
    f"Return ONLY markdown. No backticks wrapping."
), "markdown")
print(f"  [OK]    {len(readme)} chars\n")
time.sleep(15)

print("  [3/3] requirements.txt ...")
requirements = strip_fences(gemini_generate(client,
    f"List ONLY third-party pip packages needed for: {topic}\n"
    f"One per line, lowercase. No stdlib modules.\n"
    f"If none needed, return exactly: # no external dependencies\n"
    f"Return ONLY the list. No explanation."
))
print(f"  [OK]    {len(requirements)} chars\n")

GITIGNORE = "__pycache__/\n*.pyc\n*.pyo\n.env\n.venv/\nvenv/\n*.egg-info/\ndist/\nbuild/\n.DS_Store\n*.log\n"
print("  All files generated!\n")

# ── Delete repo if exists, then recreate fresh ──────────────
print(f"Checking repo '{repo_name}'...")
check = requests.get(f"https://api.github.com/repos/{GITHUB_USER}/{repo_name}", headers=HEADERS)
if check.status_code == 200:
    print(f"  [Fix] Repo exists — deleting for clean start...")
    d = requests.delete(f"https://api.github.com/repos/{GITHUB_USER}/{repo_name}", headers=HEADERS)
    if d.status_code == 204:
        print(f"  [OK]  Deleted.")
        time.sleep(8)  # wait for GitHub to fully process deletion
    else:
        print(f"  [ERROR] Could not delete: {d.status_code} {d.json()}")
        exit(1)

# ── Create repo WITH auto_init=True ─────────────────────────
print(f"Creating repo '{repo_name}'...")
for attempt in range(1, 4):  # retry up to 3 times
    res = requests.post("https://api.github.com/user/repos", headers=HEADERS, json={
        "name":        repo_name,
        "description": f"Daily Python Project #{topic_index+1}/{len(TOPICS)}: {topic[:80]} | {today} | by HarisAhmed83",
        "private":     False,
        "auto_init":   True,
        "has_issues":  True,
    })
    if res.status_code == 201:
        print(f"  [OK]  Repo created!")
        break
    elif res.status_code == 422:
        print(f"  [Wait] 422 — repo still deleting, waiting 10s (attempt {attempt}/3)...")
        time.sleep(10)
    else:
        print(f"  [ERROR] {res.status_code}: {res.json().get('message')}")
        exit(1)
else:
    print(f"  [ERROR] Could not create repo after 3 attempts.")
    exit(1)
time.sleep(5)  # wait for GitHub to fully initialise the branch

# ── Push files via Contents API ──────────────────────────────
def push_file(filepath, content, msg):
    """Push one file. Gets SHA first if file already exists (e.g. README from auto_init)."""
    url = f"https://api.github.com/repos/{GITHUB_USER}/{repo_name}/contents/{filepath}"
    body = {
        "message": msg,
        "content": base64.b64encode(content.encode("utf-8")).decode("utf-8"),
    }
    existing = requests.get(url, headers=HEADERS)
    if existing.status_code == 200:
        body["sha"] = existing.json().get("sha")
    r = requests.put(url, headers=HEADERS, json=body)
    if r.status_code in (200, 201):
        return True
    print(f"  [ERROR] {filepath}: {r.status_code} — {r.json().get('message','')}")
    return False

print("\nPushing files...")
files = {
    "src/main.py":      (code,         f"Add project: {topic[:60]}"),
    "README.md":        (readme,       "Add README"),
    "requirements.txt": (requirements, "Add requirements"),
    ".gitignore":       (GITIGNORE,    "Add .gitignore"),
}

results = {}
for path, (content, msg) in files.items():
    ok = push_file(path, content, msg)
    results[path] = ok
    print(f"  {'✅' if ok else '❌'}  {path}")
    time.sleep(2)  # small delay between pushes

failed = [f for f, ok in results.items() if not ok]
print(f"\n{'='*60}")
if not failed:
    print(f"  ✅ SUCCESS — Project {topic_index+1}/{len(TOPICS)}")
    print(f"  🔗 https://github.com/{GITHUB_USER}/{repo_name}")
else:
    print(f"  ❌ FAILED: {failed}")
    exit(1)
print(f"{'='*60}\n")
