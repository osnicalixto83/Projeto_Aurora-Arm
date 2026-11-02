# Matriz de rastreabilidade — AuroraArm

| Requisito | Modelo/elemento | Implementação | Teste/evidência | Estado |
|---|---|---|---|---|
| REQ-CTRL-AA-001 erro estacionário nulo para degrau | Planta 3 estados + malha de posição | `src/model.py`, controlador a completar/sintonizar | Teste de degrau, erro final dentro de tolerância declarada | Pendente de sintonia |
| REQ-CTRL-AA-002 overshoot <= 8% | Dinâmica fechada | `src/generate_c.py` gera controlador PD inicial | Varredura de degraus/cargas e medição de pico | Pendente de validação |
| REQ-CTRL-AA-003 acomodação <= 300 ms | Dinâmica fechada | Controlador e Ts=2 ms | Ensaio temporal com critério ±2% declarado | Pendente de validação |
| REQ-CTRL-AA-004 | Saturação ±48 V e limite de corrente 8 A | `controller_generated.c` + driver físico | Teste de saturação; medir corrente real | Parcial: tensão em software; corrente depende do driver |
| REQ-SAFE-AA-001 prazo <=100 ms | Supervisor + orçamento temporal | `src/safety_supervisor.py` | Varredura de atrasos; pior comando estimado 22,2 ms | Abstração passa; torque físico não provado |
| REQ-SAFE-AA-002 sem reinício automático | WAIT_REARM | `src/safety_supervisor.py` | `test_no_automatic_restart` | Teste de unidade |
| REQ-SAFE-AA-003 retomar trajetória após remoção e rearme | Estado WAIT_REARM/RUN; referência de trajetória precisa ser preservada | Extensão a implementar no integrador de trajetória | Teste de trajetória antes/depois do evento | Pendente |
| REQ-SAFE-AA-004 velocidade linear <=250 mm/s na zona | Supervisor de velocidade + geometria/raio do efetuador | Não inferível só pelo modelo de junta | Teste com encoder e cálculo v_linear = r_eff*omega_joint | Pendente de dados geométricos |
