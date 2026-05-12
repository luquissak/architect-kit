import os
import sys
from diagrams import Diagram, Cluster, Edge

# Importação obrigatória dos atributos comuns de grafo e injeção do diretório
# Ajustando o path para encontrar o backend se necessário, ou mantendo o original se funcionar
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'backend')))
try:
    from common_attr import graph_attr
except ImportError:
    graph_attr = {
        "fontname": "Arial",
        "fontsize": "20",
        "ranksep": "1.0",
        "nodesep": "0.6",
        "pad": "0.4",
        "splines": "ortho",
        "dpi": "600"
    }

# Importações de componentes da biblioteca diagrams
from diagrams.onprem.client import Users, Client
from diagrams.onprem.compute import Server
from diagrams.gcp.network import LoadBalancing, Armor, DNS
from diagrams.gcp.api import APIGateway
from diagrams.gcp.ml import AIPlatform
from diagrams.gcp.analytics import BigQuery
from diagrams.gcp.compute import Run
from diagrams.gcp.operations import Monitoring
from diagrams.gcp.security import SecretManager
from diagrams.gcp.database import Spanner

# Configuração para forçar linhas ortogonais em ângulos de 90 graus
# Forçando DPI 600 conforme solicitado
graph_attr.update({"splines": "ortho", "nodesep": "1.2", "ranksep": "1.5", "dpi": "600"})

with Diagram("MLOps Network and Security Ecosystem - SIPML v3", show=False, direction="LR", graph_attr=graph_attr, outformat="svg"):

    # 1. CAMADA EXTERNA: Origens de Tráfego (Borda Esquerda)
    with Cluster("Origens de Tráfego"):
        users = Users("Cientistas de Dados /\nEngenheiros")
        apps = Client("Aplicações Consumidoras\n/ Sistemas Legados")

    # 2. COLUNA 1: Spoke de Modelagem
    with Cluster("Spoke de Modelagem (Ingestão/Treino)"):
        dns_internal = DNS("Cloud DNS\n(Internal)")
        model_lb = LoadBalancing("Internal HTTP(S) LB")
        workbench = AIPlatform("Vertex AI Workbench\n(VPC Service Controls)")
        training = AIPlatform("Custom Training Jobs")

    # 3. COLUNA 2: Spoke de Inferência (Runtime)
    with Cluster("Spoke de Inferência (Consumo/Serving)"):
        dns_external = DNS("Cloud DNS\n(External)")
        armor = Armor("Cloud Armor\n(WAF/Anti-DDoS)")
        serving_lb = LoadBalancing("External HTTP(S) LB")
        api_gw = APIGateway("Cloud API Gateway")
        endpoints = AIPlatform("Vertex AI Endpoints")
        run_rules = Run("Cloud Run\n(Business Rules)")

    # 4. CAMADA TRANSVERSAL: Dados e Segurança
    with Cluster("Dados e Segurança (Shared VPC)"):
        bq = BigQuery("BigQuery\n(VPC Private Service Connect)")
        secrets = SecretManager("Cloud Secret Manager")
        monitoring = Monitoring("Cloud Operations Suite\n(Logging/Monitoring)")
        spanner = Spanner("Cloud Spanner\n(Transacional)")

    # FLUXOS E CONEXÕES
    
    # Acesso Cientistas/Engenheiros
    users >> dns_internal >> model_lb >> workbench
    workbench >> training >> bq
    
    # Acesso Aplicações (Consumo Externo)
    apps >> dns_external >> armor >> serving_lb >> api_gw >> run_rules >> endpoints
    
    # Relações de Segurança e Dados
    endpoints >> bq
    run_rules >> spanner
    
    # Monitoramento e Segredos (Transversal)
    [workbench, training, endpoints, run_rules] >> monitoring
    [workbench, training, endpoints, run_rules] >> secrets
