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
