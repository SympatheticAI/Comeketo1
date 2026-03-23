"""
Scheduler — Time-based and Event-based Trigger Coordination

Responsibilities:
- Manage time-based sweeps (every 5 min, hourly, daily, weekly)
- Monitor for event-based triggers (new lead, event approaching, etc.)
- Dispatch trigger evaluations to corridor agents
- Coordinate concurrent corridor execution
"""

import asyncio
from typing import Optional
from loguru import logger


class Scheduler:
    """
    Coordinates trigger evaluation and corridor execution.

    Time-based sweeps:
    - Every 5 minutes (realtime monitoring)
    - Hourly (medium-term monitoring)
    - Daily (end-of-day summaries, next-day prep)
    - Weekly (summaries, trend analysis)

    Event-based triggers:
    - Integration webhooks (ClickUp, Close, etc.)
    - File system watchers (Google Sheets changes)
    - State change detection
    """

    def __init__(self, trigger_engine, dispatcher, corridor_filter: Optional[str] = None):
        """
        Initialize scheduler.

        Args:
            trigger_engine: TriggerEngine instance for evaluation
            dispatcher: Dispatcher for routing work to corridors
            corridor_filter: Optional single corridor to run
        """
        self.trigger_engine = trigger_engine
        self.dispatcher = dispatcher
        self.corridor_filter = corridor_filter
        self.running = False
        self.tasks = []

    async def start(self):
        """
        Start all scheduled tasks.

        Launches:
        - Realtime sweep task (every 5 minutes)
        - Hourly sweep task
        - Daily sweep task
        - Weekly sweep task
        - Event listener tasks
        """
        self.running = True
        logger.info("Scheduler starting...")

        # Launch sweep tasks
        self.tasks.append(asyncio.create_task(self._realtime_sweep()))
        self.tasks.append(asyncio.create_task(self._hourly_sweep()))
        self.tasks.append(asyncio.create_task(self._daily_sweep()))
        self.tasks.append(asyncio.create_task(self._weekly_sweep()))

        # TODO: Launch event listener tasks
        # self.tasks.append(asyncio.create_task(self._webhook_listener()))

        logger.info(f"Scheduler running with {len(self.tasks)} tasks")

    async def stop(self):
        """Stop all scheduled tasks."""
        self.running = False
        logger.info("Stopping scheduler...")

        for task in self.tasks:
            task.cancel()

        await asyncio.gather(*self.tasks, return_exceptions=True)
        logger.info("Scheduler stopped")

    async def _realtime_sweep(self):
        """
        Realtime sweep — every 5 minutes.

        Monitors:
        - New leads in Close
        - Stale lead detection
        - Event proximity alerts
        - Payment due alerts
        - Urgent exceptions
        """
        while self.running:
            try:
                logger.debug("Running realtime sweep")
                await self.trigger_engine.evaluate_realtime_triggers()
                await asyncio.sleep(300)  # 5 minutes
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.exception(f"Error in realtime sweep: {e}")
                await asyncio.sleep(300)

    async def _hourly_sweep(self):
        """
        Hourly sweep.

        Monitors:
        - Partner relationship drift
        - Staffing conflicts
        - Shopping list generation
        - Social media engagement
        """
        while self.running:
            try:
                logger.debug("Running hourly sweep")
                await self.trigger_engine.evaluate_hourly_triggers()
                await asyncio.sleep(3600)  # 1 hour
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.exception(f"Error in hourly sweep: {e}")
                await asyncio.sleep(3600)

    async def _daily_sweep(self):
        """
        Daily sweep.

        Generates:
        - Executive daily brief
        - Tomorrow's event readiness summary
        - Finance update
        - Team task summaries
        """
        while self.running:
            try:
                logger.debug("Running daily sweep")
                await self.trigger_engine.evaluate_daily_triggers()
                await asyncio.sleep(86400)  # 24 hours
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.exception(f"Error in daily sweep: {e}")
                await asyncio.sleep(86400)

    async def _weekly_sweep(self):
        """
        Weekly sweep.

        Generates:
        - Executive weekly summary
        - Trend analysis
        - Partner performance review
        - Labor hour reports
        - Shadow mode promotion review
        """
        while self.running:
            try:
                logger.debug("Running weekly sweep")
                await self.trigger_engine.evaluate_weekly_triggers()
                await asyncio.sleep(604800)  # 7 days
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.exception(f"Error in weekly sweep: {e}")
                await asyncio.sleep(604800)
