# Resumo da Aula 7 — Knowledge Graphs e SPARQL

Disciplina: Sistemas Baseados em Conhecimento (SBC), edição 2026.2.
Bloco 3 — Knowledge Graphs.

## O que foi visto

A Aula 7 apresentou os grafos de conhecimento como a evolução moderna das redes
semânticas clássicas. O conhecimento é representado por triplas no formato
sujeito, predicado, objeto, e o conjunto de triplas forma um grafo dirigido e
rotulado.

## RDF, RDFS e OWL

O modelo RDF define a estrutura das triplas. O RDFS acrescenta vocabulário para
hierarquias de classes e propriedades, com rdfs:subClassOf e rdfs:subPropertyOf.
O OWL adiciona construções lógicas mais expressivas, como owl:inverseOf,
owl:TransitiveProperty, owl:disjointWith e restrições de cardinalidade, que
permitem inferência automática sobre o grafo.

## SPARQL

A consulta a grafos RDF é feita com SPARQL, uma linguagem declarativa baseada em
casamento de padrões de triplas. A cláusula WHERE especifica um padrão de grafo,
e o motor de consulta retorna todas as combinações de valores que satisfazem o
padrão. Recursos como FILTER, OPTIONAL, UNION e agregações com GROUP BY tornam a
linguagem expressiva o suficiente para perguntas complexas.

## Grafos corporativos

Foram discutidos grafos de conhecimento em produção. A Airbnb usa um grafo para
conectar destinos, experiências e anfitriões. O LinkedIn mantém um grande grafo
econômico ligando pessoas, empresas, competências e vagas. A Netflix modela
relações entre títulos, gêneros e preferências. Esses grafos mostram que a
representação simbólica explícita continua central em sistemas de larga escala.

## Infraestrutura da disciplina

A demonstração da aula usou o Memgraph rodando em Docker, com o Memgraph Lab para
visualização. O domínio de exemplo foi a banda Queen, modelada como um grafo com
integrantes, álbuns e músicas, consultado com Cypher. Essa mesma infraestrutura
será reaproveitada na aula sobre GraphRAG, quando o grafo passará a servir de
fonte de recuperação para um agente baseado em LLM.

## Ponte para o Bloco 4

O fechamento da aula destacou que o grafo de conhecimento é uma base de
conhecimento explícita e auditável, exatamente o tipo de estrutura que os
agentes LLM do Bloco 4 precisam para responder com rastreabilidade. A separação
entre a base de conhecimento e o motor de consulta antecipa a separação entre o
corpus e o LLM que veremos em RAG.
