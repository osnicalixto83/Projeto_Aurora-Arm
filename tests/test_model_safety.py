import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import numpy as np
from model import A, B, C_POS, C_SPEED, controllability_matrix, observability_matrix, derivative
from safety_supervisor import Supervisor, State, exhaustive_delay_sweep, worst_case_command_latency_ms

def test_model_shapes_and_finite():
    assert A.shape == (3,3)
    assert B.shape == (3,1)
    assert np.all(np.isfinite(derivative([0,0,0], 0)))

def test_controllability_observability():
    assert np.linalg.matrix_rank(controllability_matrix()) == 3
    assert np.linalg.matrix_rank(observability_matrix()) == 3

def test_safe_stop_priority():
    s = Supervisor()
    state, torque = s.step(hand_detected=True)
    assert state == State.STOPPING
    assert torque == 0.0

def test_no_automatic_restart():
    s = Supervisor()
    s.step(hand_detected=True)
    s.step(torque_zero_feedback=True)
    state, torque = s.step(hand_clear=True, explicit_rearm=False)
    assert state == State.WAIT_REARM
    assert torque == 0.0

def test_rearm_requires_clear_and_explicit_action():
    s = Supervisor()
    s.step(hand_detected=True)
    s.step(torque_zero_feedback=True)
    state, torque = s.step(hand_clear=True, explicit_rearm=True)
    assert state == State.RUN
    assert torque == 1.0

def test_deadline_sweep():
    worst, violations = exhaustive_delay_sweep()
    assert worst[0] <= 100.0
    assert len(violations) == 0
    assert abs(worst_case_command_latency_ms() - 22.2) < 1e-9
