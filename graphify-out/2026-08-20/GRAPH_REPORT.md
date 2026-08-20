# Graph Report - webAcademia  (2026-08-20)

## Corpus Check
- 32 files · ~99,532 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 207 nodes · 388 edges · 18 communities (16 shown, 2 thin omitted)
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 42 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `0e4688d3`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- AlunoDAO
- usuario_bp.py
- email_servico.py
- Aluno Detail (Admin) Page
- /graphify Command
- Exports & Benchmark Reference
- Python Dependencies (requirements.txt)
- pgAdm.js
- index.js
- adm_bp.py
- Academia do Bitelo (brand name)
- graphify clone
- pgUsuario.js
- ProjetoWeb / Sistema-academia
- TestAlteracaoCredenciais

## God Nodes (most connected - your core abstractions)
1. `AlunoDAO` - 28 edges
2. `PlanoDAO` - 14 edges
3. `detalhes_usuario()` - 12 edges
4. `PagamentoDAO` - 12 edges
5. `enviar_email()` - 12 edges
6. `cadastrar_pagamento()` - 11 edges
7. `pagina_cadastro()` - 10 edges
8. `pagina_perfil()` - 10 edges
9. `Aluno` - 10 edges
10. `Python Dependencies (requirements.txt)` - 10 edges

## Surprising Connections (you probably didn't know these)
- `cadastrar_plano()` --uses--> `Plano`  [INFERRED]
  blueprints/adm_bp.py → modelos/plano.py
- `cadastrar_pagamento()` --uses--> `Pagamento`  [INFERRED]
  blueprints/adm_bp.py → modelos/pagamento.py
- `pagina_login()` --uses--> `AlunoDAO`  [INFERRED]
  blueprints/usuario_bp.py → dao/usuarioDAO.py
- `pagina_cadastro()` --uses--> `AlunoDAO`  [INFERRED]
  blueprints/usuario_bp.py → dao/usuarioDAO.py
- `editar_perfil()` --uses--> `AlunoDAO`  [INFERRED]
  blueprints/usuario_bp.py → dao/usuarioDAO.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Gym Brand Identity Composition** — static_imagens_logo_academia_do_bitelo_brand, static_imagens_logo_bodybuilder_mascot, static_imagens_logo_forca_resistencia_tagline, static_imagens_logo_gear_badge_design [EXTRACTED 0.95]
- **Admin Student Management Flow** — templates_pgadm_page, templates_dt_aluno_page, templates_components_confirm_modal_dialog [EXTRACTED 1.00]
- **Email-Verified Profile Edit Flow** — templates_editar_perfil_page, templates_verificar_codigo_page, templates_pgusuario_page [EXTRACTED 1.00]
- **Authentication & Onboarding Flow** — templates_index_page, templates_login_page, templates_cadastro_page, templates_recuperar_page [INFERRED 0.85]

## Communities (18 total, 2 thin omitted)

### Community 0 - "AlunoDAO"
Cohesion: 0.14
Nodes (13): alterar_mensalidade(), atualizar_status_pagamento(), cadastrar_pagamento(), cadastrar_plano(), detalhes_usuario(), painel_adm(), route, remover_plano() (+5 more)

### Community 1 - "usuario_bp.py"
Cohesion: 0.19
Nodes (20): cancelar_alteracao(), editar_perfil(), mascarar_email(), pagina_cadastro(), pagina_login(), route, recuperar_senha(), reenviar_codigo() (+12 more)

### Community 2 - "email_servico.py"
Cohesion: 0.18
Nodes (16): enviar_aviso_pagamento_atrasado(), enviar_aviso_status_mensalidade(), enviar_confirmacao_pagamento(), enviar_email(), _enviar_email_brevo(), _enviar_email_resend(), enviar_notificacao_plano(), _formatar_rotulo_forma_pagamento() (+8 more)

### Community 3 - "Aluno Detail (Admin) Page"
Cohesion: 0.13
Nodes (22): Cadastro Form, Cadastro (Registration) Page, Confirm Dialog Component, Aluno Profile Update Form, Mensalidade (Payment) Launch Form, Aluno Detail (Admin) Page, Editar Credenciais Form, Editar Perfil (Edit Profile) Page (+14 more)

### Community 4 - "/graphify Command"
Cohesion: 0.14
Nodes (19): /graphify Trigger (Local Skill Reference), Project Graphify Usage Rules, Add & Watch Reference, /graphify add, --watch Mode, graphify claude install, Commit Hook & CLAUDE.md Integration Reference, graphify hook install (post-commit) (+11 more)

### Community 5 - "Exports & Benchmark Reference"
Cohesion: 0.12
Nodes (18): Token Reduction Benchmark, Exports & Benchmark Reference, FalkorDB Export, MCP Server, Neo4j Export, Wiki Export, Confidence Score Rubric, Extraction Subagent Prompt Spec (+10 more)

### Community 6 - "Python Dependencies (requirements.txt)"
Cohesion: 0.22
Nodes (11): Flask, Flask-SQLAlchemy, gunicorn, litellm, openai, psycopg2-binary, pydantic, python-dotenv (+3 more)

### Community 7 - "pgAdm.js"
Cohesion: 0.20
Nodes (10): atualizarListaDeAlunos(), avisoSemResultados, campoBusca, campoDuracao, campoPreco, contadorAlunos, formatadorDePreco, formularioPlano (+2 more)

### Community 8 - "index.js"
Cohesion: 0.29
Nodes (3): icone_senha, input_senha, modal

### Community 9 - "adm_bp.py"
Cohesion: 0.23
Nodes (7): Pagamento, Plano, home(), logout(), pagina_cadastro(), pagina_login(), route

### Community 10 - "Academia do Bitelo (brand name)"
Cohesion: 0.70
Nodes (5): Academia do Bitelo (brand name), Bearded Bodybuilder Mascot Illustration, "Força & Resistência" Tagline, Gear-shaped Badge Emblem Design, Academia do Bitelo Logo

### Community 11 - "graphify clone"
Cohesion: 1.00
Nodes (3): graphify clone, GitHub Clone & Cross-Repo Merge Reference, graphify merge-graphs

### Community 17 - "TestAlteracaoCredenciais"
Cohesion: 0.25
Nodes (3): patch, TestAlteracaoCredenciais, TestEmailServico

## Knowledge Gaps
- **31 isolated node(s):** `modal`, `input_senha`, `icone_senha`, `campoBusca`, `linhasDeAlunos` (+26 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `AlunoDAO` connect `AlunoDAO` to `adm_bp.py`, `usuario_bp.py`?**
  _High betweenness centrality (0.054) - this node is a cross-community bridge._
- **Why does `Aluno` connect `usuario_bp.py` to `AlunoDAO`, `adm_bp.py`, `TestAlteracaoCredenciais`?**
  _High betweenness centrality (0.019) - this node is a cross-community bridge._
- **Are the 13 inferred relationships involving `AlunoDAO` (e.g. with `alterar_mensalidade()` and `cadastrar_pagamento()`) actually correct?**
  _`AlunoDAO` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `PlanoDAO` (e.g. with `cadastrar_pagamento()` and `cadastrar_plano()`) actually correct?**
  _`PlanoDAO` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `detalhes_usuario()` (e.g. with `PagamentoDAO` and `PlanoDAO`) actually correct?**
  _`detalhes_usuario()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `PagamentoDAO` (e.g. with `atualizar_status_pagamento()` and `cadastrar_pagamento()`) actually correct?**
  _`PagamentoDAO` has 5 INFERRED edges - model-reasoned connections that need verification._
- **What connects `modal`, `input_senha`, `icone_senha` to the rest of the system?**
  _31 weakly-connected nodes found - possible documentation gaps or missing edges._