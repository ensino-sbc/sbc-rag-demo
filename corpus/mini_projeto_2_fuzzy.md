# Mini-Projeto 2 — Controlador Fuzzy com scikit-fuzzy

Disciplina: Sistemas Baseados em Conhecimento (SBC), edição 2026.2.
Bloco 2 — Raciocínio sob Incerteza. Entrega associada à Aula 5.

## Objetivo

Projetar e implementar um controlador de lógica fuzzy pelo método de Mamdani,
usando a biblioteca scikit-fuzzy em Python. O controlador deve modelar um
problema real de decisão sob incerteza, com variáveis linguísticas e regras
fuzzy. O projeto aprofunda o raciocínio aproximado, mostrando como capturar
conhecimento especialista impreciso em um sistema executável.

## Prazo de entrega

O Mini-Projeto 2 deve ser entregue no dia 30/05/2026, até as 23h59, via GitHub
Classroom. A entrega inclui um vídeo curto, de no máximo 5 minutos, demonstrando
o controlador em funcionamento e explicando as escolhas de projeto.

## Requisitos mínimos obrigatórios

O controlador entregue deve conter, no mínimo:

- Exatamente 2 variáveis de entrada (antecedentes) e 1 variável de saída
  (consequente).
- Ao menos 3 conjuntos fuzzy (funções de pertinência) por variável.
- Um mínimo de 6 regras fuzzy cobrindo as combinações relevantes das entradas.
- Inferência de Mamdani completa: fuzzificação, agregação das regras e
  defuzzificação pelo método do centroide.
- Ao menos 3 pontos de teste com os valores de entrada e a saída defuzzificada
  correspondente, discutidos no relatório.

## Entregáveis

- Um script `controlador.py` com a definição das variáveis, dos conjuntos fuzzy,
  das regras e do sistema de controle.
- Um `README.md` com a descrição do problema, as variáveis linguísticas e as
  instruções de execução.
- O vídeo de demonstração de até 5 minutos, com o link no README.

## Peso na avaliação

O Mini-Projeto 2 compõe, junto com os Mini-Projetos 1 e 3, a fatia de 30% da
nota final reservada aos mini-projetos.
