## Versão 1 - 2026-05-05 15:42:11
**Prompt do Usuário:**
Gere um diagrama Python (biblioteca diagrams) para a seguinte arquitetura de solução:

Cloud: GCP
Padrão arquitetural: Lakehouse
Nível de detalhe: técnico
Descriçao: Gere um diagrama de arquitetura em Google Cloud Platform (GCP) para o projeto SIGRM - simplificado.

Camadas:

1. Criar uma camada On Premises representando múltiplas interfaces e sistemas internos/externos
2. Criar uma camada de ingestão com Dataflow e armazenamento no Big Query e/ou Spanner (ligar os 2 serviços)
3. Criar uma camada de processamento no Big Query com Dataform, Dataproc Spark em Python e Cloud Run em Java orquestrado pelo Composer
4. Criar uma camada base com Governança em Dataprep (ponha descrição Dataplex), IAM para autorização e Cloud Build com CI/CD
5. Criar uma camada de consumo com Endpoint em Cloud Run e diagrams.gcp.analytics.Looker, opcional Vertex AI

---
