## Versão 1 - 2026-05-06 09:38:16
**Prompt do Usuário:**
Gere um diagrama Python (biblioteca diagrams) para a seguinte arquitetura de solução:

Cloud: GCP
Padrão arquitetural: Lakehouse
Nível de detalhe: técnico
Descriçao: Atue como um Arquiteto de Soluções Cloud Enterprise especialista em Redes e Segurança no Google Cloud. Quero gerar um diagrama de arquitetura de rede no padrão Hub-and-Spoke para a plataforma MLOps - SIPML usando a biblioteca `diagrams` do Python.

Siga rigidamente as diretrizes de design abaixo para garantir simetria, alinhamento e clareza corporativa:

### 📐 Diretrizes Visuais e de Alinhamento
1. DIREÇÃO: Use 'direction="LR"' (Left to Right) para orientar o fluxo em colunas lógicas de tráfego.
2. LINHAS ORTOGONAIS: Configure "splines": "ortho" no 'graph_attr' para linhas de rede limpas em ângulos de 90°.
3. ISOLAMENTO RESTRITO: Cada projeto/ambiente deve ser encapsulado em um bloco `with Cluster("Nome do Projeto")` simulando o isolamento de VPC / VPC Network Peering.
4. ESPINHA DORSAL INVISÍVEL: Trave as colunas verticalmente usando conexões ocultas ('style="invis"') entre os componentes líderes de cada camada no final do script para garantir o paralelismo perfeito.

### 🏛️ Estrutura de Camadas e Clusters Lógicos

O diagrama deve representar três grandes projetos isolados (VPCs) interconectados, dispostos sequencialmente em colunas:

1. COLUNA 1 (Esquerda): "Spoke de Modelagem (`prj-sipml-modelagem-anl`)"
   - Componentes: Vertex AI Workbench, Vertex AI Pipelines, e BigQuery (Sandbox).
   - Este bloco representa a ponta de desenvolvimento analítico que precisa consumir e enviar dados de forma segura.

2. COLUNA 2 (Centro): "Hub Central de Orquestração (`prj-sipml-gateway-prd`)"
   - Deve ser o cluster central do diagrama. Componentes internos:
     * Cloud Load Balancing (HTTPS) -> Porta de entrada unificada.
     * Cloud Armor -> Proteção WAF na borda do Load Balancer.
     * Cloud API Gateway / Apigee -> Orquestrador e roteador interno de requisições.
     * Cloud DNS / Private Service Connect (PSC) -> Responsável por resolver e conectar os serviços com segurança via IPs privados.

3. COLUNA 3 (Direita): "Spoke de Inferência e Serving (`prj-sipml-inferencia-prd`)"
   - Componentes internos de execução:
     * Cloud Run (Business Rules).
     * Vertex AI Endpoint (Online Serving).
     * BigQuery (Repositório de Features).
     * Vertex AI Model Monitoring + BigQuery (Logs).

4. CAMADA COMPLEMENTAR EXTERNA (Borda Esquerda): "Origens de Tráfego"
   - Usuários (Cientistas de Dados/Engenheiros) e Aplicações Consumidoras/Sistemas Legados externos à VPC.

### 🔀 Fluxos e Conexões Reais (Quem chama quem)

Mapeie as conexões explicitando as fronteiras de rede (VPC Peering / PSC) através das labels:
- Origens de Tráfego (Usuários/Aplicações) batem primeiro no Cloud Load Balancing + Cloud Armor no Hub Central.
- O Load Balancer repassa o tráfego inspecionado para o Cloud API Gateway (Hub).
- O Cloud API Gateway consulta o Cloud DNS / PSC para decidir o destino privado:
  * Se a requisição for de desenvolvimento/orquestração, roteia para o Spoke de Modelagem (entrando via Vertex AI Workbench/Pipelines).
  * Se a requisição for de negócio ou predição em tempo real, roteia para o Spoke de Inferência (chamando o Cloud Run).
- Dentro do Spoke de Inferência, o fluxo segue o padrão operacional: Cloud Run chama o Vertex AI Endpoint -> Endpoint faz lookup no BigQuery Features -> Endpoint gera telemetria para o Model Monitoring -> Logs persistem no BigQuery Logs.
- Configurações de conexão: use setas pretas sólidas para fluxos de dados, setas tracejadas para validações de DNS/PSC, e uma linha invisível unindo os componentes centrais de cada cluster para fixar o alinhamento horizontal.

Gere o código Python completo baseado nessas especificações.

---
## Versão 2 - 2026-05-06 09:44:16
**Prompt do Usuário:**
Temos o diagrama versão 1. Por favor, modifique o código Python existente de acordo com este novo pedido: Atue como um Arquiteto de Soluções Cloud Enterprise especialista em Redes, Segurança e MLOps no Google Cloud. Quero gerar o código em Python usando a biblioteca `diagrams` para representar o ecossistema de rede e segurança da Plataforma MLOps - SIPML. 

O diagrama deve seguir o padrão Hub-and-Spoke, estruturado estritamente da esquerda para a direita (direction="LR"), utilizando linhas ortogonais ("splines": "ortho") e uma espinha dorsal invisível no final do script para travar o alinhamento das colunas (VPCs/Projetos).

### 🏛️ Estrutura de Camadas, Projetos (Clusters) e Componentes

Organize o diagrama em três grandes macro-projetos isolados, além das origens externas:

1. CAMADA EXTERNA (Borda Esquerda): "Origens de Tráfego"
   - Componentes: "Aplicações Consumidoras / Sistemas Legados" e "Cientistas de Dados / Engenheiros".

2. COLUNA 1 (Esquerda): "Spoke de Modelagem (`prj-sipml-modelagem-anl`)"
   - Componentes internos: Vertex AI Workbench, Vertex AI Pipelines e BigQuery (Sandbox).

3. COLUNA 2 (Centro): "Hub Central de Orquestração (`prj-sipml-gateway-prd`)"
   - Este deve ser o cluster central do diagrama, consolidando a camada de borda e segurança. Componentes internos:
     * Cloud Load Balancing (HTTPS) + Cloud Armor (Proteção WAF na borda).
     * Cloud API Gateway: Atua na gestão de contratos, autenticação e Rate Limiting.
     * Cloud Run (Decision Broker): Atua exclusivamente como Cliente HTTP para ingestão de dados de inferência e orquestrador da lógica de negócio (responsável pela captura online de bureaus externos e pela persistência de auditoria).
     * Secret Manager: Armazenamento seguro de chaves e certificados para o acesso aos bureaus externos.
     * Cloud Spanner (Audit Vault): Persistência de logs de auditoria e Cache de Bureaus (otimização de custos e performance), conectado diretamente ao Cloud Run.
     * Private Service Connect (PSC) / Cloud DNS: Para resolução e interconexão privada com os Spokes.

4. COLUNA 3 (Direita): "Spoke de Inferência e Serving (`prj-sipml-inferencia-prd`)"
   - Componentes internos: Vertex AI Endpoint (Online Serving), BigQuery (Repositório de Features), Vertex AI Model Monitoring e BigQuery (Logs Operacionais).

5. ECOSSISTEMA EXTERNO (Extremo Topo Direito): "Bureaus de Crédito Externos"
   - Componentes externos fora da rede: "Bureaus (SCR BACEN, Serasa, Boa Vista)".

### 🔀 Fluxos de Conectividade e Regras de Negócio (Sem Round-Trips Excessivos)

Desenhe um fluxo linear e limpo para evitar cruzamento de linhas desnecessárias:
- O tráfego das Aplicações entra pelo Cloud Load Balancing + Cloud Armor no Hub Central.
- O Load Balancer repassa para o Cloud API Gateway (que valida autenticação, contratos e aplica Rate Limiting).
- O API Gateway aciona o Cloud Run (Decision Broker).
- O Cloud Run (Decision Broker) realiza as seguintes ações locais e simplificadas dentro do Hub:
  * Consulta o Secret Manager para obter credenciais.
  * Consome de forma direta e linear os "Bureaus de Crédito Externos" via HTTP.
  * Grava os logs de auditoria e faz a busca/gravação de cache diretamente no Cloud Spanner (Audit Vault).
- Após consolidar a lógica e os dados dos bureaus, o Cloud Run (Decision Broker) direciona o fluxo via Private Service Connect (PSC) para o Spoke de Inferência, acionando diretamente o Vertex AI Endpoint.
- Dentro do Spoke de Inferência: O Vertex AI Endpoint faz o lookup de variáveis no BigQuery (Repositório de Features) e envia telemetria para o Model Monitoring.

Gere o código Python completo baseado nessas especificações de arquitetura.

Código anterior:
import os
import sys
from diagrams import Diagram, Cluster, Edge

# Importação obrigatória dos atributos comuns de grafo e injeção do diretório
sys.path.append(os.path.abspath('../..'))
from common_attr import graph_attr

# Importações de componentes da biblioteca diagrams
from diagrams.onprem.client import Users, Client
from diagrams.gcp.network import LoadBalancing, Armor, DNS
from diagrams.gcp.api import APIGateway
from diagrams.gcp.ml import AIPlatform
from diagrams.gcp.analytics import BigQuery
from diagrams.gcp.compute import Run
from diagrams.gcp.operations import Monitoring

# Configuração para forçar linhas ortogonais em ângulos de 90 graus (Diretriz Visual 2)
graph_attr.update({"splines": "ortho", "nodesep": "1.2", "ranksep": "1.5"})

with Diagram("MLOps Network - SIPML", show=False, direction="LR", graph_attr=graph_attr):

    # CAMADA COMPLEMENTAR: Origens de Tráfego (Borda Esquerda)
    with Cluster("Origens de Tráfego Externo"):
        users = Users("Usuários\n(Cientistas/Engenheiros)")
        apps = Client("Aplicações\nConsumidoras")

    # COLUNA 1: Spoke de Modelagem (Esquerda)
    with Cluster("Spoke de Modelagem\n(prj-sipml-modelagem-anl)"):
        workbench = AIPlatform("Vertex AI\nWorkbench")
        pipelines = AIPlatform("Vertex AI\nPipelines")
        bq_sandbox = BigQuery("BigQuery\n(Sandbox)")

        # Fluxo interno de desenvolvimento analítico
        workbench >> pipelines >> bq_sandbox

    # COLUNA 2: Hub Central (Centro)
    with Cluster("Hub Central de Orquestração\n(prj-sipml-gateway-prd)"):
        armor = Armor("Cloud Armor\n(WAF)")
        lb = LoadBalancing("Cloud Load\nBalancing")
        api_gw = APIGateway("API Gateway\n/ Apigee")
        dns_psc = DNS("Cloud DNS\n+ PSC")

        # Entrada unificada e orquestração
        armor >> lb >> api_gw
        # Resolução de DNS / Lookup Privado para os Spokes
        api_gw >> Edge(style="dashed", color="gray", label="Lookup Privado") >> dns_psc

    # COLUNA 3: Spoke de Inferência (Direita)
    with Cluster("Spoke de Inferência e Serving\n(prj-sipml-inferencia-prd)"):
        run_rules = Run("Cloud Run\n(Business Rules)")
        vertex_endpoint = AIPlatform("Vertex AI\nEndpoint")
        bq_features = BigQuery("BigQuery\n(Feature Store)")
        model_monitor = Monitoring("Vertex AI\nModel Monitoring")
        bq_logs = BigQuery("BigQuery\n(Logs)")

        # Fluxo de chamada online e telemetria
        run_rules >> vertex_endpoint
        vertex_endpoint >> bq_features
        vertex_endpoint >> model_monitor >> bq_logs

    # FLUXOS REAIS DE CONEXÃO (Interconectividade Hub-and-Spoke)
    
    # 1. Tráfego externo atinge o Hub Central na borda
    users >> armor
    apps >> armor

    # 2. API Gateway roteia para o Spoke de Modelagem (Desenvolvimento / Orquestração)
    api_gw >> Edge(label="Roteamento Dev\n(VPC Peering)", color="black", dir="forward") >> workbench

    # 3. API Gateway roteia para o Spoke de Inferência (Negócios / Serving)
    api_gw >> Edge(label="Roteamento Negócio\n(PSC)", color="black") >> run_rules

    # ESPINHA DORSAL INVISÍVEL: Trava estrutural para forçar o alinhamento em colunas (Diretriz Visual 4)
    # A ordem força: Origens -> Modelagem -> Hub -> Inferência
    users - Edge(style="invis") - workbench - Edge(style="invis") - armor - Edge(style="invis") - run_rules
    apps - Edge(style="invis") - bq_sandbox - Edge(style="invis") - api_gw - Edge(style="invis") - bq_logs

# ==========================================
# INSTRUÇÕES PARA EXECUÇÃO DO SCRIPT
# ==========================================
# 1. Certifique-se de ter o Graphviz instalado no seu sistema operacional:
#    - Linux: sudo apt-get install graphviz
#    - Mac: brew install graphviz
#    - Windows: choco install graphviz
# 2. Instale a biblioteca Python:
#    pip install diagrams
# 3. Execute o script:
#    python nome_do_arquivo.py

---
