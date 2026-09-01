"""
Comprehensive Unit Tests for Circuit Breaker Pattern
Tests state transitions, failure handling, and recovery.
"""

import time
import pytest
from src.utils.circuit_breaker import CircuitBreaker, CircuitState


class TestCircuitBreakerClosedState:
    def test_initial_state_is_closed(self):
        """Should start in the CLOSED state."""
        cb = CircuitBreaker()
        assert cb.state == CircuitState.CLOSED

    def test_successful_call_resets_failures(self):
        """Should reset the failure count after a success."""
        cb = CircuitBreaker()
        cb.call(lambda: 1 + 1)
        assert cb.failure_count == 0

    def test_call_successfully_executes(self):
        """Should execute the function normally when closed."""
        cb = CircuitBreaker()
        result = cb.call(lambda: 10 * 2)
        assert result == 20


class TestCircuitBreakerOpenState:
    def test_transitions_to_open_after_threshold(self):
        """Should transition to OPEN after 3 failures."""
        cb = CircuitBreaker(failure_threshold=3)
        for _ in range(3):
            with pytest.raises(Exception):
                cb.call(lambda: 1 / 0)
        assert cb.state == CircuitState.OPEN

    def test_open_state_rejects_calls(self):
        """Should raise an error when in the OPEN state."""
        cb = CircuitBreaker(failure_threshold=3)
        for _ in range(3):
            with pytest.raises(Exception):
                cb.call(lambda: 1 / 0)
        with pytest.raises(Exception, match="OPEN"):
            cb.call(lambda: 1 + 1)

    def test_failure_count_increments(self):
        """Should increment the failure count on each failure."""
        cb = CircuitBreaker(failure_threshold=5)
        with pytest.raises(Exception):
            cb.call(lambda: 1 / 0)
        assert cb.failure_count == 1


class TestCircuitBreakerRecovery:
    def test_transitions_to_half_open_after_timeout(self):
        """Should transition to HALF_OPEN after the cooldown period."""
        cb = CircuitBreaker(failure_threshold=1, recovery_timeout=1)
        with pytest.raises(Exception):
            cb.call(lambda: 1 / 0)
        assert cb.state == CircuitState.OPEN
        time.sleep(1.2)
        # Manually trigger the check
        with pytest.raises(Exception):
            cb.call(lambda: 1 / 0)
        assert cb.state == CircuitState.HALF_OPEN

    def test_success_in_half_open_closes_circuit(self):
        """A success in HALF_OPEN should transition back to CLOSED."""
        cb = CircuitBreaker(failure_threshold=1, recovery_timeout=1)
        with pytest.raises(Exception):
            cb.call(lambda: 1 / 0)
        time.sleep(1.2)
        # Transition to HALF_OPEN
        with pytest.raises(Exception):
            cb.call(lambda: 1 / 0)
        # Call succeeds
        cb.call(lambda: 1 + 1)
        assert cb.state == CircuitState.CLOSED


class TestCircuitBreakerEdgeCases:
    def test_multiple_instances_are_isolated(self):
        """Different breakers should not affect each other."""
        cb1 = CircuitBreaker(failure_threshold=1)
        cb2 = CircuitBreaker(failure_threshold=1)
        with pytest.raises(Exception):
            cb1.call(lambda: 1 / 0)
        assert cb1.state == CircuitState.OPEN
        assert cb2.state == CircuitState.CLOSED

    def test_large_threshold(self):
        """Should handle large failure thresholds."""
        cb = CircuitBreaker(failure_threshold=100)
        for _ in range(50):
            with pytest.raises(Exception):
                cb.call(lambda: 1 / 0)
        assert cb.state == CircuitState.CLOSED