import { useState, useEffect } from "react";

const TEMPLATES = [
  {
    label: "Data Lakehouse GCP",
    cloud: "GCP",
    pattern: "Lakehouse",
    detail: "técnico",
    description: "Ingestão de dados batch e streaming via Pub/Sub e Dataflow, armazenamento no GCS em camadas Bronze/Silver/Gold, processamento com BigQuery e Dataproc Spark, catálogo com Dataplex, consumo via Looker e Vertex AI para modelos de ML.",
  },
  {
    label: "RAG Pipeline AWS",
    cloud: "AWS",
    pattern: "RAG / GenAI",
    detail: "técnico",
    description: "Pipeline RAG na AWS: documentos ingeridos via S3, processados com Lambda, embeddings gerados pelo Bedrock Titan, armazenados no OpenSearch Serverless como vector store, orquestração com Step Functions, API Gateway expondo endpoint de chat com Claude via Bedrock.",
  },
  {
    label: "MLOps Azure",
    cloud: "Azure",
    pattern: "MLOps",
    detail: "técnico",
    description: "Plataforma MLOps no Azure: dados no ADLS Gen2, feature engineering com Azure Databricks, treinamento e registro de modelos no Azure ML, CI/CD com Azure DevOps, deploy como endpoint gerenciado, monitoramento com Azure Monitor e Application Insights.",
  },
  {
    label: "Streaming Analytics GCP",
    cloud: "GCP",
    pattern: "Streaming",
    detail: "técnico",
    description: "Arquitetura de streaming analytics: eventos publicados no Pub/Sub, processamento em tempo real com Dataflow (Apache Beam), resultados gravados no BigQuery e no Bigtable para baixa latência, dashboards em tempo real no Looker Studio.",
  },
  {
    label: "Landing Zone Multi-cloud",
    cloud: "Multi-cloud",
    pattern: "Landing Zone",
    detail: "executivo",
    description: "Landing zone multi-cloud para dados corporativos: governança centralizada, data mesh com domínios de dados independentes em GCP e Azure, federação de identidade, segurança perimetral e catálogo unificado com tags e políticas de acesso.",
  },
];

const CLOUDS = ["GCP", "AWS", "Azure", "Multi-cloud"];
const PATTERNS = ["Lakehouse", "Streaming", "Batch ETL", "RAG / GenAI", "MLOps", "Landing Zone", "Data Mesh", "Personalizado"];
const DETAILS = ["executivo", "técnico"];

const SYSTEM_PROMPT = `Você é um arquiteto de soluções especialista em dados e IA. Sua tarefa é gerar código Python usando a biblioteca \`diagrams\` (diagrams.mingrammer.com) para criar diagramas de arquitetura de solução em nuvem.

Regras obrigatórias:
1. Use SEMPRE imports corretos da biblioteca diagrams (diagrams.aws.*, diagrams.gcp.*, diagrams.azure.*, diagrams.onprem.*)
2. Use with Diagram(..., show=False, direction="LR") como padrão
3. Agrupe componentes com Cluster para representar camadas (Ingestão, Processamento, Armazenamento, Consumo, etc.)
4. Use os ícones mais adequados disponíveis na biblioteca para cada serviço mencionado
5. Represente fluxo de dados com >> entre os componentes
6. Inclua comentários curtos no código para guiar o leitor
7. Ao final, inclua um bloco de comentários com o comando para instalar dependências e rodar o script

Responda APENAS com o bloco de código Python, sem explicações antes ou depois. Comece com \`from diagrams import...\` e termine com o fechamento do bloco \`with\`.`;

export default function App() {
  const [cloud, setCloud] = useState("GCP");
  const [pattern, setPattern] = useState("Lakehouse");
  const [provider, setProvider] = useState("anthropic");
  const [detail, setDetail] = useState("técnico");
  const [description, setDescription] = useState("");
  const [output, setOutput] = useState("");
  const [imageUrl, setImageUrl] = useState("");
  const [archId, setArchId] = useState("");
  const [version, setVersion] = useState(0);
  const [iterationPrompt, setIterationPrompt] = useState("");
  const [loading, setLoading] = useState(false);
  const [copied, setCopied] = useState(false);
  const [activeTab, setActiveTab] = useState("gerador");
  
  // History states
  const [history, setHistory] = useState([]);
  const [historySearch, setHistorySearch] = useState("");
  const [loadingHistory, setLoadingHistory] = useState(false);

  // Skill states
  const [runAudit, setRunAudit] = useState(false);
  const [auditReport, setAuditReport] = useState("");

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    setLoadingHistory(true);
    try {
      const response = await fetch("/api/history");
      if (response.ok) {
        const data = await response.json();
        setHistory(data);
      }
    } catch (e) {
      console.error("Erro ao carregar histórico:", e);
    } finally {
      setLoadingHistory(false);
    }
  };

  const loadHistoryItem = async (id) => {
    setLoading(true);
    try {
      const response = await fetch(`/api/history/${id}`);
      if (response.ok) {
        const data = await response.json();
        setArchId(data.arch_id);
        setVersion(data.version);
        setOutput(data.content);
        setImageUrl(data.image_url ? data.image_url + "?t=" + new Date().getTime() : "");
        setActiveTab("gerador");
      }
    } catch (e) {
      console.error("Erro ao carregar item do histórico:", e);
    } finally {
      setLoading(false);
    }
  };

  const applyTemplate = (tpl) => {
    setCloud(tpl.cloud);
    setPattern(tpl.pattern);
    setDetail(tpl.detail);
    setDescription(tpl.description);
    setOutput("");
    setActiveTab("gerador");
  };

  const generate = async () => {
    const isIteration = archId !== "";
    const promptBase = isIteration ? iterationPrompt : description;
    
    if (!promptBase.trim()) return;
    setLoading(true);
    
    // Se não for iteração, limpa os outputs antigos
    if (!isIteration) {
      setOutput("");
      setImageUrl("");
    }

    const userPrompt = isIteration 
      ? `Temos o diagrama versão ${version}. Por favor, modifique o código Python existente de acordo com este novo pedido: ${iterationPrompt}\n\nCódigo anterior:\n${output}`
      : `Gere um diagrama Python (biblioteca diagrams) para a seguinte arquitetura de solução:

Cloud: ${cloud}
Padrão arquitetural: ${pattern}
Nível de detalhe: ${detail}
Descriçao: ${description}`;

    try {
      const response = await fetch("/api/generate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          provider: provider,
          system_prompt: SYSTEM_PROMPT,
          user_prompt: userPrompt,
          arch_id: archId || null,
          run_audit: runAudit
        }),
      });
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.detail || data.error?.message || "Erro na API");
      }
      const text = typeof data.content === 'string' ? data.content : (data.content?.map?.((b) => b.text || "")?.join("") || "Erro ao gerar.");
      const clean = text.replace(/```python\n?/g, "").replace(/```\n?/g, "").trim();
      setOutput(clean);
      if (data.image_url) {
        setImageUrl(data.image_url + "?t=" + new Date().getTime()); // Evitar cache
      } else {
        setImageUrl("");
      }
      
      setArchId(data.arch_id);
      setVersion(data.version);
      setAuditReport(data.audit_report || "");
      
      if (data.error) {
        const errorComments = data.error.split('\\n').map(line => `# ${line}`).join('\\n');
        setOutput(`${errorComments}\\n\\n${clean}`);
      }
      
      setIterationPrompt("");
      fetchHistory(); // Atualiza o histórico após gerar
    } catch (e) {
      setOutput("# Erro ao chamar a API. Verifique sua conexão ou API Key.\n# Detalhe: " + e.message);
    } finally {
      setLoading(false);
    }
  };

  const copy = () => {
    navigator.clipboard.writeText(output);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const filteredHistory = history.filter(item => 
    item.name.toLowerCase().includes(historySearch.toLowerCase()) || 
    item.date.toLowerCase().includes(historySearch.toLowerCase())
  );

  return (
    <div style={{
      minHeight: "100vh",
      background: "#0a0f1a",
      color: "#e2e8f0",
      fontFamily: "'IBM Plex Sans', 'Segoe UI', sans-serif",
      display: "flex",
      flexDirection: "column",
    }}>
      {/* Header */}
      <div style={{
        borderBottom: "1px solid #1e2d45",
        padding: "18px 32px",
        display: "flex",
        alignItems: "center",
        gap: 14,
        background: "#07101f",
      }}>
        <div style={{
          width: 36, height: 36,
          background: "linear-gradient(135deg, #0ea5e9, #6366f1)",
          borderRadius: 8,
          display: "flex", alignItems: "center", justifyContent: "center",
          fontSize: 18,
        }}>⬡</div>
        <div>
          <div style={{ fontWeight: 700, fontSize: 16, letterSpacing: "-0.3px" }}>
            ArchDiagram <span style={{ color: "#0ea5e9" }}>AI</span>
          </div>
          <div style={{ fontSize: 11, color: "#4a6080", marginTop: 1 }}>
            Gerador de diagramas cloud com IA · Pre-Sales Kit
          </div>
        </div>
        <div style={{ marginLeft: "auto", display: "flex", gap: 8 }}>
          {["gerador", "templates"].map((tab) => (
            <button key={tab} onClick={() => setActiveTab(tab)} style={{
              background: activeTab === tab ? "#0ea5e920" : "transparent",
              border: activeTab === tab ? "1px solid #0ea5e950" : "1px solid transparent",
              color: activeTab === tab ? "#0ea5e9" : "#4a6080",
              padding: "5px 14px",
              borderRadius: 6,
              fontSize: 12,
              cursor: "pointer",
              fontWeight: 500,
              textTransform: "capitalize",
            }}>{tab}</button>
          ))}
        </div>
      </div>

      <div style={{ flex: 1, display: "flex", overflow: "hidden" }}>
        {/* Sidebar Histórico */}
        <div style={{
          width: 280,
          borderRight: "1px solid #1e2d45",
          background: "#07101f",
          display: "flex",
          flexDirection: "column",
          overflow: "hidden"
        }}>
          <div style={{ padding: "20px 20px 10px 20px" }}>
            <div style={{ fontSize: 11, color: "#4a8ab5", fontWeight: 600, letterSpacing: "0.08em", textTransform: "uppercase", marginBottom: 12 }}>
              Histórico
            </div>
            <div style={{ position: "relative" }}>
              <input 
                type="text" 
                placeholder="Buscar no histórico..." 
                value={historySearch}
                onChange={(e) => setHistorySearch(e.target.value)}
                style={{
                  width: "100%",
                  background: "#0d1829",
                  border: "1px solid #1e2d45",
                  borderRadius: 6,
                  padding: "8px 12px 8px 32px",
                  fontSize: 12,
                  color: "#e2e8f0",
                  outline: "none"
                }}
              />
              <div style={{ position: "absolute", left: 10, top: "50%", transform: "translateY(-50%)", color: "#4a6080", fontSize: 12 }}>
                🔍
              </div>
            </div>
          </div>
          
          <div style={{ flex: 1, overflowY: "auto", padding: "10px 10px" }}>
            {loadingHistory && history.length === 0 ? (
              <div style={{ padding: 20, textAlign: "center", color: "#4a6080", fontSize: 12 }}>Carregando...</div>
            ) : filteredHistory.length === 0 ? (
              <div style={{ padding: 20, textAlign: "center", color: "#4a6080", fontSize: 12 }}>Nenhum item encontrado.</div>
            ) : (
              filteredHistory.map(item => (
                <div 
                  key={item.id} 
                  onClick={() => loadHistoryItem(item.id)}
                  style={{
                    padding: "12px 15px",
                    borderRadius: 8,
                    cursor: "pointer",
                    background: archId === item.id ? "#0ea5e915" : "transparent",
                    border: archId === item.id ? "1px solid #0ea5e930" : "1px solid transparent",
                    marginBottom: 4,
                    transition: "all 0.2s"
                  }}
                  onMouseEnter={(e) => { if(archId !== item.id) e.currentTarget.style.background = "#1e2d4550"; }}
                  onMouseLeave={(e) => { if(archId !== item.id) e.currentTarget.style.background = "transparent"; }}
                >
                  <div style={{ fontSize: 13, fontWeight: 600, color: archId === item.id ? "#0ea5e9" : "#cbd5e1", whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}>
                    {item.name.split('-').slice(1, -1).join(' ') || item.name}
                  </div>
                  <div style={{ fontSize: 10, color: "#4a6080", marginTop: 4 }}>
                    {item.date || "Sem data"}
                  </div>
                </div>
              ))
            )}
          </div>
        </div>

        {/* Main Content */}
        {activeTab === "gerador" && (
          <div style={{ flex: 1, display: "flex", gap: 0, overflow: "hidden" }}>
            {/* Left Panel (Controls) */}
            <div style={{
              width: 340,
              borderRight: "1px solid #1e2d45",
              padding: 24,
              display: "flex",
              flexDirection: "column",
              gap: 20,
              overflowY: "auto"
            }}>
              <div>
                <label style={{ fontSize: 11, color: "#4a8ab5", fontWeight: 600, letterSpacing: "0.08em", textTransform: "uppercase" }}>
                  Motor de IA (LLM)
                </label>
                <div style={{ display: "flex", gap: 6, marginTop: 8, marginBottom: 20 }}>
                  {["anthropic", "gemini"].map((p) => (
                    <button key={p} onClick={() => setProvider(p)} style={{
                      flex: 1, padding: "6px 0",
                      borderRadius: 6,
                      border: provider === p ? "1px solid #10b981" : "1px solid #1e2d45",
                      background: provider === p ? "#10b98115" : "#0d1829",
                      color: provider === p ? "#10b981" : "#6b8aaa",
                      fontSize: 12, cursor: "pointer", fontWeight: 500,
                      textTransform: "capitalize"
                    }}>{p === "anthropic" ? "Claude 3.5" : "Gemini 1.5"}</button>
                  ))}
                </div>
              </div>

              <div>
                <label style={{ fontSize: 11, color: "#4a8ab5", fontWeight: 600, letterSpacing: "0.08em", textTransform: "uppercase" }}>
                  Cloud Provider
                </label>
                <div style={{ display: "flex", gap: 6, marginTop: 8, flexWrap: "wrap" }}>
                  {CLOUDS.map((c) => (
                    <button key={c} onClick={() => setCloud(c)} style={{
                      padding: "5px 12px",
                      borderRadius: 6,
                      border: cloud === c ? "1px solid #0ea5e9" : "1px solid #1e2d45",
                      background: cloud === c ? "#0ea5e915" : "#0d1829",
                      color: cloud === c ? "#0ea5e9" : "#6b8aaa",
                      fontSize: 12, cursor: "pointer", fontWeight: 500,
                    }}>{c}</button>
                  ))}
                </div>
              </div>

              <div>
                <label style={{ fontSize: 11, color: "#4a8ab5", fontWeight: 600, letterSpacing: "0.08em", textTransform: "uppercase" }}>
                  Padrão Arquitetural
                </label>
                <div style={{ display: "flex", gap: 6, marginTop: 8, flexWrap: "wrap" }}>
                  {PATTERNS.map((p) => (
                    <button key={p} onClick={() => setPattern(p)} style={{
                      padding: "5px 10px",
                      borderRadius: 6,
                      border: pattern === p ? "1px solid #6366f1" : "1px solid #1e2d45",
                      background: pattern === p ? "#6366f115" : "#0d1829",
                      color: pattern === p ? "#818cf8" : "#6b8aaa",
                      fontSize: 11, cursor: "pointer", fontWeight: 500,
                    }}>{p}</button>
                  ))}
                </div>
              </div>

              <div>
                <label style={{ fontSize: 11, color: "#4a8ab5", fontWeight: 600, letterSpacing: "0.08em", textTransform: "uppercase" }}>
                  Nível de Detalhe
                </label>
                <div style={{ display: "flex", gap: 6, marginTop: 8 }}>
                  {DETAILS.map((d) => (
                    <button key={d} onClick={() => setDetail(d)} style={{
                      padding: "5px 14px",
                      borderRadius: 6,
                      border: detail === d ? "1px solid #10b981" : "1px solid #1e2d45",
                      background: detail === d ? "#10b98115" : "#0d1829",
                      color: detail === d ? "#34d399" : "#6b8aaa",
                      fontSize: 12, cursor: "pointer", fontWeight: 500, textTransform: "capitalize",
                    }}>{d}</button>
                  ))}
                </div>
              </div>

              <div>
                <label style={{ fontSize: 11, color: "#4a8ab5", fontWeight: 600, letterSpacing: "0.08em", textTransform: "uppercase" }}>
                  Skills Adicionais
                </label>
                <div style={{ marginTop: 8 }}>
                  <button 
                    onClick={() => setRunAudit(!runAudit)}
                    style={{
                      width: "100%",
                      padding: "8px 12px",
                      borderRadius: 6,
                      border: runAudit ? "1px solid #10b981" : "1px solid #1e2d45",
                      background: runAudit ? "#10b98115" : "#0d1829",
                      color: runAudit ? "#10b981" : "#6b8aaa",
                      fontSize: 12, cursor: "pointer", fontWeight: 500,
                      display: "flex", alignItems: "center", gap: 8
                    }}
                  >
                    <span style={{ fontSize: 16 }}>{runAudit ? "🛡️" : "🛡️"}</span>
                    Auditoria de Segurança {runAudit ? "(Ativa)" : "(Inativa)"}
                  </button>
                </div>
              </div>

              <div style={{ flex: 1, display: "flex", flexDirection: "column" }}>
                <label style={{ fontSize: 11, color: "#4a8ab5", fontWeight: 600, letterSpacing: "0.08em", textTransform: "uppercase" }}>
                  Descrição da Solução
                </label>
                <textarea
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  placeholder="Descreva a arquitetura em linguagem natural. Ex: pipeline de ingestão batch com Glue, armazenamento no S3 em camadas, catálogo com Glue Catalog, consumo no Athena e dashboards no QuickSight..."
                  style={{
                    marginTop: 8,
                    flex: 1,
                    minHeight: 160,
                    background: "#0d1829",
                    border: "1px solid #1e2d45",
                    borderRadius: 8,
                    color: "#cbd5e1",
                    fontSize: 13,
                    padding: "12px 14px",
                    resize: "vertical",
                    outline: "none",
                    lineHeight: 1.6,
                    fontFamily: "inherit",
                  }}
                />
              </div>

              <button
                onClick={generate}
                disabled={loading || !description.trim()}
                style={{
                  padding: "12px 0",
                  borderRadius: 8,
                  border: "none",
                  background: loading || !description.trim()
                    ? "#1e2d45"
                    : "linear-gradient(135deg, #0ea5e9, #6366f1)",
                  color: loading || !description.trim() ? "#2d4060" : "#fff",
                  fontSize: 13,
                  fontWeight: 700,
                  cursor: loading || !description.trim() ? "not-allowed" : "pointer",
                  letterSpacing: "0.05em",
                  transition: "opacity 0.2s",
                }}
              >
                {loading ? "⟳  Gerando..." : "⬡  Gerar Diagrama"}
              </button>
            </div>

            <div style={{ flex: 1, padding: 32, display: "flex", flexDirection: "column", gap: 20, overflowY: "auto" }}>
              <div style={{
                background: "#0d1829",
                border: "1px solid #1e2d45",
                borderRadius: 12,
                flex: 1,
                display: "flex",
                flexDirection: "column",
                overflow: "hidden",
                minHeight: 400
              }}>
                <div style={{
                  padding: "12px 20px",
                  borderBottom: "1px solid #1e2d45",
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center"
                }}>
                  <div style={{ fontWeight: 600, fontSize: 13, color: "#e2e8f0" }}>
                    {archId ? `Visualização da Arquitetura (v${version})` : 'Código Python Gerado'}
                  </div>
                  {output && (
                    <button onClick={copy} style={{
                      background: copied ? "#10b98120" : "transparent",
                      border: copied ? "1px solid #10b98150" : "1px solid #4a6080",
                      color: copied ? "#10b981" : "#a8c7e8",
                      padding: "4px 12px", borderRadius: 4, fontSize: 12, cursor: "pointer",
                      transition: "all 0.2s"
                    }}>
                      {copied ? "Copiado!" : "Copiar Código"}
                    </button>
                  )}
                </div>

                <div style={{ flex: 1, display: "flex", flexDirection: "column", overflow: "hidden" }}>
                  {loading && (
                    <div style={{ flex: 1, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", gap: 16 }}>
                      <div style={{ width: 40, height: 40, border: "3px solid #1e2d45", borderTop: "3px solid #0ea5e9", borderRadius: "50%", animation: "spin 1s linear infinite" }} />
                      <div style={{ color: "#0ea5e9", fontSize: 14 }}>Gerando arquitetura...</div>
                      <style>{`@keyframes spin { to { transform: rotate(360deg); } }`}</style>
                    </div>
                  )}

                  {!loading && !output && (
                    <div style={{ flex: 1, display: "flex", alignItems: "center", justifyContent: "center" }}>
                      <div style={{ color: "#4a6080", fontSize: 14 }}>Preencha as configurações e clique em Gerar Diagrama.</div>
                    </div>
                  )}

                  {!loading && output && (
                    <>
                      {imageUrl && (
                        <div style={{ flex: 2, borderBottom: "1px solid #1e2d45", background: "white", display: "flex", justifyContent: "center", alignItems: "center", padding: 20 }}>
                          <img src={imageUrl} alt="Diagrama da Arquitetura" style={{ maxWidth: "100%", maxHeight: "100%", objectFit: "contain" }} />
                        </div>
                      )}
                      <div style={{ flex: imageUrl ? 1 : 2, overflowY: "auto", background: "#0a0f1a", padding: 20 }}>
                        <pre style={{ margin: 0, fontSize: 13, lineHeight: 1.6, fontFamily: "'JetBrains Mono', 'Fira Code', monospace", whiteSpace: "pre-wrap", wordBreak: "break-word" }}>
                          {output.split("\n").map((line, i) => {
                            const isComment = line.trim().startsWith("#");
                            const isImport = line.startsWith("from") || line.startsWith("import");
                            const isKeyword = /^\s*(with|for|if|def|class|return)\b/.test(line);
                            return (
                              <span key={i} style={{ color: isComment ? "#4a8060" : isImport ? "#c084fc" : isKeyword ? "#0ea5e9" : "#a8c7e8", display: "block" }}>{line}</span>
                            );
                          })}
                        </pre>
                      </div>
                    </>
                  )}
                </div>
              </div>

              {/* Área de Iteração */}
              {archId && !loading && (
                <div style={{ background: "#0d1829", border: "1px solid #1e2d45", borderRadius: 12, padding: 20, display: "flex", flexDirection: "column", gap: 12 }}>
                  <div style={{ fontSize: 13, fontWeight: 600, color: "#0ea5e9" }}>Refinar Diagrama</div>
                  <textarea
                    placeholder="Ex: Mude o banco de dados para PostgreSQL..."
                    value={iterationPrompt}
                    onChange={(e) => setIterationPrompt(e.target.value)}
                    style={{ background: "#0a0f1a", border: "1px solid #1e2d45", borderRadius: 8, padding: 12, color: "#e2e8f0", fontSize: 13, minHeight: 60, resize: "vertical" }}
                  />
                  <div style={{ display: "flex", gap: 12, justifyContent: "flex-end" }}>
                    <button onClick={() => { setArchId(""); setImageUrl(""); setOutput(""); setDescription(""); }} style={{ padding: "8px 16px", borderRadius: 8, border: "1px solid #4a6080", background: "transparent", color: "#a8c7e8", fontSize: 13, cursor: "pointer", fontWeight: 600 }}>Concluir / Nova Arquitetura</button>
                    <button onClick={generate} disabled={!iterationPrompt.trim() || loading} style={{ padding: "8px 16px", borderRadius: 8, background: "linear-gradient(135deg, #0ea5e9, #6366f1)", border: "none", color: "white", fontSize: 13, cursor: "pointer", fontWeight: 600, opacity: iterationPrompt.trim() ? 1 : 0.5 }}>Gerar nova versão</button>
                  </div>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Templates Tab */}
        {activeTab === "templates" && (
          <div style={{ flex: 1, padding: 32, overflowY: "auto" }}>
            <div style={{ marginBottom: 24 }}>
              <div style={{ fontSize: 18, fontWeight: 700, letterSpacing: "-0.3px" }}>
                Templates de Pré-Vendas
              </div>
              <div style={{ fontSize: 13, color: "#4a6080", marginTop: 4 }}>
                Padrões arquiteturais prontos para acelerar suas propostas
              </div>
            </div>
            <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(300px, 1fr))", gap: 16 }}>
              {TEMPLATES.map((tpl) => (
                <div key={tpl.label} style={{
                  background: "#0d1829",
                  border: "1px solid #1e2d45",
                  borderRadius: 10,
                  padding: 20,
                  cursor: "pointer",
                  transition: "border-color 0.2s",
                }} onMouseEnter={(e) => e.currentTarget.style.borderColor = "#0ea5e950"}
                  onMouseLeave={(e) => e.currentTarget.style.borderColor = "#1e2d45"}>
                  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 10 }}>
                    <div style={{ fontWeight: 700, fontSize: 14 }}>{tpl.label}</div>
                    <span style={{
                      background: "#0ea5e915",
                      border: "1px solid #0ea5e930",
                      color: "#0ea5e9",
                      fontSize: 10,
                      padding: "2px 8px",
                      borderRadius: 4,
                      fontWeight: 600,
                    }}>{tpl.cloud}</span>
                  </div>
                  <div style={{ fontSize: 11, color: "#6366f1", marginBottom: 8, fontWeight: 600 }}>
                    {tpl.pattern} · {tpl.detail}
                  </div>
                  <div style={{ fontSize: 12, color: "#4a6080", lineHeight: 1.6, marginBottom: 16 }}>
                    {tpl.description.slice(0, 120)}...
                  </div>
                  <button onClick={() => applyTemplate(tpl)} style={{
                    background: "linear-gradient(135deg, #0ea5e920, #6366f120)",
                    border: "1px solid #0ea5e940",
                    color: "#0ea5e9",
                    padding: "7px 16px",
                    borderRadius: 6,
                    fontSize: 12,
                    cursor: "pointer",
                    fontWeight: 600,
                    width: "100%",
                  }}>
                    Usar este template →
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}


