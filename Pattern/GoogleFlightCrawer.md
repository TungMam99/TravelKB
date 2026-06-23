de, and Python.

⭐️ Star this repo if you hate enterprise API pricing.

This tool wraps the fast-flights library to provide a clean JSON API for flight data. No API keys, no Selenium bloat, just raw Protobuf decoding.

🚀 Features
Real-time Google Flights Data: Scrapes live prices via Protobuf reverse-engineering.
Structured Output: Returns clean JSON for AI consumption.
Fast: No browser automation required (uses requests fallback).
Unit Tested: Includes comprehensive test suite.
📦 Installation
Clone the repo:
*.bash
Shell
git clone https://github.com/Anmoldureha/flights-skill.git
cd flights-skill
Set up Python environment:
*.bash
Shell
python3 -m venv venv
source venv/bin/activate
pip install fast-flights typing-extensions
🛠️ Usage
Run the script directly from the command line:

*.bash
Shell
# Syntax: python search.py ORIGIN DEST DATE
python search.py SFO JFK 2026-03-01
Output:

*.json
JSON
{
  "current_price": "typical",
  "flights": [
    {
      "name": "Delta",
      "price": "$120",
      "duration": "5h 30m",
      ...
    }
  ]
}
🧪 Testing
Run the unit tests to verify logic:

python3 tests/test_search.py
🤖 Agent Integration
Claude Code (MCP)
This repo includes a native MCP Server implementation (compatible with Claude Desktop).

Add to your claude_desktop_config.json:
*.json
JSON
{
  "mcpServers": {
    "flights": {
      "command": "/absolute/path/to/skills/flights/venv/bin/python3",
      "args": ["/absolute/path/to/skills/flights/mcp_server.py"]
    }
  }
}
Restart Claude Desktop. You can now ask: "Find me cheap flights to Tokyo".
OpenClaw
Add this repo to your skills directory and map flight_search to: venv/bin/python3 search.py {{from}} {{to}} {{date}}

🌟 Why is this great? (The Advantage)
Most flight search APIs are broken, expensive, or stale. This tool solves the "Google Flights Data Problem":

1. 🧠 AI-Native Design
Most scrapers return messy HTML. This tool outputs clean, structured JSON specifically optimized for LLM consumption.

Lower Token Cost: No fluff, just data.
Higher Accuracy: Agents don't have to hallucinate parsing logic.
2. ⚡ The "Impossible" API
Google discontinued their public Flights API in 2018. Developers have been forced to use:

Expensive Aggregators (Amadeus/Duffel): Cost $0.002+ per request and require KYC.
Slow Selenium Bots: Break easily and take 10s+ to load.
Stale Data: Most APIs cache prices for 24 hours.
This tool hacks the matrix. It reverse-engineers the Protobuf data stream used by Google's own frontend, giving you Enterprise-grade speed (ms) without the Enterprise price tag.

3. 🛡️ Local & Private
Runs 100% on your machine (or your agent's container). No third-party server logging your travel plans or selling your search intent data to airlines.

🙏 Credits
This skill is a wrapper around the brilliant fast-flights library by AWeirdDev. They did the heavy lifting of reverse-engineering Google's Protobuf format. Go star their repo! ⭐