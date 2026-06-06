# Halal Finder Agent

An AI agent that finds halal restaurants in London using natural language queries. Built as a portfolio project to demonstrate a real tool-calling agent loop using the Anthropic Claude API.

## What it does

You ask a question in plain English. The agent decides which tools to call, calls them in sequence, reasons about the evidence, and returns structured results as a clean HTML page.

```
python3 main.py "halal Turkish near Shoreditch"
```

![Example output showing restaurant cards with halal status badges](docs/example.png)

## How it works — the agent loop

This is not a wrapper around a single API call. The agent:

1. Receives your query
2. Calls `search_restaurants` to find candidates via Google Places
3. Independently decides to call `get_place_details` on each result
4. Reads reviews and metadata to assess halal status
5. Synthesises evidence into a verdict: `LIKELY HALAL`, `POSSIBLY HALAL`, or `UNVERIFIED`
6. Returns structured JSON which is rendered as an HTML results page

The key point: the model decides what to call, in what order, and how many times — not the code. That's what makes it an agent rather than a script.

## Setup

**Requirements:** Python 3.9+, a Google Cloud account, an Anthropic API key

**1. Clone and install**
```bash
git clone https://github.com/affaniqbal/halal-finder-agent
cd halal-finder-agent
pip install -r requirements.txt
```

**2. Get API keys**
- Google Places API: [console.cloud.google.com](https://console.cloud.google.com) → Enable Places API → Create API key
- Anthropic API: [console.anthropic.com](https://console.anthropic.com)

**3. Configure**
```bash
cp .env.example .env
# Add your keys to .env
```

**4. Run**
```bash
python3 main.py "halal Lebanese near Bethnal Green"
```

Results open automatically in your browser as `results.html`.

## Project structure

```
halal-finder-agent/
├── main.py          # Entry point — parses args, runs agent, renders output
├── src/
│   ├── agent.py     # Agent loop — manages tool calls and Claude conversation
│   ├── tools.py     # Tool definitions and Google Places API calls
│   └── renderer.py  # Renders JSON results as a static HTML page
├── requirements.txt
└── .env.example
```

## Limitations

Halal status is inferred from Google Places reviews and metadata — not from a certification authority. Results are labelled clearly with confidence levels. Always verify directly with the restaurant for certainty.

## Planned improvements

- Cross-reference against halal certification directories
- Auto-detect current location
- Filter by cuisine, distance, rating
