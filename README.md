# ProjetoWeb
# Sistema-academia

## Configuração de e-mail

O projeto envia avisos usando Gmail SMTP. Copie `.env.example` para `.env` e
preencha `MAIL_USERNAME`, `MAIL_PASSWORD` e `MAIL_DEFAULT_SENDER`. Em
`MAIL_PASSWORD`, use uma senha de aplicativo nova do Google, nunca a senha
normal da conta.

O arquivo `.env` é ignorado pelo Git e não deve ser compartilhado. Para testar
a configuração sem criar uma rota pública, execute:

```bash
flask --app servidor testar-email destinatario@example.com
```

Em produção, configure também `SECRET_KEY` com um valor longo e aleatório e
`APP_BASE_URL` com o endereço público HTTPS da aplicação.

### Configuração no Render

O Render não lê o arquivo `.env` do seu computador. No serviço publicado, abra
**Environment** e cadastre individualmente as variáveis `MAIL_SERVER`,
`MAIL_PORT`, `MAIL_USE_TLS`, `MAIL_USERNAME`, `MAIL_PASSWORD`,
`MAIL_DEFAULT_SENDER` e `MAIL_SENDER_NAME` descritas no `.env.example`.

Para Gmail, `MAIL_PASSWORD` deve ser uma senha de app gerada pela conta Google,
sem aspas. O texto `senha_de_aplicativo_sem_espacos` é apenas um exemplo e é
rejeitado pela aplicação. Depois de salvar as variáveis, faça um novo deploy e
teste no Shell do Render com:

```bash
flask --app servidor testar-email seu_email@gmail.com
```
