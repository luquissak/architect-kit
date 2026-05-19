import os
import sys
from unittest.mock import MagicMock

# Evita o travamento do módulo 'platform' ao consultar o WMI no Windows
platform_mock = MagicMock()
platform_mock.system.return_value = 'Windows'
sys.modules['platform'] = platform_mock

from diagrams import Cluster, Diagram, Edge
from diagrams.onprem.client import User
from diagrams.gcp.network import VPC
from diagrams.gcp.compute import GKE
from diagrams.gcp.ml import TPU
from diagrams.gcp.storage import Storage
from diagrams.gcp.devtools import ContainerRegistry
from diagrams.gcp.security import Iam
from diagrams.k8s.compute import Pod, Job
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
        name="GKE TPU v6e Fine-Tuning Architecture (southamerica-east1)",
        show=False,
        filename="gke_tpu_southamerica_architecture",
        direction="LR",
        graph_attr=graph_attr,
        outformat=outformat
    ):
        # Cientista de dados / Arquiteto na ponta externa
        developer = User("Arquiteto / Dev\n(Estacao Local)")

        with Cluster("Google Cloud Platform - Regiao: southamerica-west1"):
            # Segurança IAM e Registros de Recursos Globais / Regionais
            iap = Iam("Identity-Aware Proxy\n(IAP-secured Tunnel)")
            artifact_registry = ContainerRegistry("Artifact Registry\n(SouthAmerica Docker Repo)")
            gcs_bucket = Storage("Cloud Storage Bucket\n(Gemma weights & datasets)")

            with Cluster("VPC Network (VPC Privada)"):
                with Cluster("Subnet: southamerica-east1-a"):
                    
                    # Instanciação do GKE Enterprise/Standard Cluster
                    with Cluster("GKE Cluster (Autopilot / Standard)"):
                        gke_control_plane = GKE("GKE Control Plane")

                        # Cluster lógico para os Pods/Jobs que rodam as aplicações
                        with Cluster("Kubernetes Pods Namespace"):
                            k8s_service = Service("K8s Service\n(Porta 8888 & 8080)")
                            gdev_pod = Pod("Pod: Dev Environment\n(Jupyter + VS Code)")
                            train_job = Job("Job: Fine-Tuning\n(Gemma Gemma3LLMTrain)")

                        # Pool de Nós dedicados com aceleradores físicos
                        with Cluster("TPU Node Pool"):
                            tpu_trillium = TPU("Cloud TPU v6e Slice\n(Topology: 2x4/Trillium)")

        # --- Fluxo de Conectividade e Acesso ---
        # Desenvolvedor fecha o túnel seguro na porta 22 mapeando portas locais
        developer >> Edge(
            label="Tunnel TCP via IAP\n(Porta 22)", 
            color="red", 
            style="dashed"
        ) >> iap
        
        # O IAP redireciona de forma segura ao Control Plane do GKE para port-forwarding
        iap >> Edge(
            label="kubectl port-forward\n(localhost:8888 -> 8888)", 
            color="blue"
        ) >> gke_control_plane

        # Encaminhamento interno do GKE do Service até o Pod de desenvolvimento
        gke_control_plane >> k8s_service >> gdev_pod

        # --- Fluxo de Orquestração, Dados e Hardware ---
        # O nó do GKE baixa a imagem personalizada diretamente do Artifact Registry regional
        artifact_registry >> Edge(
            label="K8s Image Pull\n(Always)", 
            color="darkgreen", 
            style="dashed"
        ) >> gdev_pod

        # GCS FUSE CSI Driver realiza a montagem direta de volumes sem intervenção de scripts manuais no host
        gcs_bucket >> Edge(
            label="GCS FUSE CSI Driver\ngcsfuse.csi.storage.gke.io", 
            color="darkorange"
        ) >> gdev_pod

        gcs_bucket >> Edge(
            label="Mount Dataset & Weight\nPath: /data", 
            color="darkorange"
        ) >> train_job

        # Os pods interagem de forma nativa e privilegiada com os nós TPU associados
        gdev_pod >> Edge(
            label="Privileged Mode\nDevice Allocation", 
            color="purple"
        ) >> tpu_trillium

        train_job >> Edge(
            label="Target Topology\nLimits: google.com/tpu: 4", 
            color="purple"
        ) >> tpu_trillium

if __name__ == "__main__":
    # Gera o diagrama em ambos os formatos desejados (PNG para visualização rápida e SVG para qualidade infinita)
    generate_diagram("png")
    generate_diagram("svg")
    print("Diagrams generated successfully in PNG and SVG formats!")
