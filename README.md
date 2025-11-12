# NationStates AI Governance Simulator

This project is an AI-powered simulator for NationStates, a nation simulation game. It uses a local LLM (via Ollama) to make governance decisions on issues that arise in your nation.

## Features

- Automatically fetches and responds to NationStates issues
- Uses AI (configurable Ollama models) to choose the best policy options
- Logs all decisions to an NDJSON file for analysis
- Supports test mode for safe experimentation
- Rate-limited to respect NationStates API guidelines
- **NEW**: Analytics script to analyze decision patterns and AI performance
- **NEW**: Configurable LLM model support (not just llama3.2:3b)
- **NEW**: Optional decision reasoning logging to understand AI choices
- **NEW**: Retry logic for improved API reliability
- **NEW**: Nation statistics tracking to monitor your nation's progress over time

## Prerequisites

- Python 3.8+
- [Ollama](https://ollama.com/) installed and running locally
- Llama 3.2 3B model: `ollama pull llama3.2:3b`
- A NationStates account with API access

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/kunpai/LLMs-Play-NationStates.git
   cd LLMs-Play-NationStates
   ```

2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Setup

1. Create a `.env` file in the project root with your NationStates credentials:
   ```
   NATION=your_nation_name
   PASSWORD=your_password
   USER_AGENT=Your App Name/1.0 (contact@example.com)
   SLEEP_BETWEEN_REQUESTS=10
   TEST_MODE=false
   ```

2. Ensure Ollama is running:
   ```bash
   ollama serve
   ```

## Usage

Run the simulator:
```bash
python main.py
```

In test mode (set `TEST_MODE=true` in `.env`), it will log decisions without submitting them.

The script checks for new issues every hour. Decisions are logged to `choices.ndjson`.

## Configuration

- `NATION`: Your NationStates nation name
- `PASSWORD`: Your NationStates password
- `USER_AGENT`: A descriptive user agent for API requests
- `SLEEP_BETWEEN_REQUESTS`: Seconds to wait between API calls (default: 10)
- `TEST_MODE`: Set to `true` to test without submitting answers
- `OLLAMA_MODEL`: Ollama model to use (default: llama3.2:3b)
- `MAX_RETRIES`: Number of retry attempts for API calls (default: 3)
- `LOG_REASONING`: Set to `true` to log AI reasoning for decisions (default: false)

## Logging

All decisions are logged to `choices.ndjson` in NDJSON format, including:
- Timestamp
- Issue ID and text
- Chosen option
- Selection method (AI or random fallback)
- AI reasoning (if `LOG_REASONING=true`)

## Analytics

Analyze your decision history using the analytics script:

```bash
python analytics.py
```

This will show:
- Total decisions made
- AI vs random decision breakdown
- Issue category trends
- Recent decisions with details
- AI success rate

## Nation Statistics Tracking

Track your nation's statistics over time:

```bash
python stats_tracker.py
```

This will:
- Fetch current nation statistics (population, GDP, freedoms, etc.)
- Compare with previous statistics to show changes
- Save statistics to `nation_stats.ndjson` for historical tracking

Run this periodically (e.g., daily) to build a historical record of how your nation evolves based on the AI's decisions.

## Automated Daily Runs (GitHub Actions)

The repository includes a GitHub Actions workflow that can automatically check for and respond to NationStates issues once per day.

### Setup

1. Go to your repository settings on GitHub
2. Navigate to "Secrets and variables" > "Actions"
3. Add the following repository secrets:
   - `NATION`: Your NationStates nation name
   - `PASSWORD`: Your NationStates password
   - `USER_AGENT`: A descriptive user agent (e.g., "NationStates-AI-Simulator/1.0 (your-email@example.com)")

### How it works

- The workflow runs daily at 12:00 UTC (adjust the cron schedule in `.github/workflows/daily-run.yml` if needed)
- It sets up Ollama with the Llama 3.2 3B model
- Runs the script in single-run mode to check for and answer any pending issues
- Logs decisions to `choices.ndjson` (though this won't persist between runs in the workflow environment)

### Manual Trigger

You can also trigger the workflow manually from the Actions tab on GitHub.

**Note**: This workflow runs on GitHub's servers and requires storing your credentials as secrets.
