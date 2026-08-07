# New Features Summary

This document summarizes the new features added to the NationStates AI Simulator.

## 🎯 Feature Overview

### 1. Analytics Dashboard (`analytics.py`)
Analyze your nation's decision-making history with detailed statistics.

**Usage:**
```bash
python analytics.py
```

**Features:**
- Total decisions count and date range analysis
- AI vs Random decision breakdown with percentages
- Top 10 issue categories
- Recent decisions display with full details
- AI success rate calculation

**Example Output:**
```
============================================================
NATIONSTATES DECISION ANALYTICS
============================================================

Total Decisions Made: 23
Date Range: 2025-11-08 to 2025-11-12
Duration: 3 days
Average Decisions per Day: 7.67

------------------------------------------------------------
DECISION METHOD BREAKDOWN
------------------------------------------------------------
AI: 17 (73.9%)
RANDOM: 6 (26.1%)
```

### 2. Nation Statistics Tracker (`stats_tracker.py`)
Track how your nation evolves over time with comprehensive statistics.

**Usage:**
```bash
python stats_tracker.py
```

**Features:**
- Fetches current nation statistics from NationStates API
- Tracks: population, GDP, income, tax rate, freedoms, government spending, causes of death
- Compares with historical data to show changes
- Saves statistics to `nation_stats.ndjson` for long-term tracking

**Example Output:**
```
============================================================
NATION STATISTICS FOR YOUR_NATION
============================================================
Date: 2025-11-12T15:30:00
Category: Democratic Socialists
Population: 1,234,567
GDP: $45,678,901,234
Average Income: $37,000
Tax Rate: 45.2%

------------------------------------------------------------
FREEDOMS
------------------------------------------------------------
Civil Rights: Excellent
Economy: Good
Political Freedom: Very Good
```

### 3. Configurable AI Models
Use different Ollama models for decision-making.

**Configuration:**
```bash
# In your .env file
OLLAMA_MODEL=llama3.2:3b  # Default
# Or try:
# OLLAMA_MODEL=llama3.1:8b
# OLLAMA_MODEL=mistral:7b
# OLLAMA_MODEL=gemma2:9b
```

**Benefits:**
- Experiment with different AI personalities
- Compare decision-making styles
- Use more powerful models for complex decisions
- Use faster models for quick responses

### 4. Decision Reasoning Logging
Understand why the AI makes specific decisions.

**Configuration:**
```bash
# In your .env file
LOG_REASONING=true
```

**Benefits:**
- See AI's reasoning for each decision
- Learn from AI's decision-making process
- Debug unexpected choices
- Build trust in AI decisions

**Example Log Entry:**
```json
{
  "timestamp": 1731445859.0,
  "issue_id": "123",
  "title": "Budget Crisis",
  "option_id": "2",
  "method": "AI",
  "reasoning": "Chose option 2 to balance economic stability with social welfare. This option increases taxes moderately while protecting essential services, which aligns with maintaining both economic strength and citizen wellbeing."
}
```

### 5. Enhanced Retry Logic
Improved reliability with automatic retries and exponential backoff.

**Configuration:**
```bash
# In your .env file
MAX_RETRIES=3  # Number of retry attempts
```

**Benefits:**
- Automatic recovery from temporary API failures
- Exponential backoff prevents API overload
- Better handling of network issues
- More reliable long-running operations

### 6. Configuration Template (`.env.example`)
Easy setup with a comprehensive configuration template.

**Usage:**
```bash
cp .env.example .env
# Edit .env with your credentials
```

**Benefits:**
- Clear documentation of all options
- Quick setup for new users
- Example values for guidance
- Prevents configuration mistakes

## 📊 Data Files

The simulator now creates/uses the following data files:

- `choices.ndjson` - Decision history log (existing)
- `nation_stats.ndjson` - Nation statistics history (new)

Both use NDJSON format (newline-delimited JSON) for easy processing and analysis.

## 🔧 Updated Configuration Options

New environment variables available:

| Variable | Default | Description |
|----------|---------|-------------|
| `OLLAMA_MODEL` | `llama3.2:3b` | Ollama model to use for decisions |
| `MAX_RETRIES` | `3` | Number of API retry attempts |
| `LOG_REASONING` | `false` | Log AI reasoning for decisions |

Existing variables remain unchanged:
- `NATION`, `PASSWORD`, `USER_AGENT`
- `SLEEP_BETWEEN_REQUESTS`, `TEST_MODE`, `SINGLE_RUN`

## 🚀 Example Workflows

### Basic Analysis Workflow
```bash
# 1. Run the simulator
python main.py

# 2. Analyze decisions
python analytics.py

# 3. Check nation stats
python stats_tracker.py
```

### Advanced Experimentation Workflow
```bash
# 1. Enable reasoning logging
echo "LOG_REASONING=true" >> .env

# 2. Try a different model
echo "OLLAMA_MODEL=llama3.1:8b" >> .env
ollama pull llama3.1:8b

# 3. Run in test mode first
echo "TEST_MODE=true" >> .env
python main.py

# 4. Analyze with reasoning
python analytics.py

# 5. Compare with previous data
python stats_tracker.py
```

## 🛡️ Security

All new features have been security-reviewed:
- No hardcoded credentials
- Proper error handling
- Timeout configurations
- Safe file operations
- CodeQL scan: 0 alerts

## 📝 Future Enhancement Ideas

Potential future improvements (not implemented):
- Web dashboard for visualizations
- Automated A/B testing between models
- Export to CSV/Excel formats
- Email notifications for major nation changes
- Integration with other NationStates tools
- Multi-nation management
- Decision simulation mode (what-if analysis)

---

**Note:** All features are optional and backward-compatible. The simulator works exactly as before without any configuration changes.
