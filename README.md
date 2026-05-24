# Extrator de Dados Estruturados de Documentos (Engine de Inteligência Financeira)

Uma aplicação nativa em Python voltada para engenharia de dados financeiros. O sistema realiza o parsing de arquivos bancários brutos no formato `OFX`, isola e higieniza os dados contra ataques de *Prompt Injection*, e utiliza modelos de linguagem grandes (LLMs) para categorização comportamental e geração de insights de economia de forma 100% estruturada, tipada e validada.

---

## 🛠️ Tecnologias e Ferramentas

- **Python 3.13+** — Core do projeto
- **Google GenAI SDK** — Integração direta com o modelo `gemini-2.5-flash`
- **Pydantic** — Validação determinística de dados e garantia de types
- **OfxParse** — Parser para tratamento do formato semi-estruturado OFX
- **Pytest** — Framework de testes para validação de contratos e TDD

---

## 🏗️ Arquitetura e Padrões de Projeto

O projeto foi desenhado seguindo os princípios do **SOLID** (foco em Responsabilidade Única e Desacoplamento) e desenvolvido utilizando **TDD (Test-Driven Development)**.

```
src/
├── connectors/     # Camada de infraestrutura — ingestão e parsing do arquivo OFX bruto
├── extractors/     # Camada de IA — comunicação com a API de LLM e retorno estruturado
│   ├── base_extractor.py    # Contrato abstrato (Open/Closed — troca de provider sem modificar código)
│   └── gemini_extractor.py  # Implementação concreta com Google Gemini
└── validators/     # Camada de domínio — regras de negócio e validação rígida de dados
```

### Decisões de Design

- **Dependency Inversion:** o `GeminiExtractor` recebe o client como dependência injetada, eliminando o acoplamento direto com a infraestrutura e tornando a classe testável de forma isolada.
- **Open/Closed:** `BaseExtractor` define o contrato abstrato. Adicionar suporte a OpenAI ou Claude exige apenas uma nova classe — sem modificar código existente.
- **Single Responsibility:** cada camada possui uma única razão para mudar. O connector não conhece IA; o extractor não conhece arquivos OFX.

---

## 🔒 Estratégia de Segurança em 3 Camadas (Zero-Trust AI)

Para evitar que comandos maliciosos embutidos nas descrições de transações bancárias (como tentativas de *Jailbreak* ou injeções de código) afetem o sistema, a aplicação implementa:

1. **Separação de Contexto (Camada 1):** Os dados extraídos do OFX são injetados de forma estritamente passiva na API, isolados das instruções de sistema do modelo.

2. **Privilégio Mínimo via Saída Estruturada (Camada 2):** A chamada da API exige nativamente um *Response Schema* baseado em Pydantic, impedindo que o modelo retorne texto livre ou códigos executáveis (ex: Javascript loops).

3. **Validação Determinística Externa (Camada 3):** O payload JSON gerado pela IA é interceptado pelo código Python, onde validadores customizados do Pydantic checam ranges numéricos e regras de negócio de forma isolada do modelo.

---

## 🧪 Suíte de Testes

O projeto conta com cobertura de testes unitários e de integração para garantir a estabilidade do pipeline de dados.

| Arquivo              | Tipo       | O que valida                                                  |
| -------------------- | ---------- | ------------------------------------------------------------- |
| `test_connectors.py` | Integração | Parsing do OFX real e estrutura do dicionário retornado       |
| `test_extractors.py` | Unitário   | Contrato do extrator com mock do client — sem chamada de rede |

Para rodar os testes:

```bash
pytest
```

---

## 🚀 Como Executar o Projeto

**1. Clone o repositório:**

```bash
git clone https://github.com/ViniciusOliver-stack/extrator-dados-estruturados-documentos.git
cd extrator-dados-estruturados-documentos
```

**2. Configure o ambiente virtual (Windows):**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**3. Instale as dependências:**

```bash
pip install -r requirements.txt
```

**4. Configure suas credenciais:**

Copie o arquivo `.env.example` para `.env` e insira sua chave do Google AI Studio:

```env
GEMINI_API_KEY=sua_chave_secreta_aqui
```

**5. Adicione seu arquivo OFX:**

Coloque seu arquivo bancário `.ofx` na raiz do projeto com o nome `NU_FILE.ofx`.

**6. Execute a aplicação:**

```bash
python main.py
```

O resultado será salvo em `insight_financeiro.json` na raiz do projeto.
