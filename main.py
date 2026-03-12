from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import WorkflowRequest, WorkflowResponse, WorkflowSummary
from orchestrator import run_workflow, get_workflow_history, get_workflow_summary, AGENTS

app = FastAPI(
    title="AutoAgent — Multi-Agent Orchestration Engine",
    description="""
    A multi-agent orchestration system where AI agents chain together 
    to complete complex tasks. Each agent has specialized skills and 
    passes its output to the next agent.
    
    Agents: Researcher → Analyzer → Writer → Reviewer
    
    Features:
    - Configurable agent pipelines
    - Execution tracing per agent
    - Cost and token tracking
    - Automatic error handling and fallback
    
    Built by Kethavath Santhosh
    """,
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "name": "AutoAgent — Multi-Agent Orchestration Engine",
        "version": "1.0.0",
        "agents": list(AGENTS.keys()),
        "endpoints": {
            "POST /api/v1/workflow": "Run a multi-agent workflow",
            "GET /api/v1/workflows": "Get workflow history",
            "GET /api/v1/summary": "Get usage summary",
            "GET /api/v1/agents": "List available agents"
        }
    }


@app.post("/api/v1/workflow", response_model=WorkflowResponse)
def execute_workflow(request: WorkflowRequest):
    """Run a multi-agent workflow"""
    try:
        result = run_workflow(
            task=request.task,
            context=request.context,
            agent_order=request.agents
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/workflows")
def list_workflows(limit: int = 10):
    """Get recent workflow history"""
    history = get_workflow_history()
    return {
        "total": len(history),
        "workflows": history[-limit:]
    }


@app.get("/api/v1/summary")
def workflow_summary():
    """Get overall usage summary"""
    return get_workflow_summary()


@app.get("/api/v1/agents")
def list_agents():
    """List all available agents"""
    agents_info = {}
    for name, agent in AGENTS.items():
        agents_info[name] = {
            "name": agent.name,
            "role": agent.role,
            "model": agent.model,
            "description": agent.system_prompt[:200] + "..."
        }
    return agents_info


@app.post("/api/v1/single-agent")
def run_single_agent(agent_name: str, task: str):
    """Run a single agent only"""
    try:
        result = run_workflow(
            task=task,
            agent_order=[agent_name]
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
