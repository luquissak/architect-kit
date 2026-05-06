## Versão 1 - 2026-05-06 09:10:42
**Prompt do Usuário:**
Gere um diagrama Python (biblioteca diagrams) para a seguinte arquitetura de solução:

Cloud: GCP
Padrão arquitetural: Personalizado
Nível de detalhe: técnico
Descriçao: Atue como um Arquiteto de Soluções especialista em Inteligência Artificial e MLOps. Quero refatorar o diagrama da "Plataforma MLOps - SIPML" para torná-lo aderente ao Modelo de Referência do Gartner no Google Cloud, utilizando a biblioteca `diagrams` do Python.

Siga rigidamente as diretrizes de design abaixo para garantir simetria, alinhamento e clareza corporativa:

### 📐 Diretrizes Visuais e de Alinhamento
1. DIREÇÃO: Use 'direction="LR"' (Left to Right) para orientar o fluxo em colunas cronológicas.
2. LINHAS ORTOGONAIS: Configure "splines": "ortho" no 'graph_attr' para linhas limpas em ângulos de 90°.
3. ABSTRAÇÃO DE AMBIENTES (SPOKES): Não instancie projetos duplicados ("modelagem-a", "modelagem-b"). Use abstrações unificadas e genéricas (ex: "Spoke de Modelagem", "Spoke de Inferência").
4. PADRÃO GARTNER / VERTEX AI 1:1: Utilize termos nativos (Vertex AI Pipelines, Vertex AI Feature Store, Vertex AI Endpoint, etc.).
5. ESPINHA DORSAL INVISÍVEL: Trave as colunas verticalmente usando conexões ocultas ('style="invis"') entre os componentes líderes de cada camada no final do script.

### 🏛️ Estrutura de Camadas e Clusters Lógicos

O diagrama deve ser dividido em macro-blocos organizados vertical e horizontalmente:

1. BLOCO ESQUERDO: "Fontes de Dados Externas"
   - Dividido em dois sub-clusters verticais:
     * "Dados Analíticos": Azure Databricks (Delta Lake).
     * "Dados Operacionais": SIARA / On-Premises (IBM Db2, File Storage) e APIs do Banco Central / Serasa.

2. BLOCO CENTRAL SUPERIOR: "Spoke de Modelagem e P&D" (Ambiente Analítico/Sandbox)
   Organizado nas seguintes colunas sequenciais (da esquerda para a direita):
   - Coluna M1: "Ingestão e P&D" -> BigQuery (Sandbox), Cloud Storage (Raw Data) e Vertex AI Workbench (Notebooks).
   - Coluna M2: "Orquestração MLOps" -> Cluster "Vertex AI Pipelines" contendo: Dataproc/Dataflow (Transformações) e Vertex AI Custom Training (com ML Experiments e Hyperparameter Tuning).
   - Coluna M3: "Registro de Modelos" -> Vertex AI Model Registry (Candidato Homologado).

3. BLOCO CENTRAL INFERIOR: "Spoke de Inferência e Serving" (Ambiente Operacional/Produção)
   Organizado nas seguintes colunas sequenciais (alinhado horizontalmente abaixo da Modelagem):
   - Coluna I1: "Ingestão e Entrada" -> Cloud API Gateway, Cloud Run (Regras de Negócio) e Pub/Sub (Streaming).
   - Coluna I2: "Armazenamento Técnico" -> BigQuery (Repositório de Features - Serving) e Cloud Spanner.
   - Coluna I3: "Serving e Execução" -> Vertex AI Endpoint de Inferência (Online/Batch Prediction).
   - Coluna I4: "Observabilidade" -> Vertex AI Model Monitoring e BigQuery (Logs Operacionais).

4. BLOCO DIREITO TRANSVERSAL: "Governança"
   - Posicionado de forma que cubra ambos os spokes -> Dataplex (Data Mesh - Catálogo, Qualidade, Linhagem e Auditoria).

### 🔀 Fluxos e Conexões Reais (Quem chama quem)

Configure as conexões explicitando os tipos de fluxos por cores e estilos:
- Fluxo de Dados/Analítico (Cientistas/Engenheiros): Seta azul sólida.
- Fluxo de Produção/Inferência (Aplicação/Consumo): Seta preta sólida.
- Fluxo de Metadados/Governança: Seta verde tracejada ('style="dashed"', 'color="darkgreen"').

Mapeie as interações:
- Azure Databricks envia dados para o BigQuery (Sandbox) do Spoke de Modelagem.
- As fontes On-Premises/Operacionais enviam dados para o Spoke de Inferência via Cloud API Gateway e Pub/Sub.
- Dentro do Spoke de Modelagem: O Workbench engaja o Vertex AI Pipelines, que treina o modelo e o publica no Vertex AI Model Registry ("Promoção"). O Dataproc/Dataflow salva as features processadas diretamente no BigQuery (Repositório de Features) localizado no Spoke de Inferência.
- Dentro do Spoke de Inferência: O Cloud API Gateway repassa a requisição para o Cloud Run (Regras de Negócio), que aciona o Vertex AI Endpoint. O Endpoint consome as features em tempo real do BigQuery (Repositório de Features) e envia telemetria para o Model Monitoring. Os logs vão para o BigQuery Operacional.
- Dataplex monitora e coleta metadados/linhagem de todos os repositórios analíticos e de logs (BigQuery do Sandbox, BigQuery de Features e BigQuery de Logs).

Gere o código Python completo baseado nessas especificações.

---
