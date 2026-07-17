# Mini-Projeto 1 — Sistema de Regras de Produção com experta

Disciplina: Sistemas Baseados em Conhecimento (SBC), edição 2026.2.
Bloco 1 — Regras Explicáveis. Entrega associada à Aula 3.

## Objetivo

Construir um sistema especialista baseado em regras de produção do tipo
SE-ENTÃO, usando a biblioteca experta em Python. O domínio é livre, à escolha da
equipe, desde que permita raciocínio por encadeamento. O projeto consolida a
separação entre a base de conhecimento (as regras) e o motor de inferência (o
mecanismo que dispara as regras), tese central do Bloco 1.

## Prazo de entrega

O Mini-Projeto 1 deve ser entregue no dia 25/04/2026, até as 23h59, via GitHub
Classroom. Entregas com atraso sofrem penalidade de 1,0 ponto por dia, até o
limite de 3 dias, após o qual a nota é zerada.

## Requisitos mínimos obrigatórios

O sistema entregue deve conter, no mínimo:

- 10 regras de produção declaradas com o decorador @Rule da experta.
- 3 fatos iniciais distintos declarados na classe de fatos (Fact).
- Uso explícito de encadeamento progressivo (forward chaining), partindo dos
  fatos iniciais até as conclusões.
- Ao menos 2 regras que dependam de conclusões de outras regras, demonstrando
  encadeamento em mais de um nível.
- Uma explicação, impressa ao final, de qual sequência de regras foi disparada
  para chegar a cada conclusão (rastreabilidade).

## Entregáveis

O repositório no GitHub Classroom deve conter:

- Um script `sistema.py` com a KnowledgeEngine, os fatos e as 10 regras.
- Um `README.md` descrevendo o domínio, as regras em linguagem natural e as
  instruções de execução.
- Ao menos 3 cenários de teste, cada um com um conjunto de fatos iniciais e a
  saída esperada.

## Peso na avaliação

O Mini-Projeto 1 compõe, junto com os Mini-Projetos 2 e 3, a fatia de 30% da
nota final reservada aos mini-projetos.
