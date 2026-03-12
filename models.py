from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime
from enum import Enum


class AgentRole(str, Enum):
    RESEARCHER = "researcher"
    ANALYZER = "analyzer"
    WRITER = "writer"
    REVIEWER = "reviewer"


class AgentStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class AgentStep(BaseModel):
    agent_name: str
    role: str
    status: str = "pending"
    input_text: str = ""
    output_text: str = ""
    model: str = ""
    tokens_used: Dict = {}
    cost_usd: float = 0.0
    latency_ms: float = 0.0
    started_at: str = ""
    completed_at: str = ""
    error: Optional[str] = None


class WorkflowRequest(BaseModel):
    task: str = Field(..., description="What you want the agents to do")
    context: Optional[str] = Field(default=None, description="Additional context")
    agents: List[str] = Field(
        default=["researcher", "analyzer", "writer", "reviewer"],
        description="Which agents to use and in what order"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "task": "Research AI trends in 2024 and write a professional summary",
                "context": "Focus on LLMs and automation",
                "agents": ["researcher", "analyzer", "writer", "reviewer"]
            }
        }


class WorkflowResponse(BaseModel):
    workflow_id: str
    task: str
    status: str
    steps: List[AgentStep]
    final_output: str
    total_tokens: Dict
    total_cost_usd: float
    total_latency_ms: float
    agents_used: int
    created_at: str


class WorkflowSummary(BaseModel):
    total_workflows: int
    total_cost: float
    total_tokens_used: int
    average_latency_ms: float
    workflows_by_status: Dict
    agents_usage: Dict
