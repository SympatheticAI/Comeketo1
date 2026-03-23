"""
Sub-Loop — Bounded Episode of Live Work

A sub-loop is temporary by design. It must terminate cleanly.

The master loop persists. Sub-loops do not.

Every sub-loop:
- Opens on a defined trigger
- Reads current relevant state
- Gathers corridor-specific context
- Evaluates candidate interpretations/next moves
- Rejects branches that should not be pursued
- Selects what is strong enough to survive
- Writes back its outcomes
- CLOSES (mandatory)

A sub-loop MUST close through one of four lawful exits:
- LOCK (promotion)
- REFUSAL (explicit rejection)
- TIMEOUT (time boundary)
- HANDOFF (escalation)
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum


logger = logging.getLogger(__name__)


class SubLoopExit(Enum):
    """
    The four lawful exits of every sub-loop.

    Every sub-loop MUST close through one of these paths.
    """
    LOCK = "lock"          # Successful promotion
    REFUSAL = "refusal"    # Explicit rejection
    TIMEOUT = "timeout"    # Time boundary
    HANDOFF = "handoff"    # Escalation


class SubLoopPhase(Enum):
    """Phases of sub-loop execution."""
    INITIALIZING = "initializing"
    GATHERING = "gathering"
    EVALUATING = "evaluating"
    DECIDING = "deciding"
    WRITING = "writing"
    CLOSING = "closing"
    CLOSED = "closed"


@dataclass
class SubLoopContext:
    """
    Context loaded at sub-loop initialization.

    This is the relevant state the sub-loop needs to perform bounded work.
    """

    # Trigger information
    trigger_id: str
    trigger_type: str  # time-based, event-based, human-invoked
    trigger_data: Dict[str, Any]

    # Corridor information
    corridor: str
    corridor_config: Dict[str, Any]

    # Memory context
    relevant_memory: List[Dict[str, Any]] = field(default_factory=list)
    recent_history: List[Dict[str, Any]] = field(default_factory=list)

    # Open obligations related to this work
    related_obligations: List[Dict[str, Any]] = field(default_factory=list)

    # Permissions and authority
    allowed_actions: List[str] = field(default_factory=list)
    approval_required: bool = False


@dataclass
class SubLoopResult:
    """
    Result of a sub-loop's work.

    This is what gets written back to state or surfaced to the human.
    """

    # Exit information
    exit_type: SubLoopExit
    exit_reason: str

    # Outcome (if promotable)
    outcome: Optional[Dict[str, Any]] = None

    # What survived filtering
    promoted_facts: List[Dict[str, Any]] = field(default_factory=list)
    promoted_actions: List[Dict[str, Any]] = field(default_factory=list)
    promoted_recommendations: List[Dict[str, Any]] = field(default_factory=list)

    # What was refused
    refused_branches: List[Dict[str, Any]] = field(default_factory=list)

    # Handoff information (if escalating)
    handoff_to: Optional[str] = None
    handoff_context: Optional[Dict[str, Any]] = None

    # New obligations created
    new_obligations: List[Dict[str, Any]] = field(default_factory=list)

    # Execution metadata
    execution_time_ms: int = 0
    confidence_score: Optional[float] = None


class SubLoop:
    """
    A bounded episode of live operational work.

    Sub-loops are temporary. They exist only long enough to complete
    a specific cycle of inference and action within a defined corridor.
    """

    def __init__(
        self,
        sub_loop_id: str,
        context: SubLoopContext,
        timeout_seconds: int = 300  # 5 minutes default
    ):
        self.sub_loop_id = sub_loop_id
        self.context = context
        self.timeout_seconds = timeout_seconds

        # Execution state
        self.phase = SubLoopPhase.INITIALIZING
        self.started_at = datetime.utcnow()
        self.closed_at: Optional[datetime] = None

        # Result (built during execution)
        self.result = SubLoopResult(
            exit_type=SubLoopExit.REFUSAL,  # Default to refusal
            exit_reason="Sub-loop did not complete"
        )

        # Tracking
        self.is_closed = False

        logger.info(f"Sub-loop created: {sub_loop_id} (corridor: {context.corridor}, "
                   f"trigger: {context.trigger_id})")

    async def execute(self) -> SubLoopResult:
        """
        Execute the sub-loop's work.

        This is the bounded cycle: gather → evaluate → decide → write → close.
        """
        start_time = datetime.utcnow()

        try:
            # Check timeout before each phase
            async with asyncio.timeout(self.timeout_seconds):

                # Phase 1: Gather context
                self.phase = SubLoopPhase.GATHERING
                gathered = await self._gather_context()

                # Phase 2: Evaluate candidates
                self.phase = SubLoopPhase.EVALUATING
                candidates = await self._evaluate_candidates(gathered)

                # Phase 3: Decide what survives
                self.phase = SubLoopPhase.DECIDING
                decision = await self._decide(candidates)

                # Phase 4: Write back
                self.phase = SubLoopPhase.WRITING
                await self._writeback(decision)

                # Phase 5: Close
                self.phase = SubLoopPhase.CLOSING
                await self._close(decision)

        except asyncio.TimeoutError:
            # Timeout is a lawful exit
            logger.warning(f"Sub-loop {self.sub_loop_id} timed out after {self.timeout_seconds}s")
            await self._close_timeout()

        except Exception as e:
            # Unexpected error - refuse and escalate
            logger.exception(f"Sub-loop {self.sub_loop_id} encountered error")
            await self._close_error(str(e))

        # Calculate execution time
        execution_time = (datetime.utcnow() - start_time).total_seconds() * 1000
        self.result.execution_time_ms = int(execution_time)

        return self.result

    async def _gather_context(self) -> Dict[str, Any]:
        """
        Gather all context needed for this sub-loop's work.

        This includes:
        - Current state from relevant business systems
        - Memory context
        - Related obligations
        - Historical patterns
        """
        logger.debug(f"[{self.sub_loop_id}] Gathering context...")

        gathered = {
            "trigger": self.context.trigger_data,
            "corridor_config": self.context.corridor_config,
            "memory": self.context.relevant_memory,
            "history": self.context.recent_history,
            "obligations": self.context.related_obligations,
            "permissions": {
                "allowed_actions": self.context.allowed_actions,
                "approval_required": self.context.approval_required
            }
        }

        # In a real implementation, would fetch from:
        # - CRM
        # - Google Sheets
        # - Calendar
        # - Memory systems
        # - etc.

        return gathered

    async def _evaluate_candidates(self, gathered: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Evaluate candidate interpretations, actions, or next moves.

        This is where Claude Code performs reasoning over the gathered context.

        Returns candidates ranked by strength/confidence.
        """
        logger.debug(f"[{self.sub_loop_id}] Evaluating candidates...")

        # This is where corridor-specific logic runs
        # Each corridor may have different evaluation criteria

        candidates = []

        # Placeholder: In real implementation, would invoke corridor logic
        # to generate and rank candidate next moves

        return candidates

    async def _decide(self, candidates: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Decide what survives filtering.

        This is the narrowing: many things noticed, few things promoted.

        Returns decision with exit type and outcome.
        """
        logger.debug(f"[{self.sub_loop_id}] Deciding what survives...")

        # Apply survival filters:
        # - Is this real enough?
        # - Is this relevant enough?
        # - Is this current enough?
        # - Is this allowed?
        # - Is this worth surfacing?
        # - Is this more likely to help than to distract?

        decision = {
            "exit_type": SubLoopExit.REFUSAL,  # Default to refusal
            "reason": "No candidates survived filtering"
        }

        if not candidates:
            # No candidates - refuse
            decision["exit_type"] = SubLoopExit.REFUSAL
            decision["reason"] = "No candidates generated"
            return decision

        # Check strongest candidate
        strongest = candidates[0]

        # Check admissibility
        if not await self._is_admissible(strongest):
            decision["exit_type"] = SubLoopExit.REFUSAL
            decision["reason"] = f"Strongest candidate not admissible: {strongest.get('inadmissible_reason')}"
            self.result.refused_branches.append(strongest)
            return decision

        # Check if requires handoff
        if strongest.get("requires_human_judgment"):
            decision["exit_type"] = SubLoopExit.HANDOFF
            decision["reason"] = "Requires human judgment"
            decision["handoff_to"] = "human_approval"
            decision["outcome"] = strongest
            return decision

        # Candidate survives - lock it in
        decision["exit_type"] = SubLoopExit.LOCK
        decision["reason"] = "Candidate survived all filters"
        decision["outcome"] = strongest

        return decision

    async def _is_admissible(self, candidate: Dict[str, Any]) -> bool:
        """
        Check if a candidate is admissible.

        Admissibility criteria:
        - Coherent
        - Sufficiently evidenced
        - Permission-compatible
        - Proportionate to stakes
        """
        # Check permissions
        required_action = candidate.get("action_type")
        if required_action and required_action not in self.context.allowed_actions:
            candidate["inadmissible_reason"] = f"Action '{required_action}' not in allowed actions"
            return False

        # Check confidence
        confidence = candidate.get("confidence", 0.0)
        min_confidence = self.context.corridor_config.get("min_confidence_for_action", 0.7)

        if confidence < min_confidence:
            candidate["inadmissible_reason"] = f"Confidence {confidence} below threshold {min_confidence}"
            return False

        # Check if requires approval but not configured for it
        if self.context.approval_required and not candidate.get("draft_mode"):
            # In approval-required mode, must be marked as draft
            candidate["inadmissible_reason"] = "Approval required but not in draft mode"
            return False

        # Admissible
        return True

    async def _writeback(self, decision: Dict[str, Any]):
        """
        Write back the decision's outcomes to state.

        This is what makes the loop learn and accumulate intelligence.
        """
        logger.debug(f"[{self.sub_loop_id}] Writing back decision...")

        # Build result based on exit type
        exit_type = decision["exit_type"]

        if exit_type == SubLoopExit.LOCK:
            # Promotion - record what survived
            outcome = decision.get("outcome", {})
            self.result.outcome = outcome

            # Extract promoted components
            if "facts" in outcome:
                self.result.promoted_facts = outcome["facts"]
            if "actions" in outcome:
                self.result.promoted_actions = outcome["actions"]
            if "recommendations" in outcome:
                self.result.promoted_recommendations = outcome["recommendations"]

        elif exit_type == SubLoopExit.HANDOFF:
            # Handoff - record escalation
            self.result.handoff_to = decision.get("handoff_to")
            self.result.handoff_context = decision.get("outcome", {})

        # In real implementation, would write to:
        # - State manager
        # - Memory systems
        # - CRM
        # - Task systems
        # etc.

    async def _close(self, decision: Dict[str, Any]):
        """
        Close the sub-loop.

        This is mandatory. Every sub-loop must close.
        """
        self.phase = SubLoopPhase.CLOSING

        # Set result
        self.result.exit_type = decision["exit_type"]
        self.result.exit_reason = decision["reason"]

        # Mark as closed
        self.is_closed = True
        self.closed_at = datetime.utcnow()
        self.phase = SubLoopPhase.CLOSED

        logger.info(f"Sub-loop {self.sub_loop_id} closed: {self.result.exit_type.value} "
                   f"({self.result.exit_reason})")

    async def _close_timeout(self):
        """Close sub-loop due to timeout."""
        self.result.exit_type = SubLoopExit.TIMEOUT
        self.result.exit_reason = f"Sub-loop exceeded {self.timeout_seconds}s timeout"

        self.is_closed = True
        self.closed_at = datetime.utcnow()
        self.phase = SubLoopPhase.CLOSED

        logger.warning(f"Sub-loop {self.sub_loop_id} timed out")

    async def _close_error(self, error: str):
        """Close sub-loop due to unexpected error."""
        self.result.exit_type = SubLoopExit.REFUSAL
        self.result.exit_reason = f"Error during execution: {error}"

        self.is_closed = True
        self.closed_at = datetime.utcnow()
        self.phase = SubLoopPhase.CLOSED

        logger.error(f"Sub-loop {self.sub_loop_id} closed due to error: {error}")


# Factory function for creating sub-loops
async def create_sub_loop(
    sub_loop_id: str,
    trigger_id: str,
    trigger_type: str,
    trigger_data: Dict[str, Any],
    corridor: str,
    corridor_config: Dict[str, Any],
    state_manager: Any,  # StateManager instance
    timeout_seconds: int = 300
) -> SubLoop:
    """
    Create and initialize a new sub-loop.

    This gathers the initial context needed for bounded work.
    """
    # Load relevant memory
    relevant_memory = await state_manager.get_relevant_memory(corridor, trigger_data)

    # Load recent history
    recent_history = await state_manager.get_recent_history(corridor, limit=10)

    # Load related obligations
    related_obligations = await state_manager.get_related_obligations(corridor, trigger_data)

    # Determine permissions
    allowed_actions = corridor_config.get("allowed_actions", [])
    approval_required = corridor_config.get("approval_required", True)

    # Build context
    context = SubLoopContext(
        trigger_id=trigger_id,
        trigger_type=trigger_type,
        trigger_data=trigger_data,
        corridor=corridor,
        corridor_config=corridor_config,
        relevant_memory=relevant_memory,
        recent_history=recent_history,
        related_obligations=related_obligations,
        allowed_actions=allowed_actions,
        approval_required=approval_required
    )

    # Create sub-loop
    sub_loop = SubLoop(
        sub_loop_id=sub_loop_id,
        context=context,
        timeout_seconds=timeout_seconds
    )

    return sub_loop
