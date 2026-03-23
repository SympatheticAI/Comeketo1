"""
Master Loop — Persistent Operational Intelligence Core

The master loop is the standing presence of the Company Loop system.
It is NOT a stream of constant output. It is the field of readiness
within which all sub-loops operate.

The master loop:
- Maintains continuity across sessions
- Holds active corridor definitions
- Preserves memory relationships
- Tracks open obligations
- Integrates writebacks from sub-loops
- Preserves the internal shape of the business as the system understands it

The master loop PERSISTS. Sub-loops are TEMPORARY.

This is the organism. Sub-loops are the episodes.
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum

from runtime.loop.state_manager import StateManager
from runtime.loop.trigger_engine import TriggerEngine
from runtime.loop.dispatcher import Dispatcher


logger = logging.getLogger(__name__)


class LoopHealth(Enum):
    """Master loop health states."""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    CRITICAL = "critical"
    FAILED = "failed"


@dataclass
class MasterLoopState:
    """
    The persistent state of the master loop.

    This is the organism's internal shape. It is NOT visible output.
    It is the standing readiness that makes bounded work possible.
    """

    # Identity and continuity
    deployment_id: str
    started_at: datetime
    last_heartbeat: datetime
    session_count: int = 0

    # Health status
    health: LoopHealth = LoopHealth.HEALTHY
    last_health_check: Optional[datetime] = None

    # Active corridors
    active_corridors: List[str] = field(default_factory=list)
    corridor_states: Dict[str, Dict[str, Any]] = field(default_factory=dict)

    # Open obligations
    open_obligations: List[Dict[str, Any]] = field(default_factory=list)
    deferred_items: List[Dict[str, Any]] = field(default_factory=list)

    # Sub-loop tracking
    sub_loops_opened: int = 0
    sub_loops_closed: int = 0
    sub_loops_active: int = 0

    # Memory relationships
    memory_version: int = 0
    last_memory_update: Optional[datetime] = None

    # Failure tracking
    failures_since_last_recovery: int = 0
    last_recovery_attempt: Optional[datetime] = None

    def mark_healthy(self):
        """Mark the loop as healthy."""
        self.health = LoopHealth.HEALTHY
        self.failures_since_last_recovery = 0
        self.last_health_check = datetime.utcnow()

    def mark_degraded(self, reason: str):
        """Mark the loop as degraded."""
        self.health = LoopHealth.DEGRADED
        self.last_health_check = datetime.utcnow()
        logger.warning(f"Master loop degraded: {reason}")

    def mark_critical(self, reason: str):
        """Mark the loop as critical."""
        self.health = LoopHealth.CRITICAL
        self.failures_since_last_recovery += 1
        self.last_health_check = datetime.utcnow()
        logger.error(f"Master loop critical: {reason}")

    def mark_failed(self, reason: str):
        """Mark the loop as failed."""
        self.health = LoopHealth.FAILED
        self.failures_since_last_recovery += 1
        self.last_health_check = datetime.utcnow()
        logger.critical(f"Master loop failed: {reason}")


class MasterLoop:
    """
    The persistent operational intelligence core.

    This is the organism itself. It does not sleep. It does not restart from zero.
    It maintains continuity while the world changes around it.

    Claude Code serves as the reasoning engine. The master loop is the
    persistence layer that gives that reasoning operational continuity.
    """

    def __init__(
        self,
        deployment_id: str,
        state_manager: StateManager,
        trigger_engine: TriggerEngine,
        dispatcher: Dispatcher,
        config: Dict[str, Any]
    ):
        self.deployment_id = deployment_id
        self.state_manager = state_manager
        self.trigger_engine = trigger_engine
        self.dispatcher = dispatcher
        self.config = config

        # Initialize master loop state
        self.state = MasterLoopState(
            deployment_id=deployment_id,
            started_at=datetime.utcnow(),
            last_heartbeat=datetime.utcnow()
        )

        # Running flag
        self.running = False

        logger.info(f"Master loop initialized: {deployment_id}")

    async def start(self):
        """
        Start the master loop.

        This establishes the persistent presence. The loop will remain alive
        until explicitly stopped or until a critical failure requires shutdown.
        """
        logger.info("Starting master loop...")

        # Load previous state if exists
        await self._restore_continuity()

        # Mark as running
        self.running = True
        self.state.session_count += 1

        # Verify health
        await self._health_check()

        # Begin continuous operation
        logger.info("Master loop is now persistent and active")

        return self.state

    async def stop(self):
        """
        Stop the master loop gracefully.

        This preserves continuity for the next session.
        """
        logger.info("Stopping master loop...")

        # Mark as not running
        self.running = False

        # Close any active sub-loops
        await self._close_active_sub_loops()

        # Save state for continuity
        await self._preserve_continuity()

        logger.info("Master loop stopped gracefully")

    async def heartbeat(self):
        """
        Master loop heartbeat.

        This is the pulse of the organism. It checks continuity,
        verifies health, and ensures the loop remains coherent.
        """
        self.state.last_heartbeat = datetime.utcnow()

        # Check health
        await self._health_check()

        # Update active corridor states
        await self._update_corridor_states()

        # Check for stale obligations
        await self._check_stale_obligations()

        # Write heartbeat to state
        await self.state_manager.record_heartbeat(self.state)

        logger.debug(f"Heartbeat: {self.state.health.value}, "
                    f"{self.state.sub_loops_active} active sub-loops, "
                    f"{len(self.state.open_obligations)} open obligations")

    async def open_sub_loop(
        self,
        trigger_id: str,
        corridor: str,
        trigger_data: Dict[str, Any]
    ) -> str:
        """
        Open a new sub-loop.

        A sub-loop is a bounded episode of live work. It must close.
        The master loop tracks it until closure.
        """
        # Generate sub-loop ID
        sub_loop_id = f"{corridor}_{trigger_id}_{datetime.utcnow().timestamp()}"

        # Update tracking
        self.state.sub_loops_opened += 1
        self.state.sub_loops_active += 1

        logger.info(f"Opening sub-loop: {sub_loop_id} (corridor: {corridor}, trigger: {trigger_id})")

        return sub_loop_id

    async def close_sub_loop(
        self,
        sub_loop_id: str,
        exit_type: str,
        result: Optional[Dict[str, Any]] = None
    ):
        """
        Close a sub-loop.

        Exit types: lock, refusal, timeout, handoff

        This is mandatory. Every sub-loop must close.
        """
        self.state.sub_loops_closed += 1
        self.state.sub_loops_active -= 1

        # Process result based on exit type
        if exit_type == "lock":
            # Promotion - write to state
            await self._process_promotion(sub_loop_id, result)

        elif exit_type == "refusal":
            # Explicit rejection - record why
            await self._process_refusal(sub_loop_id, result)

        elif exit_type == "timeout":
            # Time boundary - preserve state for later
            await self._process_timeout(sub_loop_id, result)

        elif exit_type == "handoff":
            # Escalation - track handoff state
            await self._process_handoff(sub_loop_id, result)

        else:
            logger.warning(f"Unknown exit type: {exit_type} for sub-loop {sub_loop_id}")

        logger.info(f"Closed sub-loop: {sub_loop_id} (exit: {exit_type})")

    async def _restore_continuity(self):
        """
        Restore continuity from previous session.

        The loop does not wake up as a stranger to yesterday.
        """
        logger.info("Restoring continuity from previous session...")

        # Load previous state
        previous_state = await self.state_manager.load_master_state(self.deployment_id)

        if previous_state:
            # Restore corridor states
            self.state.corridor_states = previous_state.get("corridor_states", {})

            # Restore open obligations
            self.state.open_obligations = previous_state.get("open_obligations", [])

            # Restore deferred items
            self.state.deferred_items = previous_state.get("deferred_items", [])

            # Restore memory version
            self.state.memory_version = previous_state.get("memory_version", 0)

            logger.info(f"Continuity restored: {len(self.state.open_obligations)} open obligations, "
                       f"{len(self.state.corridor_states)} corridor states")
        else:
            logger.info("No previous state found - starting fresh")

    async def _preserve_continuity(self):
        """
        Preserve continuity for next session.

        This is what makes the loop persistent across time.
        """
        logger.info("Preserving continuity for next session...")

        state_snapshot = {
            "deployment_id": self.deployment_id,
            "last_session": datetime.utcnow().isoformat(),
            "corridor_states": self.state.corridor_states,
            "open_obligations": self.state.open_obligations,
            "deferred_items": self.state.deferred_items,
            "memory_version": self.state.memory_version,
            "health": self.state.health.value,
            "total_sessions": self.state.session_count,
            "total_sub_loops": self.state.sub_loops_opened
        }

        await self.state_manager.save_master_state(self.deployment_id, state_snapshot)

        logger.info("Continuity preserved")

    async def _health_check(self):
        """
        Check the health of the master loop.

        This verifies that the organism remains coherent.
        """
        try:
            # Check state manager
            if not await self.state_manager.is_healthy():
                self.state.mark_degraded("State manager unhealthy")
                return

            # Check trigger engine
            if not await self.trigger_engine.is_healthy():
                self.state.mark_degraded("Trigger engine unhealthy")
                return

            # Check dispatcher
            if not await self.dispatcher.is_healthy():
                self.state.mark_degraded("Dispatcher unhealthy")
                return

            # All checks passed
            self.state.mark_healthy()

        except Exception as e:
            self.state.mark_critical(f"Health check failed: {str(e)}")
            logger.exception("Health check exception")

    async def _update_corridor_states(self):
        """Update the state of all active corridors."""
        for corridor in self.state.active_corridors:
            corridor_state = await self.state_manager.get_corridor_state(corridor)
            if corridor_state:
                self.state.corridor_states[corridor] = corridor_state

    async def _check_stale_obligations(self):
        """Check for stale open obligations that may need attention."""
        now = datetime.utcnow()
        stale_threshold_hours = self.config.get("stale_obligation_threshold_hours", 48)

        stale_count = 0
        for obligation in self.state.open_obligations:
            created_at = datetime.fromisoformat(obligation.get("created_at"))
            age_hours = (now - created_at).total_seconds() / 3600

            if age_hours > stale_threshold_hours:
                stale_count += 1
                logger.warning(f"Stale obligation detected: {obligation.get('id')} "
                             f"(age: {age_hours:.1f} hours)")

        if stale_count > 0:
            logger.info(f"Found {stale_count} stale obligations")

    async def _close_active_sub_loops(self):
        """Close any active sub-loops during shutdown."""
        if self.state.sub_loops_active > 0:
            logger.warning(f"Closing {self.state.sub_loops_active} active sub-loops during shutdown")
            # In a real implementation, would gracefully close each sub-loop
            self.state.sub_loops_active = 0

    async def _process_promotion(self, sub_loop_id: str, result: Dict[str, Any]):
        """Process a promoted result (lock exit)."""
        logger.info(f"Processing promotion from {sub_loop_id}")
        # Write promoted result to appropriate memory/state layer
        await self.state_manager.record_promotion(sub_loop_id, result)

    async def _process_refusal(self, sub_loop_id: str, result: Dict[str, Any]):
        """Process a refusal (explicit rejection)."""
        logger.info(f"Processing refusal from {sub_loop_id}: {result.get('reason')}")
        # Record refusal to prevent repetition of dead paths
        await self.state_manager.record_refusal(sub_loop_id, result)

    async def _process_timeout(self, sub_loop_id: str, result: Dict[str, Any]):
        """Process a timeout (time boundary)."""
        logger.info(f"Processing timeout from {sub_loop_id}")
        # Preserve state for possible later resumption
        self.state.deferred_items.append({
            "sub_loop_id": sub_loop_id,
            "deferred_at": datetime.utcnow().isoformat(),
            "reason": "timeout",
            "state": result
        })

    async def _process_handoff(self, sub_loop_id: str, result: Dict[str, Any]):
        """Process a handoff (escalation)."""
        logger.info(f"Processing handoff from {sub_loop_id} to {result.get('handoff_to')}")
        # Create obligation for the handoff target
        self.state.open_obligations.append({
            "id": f"handoff_{sub_loop_id}",
            "created_at": datetime.utcnow().isoformat(),
            "type": "handoff",
            "from_sub_loop": sub_loop_id,
            "handoff_to": result.get("handoff_to"),
            "context": result.get("context"),
            "escalation_reason": result.get("reason")
        })
