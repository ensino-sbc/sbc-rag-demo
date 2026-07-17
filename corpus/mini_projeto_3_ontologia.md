# Mini-Projeto 3 — Ontologia em Turtle e Consultas SPARQL

Disciplina: Sistemas Baseados em Conhecimento (SBC), edição 2026.2.
Bloco 3 — Knowledge Graphs. Entrega associada à Aula 7.

## Objetivo

Modelar um domínio à escolha da equipe como uma ontologia em RDF/RDFS/OWL,
serializada em Turtle (arquivo `.ttl`), e consultá-la com `rdflib` e SPARQL.
O objetivo é consolidar a separação entre a base de conhecimento (o grafo de
triplas) e o mecanismo de consulta (o motor SPARQL), reforçando a tese da
disciplina de que o conhecimento deve ser um artefato explícito e auditável.

## Prazo de entrega

A entrega do Mini-Projeto 3 é no dia 19/07/2026, até as 23h59, via GitHub
Classroom. Entregas após essa data sofrem penalidade de 1,0 ponto por dia de
atraso, até o limite de 3 dias, após o qual a nota é zerada.

## Requisitos mínimos obrigatórios

A ontologia entregue deve conter, no mínimo:

- 8 classes declaradas (owl:Class ou rdfs:Class).
- 10 propriedades, entre owl:ObjectProperty e owl:DatatypeProperty.
- 25 indivíduos (instâncias das classes).
- 120 triplas no total no arquivo Turtle.
- 2 construções OWL além das básicas, por exemplo owl:inverseOf,
  owl:TransitiveProperty, owl:disjointWith, rdfs:subClassOf com hierarquia de
  pelo menos 3 níveis, ou restrições owl:Restriction.

## Consultas exigidas

O script de consulta deve demonstrar:

- 5 consultas usando o método g.triples() da API do rdflib, navegando o grafo
  programaticamente.
- 8 consultas em SPARQL, incluindo ao menos uma com FILTER, uma com OPTIONAL e
  uma com agregação (COUNT, GROUP BY ou similar).

## Entregáveis

O repositório no GitHub Classroom deve conter:

- O arquivo `ontologia.ttl` com o grafo de conhecimento.
- Um script `consultas.py` que carrega o `.ttl` com rdflib e executa todas as
  consultas exigidas, imprimindo os resultados.
- Um `README.md` descrevendo o domínio modelado, o significado das classes e
  propriedades principais, e instruções de execução.

## Peso na avaliação

O Mini-Projeto 3 compõe, junto com os Mini-Projetos 1, 2 e 4, a fatia de 30%
da nota final reservada aos mini-projetos.
