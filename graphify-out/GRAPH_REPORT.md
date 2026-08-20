# Graph Report - webAcademia  (2026-08-19)

## Corpus Check
- 44 files · ~98,107 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 201 nodes · 367 edges · 17 communities (15 shown, 2 thin omitted)
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 42 edges (avg confidence: 0.92)
- Token cost: 167,487 input · 0 output

## Community Hubs (Navigation)
- Admin Panel & Payments Backend
- User Auth & Profile Flow
- Email Service & User Model Tests
- Frontend Templates
- Graphify Skill - Core Pipeline
- Graphify Skill - Exports & Extraction Spec
- Python Dependencies
- Admin Panel JS
- Landing Page JS
- Flask Server Entrypoint
- Gym Brand Logo
- Graphify - GitHub & Merge
- User Panel JS
- Project README

## God Nodes (most connected - your core abstractions)
1. `AlunoDAO` - 28 edges
2. `PlanoDAO` - 14 edges
3. `PagamentoDAO` - 12 edges
4. `detalhes_usuario()` - 10 edges
5. `cadastrar_pagamento()` - 10 edges
6. `pagina_cadastro()` - 10 edges
7. `Aluno` - 10 edges
8. `Python Dependencies (requirements.txt)` - 10 edges
9. `enviar_email()` - 9 edges
10. `pagina_perfil()` - 8 edges

## Surprising Connections (you probably didn't know these)
- `painel_adm()` --uses--> `AlunoDAO`  [INFERRED]
  blueprints/adm_bp.py → dao/usuarioDAO.py
- `remover_usuario()` --uses--> `AlunoDAO`  [INFERRED]
  blueprints/adm_bp.py → dao/usuarioDAO.py
- `alterar_mensalidade()` --uses--> `AlunoDAO`  [INFERRED]
  blueprints/adm_bp.py → dao/usuarioDAO.py
- `detalhes_usuario()` --uses--> `AlunoDAO`  [INFERRED]
  blueprints/adm_bp.py → dao/usuarioDAO.py
- `cadastrar_pagamento()` --uses--> `AlunoDAO`  [INFERRED]
  blueprints/adm_bp.py → dao/usuarioDAO.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Authentication & Onboarding Flow** — templates_index_page, templates_login_page, templates_cadastro_page, templates_recuperar_page [INFERRED 0.85]
- **Email-Verified Profile Edit Flow** — templates_editar_perfil_page, templates_verificar_codigo_page, templates_pgusuario_page [EXTRACTED 1.00]
- **Admin Student Management Flow** — templates_pgadm_page, templates_dt_aluno_page, templates_components_confirm_modal_dialog [EXTRACTED 1.00]
- **Gym Brand Identity Composition** — static_imagens_logo_academia_do_bitelo_brand, static_imagens_logo_bodybuilder_mascot, static_imagens_logo_forca_resistencia_tagline, static_imagens_logo_gear_badge_design [EXTRACTED 0.95]

## Communities (17 total, 2 thin omitted)

### Community 0 - "Admin Panel & Payments Backend"
Cohesion: 0.13
Nodes (13): alterar_mensalidade(), atualizar_status_pagamento(), cadastrar_pagamento(), cadastrar_plano(), detalhes_usuario(), painel_adm(), route, remover_plano() (+5 more)

### Community 1 - "User Auth & Profile Flow"
Cohesion: 0.18
Nodes (21): cancelar_alteracao(), editar_perfil(), mascarar_email(), pagina_cadastro(), pagina_login(), pagina_perfil(), route, recuperar_senha() (+13 more)

### Community 2 - "Email Service & User Model Tests"
Cohesion: 0.13
Nodes (14): Aluno, patch, enviar_confirmacao_pagamento(), enviar_email(), _enviar_email_brevo(), _enviar_email_resend(), _formatar_rotulo_forma_pagamento(), obter_configuracoes_email() (+6 more)

### Community 3 - "Frontend Templates"
Cohesion: 0.13
Nodes (22): Cadastro Form, Cadastro (Registration) Page, Confirm Dialog Component, Aluno Profile Update Form, Mensalidade (Payment) Launch Form, Aluno Detail (Admin) Page, Editar Credenciais Form, Editar Perfil (Edit Profile) Page (+14 more)

### Community 4 - "Graphify Skill - Core Pipeline"
Cohesion: 0.14
Nodes (19): /graphify Trigger (Local Skill Reference), Project Graphify Usage Rules, Add & Watch Reference, /graphify add, --watch Mode, graphify claude install, Commit Hook & CLAUDE.md Integration Reference, graphify hook install (post-commit) (+11 more)

### Community 5 - "Graphify Skill - Exports & Extraction Spec"
Cohesion: 0.12
Nodes (18): Token Reduction Benchmark, Exports & Benchmark Reference, FalkorDB Export, MCP Server, Neo4j Export, Wiki Export, Confidence Score Rubric, Extraction Subagent Prompt Spec (+10 more)

### Community 6 - "Python Dependencies"
Cohesion: 0.22
Nodes (11): Flask, Flask-SQLAlchemy, gunicorn, litellm, openai, psycopg2-binary, pydantic, python-dotenv (+3 more)

### Community 7 - "Admin Panel JS"
Cohesion: 0.20
Nodes (10): atualizarListaDeAlunos(), avisoSemResultados, campoBusca, campoDuracao, campoPreco, contadorAlunos, formatadorDePreco, formularioPlano (+2 more)

### Community 8 - "Landing Page JS"
Cohesion: 0.29
Nodes (3): icone_senha, input_senha, modal

### Community 9 - "Flask Server Entrypoint"
Cohesion: 0.53
Nodes (5): home(), logout(), pagina_cadastro(), pagina_login(), route

### Community 10 - "Gym Brand Logo"
Cohesion: 0.70
Nodes (5): Academia do Bitelo (brand name), Bearded Bodybuilder Mascot Illustration, "Força & Resistência" Tagline, Gear-shaped Badge Emblem Design, Academia do Bitelo Logo

### Community 11 - "Graphify - GitHub & Merge"
Cohesion: 1.00
Nodes (3): graphify clone, GitHub Clone & Cross-Repo Merge Reference, graphify merge-graphs

## Knowledge Gaps
- **31 isolated node(s):** `modal`, `input_senha`, `icone_senha`, `campoBusca`, `linhasDeAlunos` (+26 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `AlunoDAO` connect `User Auth & Profile Flow` to `Admin Panel & Payments Backend`, `Email Service & User Model Tests`?**
  _High betweenness centrality (0.055) - this node is a cross-community bridge._
- **Why does `Aluno` connect `Email Service & User Model Tests` to `Admin Panel & Payments Backend`, `User Auth & Profile Flow`?**
  _High betweenness centrality (0.019) - this node is a cross-community bridge._
- **Are the 13 inferred relationships involving `AlunoDAO` (e.g. with `alterar_mensalidade()` and `cadastrar_pagamento()`) actually correct?**
  _`AlunoDAO` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `PlanoDAO` (e.g. with `cadastrar_pagamento()` and `cadastrar_plano()`) actually correct?**
  _`PlanoDAO` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `PagamentoDAO` (e.g. with `atualizar_status_pagamento()` and `cadastrar_pagamento()`) actually correct?**
  _`PagamentoDAO` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `detalhes_usuario()` (e.g. with `PagamentoDAO` and `PlanoDAO`) actually correct?**
  _`detalhes_usuario()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `cadastrar_pagamento()` (e.g. with `PagamentoDAO` and `PlanoDAO`) actually correct?**
  _`cadastrar_pagamento()` has 4 INFERRED edges - model-reasoned connections that need verification._