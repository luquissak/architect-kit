import os
import sys

# Import obrigatório de atributos comuns
sys.path.append(os.path.abspath('../..'))
from common_attr import graph_attr

from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.compute import Server
from diagrams.onprem.client import Client
from diagrams.gcp.analytics import Dataflow, BigQuery, Dataproc, Composer, Dataprep, Looker
from diagrams.gcp.database import Spanner
from diagrams.gcp.compute import Run
from diagrams.gcp.security import Iam
from diagrams.gcp.devtools import Build
from diagrams.gcp.ml import AIPlatform

# Configuração principal do diagrama com show=False e graph_attr obrigatório, sem filename
with Diagram("GCP Lakehouse - Projeto SIGRM", show=False, direction="LR", graph_attr=graph_attr):

    # 4. Camada base com Governança, IAM e CI/CD
    with Cluster("Fundação e Governança"):
        dataplex = Dataprep("Dataplex (Governança)")
        iam = Iam("IAM (Autorização)")
        ci_cd = Build("Cloud Build (CI/CD)")

    # 1. Camada On Premises
    with Cluster("On Premises"):
        sistemas_internos = Server("Sistemas Internos")
        sistemas_externos = Server("Sistemas Externos")
        interfaces = Client("Interfaces Diversas")
        
        fontes_dados = [sistemas_internos, sistemas_externos, interfaces]

    # 2. Camada de Ingestão e Armazenamento
    with Cluster("Ingestão"):
        dataflow = Dataflow("Dataflow")
        bq_storage = BigQuery("BigQuery (Armazenamento)")
        spanner = Spanner("Spanner")
        
        # Fluxo de Ingestão
        fontes_dados >> dataflow
        dataflow >> bq_storage
        dataflow >> spanner
        
        # Ligação entre os 2 serviços de armazenamento
        bq_storage - Edge(style="dotted", color="blue") - spanner

    # 3. Camada de Processamento
    with Cluster("Processamento"):
        composer = Composer("Composer (Orquestração)")
        
        # O Dataform não possui ícone nativo oficial, utilizando ícone de Build como representação de compilação SQL
        dataform = Build("Dataform (SQL)")
        spark = Dataproc("Dataproc (Spark/Python)")
        run_java = Run("Cloud Run (Java)")
        bq_proc = BigQuery("BigQuery (Processamento)")

        # Orquestração do Composer sobre as ferramentas de processamento
        composer >> Edge(color="darkgreen", style="dashed") >> dataform
        composer >> Edge(color="darkgreen", style="dashed") >> spark
        composer >> Edge(color="darkgreen", style="dashed") >> run_java
        
        # Leitura da Ingestão, processamento e gravação na camada processada
        bq_storage >> dataform >> bq_proc
        bq_storage >> spark >> bq_proc
        bq_storage >> run_java >> bq_proc

    # 5. Camada de Consumo
    with Cluster("Consumo"):
        endpoint_api = Run("Endpoint (Cloud Run)")
        looker = Looker("Looker")
        vertex_ai = AIPlatform("Vertex AI")
        
        # Consumo de dados processados
        bq_proc >> endpoint_api
        bq_proc >> looker
        bq_proc >> vertex_ai

    # Relacionamentos lógicos da fundação com as outras camadas (invisíveis para não poluir, ou fluxo direcional pontilhado)
    iam >> Edge(style="dotted", color="gray") >> bq_storage
    dataplex >> Edge(style="dotted", color="gray") >> bq_proc
    ci_cd >> Edge(style="dotted", color="gray") >> composer

# ===============================================================================
# INSTRUÇÕES PARA INSTALAÇÃO E EXECUÇÃO
# ===============================================================================
# 1. Instale o Graphviz no seu sistema (ex: `sudo apt-get install graphviz` ou `brew install graphviz`)
# 2. Instale a biblioteca Python: `pip install diagrams`
# 3. Salve este código num arquivo, por exemplo: `arquitetura_sigrm.py`
# 4. Certifique-se de que o arquivo `common_attr.py` existe no caminho indicado
# 5. Execute o script: `python arquitetura_sigrm.py`
# ===============================================================================