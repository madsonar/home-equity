from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class KnowledgeChunk:
    content: str
    source: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    score: float = 0.0
