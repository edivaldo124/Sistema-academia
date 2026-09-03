# ProjetoWeb
# Sistema-academia

## Deploy no Render com banco no Supabase

O sistema acessa o PostgreSQL do Supabase diretamente pelo SQLAlchemy; não é
necessário usar o pacote `supabase-py` para os DAOs existentes.

1. No painel do Supabase, clique em **Connect** e copie a URI do
   **Session pooler**, na porta `5432`.
2. No Render, crie um **Blueprint** usando o `render.yaml` deste repositório.
3. Quando solicitado, informe a URI do Supabase em `DATABASE_URL`, substituindo
   o marcador da senha pela senha real do banco.
4. Faça o deploy. O Render instala `requirements.txt` e inicia a aplicação com
   `gunicorn servidor:app`.

O `.env` é somente para desenvolvimento local e não deve ser enviado ao Git.
No Render, `DATABASE_URL` e outros segredos ficam em **Environment**. Depois de
alterar uma variável, salve e faça um novo deploy do serviço.

Na primeira conexão, o SQLAlchemy cria as tabelas `alunos`, `planos` e
`pagamentos` caso ainda não existam. A conexão com hosts do Supabase recebe
automaticamente `sslmode=require`.
