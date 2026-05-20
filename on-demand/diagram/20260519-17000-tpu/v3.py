import os
import sys
from unittest.mock import MagicMock

# Evita o travamento do módulo 'platform' ao consultar o WMI no Windows
platform_mock = MagicMock()
platform_mock.system.return_value = 'Windows'
sys.modules['platform'] = platform_mock

from diagrams import Cluster, Diagram, Edge
from diagrams.onprem.client import Users
from diagrams.gcp.network import LoadBalancing
from diagrams.gcp.security import IAP
from diagrams.gcp.ml import TPU
from diagrams.gcp.storage import Storage
from diagrams.gcp.devtools import ContainerRegistry
from diagrams.k8s.compute import Deployment
from diagrams.k8s.network import Service

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

# Configuração para forçar linhas ortogonais em ângulos de 90 graus e alta resolução (600 DPI)
graph_attr.update({"splines": "ortho", "nodesep": "0.8", "ranksep": "1.2", "dpi": "600"})

def generate_diagram(outformat):
    with Diagram(
        name="Caixa GKE Private Jupyter Lab Architecture (southamerica-east1-c)",
        show=False,
        filename="gke_caixa_internal_lb_iap",
        direction="LR",
        graph_attr=graph_attr,
        outformat=outformat
    ):
        # Usuários Caixa conectados à rede interna/perímetro corporativo (VPN ou Interconnect)
        caixa_users = Users("Usuarios Caixa\n(Perimetro Interno)")

        with Cluster("Google Cloud Project (GCP)"):
            
            # Recursos globais/regionais de armazenamento de imagens e dados
            artifact_registry = ContainerRegistry("Artifact Registry\n(Custom Dev Image)")
            gcs_bucket = Storage("Cloud Storage Bucket\n(Gemma Weights & Datasets)")

            with Cluster("VPC Network (Rede Privada)"):
                
                # Componentes do Balanceamento e Autenticação de Entrada
                with Cluster("Regional Ingress Security Layer"):
                    # O IAP é associado ao backend service do balanceador regional interno
                    iap_auth = IAP("Identity-Aware Proxy\n(IAP para ILB)")
                    
                    # Load Balancer de Aplicação Regional Interno (ILB HTTPS/HTTP)
                    internal_lb = LoadBalancing("Internal Load Balancer\n(http://10.8.8.8)")

                with Cluster("Subnet: southamerica-east1 (Sao Paulo)"):
                    
                    # Nós e Pods do GKE em rede totalmente privada
                    with Cluster("GKE Private Cluster (southamerica-east1-c)"):
                        
                        # K8s Service expondo os Pods internamente na rede via NEG (Network Endpoint Group)
                        k8s_service = Service("K8s Service\n(Jupyter HTTP:8888)")
                        
                        # Deployment que orquestra os Pods do Jupyter Server
                        jupyter_app = Deployment("Jupyter Server\nPod (Dev Environment)")

                        # Pool de Nós acelerados por hardware
                        tpu_nodes = TPU("Cloud TPU v5e/v6e\n(Node Pool Acelerado)")

            # --- Fluxo de Comunicação e Tráfego ---
            
            # 1. Usuário acessa diretamente via navegador de dentro da rede corporativa
            caixa_users >> Edge(
                label="Acesso Web Direto\nhttp://10.8.8.8", 
                color="darkgreen"
            ) >> internal_lb
            
            # 2. O ILB intercepta a requisição e aciona a política do IAP para checar permissão de acesso
            internal_lb >> Edge(
                label="Intercepta para\nAutenticacao IAM", 
                color="red", 
                style="dashed"
            ) >> iap_auth
            
            # 3. IAP valida a identidade do usuário Caixa (necessita do papel de 'IAP-secured Web App User')
            iap_auth >> Edge(
                label="Redireciona Tráfego\nAutorizado (IAP Role Check)", 
                color="blue"
            ) >> k8s_service

            # 4. O Service do Kubernetes direciona o tráfego validado para o Pod do Jupyter
            k8s_service >> jupyter_app

            # --- Dependências de Infraestrutura e Hardware ---
            
            # O GKE faz o pull da imagem do contêiner customizado
            artifact_registry >> Edge(
                label="K8s Image Pull\n(Always)", 
                color="darkgreen", 
                style="dashed"
            ) >> jupyter_app

            # Montagem do Cloud Storage FUSE direto nos Pods para acesso aos pesos do Gemma e datasets
            gcs_bucket >> Edge(
                label="gcsfuse CSI Driver\nMount /data", 
                color="darkorange"
            ) >> jupyter_app

            # Alocação física das TPUs no Pod de treinamento/Jupyter em modo privilegiado
            jupyter_app >> Edge(
                label="--privileged\nDevice Access", 
                color="purple"
            ) >> tpu_nodes

if __name__ == "__main__":
    # Gera o diagrama em ambos os formatos desejados (PNG para visualização rápida e SVG para qualidade infinita)
    generate_diagram("png")
    generate_diagram("svg")
    print("Diagrams generated successfully in PNG and SVG formats!")
