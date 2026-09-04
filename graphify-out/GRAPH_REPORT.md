# Graph Report - webAcademia  (2026-09-03)

## Corpus Check
- 44 files · ~123,346 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 337 nodes · 554 edges · 25 communities (23 shown, 2 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 46 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `6f08b8e2`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- adm_bp.py
- AlunoDAO
- professor_bp.py
- Aluno Detail (Admin) Page
- /graphify Command
- Exports & Benchmark Reference
- Python Dependencies (requirements.txt)
- pgAdm.js
- index.js
- preparar_url_banco
- Academia do Bitelo (brand name)
- graphify clone
- pgUsuario.js
- ProjetoWeb / Sistema-academia
- email_servico.py
- Writing apps with Prisma Composer
- Writing apps with Prisma Composer
- Writing apps with Prisma Composer
- Writing apps with Prisma Composer
- package.json
- TestAlteracaoCredenciais

## God Nodes (most connected - your core abstractions)
1. `AlunoDAO` - 32 edges
2. `ProfessorDAO` - 16 edges
3. `Writing apps with Prisma Composer` - 15 edges
4. `Writing apps with Prisma Composer` - 15 edges
5. `Writing apps with Prisma Composer` - 15 edges
6. `Writing apps with Prisma Composer` - 15 edges
7. `enviar_email()` - 13 edges
8. `detalhes_usuario()` - 12 edges
9. `pagina_cadastro()` - 10 edges
10. `AvaliacaoDAO` - 10 edges

## Surprising Connections (you probably didn't know these)
- `painel_adm()` --uses--> `AlunoDAO`  [INFERRED]
  blueprints/adm_bp.py → dao/usuarioDAO.py
- `enviar_recado()` --uses--> `AlunoDAO`  [INFERRED]
  blueprints/adm_bp.py → dao/usuarioDAO.py
- `cadastrar_professor()` --uses--> `ProfessorDAO`  [INFERRED]
  blueprints/adm_bp.py → dao/professorDAO.py
- `cadastrar_professor()` --uses--> `Professor`  [INFERRED]
  blueprints/adm_bp.py → modelos/professor.py
- `alterar_mensalidade()` --uses--> `AlunoDAO`  [INFERRED]
  blueprints/adm_bp.py → dao/usuarioDAO.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Gym Brand Identity Composition** — static_imagens_logo_academia_do_bitelo_brand, static_imagens_logo_bodybuilder_mascot, static_imagens_logo_forca_resistencia_tagline, static_imagens_logo_gear_badge_design [EXTRACTED 0.95]
- **Admin Student Management Flow** — templates_pgadm_page, templates_dt_aluno_page, templates_components_confirm_modal_dialog [EXTRACTED 1.00]
- **Email-Verified Profile Edit Flow** — templates_editar_perfil_page, templates_verificar_codigo_page, templates_pgusuario_page [EXTRACTED 1.00]
- **Authentication & Onboarding Flow** — templates_index_page, templates_login_page, templates_cadastro_page, templates_recuperar_page [INFERRED 0.85]

## Communities (25 total, 2 thin omitted)

### Community 0 - "adm_bp.py"
Cohesion: 0.10
Nodes (17): cadastrar_plano(), detalhes_usuario(), enviar_recado(), painel_adm(), route, remover_plano(), remover_professor(), PlanoDAO (+9 more)

### Community 1 - "AlunoDAO"
Cohesion: 0.13
Nodes (25): cadastrar_professor(), remover_usuario(), atualizar_preferencias_email(), cancelar_alteracao(), editar_perfil(), mascarar_email(), pagina_cadastro(), pagina_login() (+17 more)

### Community 2 - "professor_bp.py"
Cohesion: 0.26
Nodes (8): cadastrar_avaliacao(), detalhes_aluno_professor(), _guard(), painel_professor(), route, remover_avaliacao(), AvaliacaoDAO, Avaliacao

### Community 3 - "Aluno Detail (Admin) Page"
Cohesion: 0.13
Nodes (22): Cadastro Form, Cadastro (Registration) Page, Confirm Dialog Component, Aluno Profile Update Form, Mensalidade (Payment) Launch Form, Aluno Detail (Admin) Page, Editar Credenciais Form, Editar Perfil (Edit Profile) Page (+14 more)

### Community 4 - "/graphify Command"
Cohesion: 0.15
Nodes (18): /graphify Trigger (Local Skill Reference), Project Graphify Usage Rules, Add & Watch Reference, /graphify add, --watch Mode, graphify claude install, Commit Hook & CLAUDE.md Integration Reference, graphify hook install (post-commit) (+10 more)

### Community 5 - "Exports & Benchmark Reference"
Cohesion: 0.11
Nodes (19): Token Reduction Benchmark, Exports & Benchmark Reference, FalkorDB Export, MCP Server, Neo4j Export, Wiki Export, Confidence Score Rubric, Extraction Subagent Prompt Spec (+11 more)

### Community 6 - "Python Dependencies (requirements.txt)"
Cohesion: 0.22
Nodes (11): Flask, Flask-SQLAlchemy, gunicorn, litellm, openai, psycopg2-binary, pydantic, python-dotenv (+3 more)

### Community 7 - "pgAdm.js"
Cohesion: 0.20
Nodes (10): atualizarListaDeAlunos(), avisoSemResultados, campoBusca, campoDuracao, campoPreco, contadorAlunos, formatadorDePreco, formularioPlano (+2 more)

### Community 8 - "index.js"
Cohesion: 0.29
Nodes (3): icone_senha, input_senha, modal

### Community 9 - "preparar_url_banco"
Cohesion: 0.29
Nodes (5): opcoes_engine(), preparar_url_banco(), Evita conexões inativas após pausas ou reciclagens do pool remoto., Normaliza a URL do PostgreSQL e habilita SSL para o Supabase., TestConfiguracaoBanco

### Community 10 - "Academia do Bitelo (brand name)"
Cohesion: 0.70
Nodes (5): Academia do Bitelo (brand name), Bearded Bodybuilder Mascot Illustration, "Força & Resistência" Tagline, Gear-shaped Badge Emblem Design, Academia do Bitelo Logo

### Community 11 - "graphify clone"
Cohesion: 1.00
Nodes (3): graphify clone, GitHub Clone & Cross-Repo Merge Reference, graphify merge-graphs

### Community 17 - "email_servico.py"
Cohesion: 0.10
Nodes (22): alterar_mensalidade(), atualizar_status_pagamento(), cadastrar_pagamento(), PagamentoDAO, enviar_aviso_pagamento_atrasado(), enviar_aviso_status_mensalidade(), enviar_confirmacao_pagamento(), enviar_email() (+14 more)

### Community 18 - "Writing apps with Prisma Composer"
Cohesion: 0.10
Nodes (19): Anatomy of a service, Builds are yours, Databases, Deploy config, Deploying, Driving deploys from code, Object Storage, Production pitfalls (+11 more)

### Community 19 - "Writing apps with Prisma Composer"
Cohesion: 0.10
Nodes (19): Anatomy of a service, Builds are yours, Databases, Deploy config, Deploying, Driving deploys from code, Object Storage, Production pitfalls (+11 more)

### Community 20 - "Writing apps with Prisma Composer"
Cohesion: 0.10
Nodes (19): Anatomy of a service, Builds are yours, Databases, Deploy config, Deploying, Driving deploys from code, Object Storage, Production pitfalls (+11 more)

### Community 21 - "Writing apps with Prisma Composer"
Cohesion: 0.10
Nodes (19): Anatomy of a service, Builds are yours, Databases, Deploy config, Deploying, Driving deploys from code, Object Storage, Production pitfalls (+11 more)

### Community 22 - "package.json"
Cohesion: 0.33
Nodes (5): devDependencies, prisma, scripts, postinstall, prisma

### Community 24 - "TestAlteracaoCredenciais"
Cohesion: 0.25
Nodes (3): patch, TestAlteracaoCredenciais, TestEmailServico

## Knowledge Gaps
- **97 isolated node(s):** `formatadorDePreco`, `gradePlanos`, `Anatomy of a service`, `Builds are yours`, `Databases` (+92 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `AlunoDAO` connect `AlunoDAO` to `adm_bp.py`, `email_servico.py`, `professor_bp.py`?**
  _High betweenness centrality (0.045) - this node is a cross-community bridge._
- **Why does `ProfessorDAO` connect `adm_bp.py` to `AlunoDAO`, `professor_bp.py`?**
  _High betweenness centrality (0.013) - this node is a cross-community bridge._
- **Why does `cadastrar_pagamento()` connect `email_servico.py` to `adm_bp.py`, `AlunoDAO`?**
  _High betweenness centrality (0.010) - this node is a cross-community bridge._
- **Are the 16 inferred relationships involving `AlunoDAO` (e.g. with `alterar_mensalidade()` and `cadastrar_pagamento()`) actually correct?**
  _`AlunoDAO` has 16 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `ProfessorDAO` (e.g. with `cadastrar_professor()` and `detalhes_usuario()`) actually correct?**
  _`ProfessorDAO` has 7 INFERRED edges - model-reasoned connections that need verification._
- **What connects `formatadorDePreco`, `gradePlanos`, `Anatomy of a service` to the rest of the system?**
  _97 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `adm_bp.py` be split into smaller, more focused modules?**
  _Cohesion score 0.09872241579558652 - nodes in this community are weakly interconnected._