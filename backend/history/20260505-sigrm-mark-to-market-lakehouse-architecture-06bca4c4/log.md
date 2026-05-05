## Versão 1 - 2026-05-05 14:24:46
**Prompt do Usuário:**
Gere um diagrama Python (biblioteca diagrams) para a seguinte arquitetura de solução:

Cloud: GCP
Padrão arquitetural: Lakehouse
Nível de detalhe: técnico
Descriçao: Gere um diagrama de arquitetura em Google Cloud Platform (GCP) para o projeto SIGRM

Contexto:
-  Processamento de marcação a mercado de contratos financeiros.
- Apache Spark no GCP.
- Dataflow (como alternativa de pipeline).
- BigQuery (armazenamento analítico, resultados e intermediários).
- BigQuery UDFs (quando aplicável).

Orientações visuais:
- Mostrar o fluxo: ingestão de dados → cálculo de curvas → persistência → cálculo de fluxos → resultados.
- Evidenciar a separação entre camadas de processamento e dados.
- Indicar pontos de persistência para auditoria e reprocessamento.
- Representar a arquitetura de forma clara, modular e escalável.

O diagrama deve ser no padrão visual oficial do GCP.
``
- Necessidade de cálculos diários e múltiplos cenários.
- Regras de negócio complexas, com decisões condicionais e não totalmente vetorizáveis.
- Forte exigência de auditabilidade, rastreabilidade e reprocessamento.
- Persistência de resultados intermediários (ex.: curvas).

Requisitos arquiteturais:
- Processamento distribuído e escalável.
- Separação clara entre cálculo de curvas e cálculo de fluxos.
- Possibilidade de execução em Python, Java ou Spark.
- Persistência de dados intermediários e finais.
- Arquitetura padronizada e governável.

Serviços GCP a serem representados no diagrama:
- Cloud Run (para execução de serviços containerizados).


---
