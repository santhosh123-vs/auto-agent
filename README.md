# AutoAgent

Multi-Agent Orchestration Engine - AI agents that work together.

## Live Demo

Try it now: https://auto-agent-zqitoxg3mphcafrpkq29rq.streamlit.app/

## Key Metrics

| Metric | Value |
|--------|-------|
| Agents | 4 (Researcher, Analyzer, Writer, Reviewer) |
| Avg Task Completion | 3 steps per workflow |
| Context Passing | 100% between agents |
| Cost Tracking | Per-token monitoring |
| Workflow History | Full execution trace |

## Architecture

User Query --> Researcher Agent --> Analyzer Agent --> Writer Agent --> Reviewer Agent --> Final Output

## How It Works

1. Researcher: Gathers information on the topic
2. Analyzer: Analyzes and structures the research
3. Writer: Creates well-written content
4. Reviewer: Reviews for quality and accuracy
5. Each agent passes context to the next agent

## Features

- Multi-Agent Orchestration: 4 agents chain together automatically
- Context Passing: Each agent builds on previous agent output
- Execution Tracking: Full trace of each agent step
- Cost Monitoring: Token usage and cost per request
- Workflow History: View past executions

## Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Backend |
| FastAPI | API Framework |
| Groq | LLM Provider (Llama 3.3 70B) |
| Streamlit | Dashboard |

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| /orchestrate | POST | Run full agent pipeline |
| /agents | GET | List all agents |
| /history | GET | View workflow history |

## Quick Start

1. Clone: git clone https://github.com/santhosh123-vs/auto-agent
2. Install: pip install -r requirements.txt
3. Add .env with GROQ_API_KEY
4. Run: python main.py

## Author

Kethavath Santhosh - github.com/santhosh123-vs
