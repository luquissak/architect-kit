## Versão 1 - 2026-05-06 10:51:45
**Prompt do Usuário:**
Gere um diagrama Python (biblioteca diagrams) para a seguinte arquitetura de solução:

Cloud: GCP
Padrão arquitetural: Lakehouse
Nível de detalhe: técnico
Descriçao: Atue como um Arquiteto de Dados e Cloud Platform Engineer sênior no Google Cloud. Quero gerar o código em Python usando a biblioteca `diagrams` para representar a camada de ingestão e processamento da plataforma SIPML, focando em flexibilidade e múltiplos hubs de dados.

O diagrama deve seguir o padrão de arquitetura em camadas estruturado da esquerda para a direita (direction="LR"), com conexões ortogonais ("splines": "ortho") e uma espinha dorsal invisível ao final do script para forçar o perfeito alinhamento vertical dos componentes em colunas.

### 🏛️ Estrutura de Camadas e Clusters Lógicos

Organize o diagrama nas seguintes colunas lógicas sequenciais:

1. COLUNA 1 (Esquerda): "Origens de Dados e Eventos"
   - Dividido em dois grupos verticais distintos:
     * Cluster "Hubs de Dados Analíticos (Múltiplos)": Represente duas instâncias genéricas para ilustrar a multiplicidade (ex: "Hub Analítico A" e "Hub Analítico B"). [Use ícones genéricos de SQL/Storage]
     * Cluster "Hubs de Dados Operacionais (Múltiplos)": Represente também duas instâncias (ex: "Hub Operacional A (Streaming)" e "Hub Operacional B (Bases/APIs)"). [Use ícones genéricos de Storage/SQL]

2. COLUNA 2 (Centro-Esquerda): "Camada de Ingestão e Armazenamento Raw"
   - Componentes internos: 
     * Pub/Sub (para mensageria e tópicos de streaming vindos dos hubs operacionais).
     * Cloud Storage (Bucket de Landing/Raw Data para arquivos e cargas analíticas em lote).

3. COLUNA 3 (Centro-Direita): "Camada de Processamento e Feature Engineering"
   - Cluster unificado chamado "Motores de Processamento Distribuidor":
     * Dataflow (Processamento de Pipelines de Streaming/Batch baseado em Apache Beam).
     * Dataproc (Processamento de Cargas Analíticas de Larga Escala baseado em Apache Spark).
   * Nota de design: Ambos os componentes devem ficar pareados na mesma coluna.

4. COLUNA 4 (Direita): "Destinos Analíticos e Feature Store"
   - Componentes internos:
     * BigQuery (Repositório Central de Features / Serving).
     * Vertex AI Feature Store (para consumo de baixa latência).

### 🔀 Fluxos de Conectividade e Transformação de Dados

Mapeie as conexões de maneira estritamente linear e da esquerda para a direita para evitar linhas cruzadas:
- Os "Hubs de Dados Analíticos" exportam dados em lote DIRETAMENTE para o Cloud Storage.
- Os "Hubs de Dados Operacionais" enviam eventos em tempo real para o Pub/Sub e tabelas transacionais de apoio para o Cloud Storage.
- Na camada de processamento:
  * O Cloud Storage alimenta tanto o Dataflow quanto o Dataproc para processamento em lote (Batch).
  * O Pub/Sub entrega os dados de streaming DIRETAMENTE para o Dataflow.
- Na camada de destino:
  * O Dataflow e o Dataproc salvam as tabelas limpas e as features geradas diretamente no BigQuery (Repositório de Features).
  * O BigQuery sincroniza ou alimenta o Vertex AI Feature Store.

Gere o código Python completo baseado nessas especificações técnicas de engenharia de dados.

---
## Versão 2 - 2026-05-06 11:00:40
**Prompt do Usuário:**
Temos o diagrama versão 1. Por favor, modifique o código Python existente de acordo com este novo pedido: Atue como um Engenheiro de Dados e Arquiteto Cloud GCP sênior. Quero gerar um diagrama focado EXCLUSIVAMENTE no "Hub de Dados Analíticos" da plataforma SIPML usando a biblioteca `diagrams` do Python.

Siga rigidamente as diretrizes de design abaixo:
1. DIREÇÃO: Use 'direction="LR"' para dispor as fases de dados em colunas sequenciais.
2. LINHAS ORTOGONAIS: Configure "splines": "ortho" para linhas limpas corporativas em 90°.
3. ISOLAMENTO ANALÍTICO: Remova qualquer elemento ou menção à inferência em tempo real, APIs operacionais ou riscos. O foco é P&D, dados democratizados e treinamento.
4. ALINHAMENTO COM ESPINHA INVISÍVEL: Crie uma sequência de conexões ocultas ('style="invis"') entre os componentes líderes das camadas 1, 2, 3 e 4 no fim do script.

Mapeie as 4 colunas lógicas desta forma:
- Camada 1 (Origens): "Azure Databricks (Delta Lake / Refinados)" e "Analytical/Training Data (SILDC - Dados Sintéticos)".
- Camada 2 (Ingestão/Landing): "Cloud Storage (Raw Data / Landing)" e "BigQuery (Sandbox P&D)".
- Camada 3 (Processamento): Um cluster contendo "Cloud Dataproc (Apache Spark)" e "Cloud Dataflow (Apache Beam)".
- Camada 4 (Destino): "BigQuery (Repositório de Features)".

Fluxos de dados reais:
- Azure Databricks alimenta o BigQuery Sandbox.
- O SILDC (Dados sintéticos/democratizados) alimenta o Cloud Storage.
- O Cloud Storage e o BigQuery Sandbox fornecem dados de leitura para ambos os motores de processamento (Dataproc e Dataflow).
- O Dataproc e o Dataflow realizam a engenharia de atributos e persistem as tabelas finais de treinamento de forma consolidada no BigQuery (Repositório de Features).

Código anterior:
import os
import sys
sys.path.append(os.path.abspath('../..'))
from common_attr import graph_attr

from diagrams import Diagram, Cluster, Edge
from diagrams.gcp.analytics import BigQuery, Dataflow, Dataproc, Pubsub
from diagrams.gcp.storage import Storage
from diagrams.gcp.ml import AIPlatform
from diagrams.onprem.database import PostgreSQL, MySQL
from diagrams.onprem.queue import Kafka

# Ajuste para garantir conexões ortogonais, conforme exigido pela arquitetura
graph_attr["splines"] = "ortho"

with Diagram("Plataforma SIPML - Camada de Ingestao e Processamento", show=False, direction="LR", graph_attr=graph_attr):
    
    # --- COLUNA 1: Origens de Dados e Eventos ---
    with Cluster("Origens de Dados e Eventos"):
        
        with Cluster("Hubs de Dados Analíticos (Múltiplos)"):
            hub_analitico_a = PostgreSQL("Hub Analítico A")
            hub_analitico_b = MySQL("Hub Analítico B")
            hubs_analiticos = [hub_analitico_a, hub_analitico_b]
            
        with Cluster("Hubs de Dados Operacionais (Múltiplos)"):
            hub_op_streaming = Kafka("Hub Operacional A\n(Streaming)")
            hub_op_bases = PostgreSQL("Hub Operacional B\n(Bases/APIs)")

    # --- COLUNA 2: Camada de Ingestão e Armazenamento Raw ---
    with Cluster("Camada de Ingestão e Armazenamento Raw"):
        pubsub = Pubsub("Pub/Sub\n(Mensageria)")
        cloud_storage = Storage("Cloud Storage\n(Landing/Raw Data)")

    # --- COLUNA 3: Camada de Processamento e Feature Engineering ---
    with Cluster("Camada de Processamento e Feature Engineering"):
        with Cluster("Motores de Processamento Distribuído"):
            dataflow = Dataflow("Dataflow\n(Streaming/Batch)")
            dataproc = Dataproc("Dataproc\n(Batch/Spark)")

    # --- COLUNA 4: Destinos Analíticos e Feature Store ---
    with Cluster("Destinos Analíticos e Feature Store"):
        bigquery = BigQuery("BigQuery\n(Repositório de Features)")
        vertex_ai = AIPlatform("Vertex AI\n(Feature Store)")

    # --- FLUXOS DE DADOS ---
    
    # Hubs Analíticos -> Lote direto para Cloud Storage
    hubs_analiticos >> cloud_storage
    
    # Hubs Operacionais -> Streaming para Pub/Sub e tabelas para Storage
    hub_op_streaming >> pubsub
    hub_op_bases >> cloud_storage
    
    # Cloud Storage -> Processamento Batch
    cloud_storage >> dataflow
    cloud_storage >> dataproc
    
    # Pub/Sub -> Processamento Streaming
    pubsub >> dataflow
    
    # Processamento -> Destino Analítico Central (BigQuery)
    dataflow >> bigquery
    dataproc >> bigquery
    
    # BigQuery -> Vertex AI Feature Store
    bigquery >> vertex_ai

    # --- ESPINHA DORSAL INVISÍVEL PARA ALINHAMENTO VERTICAL ---
    # Força a estruturação das colunas perfeitamente da esquerda para a direita
    hub_analitico_a >> Edge(style="invis") >> cloud_storage >> Edge(style="invis") >> dataproc >> Edge(style="invis") >> bigquery

# ==========================================
# INSTRUÇÕES PARA EXECUÇÃO:
# 1. Instale o Graphviz no seu SO (ex: sudo apt-get install graphviz ou brew install graphviz)
# 2. Instale as dependências Python:
#    pip install diagrams
# 3. Execute o script:
#    python nome_do_arquivo.py
# ==========================================

---
