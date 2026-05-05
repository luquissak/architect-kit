import os
import sys

# Import obrigatório conforme as instruções críticas
sys.path.append(os.path.abspath('../..'))
from common_attr import graph_attr

from diagrams import Diagram, Cluster, Edge
from diagrams.gcp.analytics import BigQuery, Dataproc, Dataflow
from diagrams.gcp.compute import Run
from diagrams.gcp.storage import Storage
from diagrams.onprem.client import Users

# Criação do diagrama usando graph_attr e sem filename, conforme exigido
with Diagram("SIGRM - Mark-to-Market Lakehouse Architecture", show=False, direction="LR", graph_attr=graph_attr):

    usuarios = Users("Sistemas / Usuários")

    with Cluster("Camada de Ingestão e Orquestração"):
        # Cloud Run atua como o entrypoint para execução de serviços containerizados (ex: API de ingestão)
        api_ingestao = Run("Cloud Run\n(API Ingestão/Orquestração)")
        raw_storage = Storage("Cloud Storage\n(Landing/Raw Data)")

    with Cluster("Camada de Processamento Distribuído"):
        
        with Cluster("Fase 1: Cálculo de Curvas"):
            # Opções de motores de processamento suportando Spark/Java/Python
            spark_curvas = Dataproc("Apache Spark\n(Cálculo Curvas)")
            dataflow_curvas = Dataflow("Dataflow\n(Alt: Cálculo Curvas)")

        with Cluster("Fase 2: Cálculo de Fluxos e MtM"):
            # Separação clara de processamento para fluxos
            spark_fluxos = Dataproc("Apache Spark\n(Cálculo Fluxos)")
            dataflow_fluxos = Dataflow("Dataflow\n(Alt: Cálculo Fluxos)")

    with Cluster("Camada de Armazenamento (Lakehouse / BigQuery)"):
        # Separação dos dados para garantir auditoria, rastreabilidade e reprocessamento
        bq_raw = BigQuery("Raw Data\n(Contratos/Mercado)")
        bq_intermediario = BigQuery("Resultados Intermediários\n(Curvas / Auditoria)")
        bq_final = BigQuery("Resultados Finais\n(Fluxos e MtM)")
        
        # Representação de regras de negócio complexas via UDFs no BigQuery
        bq_udfs = BigQuery("BigQuery UDFs\n(Regras de Negócio)")

    # 1. Fluxo de Ingestão
    usuarios >> Edge(label="Inicia carga/cenário diário") >> api_ingestao
    api_ingestao >> Edge(label="Persiste raw data") >> raw_storage
    raw_storage >> Edge(label="Carga BQ Raw") >> bq_raw

    # 2. Fluxo de Cálculo de Curvas (Lê raw, calcula, persiste intermediários)
    bq_raw >> Edge(label="Leitura p/ Curvas") >> spark_curvas
    bq_raw >> Edge(label="Leitura p/ Curvas") >> dataflow_curvas
    
    spark_curvas >> Edge(label="Persiste Curvas") >> bq_intermediario
    dataflow_curvas >> Edge(label="Persiste Curvas") >> bq_intermediario

    # 3. Fluxo de Cálculo de Fluxos (Lê contratos e curvas, calcula, persiste final)
    bq_intermediario >> Edge(label="Insumo p/ Fluxos (Reprocessável)") >> spark_fluxos
    bq_raw >> spark_fluxos
    
    bq_intermediario >> Edge(label="Insumo p/ Fluxos (Reprocessável)") >> dataflow_fluxos
    bq_raw >> dataflow_fluxos
    
    spark_fluxos >> Edge(label="Persiste MtM") >> bq_final
    dataflow_fluxos >> Edge(label="Persiste MtM") >> bq_final

    # 4. Aplicação de regras complexas/condicionais na camada de dados via UDFs
    bq_udfs - Edge(style="dotted", label="Aplica lógica não-vetorizável") - bq_intermediario
    bq_udfs - Edge(style="dotted") - bq_final

    # 5. Consumo dos dados para auditoria e relatórios
    bq_final >> Edge(label="Consulta Analítica") >> usuarios
    bq_intermediario >> Edge(label="Auditoria de Cenários") >> usuarios

# ===============================================================================
# INSTRUÇÕES PARA INSTALAÇÃO E EXECUÇÃO
# ===============================================================================
# 1. Instale o Graphviz no seu sistema operacional (necessário para a renderização):
#    - Linux (Debian/Ubuntu): sudo apt-get install graphviz
#    - macOS: brew install graphviz
#    - Windows: choco install graphviz
#
# 2. Instale a biblioteca Python "diagrams":
#    pip install diagrams
#
# 3. Salve este código em um arquivo (ex: arquitetura_sigrm.py) e execute:
#    python arquitetura_sigrm.py
# ===============================================================================