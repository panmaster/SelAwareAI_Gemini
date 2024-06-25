import json
import os
from datetime import datetime
from typing import List, Dict, Any
import asyncio


class MemoryLattice:
    def __init__(self):
        self.working_memory: List[Dict[str, Any]] = []
        self.episodic_memory: List[Dict[str, Any]] = []
        self.semantic_memory: Dict[str, Any] = {}
        self.memory_dir = "memories"
        os.makedirs(self.memory_dir, exist_ok=True)

    async def get_relevant_context(self, query: str) -> List[str]:
        # TODO: Implement more sophisticated relevance ranking
        recent_memories = self.working_memory[-5:]  # Get last 5 items
        return [f"{m['input']}: {m['output']}" for m in recent_memories]

    async def store(self, input_text: str, output_text: str):
        timestamp = datetime.now().isoformat()
        memory = {
            'timestamp': timestamp,
            'input': input_text,
            'output': output_text
        }

        # Store in working memory
        self.working_memory.append(memory)
        if len(self.working_memory) > 100:
            self.working_memory.pop(0)

        # Store in episodic memory
        self.episodic_memory.append(memory)

        # Save to file
        filename = f"{self.memory_dir}/memory_{timestamp}.json"
        with open(filename, 'w') as f:
            json.dump(memory, f)

    async def update_semantic_memory(self, key: str, value: Any):
        self.semantic_memory[key] = value

        # Save semantic memory to file
        with open(f"{self.memory_dir}/semantic_memory.json", 'w') as f:
            json.dump(self.semantic_memory, f)

    async def load_memories(self):
        # Load episodic memories
        for filename in os.listdir(self.memory_dir):
            if filename.startswith("memory_") and filename.endswith(".json"):
                with open(os.path.join(self.memory_dir, filename), 'r') as f:
                    memory = json.load(f)
                    self.episodic_memory.append(memory)

        # Sort episodic memories by timestamp
        self.episodic_memory.sort(key=lambda x: x['timestamp'])

        # Load semantic memory
        if os.path.exists(f"{self.memory_dir}/semantic_memory.json"):
            with open(f"{self.memory_dir}/semantic_memory.json", 'r') as f:
                self.semantic_memory = json.load(f)

        # Initialize working memory with most recent episodic memories
        self.working_memory = self.episodic_memory[-100:]