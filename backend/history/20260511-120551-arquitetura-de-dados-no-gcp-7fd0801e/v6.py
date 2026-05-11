from diagrams import Diagram, Cluster, Edge
from diagrams.azure.database import SQLDatabases
from diagrams.onprem.compute import Server
from diagrams.gcp.storage import Storage
from diagrams.gcp.analytics import BigQuery, Looker
from diagrams.gcp.ml import DialogFlowEnterpriseEdition
from diagrams.onprem.client import Users

import sys
import os

# Configuração de atributos globais (Import Obrigatório)
sys.path.append(os.path.abspath('../..'))
from common_attr import graph_attr

# Forçando o roteamento ortogonal para evitar efeito "teia de aranha"
graph_attr["splines"] = "ortho"

# Criação do Diagrama
with Diagram("Arquitetura de Dados Simplificada no GCP", show=False, direction="LR", graph_attr=graph_attr):

    # -----------------------------------------------------------
    # ISOLAMENTO LÓGICO DAS CAMADAS
    # -----------------------------------------------------------

    with Cluster("Camada 1: Origens de Dados"):
        # Fontes de dados originais
        sql_server = SQLDatabases("SQL Server")
        sap_bw = Server("SAP BW")
        
    with Cluster("Camada 2: Ingestão de Dados"):
        # Mantendo apenas a ingestão em bulk no Storage
        gcs = Storage("Cloud Storage\n(Bulk Ingestion)")
        
    with Cluster("Camada 3: Processamento e Pipelines"):
        # Apenas ferramentas nativas de BigQuery para orquestração e scripts
        bq_pipelines = BigQuery("BigQuery Pipelines")
        sql_script = BigQuery("Script SQL")
        
    with Cluster("Camada 4: Armazenamento Analítico"):
        # Arquitetura Medalhão centralizada
        bq_bronze = BigQuery("Bronze\n(Dados Brutos)")
        bq_silver = BigQuery("Silver\n(Dados Tratados)")
        bq_gold = BigQuery("Gold\n(Dados Curados)")
        
    with Cluster("Camada 5: Consumo e Visualização"):
        # Agentes conversacionais e relatórios
        conv_agents = DialogFlowEnterpriseEdition("Conversational\nAgents")
        looker = Looker("Looker Studio")
        users = Users("Usuários Finais")

    # -----------------------------------------------------------
    # REGRAS DE FLUXO DE DADOS
    # -----------------------------------------------------------

    # Fluxo: Camada 1 -> Camada 2 (Ingestão Bulk)
    [sql_server, sap_bw] >> Edge(label="Bulk Ingest") >> gcs
    
    # Fluxo: Camada 2 -> Camada 4 (Carga direta na camada Bronze)
    gcs >> Edge(label="Carga") >> bq_bronze
    
    # Fluxo: Camada 3 e 4 (Processamento e transformações no BigQuery)
    bq_pipelines >> Edge(dir="back", color="blue", label="Lê") >> bq_bronze
    bq_pipelines >> Edge(dir="forward", color="green", label="Grava") >> bq_silver
    
    sql_script >> Edge(dir="back", color="blue", label="Lê") >> bq_silver
    sql_script >> Edge(dir="forward", color="green", label="Grava") >> bq_gold
    
    # Fluxo: Camada 4 -> Camada 5 (Consumo a partir da Gold)
    bq_gold >> Edge(label="Integração IA") >> conv_agents
    bq_gold >> Edge(label="Consumo Analítico") >> looker
    
    # Entrega ao usuário final
    [conv_agents, looker] >> users

    # -----------------------------------------------------------
    # CONTROLE DE RANKING (Alinhamento Lógico Invisível)
    # -----------------------------------------------------------
    # Mantém a organização estrutural fluindo da esquerda para a direita
    (
        sql_server 
        >> Edge(style="invis") 
        >> gcs 
        >> Edge(style="invis") 
        >> bq_pipelines 
        >> Edge(style="invis") 
        >> bq_bronze 
        >> Edge(style="invis") 
        >> looker
    )

# -----------------------------------------------------------
# INSTRUÇÕES DE INSTALAÇÃO E EXECUÇÃO
# -----------------------------------------------------------
# Dependências necessárias (Linux/Mac/Windows)
# 1. Instale o Graphviz no S.O. (ex: sudo apt install graphviz ou brew install graphviz)
# 2. Instale o pacote Python: pip install diagrams
# 
# Para executar este script:
# python nome_do_arquivo.py
# -----------------------------------------------------------