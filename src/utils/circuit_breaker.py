"""
Circuit Breaker Pattern for Third-Party API Integrations
Purpose: Prevent application crashes when external APIs experience downtime.
"""

import time
import logging
from enum import Enum
from typing import Callable, Any

logger = logging.getLogger(__name__)


class CircuitState(Enum):
    CLOSED = "CLOSED"  # Normal operation
    OPEN = "OPEN"      # Failing, stop calling
    HALF_OPEN = "HALF_OPEN"  # Testing recovery


class CircuitBreaker:
    """
    A simple circuit breaker to protect the application from external API failures.
    """

    def __init__(self, failure_threshold: int = 3, recovery_timeout: int = 30):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED

    def call(self, func: Callable, *args, **kwargs) -> Any:
        """
        Calls the external function, but checks the circuit state first.
        """
        if self.state == CircuitState.OPEN:
            # Check if the cooldown period has passed
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = CircuitState.HALF_OPEN
                logger.info("Circuit Breaker transitioning to HALF_OPEN state.")
            else:
                raise Exception("Circuit Breaker is OPEN. External API is temporarily unavailable.")

        try:
            result = func(*args, **kwargs)
            # Success: Reset the circuit
            self._on_success()
            return result
        except Exception as e:
            # Failure: Increment counter and check threshold
            self._on_failure()
            raise e

    def _on_success(self):
        """Resets the circuit to CLOSED state after a successful call."""
        self.failure_count = 0
        self.state = CircuitState.CLOSED
        logger.info("Circuit Breaker reset to CLOSED state.")

    def _on_failure(self):
        """Increments the failure count and transitions to OPEN if threshold is reached."""
        self.failure_count += 1
        self.last_failure_time = time.time()
        logger.warning(f"Circuit Breaker failure count: {self.failure_count}.")

        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
            logger.error("Circuit Breaker transitioned to OPEN state. Blocking external calls.")


# Global instances (for different APIs)
ai_breaker = CircuitBreaker(failure_threshold=3, recovery_timeout=30)
weather_breaker = CircuitBreaker(failure_threshold=3, recovery_timeout=30)