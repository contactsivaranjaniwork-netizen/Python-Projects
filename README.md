# 🐍 Python Project Portfolio

A growing collection of Python projects, ranging from simple command-line utilities to more advanced tools involving APIs, data analysis, and automation. Built as a hands-on way to practice writing clean, tested, real-world Python code.

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Tests](https://img.shields.io/badge/tests-pytest-yellow)
![Status](https://img.shields.io/badge/status-active-brightgreen)

---

## 📋 Table of Contents

- [About](#-about)
- [Repository Structure](#-repository-structure)
- [Project Index](#-project-index)
  - [Beginner](#beginner)
  - [Early Intermediate](#early-intermediate)
  - [Intermediate](#intermediate)
  - [Advanced Intermediate](#advanced-intermediate)
  - [Advanced](#advanced)
- [Getting Started](#-getting-started)
- [Running Tests](#-running-tests)
- [Project Conventions](#-project-conventions)
- [Tech Stack](#-tech-stack)
- [Progress Tracker](#-progress-tracker)
- [License](#-license)

---

## 📖 About

This repository is where I build and document Python projects as I learn — each one a self-contained, working command-line application rather than a snippet or tutorial follow-along.

Every project aims to:
- separate **core logic** from **user I/O**, so the important parts are actually unit-testable
- handle **invalid input and edge cases** gracefully instead of crashing
- follow a **consistent, professional structure** so the codebase reads well as a portfolio

The list below currently sits at 50 projects, organized roughly by difficulty — but this repo is a living collection, and new projects get added over time as separate folders.

---

## 🗂 Repository Structure

Each project lives in its own folder, named descriptively:

```
python-portfolio/
├── unit-converter/
│   ├── project.py
│   ├── test_project.py
│   ├── requirements.txt
│   └── README.md
├── quote-generator/
│   ├── project.py
│   ├── test_project.py
│   ├── quotes.json
│   ├── requirements.txt
│   └── README.md
├── expense-tracker/
│   └── ...
├── ...
├── personal-finance-dashboard/
│   └── ...
├── LICENSE
└── README.md   ← you are here
```

New projects are simply added as new top-level folders and linked in the [Project Index](#-project-index) below.

---

## 📌 Project Index

> ✅ = complete · 🚧 = in progress · ⬜ = not started
> Update as projects are built. Difficulty labels are a rough guide, not a strict rulebook.

### Beginner
*Single-concept CLI tools — a good afternoon each*

| Project | Description | Status |
|---|---|---|
| Unit Converter | Converts between temperature, length, and weight units | ✅ |
| Random Quote / Affirmation Generator | Prints a random quote from a local JSON file, filterable by category | ✅ |
| Simple Calculator with History | Basic arithmetic with a saved calculation log | ⬜ |
| Dice Roller / Coin Flip Simulator | Simulates rolls/flips with running statistics | ⬜ |
| BMI & Calorie Calculator | Computes BMI and classifies into health categories | ⬜ |
| QR Code Generator | Converts text/URLs into downloadable QR images | ⬜ |
| Random Password Generator | Customizable-length password generator | ⬜ |
| Countdown Timer / Pomodoro Clock | Work/break interval timer with alerts | ⬜ |
| Text-Based Hangman | Classic word-guessing game | ⬜ |
| Number Guessing Game | Computer-picked number with adjustable difficulty | ⬜ |

### Early Intermediate
*Adds file I/O and persistent data (CSV/JSON)*

| Project | Description | Status |
|---|---|---|
| To-Do List Manager | Add/edit/delete/complete tasks, saved to file | ⬜ |
| Expense Tracker | Logs spending by category with monthly summaries | ⬜ |
| Flash Cards — Language Learning | Word/phrase practice with spaced repetition basics | ⬜ |
| Contact Book / Phonebook | Full CRUD contact storage via CSV/SQLite | ⬜ |
| Journal / Diary App | Timestamped entries, searchable by date/keyword | ⬜ |
| Recipe Organizer | Stores and scales recipes by serving size | ⬜ |
| File Organizer | Auto-sorts files into folders by type/date | ⬜ |
| Duplicate File Finder | Detects identical files via hashing | ⬜ |
| Media Organizer | Sorts photos/videos by metadata | ⬜ |
| Habit Tracker | Daily check-ins with streak tracking | ⬜ |

### Intermediate
*Introduces live APIs and HTML parsing*

| Project | Description | Status |
|---|---|---|
| Password Manager & Generator | Encrypted credential storage | ⬜ |
| Weather App | Live current-weather and forecast lookup | ⬜ |
| Currency Converter | Real-time exchange rate conversion | ⬜ |
| Web Scraper / Parser | Extracts structured data from HTML pages | ⬜ |
| News Aggregator | Scrapes and emails a daily news digest | ⬜ |
| Job Listing Scraper | Scrapes and filters job postings | ⬜ |
| Product Price Tracker | Alerts on price drops for tracked products | ⬜ |
| IMDB / Metacritic Lookup | Displays ratings and summaries by title | ⬜ |
| YouTube Downloader (Single Video) | Downloads video/audio from a URL | ⬜ |
| YouTube Downloader (Playlist) | Batch-downloads an entire playlist | ⬜ |

### Advanced Intermediate
*Combines multiple APIs or techniques in one project*

| Project | Description | Status |
|---|---|---|
| Healthy Meal Planner | Nutrition API-based weekly meal planning | ⬜ |
| Spotify Mood Playlist Generator | Builds playlists based on mood via Spotify API | ⬜ |
| Text-to-Speech Reader | Converts text/PDFs into spoken audio | ⬜ |
| Speech-to-Text Notetaker | Transcribes voice recordings into PDF notes | ⬜ |
| Sentiment Analysis Tool | Scores tone of reviews or journal entries | ⬜ |
| TTS + Sentiment Combo | Speaks input aloud while analyzing tone | ⬜ |
| Resume / Cover Letter Generator | Template-based PDF/Word document generator | ⬜ |
| Certificate Generator | Bulk-generates personalized PDF certificates | ⬜ |
| PDF Form Filler | Auto-fills PDF form fields from CSV data | ⬜ |
| Library Management System | Book check-in/out with overdue tracking | ⬜ |

### Advanced
*Stateful systems, data analysis, or CV/ML-adjacent work*

| Project | Description | Status |
|---|---|---|
| Inventory / POS System | Stock tracking, sales, and receipts | ⬜ |
| Student Gradebook System | Grade storage, GPA calculation, report cards | ⬜ |
| Stock Correlation Heatmapper | Visualizes correlation across multiple tickers | ⬜ |
| Public Health Data Processor | Cleans and charts time-series health data | ⬜ |
| Statistical Engine | Regression analysis and fit visualization | ⬜ |
| Face-Recognition Photo Sorter | Sorts photos by detected faces | ⬜ |
| PDF-Based Q&A Bot | Natural-language Q&A over PDF content | ⬜ |
| Telegram Bot | Async bot for recipes or file delivery | ⬜ |
| YouTube Video Summarizer | LLM-based transcript summarization | ⬜ |
| Personal Finance Dashboard | Interactive dashboard over aggregated bank/expense data | ⬜ |

---

## 🚀 Getting Started

Clone the repository:

```bash
git clone https://github.com/<your-username>/python-portfolio.git
cd python-portfolio
```

Each project is self-contained. To run one:

```bash
cd unit-converter
pip install -r requirements.txt
python3 project.py
```

---

## 🧪 Running Tests

Every project includes a `test_project.py` designed for `pytest`:

```bash
cd unit-converter
pip install pytest
pytest test_project.py -v
```

To run tests across every project folder from the repo root:

```bash
pytest -v
```

---

## 📐 Project Conventions

Every project in this repo follows the same conventions for consistency:

- **`main()` entry point** — interactive/menu logic lives inside `main()`, guarded by `if __name__ == "__main__":`.
- **Pure, testable functions** — core logic (conversions, calculations, data transforms) is separated from `input()`/`print()` so it can be tested without mocking stdin.
- **Meaningful tests** — each `test_project.py` covers at least three non-`main` functions, including edge cases and invalid input.
- **Graceful error handling** — invalid input, missing files, and malformed data are caught and reported cleanly rather than raising unhandled exceptions.
- **Self-contained folders** — each project has its own `requirements.txt`, so dependencies don't leak across projects.

---

## 🛠 Tech Stack

| Category | Tools |
|---|---|
| Language | Python 3.10+ |
| Testing | pytest |
| Data | JSON, CSV, SQLite |
| APIs | OpenWeatherMap, Spotify, OpenAI, Telegram Bot API, yt-dlp |
| Data & Visualization | pandas, matplotlib, Plotly |
| Web | Flask, BeautifulSoup |

---

## 📊 Progress Tracker

```
Beginner              ██░░░░░░░░  2 / 10
Early Intermediate     ░░░░░░░░░░  0 / 10
Intermediate           ░░░░░░░░░░  0 / 10
Advanced Intermediate  ░░░░░░░░░░  0 / 10
Advanced               ░░░░░░░░░░  0 / 10
------------------------------------------
Total                  ██░░░░░░░░░░░░░░░░░░░░░░░░  2 / 50
```

*(Update this section as new projects are completed or added.)*

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
