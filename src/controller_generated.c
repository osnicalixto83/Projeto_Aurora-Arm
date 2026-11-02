/* AUTO-GERADO por generate_c.py — não editar manualmente.
 * Projeto: AuroraArm / Operação Linha Viva
 * Requisitos: REQ-CTRL-AA-004 (limites de atuador); REQ-SAFE-AA-001 (interface de parada)
 * Modelo de referência: src/model.py
 * Parâmetros Kp/Kd ilustrativos; aprovação depende de sintonia e ensaios.
 */
#include <math.h>
#include <stdint.h>

#define TS_SEC 0.002f
#define V_MAX 48.0f
#define I_MAX 8.0f
#define KP 12.0f
#define KD 0.8f

typedef struct {
    float integral;
    float previous_error;
} ControllerState;

static float clampf(float x, float lo, float hi) {
    if (x > hi) return hi;
    if (x < lo) return lo;
    return x;
}

/* Entrada em rad e rad/s; saída em V. Torque zero de segurança tem prioridade. */
float aurora_controller_step(float theta_ref, float theta, float omega,
                             int safety_stop, ControllerState *st) {
    float e = theta_ref - theta;
    if (safety_stop) {
        st->integral = 0.0f;
        st->previous_error = e;
        return 0.0f;
    }
    float u_unsat = KP * e - KD * omega;
    float u = clampf(u_unsat, -V_MAX, V_MAX);
    /* Limitador explícito; corrente deve ser limitada também no driver/hardware. */
    st->previous_error = e;
    return u;
}
