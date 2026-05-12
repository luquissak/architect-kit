# Mapeamento de Classes e Importações (Diagrams Library)

Este arquivo serve como um guia de "de-para" para resolver erros de importação ou classes inexistentes na biblioteca `diagrams`. 

## Problemas de Importação (ImportError)

| Erro / Classe Problemática | Causa Provável | Alternativa / Correção |
| :--- | :--- | :--- |
| `from diagrams.onprem.database import SQLServer` | Classe não encontrada ou renomeada | `from diagrams.azure.database import SQLDatabases` |
| `from diagrams.generic.database import SQL` | Ambiguidade | `from diagrams.onprem.database import MSSQL` (se for SQL Server) |
| `from diagrams.onprem.network import Router` | Movido | `from diagrams.generic.network import Router` |

## Mapeamento de Provedores

| Provedor Original | Alternativa Sugerida | Notas |
| :--- | :--- | :--- |
| `onprem.database.SQLServer` | `azure.database.SQLDatabases` | Frequentemente usado quando o ícone onprem não é encontrado |
| `onprem.client.Users` | `onprem.client.User` | Verifique se é singular ou plural conforme a versão |

---

### Como usar esta Skill:
Sempre que ocorrer um erro de execução em um script `v*.py`, consulte este arquivo para identificar se a classe ou o caminho de importação possui um mapeamento conhecido.
