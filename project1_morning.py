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
    "Number Guessing Game with 3 difficulty levels easy medium hard and live score tracker",
    "Simple Calculator with full operation history log and memory functions",
    "Rock Paper Scissors game with win loss draw statistics and replay option",
    "Dice Rolling Simulator with probability stats and multi-dice support",
    "Prime Number Checker and Generator with Sieve of Eratosthenes",
    "Fibonacci Sequence Generator with memoization and execution time display",
    "Palindrome Checker for words sentences and numbers with clean output",
    "ATM Machine Simulator with PIN login balance check deposit and withdraw",
    "Roman Numeral Converter bidirectional with validation",
    "Temperature Converter supporting Celsius Fahrenheit and Kelvin",
    "Snake Game in terminal using curses with levels high score and walls",
    "Maze Generator and Solver with recursive backtracking visualization",
    "Virtual Pet Game with hunger energy happiness stats and aging system",
    "Space Invaders text based with score shields lives and increasing speed",
    "Text File Word Frequency Counter with top 10 words display",
    "Student Grade Manager with file storage average calculator and pass fail",
    "Personal Expense Tracker with category budget and CSV monthly export",
    "Contact Book CLI with add search update delete and persistent JSON storage",
    "Inventory Management System with stock alerts and reorder notifications",
    "Library Book Manager with borrow return overdue tracking and fine calculator",
    "Hangman Word Game with 5 categories and ASCII art gallows",
    "Quiz Game with 3 categories score tracking timer and leaderboard",
    "Typing Speed Test with WPM accuracy score and difficulty levels",
    "Tic Tac Toe 2 player with win detection draw detection and replay",
    "Slot Machine Simulator with bet system balance and jackpot feature",
    "Blackjack Card Game with betting chips dealer AI and full rules",
    "Word Scramble Game with hints timer and category selection",
    "Trivia Quiz with 10 questions timer score and difficulty selector",
    "Math Quiz Generator with adaptive difficulty and performance tracking",
    "Text Adventure Game with rooms inventory and multiple endings",
    "Password Generator with length symbols uppercase options and strength meter",
    "Password Strength Analyzer with detailed feedback and improvement tips",
    "Countdown Timer with multiple timers alarm and pause resume",
    "Pomodoro Timer CLI with work break cycles session counter and stats",
    "Unit Converter for length weight volume area and temperature",
    "Currency Converter with 20 static exchange rates and conversion history",
    "Random Quote Generator by category with save favorites feature",
    "Simple Alarm Clock with multiple alarms snooze and label support",
    "Text Encryption Decryption tool using Caesar cipher and Vigenere cipher",
    "Markdown to Plain Text Converter with formatting cleanup",
    "Weather App using OpenWeatherMap API with 5 day forecast",
    "News Headline Fetcher using RSS feeds with category filter",
    "GitHub Profile Fetcher showing repos followers stats using GitHub API",
    "Dictionary App using Free Dictionary API with synonyms antonyms examples",
    "IP Address Lookup Tool with geolocation and ISP info",
    "URL Status Checker with HTTP response codes and redirect tracking",
    "Random Joke Fetcher with category filter and save favorites",
    "Currency Rate Fetcher with live rates and comparison",
    "Public Holiday Checker using Nager Date API for any country and year",
    "Chuck Norris Joke and Trivia Fetcher with category and search",
    "Stack Implementation with real world use cases like undo redo browser history",
    "Queue Implementation with print spooler and ticket system simulation",
    "Linked List with full CRUD insert delete search traverse and reverse",
    "Binary Search implementation with step by step visualization in terminal",
    "Bubble Sort Visualizer showing each swap step in terminal",
    "Merge Sort with step by step output comparison count and time tracking",
    "Simple Hash Map from scratch with collision handling and load factor",
    "Binary Tree with insert delete and all traversal methods",
    "Graph Representation with adjacency list BFS DFS and path finding",
    "LRU Cache implementation using OrderedDict with get put eviction demo",
]

day_of_year = datetime.now().timetuple().tm_yday
topic_index = (day_of_year - 1) % len(TOPICS)
topic       = TOPICS[topic_index]
today       = datetime.now().strftime("%Y-%m-%d")

_stop = {"with","that","and","for","the","a","an","of","to","in","by","on","using","from"}
_words = [w for w in topic.lower().split() if w not in _stop][:3]
repo_name = "-".join(_words).replace(",","").replace("(","").replace(")","").replace("/","-")

print(f"{'='*60}")
print(f"  PROJECT 1  —  5:30 PM PKT")
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

# ── Delete repo if exists (clean slate) ─────────────────────
def repo_exists():
    return requests.get(f"https://api.github.com/repos/{GITHUB_USER}/{repo_name}", headers=HEADERS).status_code == 200

if repo_exists():
    print(f"  [Fix] Repo '{repo_name}' exists — deleting for clean start...")
    d = requests.delete(f"https://api.github.com/repos/{GITHUB_USER}/{repo_name}", headers=HEADERS)
    if d.status_code == 204:
        print(f"  [OK]  Deleted.\n")
        time.sleep(3)
    else:
        print(f"  [ERROR] Could not delete: {d.status_code} {d.json()}")
        exit(1)

# ── Create repo WITH auto_init=True ─────────────────────────
# auto_init creates the default branch immediately so Contents API works
print(f"Creating repo '{repo_name}'...")
res = requests.post("https://api.github.com/user/repos", headers=HEADERS, json={
    "name":        repo_name,
    "description": f"Daily Python Project #{topic_index+1}/{len(TOPICS)}: {topic[:80]} | {today} | by HarisAhmed83",
    "private":     False,
    "auto_init":   True,   # ← KEY FIX: creates main branch instantly
    "has_issues":  True,
})
if res.status_code != 201:
    print(f"  [ERROR] {res.status_code}: {res.json().get('message')}")
    exit(1)
print(f"  [OK]  Repo created!")
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
