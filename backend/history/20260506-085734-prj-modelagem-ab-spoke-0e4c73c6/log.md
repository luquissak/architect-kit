## Versão 1 - 2026-05-06 08:57:34
**Prompt do Usuário:**
Gere um diagrama Python (biblioteca diagrams) para a seguinte arquitetura de solução:

Cloud: Multi-cloud
Padrão arquitetural: Personalizado
Nível de detalhe: técnico
Descriçao: Atue como um Arquiteto de Soluções especialista em Engenharia de Infraestrutura e Automação de Diagramas com a biblioteca `diagrams` do Python.

Quero desenhar um diagrama de arquitetura baseado em camadas lógicas (colunas sequenciais). Para garantir um alinhamento perfeito, simetria e padrão corporativo, você DEVE seguir rigidamente as seguintes diretrizes de design:

1. DIREÇÃO: Use sempre `direction="LR"` (Left to Right) para representar o fluxo cronológico das camadas em colunas verticais.
2. LINHAS ORTOGONAIS: Configure o atributo do grafo "splines": "ortho" para forçar conexões em ângulos retos de 90 graus, evitando o efeito "teia de aranha".
3. CONTROLE DE RANKING (A Espinha Dorsal Invisível): Para evitar que o Graphviz embaralhe as posições das camadas, você deve criar uma cadeia de conexões ocultas entre o nó principal de cada camada sequencial no final do script usando `>> Edge(style="invis") >>`.
4. FLUXO RETRÓGRADO: Se um componente da Camada Posterior precisar se conectar a um componente da Camada Anterior, use propriedades como `dir="back"` ou inverta a declaração da conexão para que o Graphviz não empurre a camada para trás no desenho.
5. ISOLAMENTO LÓGICO: Cada camada deve estar encapsulada em um bloco `with Cluster("Camada X: Nome")`.

Aqui estão os componentes e as camadas do diagrama atual que preciso:
Monte o código usando o template padrão de arquitetura em camadas (direction="LR" e splines="ortho"). O diagrama representa o projeto de modelagem "prj-modelagem-a/b (Spoke)".

Aqui estão os componentes divididos em suas respectivas camadas lógicas (colunas):

1. Camada 1: Ingestão e Sandbox (Extrema Esquerda)
   - Componente 1: BigQuery ("BigQuery\n(Sandbox)") [GCP Analytics]
   - Componente 2: Cloud Storage ("Cloud Storage\n(Raw Data)") [GCP Storage ou Infrastructure]
   - Componente 3: Vertex AI Workbench ("Vertex AI Workbench\n(Notebooks)") [GCP ML]
   * Nota de fluxo interno: Tanto o BigQuery quanto o Cloud Storage apontam para o Vertex AI Workbench.

2. Camada 2: Orquestração de MLOps (Central - Cluster Grande "Vertex AI Pipelines (MLOps)")
   Dentro deste cluster principal, existem 3 subcomponentes sequenciais (da esquerda para a direita):
   - Subcomponente A: "Feature Store" [GCP ML ou Custom Data]
   - Subcomponente B: "Model Training" [GCP ML]
   - Subcomponente C: "Evaluation" [GCP ML]
   * Fluxo interno da camada: Workbench (da Camada 1) aponta para o Feature Store com a label "Trigger Pipeline". Dentro do cluster, Feature Store -> Model Training -> Evaluation.

3. Camada 3: Destinos e Governança (Extrema Direita)
   - Componente 1 (Mais ao topo): Dataplex ("Dataplex") dentro de um sub-cluster chamado "Governança" [GCP Analytics/Dataprep]
   - Componente 2 (Mais abaixo): Model Registry ("Model Registry\n(Candidato Homologado)") [GCP ML]

Defina a Espinha Dorsal Invisível conectando os componentes principais para travar as colunas:
Vertex AI Workbench >> Edge(style="invis") >> Feature Store >> Edge(style="invis") >> Model Registry

---
## Versão 2 - 2026-05-12 17:08:37
**Prompt do Usuário:**
Temos o diagrama versão 1. Por favor, modifique o código Python existente de acordo com este novo pedido: mude o icone do feature store de vertex para big query, mantendo o nome

Código anterior:
from diagrams import Diagram, Cluster, Edge
from diagrams.gcp.analytics import Bigquery, DataCatalog
from diagrams.gcp.storage import Storage
from diagrams.gcp.ml import AIPlatform
import os
import sys

# Importação obrigatória dos atributos de grafo compartilhados
sys.path.append(os.path.abspath('../..'))
from common_attr import graph_attr

# Configuração de linhas ortogonais (ângulos de 90 graus)
graph_attr["splines"] = "ortho"

# Criação do diagrama sem exibir automaticamente e alinhado da Esquerda para a Direita
with Diagram("prj-modelagem-ab-Spoke", show=False, direction="LR", graph_attr=graph_attr):
    
    # Camada 1: Ingestão e Sandbox (Extrema Esquerda)
    with Cluster("Camada 1: Ingestão e Sandbox"):
        bq_sandbox = Bigquery("BigQuery\n(Sandbox)")
        gcs_raw = Storage("Cloud Storage\n(Raw Data)")
        workbench = AIPlatform("Vertex AI Workbench\n(Notebooks)")
        
        # Fluxo interno da Camada 1
        bq_sandbox >> workbench
        gcs_raw >> workbench

    # Camada 2: Orquestração de MLOps (Central)
    with Cluster("Camada 2: Vertex AI Pipelines (MLOps)"):
        feature_store = AIPlatform("Feature Store")
        model_training = AIPlatform("Model Training")
        evaluation = AIPlatform("Evaluation")
        
        # Fluxo sequencial interno da Camada 2
        feature_store >> model_training >> evaluation

    # Camada 3: Destinos e Governança (Extrema Direita)
    with Cluster("Camada 3: Destinos e Governança"):
        with Cluster("Governança"):
            dataplex = DataCatalog("Dataplex")
            
        model_registry = AIPlatform("Model Registry\n(Candidato Homologado)")

    # Conexões explícitas entre camadas
    workbench >> Edge(label="Trigger Pipeline") >> feature_store
    evaluation >> model_registry
    
    # A Espinha Dorsal Invisível: controle de ranking para travar as colunas
    # Isso impede que o Graphviz embaralhe as posições lógicas do diagrama
    workbench >> Edge(style="invis") >> feature_store >> Edge(style="invis") >> model_registry

    # =========================================================================
    # INSTRUÇÕES DE INSTALAÇÃO E EXECUÇÃO:
    # 1. Instale a biblioteca diagrams e o graphviz no sistema:
    #    pip install diagrams
    #    (Requer Graphviz instalado no S.O.: apt-get install graphviz ou choco install graphviz)
    # 2. Execute este script:
    #    python nome_do_arquivo.py
    # =========================================================================

---
