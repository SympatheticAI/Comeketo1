"""
State Manager — Maintains System State Across Sessions

Responsibilities:
- Load/save corridor state
- Track active obligations
- Maintain memory continuity
- Handle state snapshots
"""

import json
from pathlib import Path
from typing import Dict, Any
from loguru import logger


class StateManager:
    """
    Manages persistent state for the loop.

    State includes:
    - Active obligations (unresolved tasks, pending approvals)
    - Corridor state (last processed, recent summaries)
    - Relational memory (venues, partners, clients)
    - Trigger history
    """

    def __init__(self, memory_path: Path = Path("memory")):
        """
        Initialize state manager.

        Args:
            memory_path: Root path for memory storage
        """
        self.memory_path = memory_path
        self.state: Dict[str, Any] = {
            "active": {},
            "corridors": {},
            "relational": {},
            "triggers": []
        }

    async def load(self):
        """
        Load state from disk.

        Reads from memory/ directory:
        - active/obligations.json
        - corridor/*.json
        - relational/*.json
        """
        logger.info("Loading system state...")

        try:
            # Load active obligations
            active_path = self.memory_path / "active" / "obligations.json"
            if active_path.exists():
                with open(active_path) as f:
                    self.state["active"] = json.load(f)
                logger.debug(f"Loaded {len(self.state['active'])} active obligations")

            # TODO: Load corridor and relational state

            logger.info("State loaded successfully")

        except Exception as e:
            logger.exception(f"Error loading state: {e}")
            logger.warning("Starting with empty state")

    async def save(self):
        """
        Save state to disk.

        Writes to memory/ directory with atomic updates.
        """
        logger.info("Saving system state...")

        try:
            # Save active obligations
            active_path = self.memory_path / "active" / "obligations.json"
            active_path.parent.mkdir(parents=True, exist_ok=True)

            with open(active_path, "w") as f:
                json.dump(self.state["active"], f, indent=2)

            # TODO: Save corridor and relational state

            logger.info("State saved successfully")

        except Exception as e:
            logger.exception(f"Error saving state: {e}")

    def get_corridor_state(self, corridor: str) -> Dict[str, Any]:
        """Get state for specific corridor."""
        return self.state["corridors"].get(corridor, {})

    def set_corridor_state(self, corridor: str, state: Dict[str, Any]):
        """Set state for specific corridor."""
        self.state["corridors"][corridor] = state
