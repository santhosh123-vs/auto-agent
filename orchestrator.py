import uuid
import time
from datetime import datetime
from typing import List, Dict
from models import AgentStep, WorkflowResponse
from agents.researcher import ResearcherAgent
from agents.analyzer import AnalyzerAgent
from agents.writer import WriterAgent
from agents.reviewer import ReviewerAgent


# Initialize all agents
AGENTS = {
    "researcher": ResearcherAgent(),
    "analyzer": AnalyzerAgent(),
    "writer": WriterAgent(),
    "reviewer": ReviewerAgent()
}

# Store workflow history
workflow_history: List[WorkflowResponse] = []


def run_workflow(task: str, context: str = None, agent_order: List[str] = None) -> WorkflowResponse:
    """
    Run a multi-agent workflow.
    Each agent receives the output of the previous agent as context.
    """
    
    if agent_order is None:
        agent_order = ["researcher", "analyzer", "writer", "reviewer"]
    
    workflow_id = str(uuid.uuid4())[:8]
    steps: List[AgentStep] = []
    previous_output = ""
    total_tokens = {"input": 0, "output": 0, "total": 0}
    total_cost = 0.0
    total_latency = 0.0
    workflow_status = "completed"
    final_output = ""
    
    print(f"\n{'='*60}")
    print(f"WORKFLOW {workflow_id}: {task}")
    print(f"Agents: {' -> '.join(agent_order)}")
    print(f"{'='*60}\n")
    
    for i, agent_name in enumerate(agent_order):
        if agent_name not in AGENTS:
            step = AgentStep(
                agent_name=agent_name,
                role=agent_name,
                status="failed",
                error=f"Unknown agent: {agent_name}"
            )
            steps.append(step)
            workflow_status = "failed"
            continue
        
        agent = AGENTS[agent_name]
        step_input = task if i == 0 else f"Original task: {task}"
        
        if context and i == 0:
            step_input = f"{task}\n\nAdditional context: {context}"
        
        print(f"[Agent {i+1}/{len(agent_order)}] {agent.name} starting...")
        
        step = AgentStep(
            agent_name=agent.name,
            role=agent.role,
            status="running",
            input_text=step_input[:500],
            started_at=datetime.now().isoformat()
        )
        
        try:
            output, tokens, cost, latency_ms = agent.run(
                input_text=step_input,
                context=previous_output
            )
            
            step.status = "completed"
            step.output_text = output
            step.model = agent.model
            step.tokens_used = tokens
            step.cost_usd = cost
            step.latency_ms = round(latency_ms, 2)
            step.completed_at = datetime.now().isoformat()
            
            total_tokens["input"] += tokens["input"]
            total_tokens["output"] += tokens["output"]
            total_tokens["total"] += tokens["total"]
            total_cost += cost
            total_latency += latency_ms
            
            previous_output = output
            final_output = output
            
            print(f"[Agent {i+1}/{len(agent_order)}] {agent.name} completed!")
            print(f"  Tokens: {tokens['total']} | Cost: ${cost:.6f} | Time: {latency_ms:.0f}ms")
            
        except Exception as e:
            step.status = "failed"
            step.error = str(e)
            step.completed_at = datetime.now().isoformat()
            workflow_status = "partially_completed"
            
            print(f"[Agent {i+1}/{len(agent_order)}] {agent.name} FAILED: {str(e)}")
            
            if previous_output:
                final_output = previous_output
            else:
                final_output = f"Error in {agent.name}: {str(e)}"
        
        steps.append(step)
    
    workflow = WorkflowResponse(
        workflow_id=workflow_id,
        task=task,
        status=workflow_status,
        steps=steps,
        final_output=final_output,
        total_tokens=total_tokens,
        total_cost_usd=round(total_cost, 6),
        total_latency_ms=round(total_latency, 2),
        agents_used=len(agent_order),
        created_at=datetime.now().isoformat()
    )
    
    workflow_history.append(workflow)
    
    # Keep last 50 workflows
    if len(workflow_history) > 50:
        workflow_history.pop(0)
    
    print(f"\n{'='*60}")
    print(f"WORKFLOW COMPLETE!")
    print(f"Total: {total_tokens['total']} tokens | ${total_cost:.6f} | {total_latency:.0f}ms")
    print(f"{'='*60}\n")
    
    return workflow


def get_workflow_history() -> List[WorkflowResponse]:
    return workflow_history


def get_workflow_summary() -> dict:
    if not workflow_history:
        return {
            "total_workflows": 0,
            "total_cost": 0,
            "total_tokens_used": 0,
            "average_latency_ms": 0,
            "workflows_by_status": {},
            "agents_usage": {}
        }
    
    total_cost = sum(w.total_cost_usd for w in workflow_history)
    total_tokens = sum(w.total_tokens.get("total", 0) for w in workflow_history)
    avg_latency = sum(w.total_latency_ms for w in workflow_history) / len(workflow_history)
    
    status_count = {}
    agent_count = {}
    
    for w in workflow_history:
        status_count[w.status] = status_count.get(w.status, 0) + 1
        for step in w.steps:
            agent_count[step.role] = agent_count.get(step.role, 0) + 1
    
    return {
        "total_workflows": len(workflow_history),
        "total_cost": round(total_cost, 6),
        "total_tokens_used": total_tokens,
        "average_latency_ms": round(avg_latency, 2),
        "workflows_by_status": status_count,
        "agents_usage": agent_count
    }
