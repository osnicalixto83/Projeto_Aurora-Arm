"""
Supervisor de segurança discreto simplificado.
Estados: RUN, STOPPING, SAFE_STOP, WAIT_REARM.
O modelo é uma abstração para verificação didática, não um controlador certificado.
"""
from enum import Enum, auto

class State(Enum):
    RUN = auto()
    STOPPING = auto()
    SAFE_STOP = auto()
    WAIT_REARM = auto()

class Supervisor:
    def __init__(self):
        self.state = State.RUN
        self.torque_command = 1.0

    def step(self, hand_detected=False, torque_zero_feedback=True,
             hand_clear=False, explicit_rearm=False):
        if self.state == State.RUN and hand_detected:
            self.state = State.STOPPING
        elif self.state == State.STOPPING and torque_zero_feedback:
            self.state = State.WAIT_REARM
        elif self.state == State.WAIT_REARM and hand_clear and explicit_rearm:
            self.state = State.RUN
        self.torque_command = 0.0 if self.state in (State.STOPPING, State.SAFE_STOP, State.WAIT_REARM) else 1.0
        # SAFE_STOP reservado para parada latched por falha de diagnóstico.
        return self.state, self.torque_command

def worst_case_command_latency_ms(sensor_delay_ms=20.0, missed_cycles=1,
                                  sample_period_ms=2.0, execution_budget_ms=0.2):
    """Cota conservadora para comando de torque zero, não para torque físico medido."""
    return sensor_delay_ms + missed_cycles*sample_period_ms + execution_budget_ms

def exhaustive_delay_sweep():
    """Varre atraso do sensor [0,20] ms e jitter [0,2] ms em passos de 0,1 ms."""
    worst = (-1.0, None, None)
    violations = []
    vals = [round(k*0.1, 10) for k in range(201)]
    jitters = [round(k*0.1, 10) for k in range(21)]
    for sensor in vals:
        for jitter in jitters:
            total = sensor + jitter + 0.2
            if total > worst[0]:
                worst = (total, sensor, jitter)
            if total > 100.0:
                violations.append((sensor, jitter, total))
    return worst, violations
