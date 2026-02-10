from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, condecimal
from uuid import UUID, uuid4
from datetime import datetime

class TaskType(str, Enum):
    RESEARCH = "RESEARCH"
    CONTENT_GEN = "CONTENT_GEN"
    TRANSACTION = "TRANSACTION"
    ENGAGEMENT = "ENGAGEMENT"

class TaskStatus(str, Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    REVIEW = "REVIEW"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class TaskConstraints(BaseModel):
    max_cost_usd: Optional[float] = 50.0
    voice_ref: str = "specs/SOUL.md"

class AgentTask(BaseModel):
    """
    Executable Schema for Swarm Tasks. 
    Matches specs/technical.md contract.
    """
    # Allow string IDs for tests and runtime UUIDs; default to uuid4 hex string
    task_id: str = Field(default_factory=lambda: uuid4().hex)
    parent_goal_id: Optional[str] = None
    type: TaskType
    payload: Dict[str, Any]
    constraints: TaskConstraints = Field(default_factory=TaskConstraints)
    status: TaskStatus = TaskStatus.PENDING
    confidence_score: float = Field(default=1.0, ge=0.0, le=1.0)
    created_at: datetime = Field(default_factory=datetime.now)

class SkillTrendInput(BaseModel):
    source_data: str
    agent_niche: str
    min_relevance: float = 0.7

class TrendItem(BaseModel):
    topic: str
    signal_strength: float
    suggested_action: str

class SkillTrendOutput(BaseModel):
    top_trends: List[TrendItem]
    timestamp: datetime = Field(default_factory=datetime.now)

class WalletAction(str, Enum):
    TRANSFER = "TRANSFER"
    CHECK_BALANCE = "CHECK_BALANCE"

class SkillWalletInput(BaseModel):
    action: WalletAction
    to_address: Optional[str] = None
    amount: Optional[float] = None
    asset: str = "USDC"
