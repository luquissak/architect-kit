# diagrama_arquitetura.py
from diagrams import Cluster, Diagram, Edge
from diagrams.onprem.client import User
from diagrams.gcp.network import VPC
from diagrams.gcp.compute import GCE
from diagrams.gcp.ml import TPU
from diagrams.gcp.storage import Storage
from diagrams.gcp.devtools import ContainerRegistry
from diagrams.gcp.security import Iam

# Define o contexto global do diagrama
with Diagram(
    name="GCP TPU VM Fine-Tuning Workaround Architecture",
    show=False,             # Não abre a imagem automaticamente ao finalizar
    filename="gcp_tpu_architecture", # Nome do arquivo de saída (gcp_tpu_architecture.png)
    direction="LR"          # Fluxo do diagrama da Esquerda para a Direita (Left-to-Right)
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