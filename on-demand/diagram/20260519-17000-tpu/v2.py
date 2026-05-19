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
from diagrams.gcp.compute import GCE
from diagrams.gcp.ml import TPU
from diagrams.gcp.storage import Storage
from diagrams.gcp.devtools import ContainerRegistry
from diagrams.gcp.security import Iam

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
        name="GCP TPU VM Fine-Tuning Workaround Architecture",
        show=False,
        filename="gcp_tpu_architecture",
        direction="LR",
        graph_attr=graph_attr,
        outformat=outformat
    ):
        # Ator externo (Desenvolvedor)
        developer = User("Estacao do\nDesenvolvedor")

        with Cluster("Google Cloud Project (GCP)"):
            # Serviços de IAM, Segurança e Registros Globais
            iap = Iam("Identity-Aware Proxy\n(IAP)")
            artifact_registry = ContainerRegistry("Artifact Registry\n(Custom Dev Image)")
            gcs_bucket = Storage("Cloud Storage Bucket\n(Gemma Weights & Datasets)")

            with Cluster("VPC Network"):
                # Sub-rede privada sem IPs externos expostos
                with Cluster("Subnet Privada"):
                    
                    # Representação física da TPU VM
                    with Cluster("Cloud TPU VM Instance (us-central1)"):
                        tpu_host = GCE("TPU VM Host\n(OS: Ubuntu)")
                        tpu_chips = TPU("TPU Hardware\n(ex: TPU v5e-8)")

                        # Serviços rodando de forma isolada dentro do container Docker
                        with Cluster("Docker Container (Privilegiado)"):
                            jupyter_server = GCE("Jupyter Server\n(Porta 8888)")
                            vscode_server = GCE("VS Code Web (code-server)\n(Porta 8080)")

            # --- Conexões de Segurança e Acesso ---
            # Desenvolvedor faz o túnel via IAP usando SSH na porta 22
            developer >> Edge(
                label="SSH Tunnel\n(Porta 22)", 
                color="red", 
                style="dashed"
            ) >> iap
            
            # O IAP encaminha as requisições TCP criptografadas diretamente ao Host
            iap >> Edge(
                label="Mapeamento Local\nlocalhost:8888 / localhost:8080", 
                color="blue"
            ) >> tpu_host

            # --- Fluxo de Inicialização e Provisionamento ---
            # TPU Host faz o download do container customizado
            artifact_registry >> Edge(
                label="docker pull", 
                color="darkgreen", 
                style="dashed"
            ) >> tpu_host

            # Cloud Storage FUSE monta o bucket diretamente no diretório do host
            gcs_bucket >> Edge(
                label="gcsfuse mount\n/data", 
                color="darkorange"
            ) >> tpu_host

            # O Host expõe o hardware de TPU em modo privilegiado para o container
            tpu_host >> Edge(
                label="--privileged\n(Acesso direto à TPU)", 
                color="purple"
            ) >> tpu_chips

            # Integração dos endpoints das IDEs com o Host
            tpu_host >> jupyter_server
            tpu_host >> vscode_server

if __name__ == "__main__":
    # Gera o diagrama em ambos os formatos desejados (PNG para visualização rápida e SVG para qualidade infinita)
    generate_diagram("png")
    generate_diagram("svg")
    print("Diagrams generated successfully in PNG and SVG formats!")
