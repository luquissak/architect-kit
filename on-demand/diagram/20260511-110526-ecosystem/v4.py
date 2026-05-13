import os
import sys
from diagrams import Diagram, Cluster, Edge

# Importação obrigatória dos atributos comuns de grafo e injeção do diretório
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
graph_attr.update({"splines": "ortho", "nodesep": "1.2", "ranksep": "1.5", "dpi": "600"})

with Diagram("MLOps Network and Security Ecosystem - SIPML v4", show=False, direction="LR", graph_attr=graph_attr, outformat="svg"):

    # 1. CAMADA EXTERNA: Origens de Tráfego (Borda Esquerda)
    with Cluster("Origens de Tráfego"):
        users = Users("Cientistas de Dados /\nEngenheiros")
        apps = Client("Aplicações Consumidoras\n/ Sistemas Legados")

    # 2. COLUNA 1: Spoke de Modelagem
    with Cluster("Spoke de Modelagem\n(prj-sipml-modelagem-anl)"):
        workbench = AIPlatform("Vertex AI\nWorkbench")
        pipelines = AIPlatform("Vertex AI\nPipelines")
        bq_sandbox = BigQuery("BigQuery\n(Sandbox)")

        # Fluxo de experimentação isolado no spoke analítico
        workbench >> pipelines >> bq_sandbox

    # 3. COLUNA 2: Hub Central de Orquestração
    with Cluster("Hub Central de Orquestração\n(prj-sipml-gateway-prd)"):
        armor = Armor("Cloud Armor\n(Proteção WAF)")
        lb = LoadBalancing("Cloud Load\nBalancing (HTTPS)")
        api_gw = APIGateway("Cloud API Gateway\n(Contratos e Rate Limit)")
        
        # Decision Broker e ecossistema local do Hub
        run_broker = Run("Cloud Run\n(Decision Broker)")
        secret_mgr = SecretManager("Secret Manager\n(Chaves/Certificados)")
        spanner_audit = Spanner("Cloud Spanner\n(Audit Vault & Cache)")
        
        # Ponto de saída privada para Spokes
        psc_dns = DNS("Cloud DNS / PSC\n(Private Service Connect)")

        # Entrada e orquestração na borda do Hub
        armor >> lb >> api_gw >> run_broker

        # Interações locais do Decision Broker no Hub
        run_broker >> Edge(label="1. Obtém Credenciais", style="dashed") >> secret_mgr
        run_broker >> Edge(label="2. Persistência de Logs/Cache", dir="both") >> spanner_audit
        run_broker >> Edge(label="4. Roteamento Privado (PSC)") >> psc_dns

    # 4. COLUNA 3: Spoke de Inferência e Serving
    with Cluster("Spoke de Inferência e Serving\n(prj-sipml-inferencia-prd)"):
        vertex_endpoint = AIPlatform("Vertex AI\nEndpoint (Online)")
        bq_features = BigQuery("BigQuery\n(Repositório de Features)")
        model_monitor = Monitoring("Vertex AI\nModel Monitoring")
        bq_logs = BigQuery("BigQuery\n(Logs Operacionais)")

        # Lógica interna de serving de predições
        vertex_endpoint >> Edge(label="Lookup Variáveis") >> bq_features
        vertex_endpoint >> Edge(label="Telemetria") >> model_monitor >> bq_logs

    # 5. ECOSSISTEMA EXTERNO (Extremo Topo Direita)
    with Cluster("Bureaus Externos"):
        # Ajuste: Rótulo simplificado conforme solicitado
        bureaus = Server("APIs")

    # ==========================================
    # FLUXOS GLOBAIS E REGRAS DE NEGÓCIO
    # ==========================================
    
    # Cientistas acessam ambiente de modelagem
    users >> workbench
    
    # Tráfego das aplicações ingressa via Borda Segura no Hub
    apps >> armor

    # Decision Broker consome diretamente a API dos Bureaus
    run_broker >> Edge(label="3. Consulta Externa (HTTP)", color="blue", dir="forward") >> bureaus

    # Conexão do Hub (PSC) para o Spoke de Inferência
    psc_dns >> Edge(label="Aciona Inferência", color="darkgreen") >> vertex_endpoint

    # ==========================================
    # ESPINHA DORSAL INVISÍVEL (Alinhamento)
    # ==========================================
    # Trava estrutural para forçar as colunas em ordem: 
    # Origens -> Modelagem -> Hub Central -> Inferência -> Bureaus Externos
    users - Edge(style="invis") - workbench - Edge(style="invis") - api_gw - Edge(style="invis") - vertex_endpoint - Edge(style="invis") - bureaus
    apps - Edge(style="invis") - bq_sandbox - Edge(style="invis") - spanner_audit - Edge(style="invis") - bq_logs
