"""
AuroraArm — modelo linearizado da junta do cotovelo.
Estados x = [theta, omega, i]^T:
theta [rad], omega [rad/s], i [A]; entrada u = tensão aplicada [V].
Convenção: torque de carga tau_L positivo se opõe ao movimento.
"""
import numpy as np

R = 0.8
L = 1.2e-3
KT = 0.085
KE = 0.085
J = 4.2e-4
BVIS = 1.5e-4
VMAX = 48.0
IMAX = 8.0
TS = 0.002

A = np.array([
    [0.0, 1.0, 0.0],
    [0.0, -BVIS/J, KT/J],
    [0.0, -KE/L, -R/L],
], dtype=float)
B = np.array([[0.0], [0.0], [1.0/L]], dtype=float)
C_POS = np.array([[1.0, 0.0, 0.0]], dtype=float)
C_SPEED = np.array([[0.0, 1.0, 0.0]], dtype=float)

def derivative(x, u, tau_load=0.0):
    """Derivada contínua; tau_load é torque resistente no eixo do motor."""
    theta, omega, current = np.asarray(x, dtype=float)
    return np.array([
        omega,
        (KT*current - BVIS*omega - tau_load)/J,
        (u - R*current - KE*omega)/L,
    ], dtype=float)

def rk4_step(x, u, dt=TS, tau_load=0.0):
    """Integração RK4 de referência usada no SIL."""
    f = lambda z: derivative(z, u, tau_load)
    k1 = f(x)
    k2 = f(np.asarray(x)+0.5*dt*k1)
    k3 = f(np.asarray(x)+0.5*dt*k2)
    k4 = f(np.asarray(x)+dt*k3)
    return np.asarray(x) + (dt/6.0)*(k1+2*k2+2*k3+k4)

def controllability_matrix(A=A, B=B):
    return np.hstack([B, A@B, A@A@B])

def observability_matrix(A=A, C=C_POS):
    return np.vstack([C, C@A, C@A@A])
