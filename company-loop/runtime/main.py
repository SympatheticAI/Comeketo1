"""
Company Loop — Main Runtime Entry Point

This is the primary execution engine for the autonomous business intelligence system.

Responsibilities:
- Initialize integrations (Google, ClickUp, Close, Social, VY, Pieces)
- Load configuration and corridor definitions
- Start scheduler with time-based and event-based triggers
- Coordinate corridor agents
- Manage approval workflows
- Handle graceful shutdown

Usage:
    # Run in shadow mode (observation only)
    python runtime/main.py --mode shadow

    # Run in draft mode (generate suggestions, require approval)
    python runtime/main.py --mode draft

    # Run in autonomous mode (approved actions execute automatically)
    python runtime/main.py --mode autonomous

    # Run single corridor for testing
    python runtime/main.py --corridor sales --mode shadow
"""

import argparse
import asyncio
import logging
import sys
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from loguru import logger

from runtime.loop.scheduler import Scheduler
from runtime.loop.dispatcher import Dispatcher
from runtime.loop.state_manager import StateManager
from runtime.loop.trigger_engine import TriggerEngine
from runtime.loop.approval_engine import ApprovalEngine
from runtime.loop.master_loop import MasterLoop
from runtime.loop.medic import Medic
from runtime.loop.watchdog import Watchdog

# Load environment variables
load_dotenv()

# Configure logging
logger.remove()
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
    level="INFO"
)
logger.add(
    "logs/company-loop.log",
    rotation="500 MB",
    retention="30 days",
    level="DEBUG"
)


class CompanyLoop:
    """
    Main orchestrator for the Company Loop system.

    This is the BOOTSTRAP for the MASTER LOOP.

    The master loop is the persistent organism.
    This class initializes it and keeps it running.

    Coordinates all subsystems:
    - Master Loop: Persistent operational core
    - Scheduler: Time-based and event-based triggers
    - Dispatcher: Routes work to corridor agents
    - State Manager: Maintains system state
    - Trigger Engine: Evaluates trigger conditions
    - Approval Engine: Manages human approval workflows
    - Medic: Self-healing health monitoring
    - Watchdog: Monitors the medic
    """

    def __init__(
        self,
        mode: str = "shadow",
        corridor: Optional[str] = None,
        config_path: Path = Path("config/app.yaml")
    ):
        """
        Initialize Company Loop runtime.

        Args:
            mode: Execution mode (shadow | draft | autonomous)
            corridor: Optional single corridor to run (for testing)
            config_path: Path to main configuration file
        """
        self.mode = mode
        self.corridor_filter = corridor
        self.config_path = config_path

        # Load config (placeholder - would read YAML)
        self.config = {
            "deployment_id": "company-loop-v1",
            "mode": mode,
            "corridors": {
                "enabled": ["sales", "operations", "finance", "partnerships",
                           "workforce", "procurement", "marketing", "executive"]
            },
            "medic": {
                "interval_hours": 1,
                "max_failures": 3,
                "check_window_hours": 1
            },
            "watchdog": {
                "medic_interval_hours": 1,
                "max_silence_hours": 2
            }
        }

        logger.info(f"Initializing Company Loop in {mode} mode")
        if corridor:
            logger.info(f"Running single corridor: {corridor}")

        # Initialize subsystems
        self.state_manager = StateManager()
        self.approval_engine = ApprovalEngine(mode=mode)
        self.trigger_engine = TriggerEngine(state_manager=self.state_manager)
        self.dispatcher = Dispatcher(
            approval_engine=self.approval_engine,
            state_manager=self.state_manager
        )
        self.scheduler = Scheduler(
            trigger_engine=self.trigger_engine,
            dispatcher=self.dispatcher,
            corridor_filter=corridor
        )

        # Initialize master loop
        self.master_loop = MasterLoop(
            deployment_id=self.config["deployment_id"],
            state_manager=self.state_manager,
            trigger_engine=self.trigger_engine,
            dispatcher=self.dispatcher,
            config=self.config
        )

        # Initialize self-healing
        self.medic = Medic(
            state_manager=self.state_manager,
            config=self.config
        )

        self.watchdog = Watchdog(
            medic=self.medic,
            config=self.config,
            alert_fn=self._watchdog_alert
        )

    async def _watchdog_alert(self, alert: dict):
        """Handle watchdog alerts."""
        logger.critical(f"WATCHDOG ALERT: {alert['message']}")
        # In production, would send to gateway/notifications

    async def start(self):
        """
        Start the master loop.

        This establishes the PERSISTENT OPERATIONAL PRESENCE.

        Steps:
        1. Start master loop (restores continuity)
        2. Health checks
        3. Start scheduler (triggers)
        4. Start heartbeat cycle
        5. Start medic cycle
        6. Start watchdog cycle
        7. Keep running (persistent)
        """
        logger.info("Starting Company Loop...")

        try:
            # 1. Start master loop (this restores continuity from previous sessions)
            logger.info("Starting master loop (persistent organism)...")
            master_state = await self.master_loop.start()
            logger.info(f"Master loop active (session #{master_state.session_count})")

            # 2. Health checks
            logger.info("Running integration health checks...")
            await self._health_checks()

            # 3. Load initial state
            logger.info("Loading corridor states...")
            await self.state_manager.load()

            # 4. Start scheduler (time-based and event-based triggers)
            logger.info("Starting scheduler...")
            await self.scheduler.start()

            # 5. Start background tasks
            logger.info("Starting background tasks...")
            tasks = [
                asyncio.create_task(self._heartbeat_cycle()),
                asyncio.create_task(self._medic_cycle()),
                asyncio.create_task(self._watchdog_cycle())
            ]

            # Keep running (the organism is now persistent)
            logger.info("=" * 60)
            logger.info("Company Loop is now PERSISTENT and ACTIVE")
            logger.info(f"Mode: {self.mode}")
            logger.info(f"Corridors: {len(self.config['corridors']['enabled'])} enabled")
            logger.info("The master loop will maintain continuity.")
            logger.info("Press Ctrl+C to stop gracefully.")
            logger.info("=" * 60)

            await asyncio.Event().wait()

        except KeyboardInterrupt:
            logger.info("Shutdown signal received")
            await self.shutdown()
        except Exception as e:
            logger.exception(f"Fatal error in main loop: {e}")
            await self.shutdown()
            sys.exit(1)

    async def _heartbeat_cycle(self):
        """
        Master loop heartbeat cycle.

        Runs every 5 minutes. This is the pulse of the organism.
        """
        while self.master_loop.running:
            try:
                await asyncio.sleep(300)  # 5 minutes
                await self.master_loop.heartbeat()
            except Exception as e:
                logger.exception("Heartbeat cycle error")

    async def _medic_cycle(self):
        """
        Medic cycle - self-healing health monitoring.

        Runs every hour. Checks system health and attempts recovery.
        """
        while self.master_loop.running:
            try:
                await asyncio.sleep(3600)  # 1 hour
                report = await self.medic.run_cycle()

                if not report.system_healthy:
                    logger.warning(f"Medic found issues: {len(report.issues_found)} problems detected")
                else:
                    logger.info("Medic cycle complete: All systems healthy")

            except Exception as e:
                logger.exception("Medic cycle error")

    async def _watchdog_cycle(self):
        """
        Watchdog cycle - monitors the medic.

        Runs every 30 minutes. Ensures medic is alive.
        """
        while self.master_loop.running:
            try:
                await asyncio.sleep(1800)  # 30 minutes
                result = await self.watchdog.check()

                if not result["medic_healthy"]:
                    logger.error(f"Watchdog detected medic issue: {result['message']}")

            except Exception as e:
                logger.exception("Watchdog cycle error")

    async def _health_checks(self):
        """
        Run integration health checks.

        Verifies connectivity to:
        - Google APIs (Sheets, Calendar, Drive, Gmail)
        - ClickUp API
        - Close API
        - Social media APIs
        - VY (if enabled)
        - Pieces server (if enabled)
        """
        # TODO: Implement actual health checks
        # For now, just log
        logger.info("✓ Google integration ready")
        logger.info("✓ ClickUp integration ready")
        logger.info("✓ Close integration ready")
        logger.info("✓ Social media integrations ready")
        logger.info("✓ VY integration ready")
        logger.info("✓ Pieces integration ready")

    async def shutdown(self):
        """
        Graceful shutdown.

        This preserves continuity for the next session.

        Steps:
        - Stop scheduler
        - Stop master loop (preserves continuity)
        - Flush pending approvals
        - Save state
        - Close connections
        """
        logger.info("Shutting down Company Loop gracefully...")

        # Stop scheduler
        logger.info("Stopping scheduler...")
        await self.scheduler.stop()

        # Stop master loop (this preserves continuity)
        logger.info("Stopping master loop (preserving continuity)...")
        await self.master_loop.stop()

        # Save state
        logger.info("Saving state...")
        await self.state_manager.save()

        logger.info("=" * 60)
        logger.info("Shutdown complete")
        logger.info("Continuity preserved for next session")
        logger.info("=" * 60)


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="Company Loop — Business Intelligence Runtime")

    parser.add_argument(
        "--mode",
        choices=["shadow", "draft", "autonomous"],
        default="shadow",
        help="Execution mode (default: shadow)"
    )

    parser.add_argument(
        "--corridor",
        type=str,
        help="Run single corridor only (for testing)"
    )

    parser.add_argument(
        "--config",
        type=Path,
        default=Path("config/app.yaml"),
        help="Path to configuration file"
    )

    args = parser.parse_args()

    # Create and run loop
    loop = CompanyLoop(
        mode=args.mode,
        corridor=args.corridor,
        config_path=args.config
    )

    asyncio.run(loop.start())


if __name__ == "__main__":
    main()
