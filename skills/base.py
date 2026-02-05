from abc import ABC, abstractmethod
from typing import Any, Dict
from pydantic import BaseModel

class ChimeraSkill(ABC):
    """
    Base class for all Chimera Agent Skills.
    Enforces a standardized I/O contract for the Worker Swarm.
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """The unique identifier for the skill."""
        pass

    @abstractmethod
    async def execute(self, input_data: BaseModel) -> BaseModel:
        """
        Executes the skill logic. 
        Must accept a Pydantic model and return a Pydantic model.
        """
        pass
