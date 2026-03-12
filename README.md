# AutoAgent - Multi-Agent Orchestration Engine

A multi-agent orchestration system where AI agents chain together to complete complex tasks. Each agent has specialized skills and passes its output to the next agent.

## How It Works

User Task --> [Researcher] --> [Analyzer] --> [Writer] --> [Reviewer] --> Final Output

## Agents

| Agent | Role | What It Does |
|-------|------|-------------|
| Researcher | Information Gathering | Researches the topic thoroughly |
| Analyzer | Data Analysis | Organizes and analyzes findings |
| Writer | Content Creation | Creates polished professional content |
| Reviewer | Quality Check | Reviews, scores, and improves output |

## Features

- Multi-agent orchestration with configurable pipelines
- Execution tracing per agent (tokens, cost, latency)
- Automatic context passing between agents
- Error handling and partial completion support
- Real-time monitoring dashboard
- Workflow history and analytics
- Download results as TXT or JSON
- Select which agents to use per workflow

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Backend | FastAPI (Python) |
| AI Provider | Groq (Llama 3.3 70B) |
| Dashboard | Streamlit |
| Orchestration | Custom Python engine |

## Quick Start

1. Clone: git clone https://github.com/santhosh123-vs/auto-agent.git
2. Setup: python3 -m venv venv && source venv/bin/activate
3. Install: pip install -r requirements.txt
4. Add Groq key to .env file
5. Start API: uvicorn main:app --reload --port 8001
6. Start Dashboard: streamlit run dashboard.py

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/v1/workflow | Run multi-agent workflow |
| GET | /api/v1/workflows | Get workflow history |
| GET | /api/v1/summary | Usage summary |
| GET | /api/v1/agents | List available agents |
| POST | /api/v1/single-agent | Run single agent |

## Sample Workflow Result

- 4 agents chained together
- 6654 total tokens used
- Total cost: -zsh.004633
- Total time: 8.7 seconds
- Final output: Professional polished content

## Author

Built by Kethavath Santhosh
GitHub: https://github.com/santhosh123-vs

## License

MIT License
