# halal-finder-agent

An AI agent that finds and verifies halal restaurants using natural language queries.

## Usage

```bash
python main.py "halal Turkish near Shoreditch"
```

## Setup

1. Clone the repo
2. `pip install -r requirements.txt`
3. Copy `.env` and fill in your API keys
4. Run `python main.py "<your query>"`

## How it works

The agent takes a plain English query, decides which tools to call, searches Google Places, cross-references halal status, and returns structured results.
