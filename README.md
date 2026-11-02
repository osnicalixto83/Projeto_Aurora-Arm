# AuroraArm — Operação Linha Viva

## Conteúdo
- `src/model.py`: modelo contínuo de 3 estados da junta (posição, velocidade, corrente).
- `src/safety_supervisor.py`: supervisor discreto didático e varredura do prazo.
- `src/generate_c.py`: gerador que escreve `src/controller_generated.c`.
- `tests/test_model_safety.py`: testes de unidade.
- `docs/rastreabilidade.md`: matriz inicial de requisitos.

## Executar
Requer Python 3.10+ e NumPy. Para testes, instalar pytest:
```bash
python -m pip install numpy pytest
python src/generate_c.py
python -m pytest -q
```

## Limitações técnicas importantes
1. O modelo é linearizado e usa parâmetros informados no enunciado; validar com dados reais de bancada.
2. O controlador C tem ganhos ilustrativos, não sintonizados nem comprovados para overshoot/acomodação.
3. O limite de corrente precisa ser garantido por driver/hardware e monitorado; limitar tensão em software não basta.
4. A varredura de prazo demonstra uma cota para o comando de torque zero sob hipóteses explícitas, não prova que o torque físico medido zera no mesmo instante.
5. O supervisor é uma abstração didática. Não é certificação de segurança nem substitui scanner, STO, freio, validação de risco, HIL e avaliação independente.
6. O código C é gerado pelo script, mas um fluxo industrial de geração certificável requer ferramenta qualificada, versão congelada, compilador/configuração controlados e comparação SIL/HIL.
# Projeto_Aurora-Arm
