"""
Watchdog — Medic Monitor

The watchdog is the simplified supervisory process that monitors
whether the medic itself is running.

It exists because a self-healing system still requires a simpler
layer capable of noticing if self-healing itself has stalled.

Design principle: MINIMALITY

The watchdog should do LESS than the medic, depend on FEWER moving parts,
and remain simple enough to trust precisely because it is less ambitious.

The watchdog is not designed to diagnose every subsystem or run broad
recovery routines. When a system attempts to make the watchdog as
intelligent as the medic, it destroys the reason the watchdog exists.
"""

import asyncio
import logging
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from pathlib import Path


logger = logging.getLogger(__name__)


class Watchdog:
    """
    Simplified supervisory process for the medic.

    The watchdog has ONE job: Verify the medic ran within its expected window.

    If the medic hasn't run, the watchdog alerts directly.
    """

    def __init__(
        self,
        medic: Any,  # Medic instance
        config: Dict[str, Any],
        alert_fn: Optional[callable] = None
    ):
        self.medic = medic
        self.config = config
        self.alert_fn = alert_fn  # Function to call for alerts

        # Configuration
        self.expected_medic_interval_hours = config.get("watchdog", {}).get("medic_interval_hours", 1)
        self.max_medic_silence_hours = config.get("watchdog", {}).get("max_silence_hours", 2)

        # State
        self.last_check: Optional[datetime] = None
        self.alerts_sent = 0

        logger.info(f"Watchdog initialized (expecting medic every {self.expected_medic_interval_hours}h)")

    async def check(self) -> Dict[str, Any]:
        """
        Check if medic is alive.

        This is the watchdog's only function.
        """
        now = datetime.utcnow()
        self.last_check = now

        result = {
            "checked_at": now.isoformat(),
            "medic_healthy": True,
            "medic_last_run": None,
            "hours_since_medic": None,
            "alert_sent": False,
            "status": "ok"
        }

        try:
            # Check when medic last ran
            medic_last_run = self.medic.last_run

            if medic_last_run is None:
                # Medic has NEVER run
                result["medic_healthy"] = False
                result["status"] = "critical"
                result["message"] = "Medic has never run"

                await self._send_alert(
                    severity="critical",
                    message="Watchdog: Medic has never run"
                )
                result["alert_sent"] = True

            else:
                # Calculate time since last medic run
                hours_since = (now - medic_last_run).total_seconds() / 3600
                result["medic_last_run"] = medic_last_run.isoformat()
                result["hours_since_medic"] = round(hours_since, 2)

                if hours_since > self.max_medic_silence_hours:
                    # Medic is silent too long
                    result["medic_healthy"] = False
                    result["status"] = "critical"
                    result["message"] = f"Medic silent for {hours_since:.1f} hours (max: {self.max_medic_silence_hours}h)"

                    await self._send_alert(
                        severity="critical",
                        message=f"Watchdog: Medic silent for {hours_since:.1f} hours"
                    )
                    result["alert_sent"] = True

                elif hours_since > self.expected_medic_interval_hours:
                    # Medic is late but not critical yet
                    result["medic_healthy"] = False
                    result["status"] = "warning"
                    result["message"] = f"Medic late ({hours_since:.1f} hours since last run)"

                else:
                    # Medic is on schedule
                    result["status"] = "ok"
                    result["message"] = f"Medic healthy ({hours_since:.1f}h since last run)"

        except Exception as e:
            logger.exception("Watchdog check encountered error")
            result["medic_healthy"] = False
            result["status"] = "error"
            result["message"] = f"Watchdog check error: {str(e)}"

            await self._send_alert(
                severity="error",
                message=f"Watchdog encountered error: {str(e)}"
            )
            result["alert_sent"] = True

        # Log result
        if result["status"] == "ok":
            logger.debug(f"Watchdog: {result['message']}")
        elif result["status"] == "warning":
            logger.warning(f"Watchdog: {result['message']}")
        else:
            logger.error(f"Watchdog: {result['message']}")

        return result

    async def _send_alert(self, severity: str, message: str):
        """Send alert about medic health."""
        self.alerts_sent += 1

        alert = {
            "timestamp": datetime.utcnow().isoformat(),
            "source": "watchdog",
            "severity": severity,
            "message": message
        }

        # Call alert function if provided
        if self.alert_fn:
            try:
                await self.alert_fn(alert)
            except Exception as e:
                logger.exception(f"Failed to send watchdog alert: {str(e)}")

        # Also log
        logger.error(f"WATCHDOG ALERT [{severity}]: {message}")

    async def verify_heartbeat_file(self, heartbeat_path: str) -> bool:
        """
        Verify a heartbeat file exists and is recent.

        This is a simple file-based check that can work even if
        other systems are degraded.
        """
        try:
            path = Path(heartbeat_path)

            if not path.exists():
                logger.warning(f"Heartbeat file not found: {heartbeat_path}")
                return False

            # Check file modification time
            mtime = datetime.fromtimestamp(path.stat().st_mtime)
            age_hours = (datetime.utcnow() - mtime).total_seconds() / 3600

            if age_hours > self.max_medic_silence_hours:
                logger.warning(f"Heartbeat file stale: {heartbeat_path} ({age_hours:.1f}h old)")
                return False

            logger.debug(f"Heartbeat file fresh: {heartbeat_path} ({age_hours:.1f}h old)")
            return True

        except Exception as e:
            logger.exception(f"Error checking heartbeat file: {str(e)}")
            return False


# Standalone watchdog check function
async def run_watchdog_check(
    medic_last_run_file: str,
    max_silence_hours: float = 2.0,
    alert_fn: Optional[callable] = None
) -> Dict[str, Any]:
    """
    Standalone watchdog check that can run independently.

    This reads a simple timestamp file and alerts if it's too old.

    Args:
        medic_last_run_file: Path to file containing medic's last run timestamp
        max_silence_hours: Maximum hours without medic before alerting
        alert_fn: Optional function to call for alerts

    Returns:
        Dict with check results
    """
    now = datetime.utcnow()

    result = {
        "checked_at": now.isoformat(),
        "medic_healthy": True,
        "medic_last_run": None,
        "hours_since_medic": None,
        "alert_sent": False,
        "status": "ok"
    }

    try:
        path = Path(medic_last_run_file)

        if not path.exists():
            # File doesn't exist - medic has never run
            result["medic_healthy"] = False
            result["status"] = "critical"
            result["message"] = "Medic timestamp file not found"

            if alert_fn:
                await alert_fn({
                    "severity": "critical",
                    "message": "Standalone Watchdog: Medic timestamp file not found"
                })
                result["alert_sent"] = True

        else:
            # Read last run timestamp
            with open(path, 'r') as f:
                last_run_str = f.read().strip()
                last_run = datetime.fromisoformat(last_run_str)

            hours_since = (now - last_run).total_seconds() / 3600
            result["medic_last_run"] = last_run.isoformat()
            result["hours_since_medic"] = round(hours_since, 2)

            if hours_since > max_silence_hours:
                # Medic is silent too long
                result["medic_healthy"] = False
                result["status"] = "critical"
                result["message"] = f"Medic silent for {hours_since:.1f} hours"

                if alert_fn:
                    await alert_fn({
                        "severity": "critical",
                        "message": f"Standalone Watchdog: Medic silent for {hours_since:.1f} hours"
                    })
                    result["alert_sent"] = True

            else:
                # Medic is healthy
                result["status"] = "ok"
                result["message"] = f"Medic healthy ({hours_since:.1f}h since last run)"

    except Exception as e:
        logger.exception("Standalone watchdog check error")
        result["medic_healthy"] = False
        result["status"] = "error"
        result["message"] = f"Error: {str(e)}"

        if alert_fn:
            await alert_fn({
                "severity": "error",
                "message": f"Standalone Watchdog error: {str(e)}"
            })
            result["alert_sent"] = True

    return result
