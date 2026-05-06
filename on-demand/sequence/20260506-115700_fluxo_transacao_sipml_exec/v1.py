import os
from pathlib import Path

PUML = r"""
@startuml
skinparam linestyle ortho
skinparam shadowing false
skinparam BoxPadding 10
skinparam ParticipantPadding 15

title Fluxo de Transacao (Executivo) - Plataforma SIPML

actor "Canal / Originacao" as CH #LightGray
box "Hub Central de Orquestracao (prj-sipml-gateway-prd)" #LightBlue
    participant "API Gateway" as GW
    participant "Decision Broker\n(Cloud Run - Cliente HTTP)" as DB
    database "Cloud Spanner\n(Audit Vault & Cache)" as SP
end box

box "Spoke de Inferencia (prj-spoke-inferencia)" #LightGreen
    participant "Vertex AI\n(Endpoint de Inferencia)" as INF
    database "BigQuery\n(Repositorio de Features)" as FS
end box

queue "Pub/Sub" as PS #LightYellow
participant "Hubs de Dados\n(Corporativo)" as HD #LightGray

' =========================================================================
' JORNADA DO FLUXO DE TRANSACAO E INFERENCIA
' =========================================================================

CH -> GW: 1) Solicita inferencia
activate GW

GW -> DB: 2) Ingestao de dados de inferencia
activate DB

DB -> SP: 2.1) Consulta cache de Bureaus
DB <- SP: 2.2) Retorna cache (se existente)

note over DB
  Opcional: Aciona Cloud Workflow
  apenas para fluxos complexos
end note

DB -> DB: 2.3) Chamadas HTTP paralelas para Bureaus externos\n(SCR BACEN, Serasa, Boa Vista)

DB -> SP: 2.4) Grava persistencia de auditoria e atualiza cache
activate SP
deactivate SP

GW <- DB: 3) Retorna carga de dados enriquecida
deactivate DB

GW -> INF: 4) Encaminha requisicao para inferencia
activate INF

INF -> FS: 4.1) Lookup de variaveis locais em tempo real
INF <- FS: 4.2) Retorna features complementares

GW <-- INF: 5) Retorna resultado da inferencia
deactivate INF

' Fluxo de Retroalimentacao assincrono para os Hubs de Dados
GW -> PS: 6) Publica assincronamente dados capturados nos bureaus
activate PS
PS -> HD: 7) Envia dados para ingestao nos Hubs de Dados (futuros treinos)
deactivate PS

CH <-- GW: 8) Devolve resultado da inferencia ao originador
deactivate GW

@enduml
"""

from pyplantuml import generate_uml_png

def main():
    # Garante a criação do diretório de saída caso não exista
    output_dir = Path("./")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    out_file = output_dir / "v1.puml"
    out_file.write_text(PUML.strip() + "\n", encoding="utf-8")
    print(f"Arquivo PlantUML gerado com sucesso em: {out_file.resolve()}")

    # Geração da imagem PNG
    print("Gerando imagem PNG...")
    try:
        generate_uml_png(PUML.strip(), "v1.png")
        print(f"Imagem gerada com sucesso: {(output_dir / 'v1.png').resolve()}")
    except Exception as e:
        print(f"Erro ao gerar imagem: {e}")

if __name__ == "__main__":
    main()