"""
Approval Engine — Manages Human Approval Workflows

Responsibilities:
- Queue actions requiring approval
- Present approval requests to humans
- Track approval/rejection decisions
- Execute approved actions
- Learn from approval patterns
"""

from typing import Dict, Any, Optional
from enum import Enum
from loguru import logger


class ApprovalStatus(Enum):
    """Status of approval request."""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"


class ApprovalEngine:
    """
    Manages approval workflows for high-stakes actions.

    Actions requiring approval (configurable):
    - External client communication
    - Financial record changes
    - Public social media posts
    - Staff assignment modifications
    - Critical CRM updates

    In shadow mode: All actions require approval
    In draft mode: Suggestions are generated but not executed
    In autonomous mode: Approved action types execute automatically
    """

    def __init__(self, mode: str = "shadow"):
        """
        Initialize approval engine.

        Args:
            mode: Execution mode (shadow | draft | autonomous)
        """
        self.mode = mode
        self.approval_queue: Dict[str, Dict[str, Any]] = {}
        self.approval_history: list = []

    async def request_approval(
        self,
        action_type: str,
        corridor: str,
        description: str,
        context: Dict[str, Any],
        proposed_action: Dict[str, Any]
    ) -> str:
        """
        Request approval for an action.

        Args:
            action_type: Type of action (send_email, create_task, update_crm, etc.)
            corridor: Which corridor is requesting approval
            description: Human-readable description of action
            context: Context that led to this action
            proposed_action: Details of proposed action

        Returns:
            Approval request ID
        """
        import uuid
        import datetime

        request_id = str(uuid.uuid4())

        approval_request = {
            "id": request_id,
            "action_type": action_type,
            "corridor": corridor,
            "description": description,
            "context": context,
            "proposed_action": proposed_action,
            "status": ApprovalStatus.PENDING,
            "created_at": datetime.datetime.utcnow().isoformat(),
            "expires_at": None  # TODO: Add expiration logic
        }

        self.approval_queue[request_id] = approval_request

        logger.info(f"Approval requested: {action_type} from {corridor}")
        logger.debug(f"Approval request ID: {request_id}")

        # TODO: Notify human via configured channel (email, Slack, dashboard)

        return request_id

    async def approve(self, request_id: str, approved_by: str) -> bool:
        """
        Approve a pending request.

        Args:
            request_id: ID of approval request
            approved_by: Who approved (user ID or name)

        Returns:
            True if approval successful
        """
        request = self.approval_queue.get(request_id)
        if not request:
            logger.warning(f"Approval request not found: {request_id}")
            return False

        if request["status"] != ApprovalStatus.PENDING:
            logger.warning(f"Request {request_id} is not pending (status: {request['status']})")
            return False

        request["status"] = ApprovalStatus.APPROVED
        request["approved_by"] = approved_by
        request["approved_at"] = import_datetime.datetime.utcnow().isoformat()

        logger.info(f"Request {request_id} approved by {approved_by}")

        # TODO: Execute approved action
        await self._execute_approved_action(request)

        # Move to history
        self.approval_history.append(request)
        del self.approval_queue[request_id]

        return True

    async def reject(self, request_id: str, rejected_by: str, reason: Optional[str] = None) -> bool:
        """
        Reject a pending request.

        Args:
            request_id: ID of approval request
            rejected_by: Who rejected (user ID or name)
            reason: Optional reason for rejection

        Returns:
            True if rejection successful
        """
        request = self.approval_queue.get(request_id)
        if not request:
            logger.warning(f"Approval request not found: {request_id}")
            return False

        if request["status"] != ApprovalStatus.PENDING:
            logger.warning(f"Request {request_id} is not pending (status: {request['status']})")
            return False

        request["status"] = ApprovalStatus.REJECTED
        request["rejected_by"] = rejected_by
        request["rejected_at"] = import_datetime.datetime.utcnow().isoformat()
        request["rejection_reason"] = reason

        logger.info(f"Request {request_id} rejected by {rejected_by}")
        if reason:
            logger.debug(f"Rejection reason: {reason}")

        # Move to history
        self.approval_history.append(request)
        del self.approval_queue[request_id]

        return True

    async def _execute_approved_action(self, request: Dict[str, Any]):
        """
        Execute an approved action.

        Args:
            request: Approved request details
        """
        action_type = request["action_type"]
        proposed_action = request["proposed_action"]

        logger.info(f"Executing approved action: {action_type}")

        # TODO: Implement actual action execution
        # This would dispatch to appropriate integration:
        # - send_email → Gmail integration
        # - create_task → ClickUp integration
        # - update_crm → Close integration
        # - post_social → Social media integration
        # etc.

        logger.debug(f"Action executed: {action_type}")

    def requires_approval(self, action_type: str) -> bool:
        """
        Check if action type requires approval in current mode.

        Args:
            action_type: Type of action to check

        Returns:
            True if approval required
        """
        # In shadow mode, everything requires approval
        if self.mode == "shadow":
            return True

        # In draft mode, everything requires approval
        if self.mode == "draft":
            return True

        # In autonomous mode, check against approved action types
        # TODO: Load from config
        high_stakes_actions = {
            "send_email",
            "update_crm",
            "post_social",
            "modify_calendar",
            "change_staffing",
            "update_finance"
        }

        return action_type in high_stakes_actions
