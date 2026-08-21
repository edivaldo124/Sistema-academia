# Graph Report - webAcademia  (2026-08-20)

## Corpus Check
- 32 files · ~100,137 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 211 nodes · 365 edges · 17 communities (15 shown, 2 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 19 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `70584905`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- adm_bp.py
- usuario_bp.py
- email_servico.py
- Aluno Detail (Admin) Page
- /graphify Command
- Exports & Benchmark Reference
- Python Dependencies (requirements.txt)
- pgAdm.js
- index.js
- Aluno
- Academia do Bitelo (brand name)
- graphify clone
- pgUsuario.js
- ProjetoWeb / Sistema-academia

## God Nodes (most connected - your core abstractions)
1. `AlunoDAO` - 15 edges
2. `enviar_email()` - 13 edges
3. `Aluno` - 10 edges
4. `Python Dependencies (requirements.txt)` - 10 edges
5. `detalhes_usuario()` - 9 edges
6. `pagina_cadastro()` - 9 edges
7. `cadastrar_pagamento()` - 8 edges
8. `pagina_perfil()` - 7 edges
9. `editar_perfil()` - 7 edges
10. `enviar_notificacao_plano()` - 7 edges

## Surprising Connections (you probably didn't know these)
- `pagina_cadastro()` --uses--> `Aluno`  [INFERRED]
  blueprints/usuario_bp.py → modelos/usuario.py
- `recuperar_senha()` --uses--> `Aluno`  [INFERRED]
  blueprints/usuario_bp.py → modelos/usuario.py
- `AlunoDAO` --uses--> `Aluno`  [INFERRED]
  dao/usuarioDAO.py → modelos/usuario.py
- `AlunoDAO` --uses--> `Plano`  [INFERRED]
  dao/usuarioDAO.py → modelos/plano.py
- `enviar_recado()` --calls--> `enviar_recado_admin()`  [EXTRACTED]
  blueprints/adm_bp.py → servicos/email_servico.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Gym Brand Identity Composition** — static_imagens_logo_academia_do_bitelo_brand, static_imagens_logo_bodybuilder_mascot, static_imagens_logo_forca_resistencia_tagline, static_imagens_logo_gear_badge_design [EXTRACTED 0.95]
- **Admin Student Management Flow** — templates_pgadm_page, templates_dt_aluno_page, templates_components_confirm_modal_dialog [EXTRACTED 1.00]
- **Email-Verified Profile Edit Flow** — templates_editar_perfil_page, templates_verificar_codigo_page, templates_pgusuario_page [EXTRACTED 1.00]
- **Authentication & Onboarding Flow** — templates_index_page, templates_login_page, templates_cadastro_page, templates_recuperar_page [INFERRED 0.85]

## Communities (17 total, 2 thin omitted)

### Community 0 - "adm_bp.py"
Cohesion: 0.11
Nodes (14): alterar_mensalidade(), atualizar_status_pagamento(), cadastrar_pagamento(), cadastrar_plano(), detalhes_usuario(), enviar_recado(), painel_adm(), route (+6 more)

### Community 1 - "usuario_bp.py"
Cohesion: 0.16
Nodes (20): atualizar_preferencias_email(), cancelar_alteracao(), editar_perfil(), mascarar_email(), pagina_cadastro(), pagina_login(), pagina_perfil(), route (+12 more)

### Community 2 - "email_servico.py"
Cohesion: 0.11
Nodes (22): patch, enviar_aviso_pagamento_atrasado(), enviar_aviso_status_mensalidade(), enviar_confirmacao_pagamento(), enviar_email(), enviar_email_boas_vindas(), _enviar_email_brevo(), _enviar_email_resend() (+14 more)

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

### Community 9 - "Aluno"
Cohesion: 0.21
Nodes (7): Aluno, home(), logout(), pagina_cadastro(), pagina_login(), route, TestAlteracaoCredenciais

### Community 10 - "Academia do Bitelo (brand name)"
Cohesion: 0.70
Nodes (5): Academia do Bitelo (brand name), Bearded Bodybuilder Mascot Illustration, "Força & Resistência" Tagline, Gear-shaped Badge Emblem Design, Academia do Bitelo Logo

### Community 11 - "graphify clone"
Cohesion: 1.00
Nodes (3): graphify clone, GitHub Clone & Cross-Repo Merge Reference, graphify merge-graphs

## Knowledge Gaps
- **31 isolated node(s):** `formatadorDePreco`, `gradePlanos`, `avisoSemResultados`, `campoBusca`, `campoDuracao` (+26 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `AlunoDAO` connect `usuario_bp.py` to `adm_bp.py`, `Aluno`?**
  _High betweenness centrality (0.029) - this node is a cross-community bridge._
- **Why does `Aluno` connect `Aluno` to `adm_bp.py`, `usuario_bp.py`?**
  _High betweenness centrality (0.021) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `AlunoDAO` (e.g. with `Plano` and `Aluno`) actually correct?**
  _`AlunoDAO` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `Aluno` (e.g. with `pagina_cadastro()` and `recuperar_senha()`) actually correct?**
  _`Aluno` has 4 INFERRED edges - model-reasoned connections that need verification._
- **What connects `formatadorDePreco`, `gradePlanos`, `avisoSemResultados` to the rest of the system?**
  _31 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `adm_bp.py` be split into smaller, more focused modules?**
  _Cohesion score 0.1126984126984127 - nodes in this community are weakly interconnected._
- **Should `email_servico.py` be split into smaller, more focused modules?**
  _Cohesion score 0.11384615384615385 - nodes in this community are weakly interconnected._