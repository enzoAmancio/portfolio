# 📧 Sistema de Envio de Email - Portfólio

Backend simples em Python/Flask para envio de emails do portfólio com template HTML personalizado.

## ✨ Funcionalidade Principal

Quando alguém entra em contato através do formulário:

1. **Você recebe um email** 📬 com a mensagem completa (decorado com o design do portfólio)
2. **O visitante recebe uma confirmação** ✅ automática decorada com o design do seu portfólio

Perfeito para manter a profissionalidade e a marca visual consistente!

## 🚀 Configuração

### 1. Instalar Dependências

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configurar SMTP (Gmail)

1. **Ativar Verificação em 2 Etapas no Gmail:**
   - Acesse: https://myaccount.google.com/security
   - Ative a "Verificação em duas etapas"

2. **Gerar Senha de App:**
   - Vá em "Senhas de app" (https://myaccount.google.com/apppasswords)
   - Selecione "Email" como app e "Outro" como dispositivo
   - Copie a senha gerada (16 caracteres)

3. **Criar arquivo .env:**
   ```bash
   cp .env.example .env
   ```

4. **Editar .env com suas credenciais:**
   ```env
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   SMTP_EMAIL=seu-email@gmail.com
   SMTP_PASSWORD=xxxx xxxx xxxx xxxx  # Senha de app gerada
   RECIPIENT_EMAIL=enzoamancio17@gmail.com
   ```

### 3. Executar o Backend

```bash
python app.py
```

O servidor vai rodar em: `http://localhost:5000`

## 📝 Como Usar

### Testar a API

```bash
# Verificar se está funcionando
curl http://localhost:5000/api/health

# Enviar email de teste
curl -X POST http://localhost:5000/api/send-email \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Teste",
    "email": "teste@exemplo.com",
    "subject": "Mensagem de Teste",
    "message": "Esta é uma mensagem de teste do formulário"
  }'
```

### No Frontend

O formulário já está configurado. Apenas:
1. Abra o `index.html` no navegador
2. Preencha o formulário de contato
3. Clique em "Enviar Mensagem"

## 🎨 Template de Email

O email enviado mantém o mesmo design do portfólio:
- ✅ Cores e tipografia consistentes
- ✅ Layout responsivo
- ✅ Estilo profissional
- ✅ Fácil leitura

## 🔧 Estrutura

```
backend/
├── app.py              # Servidor Flask + lógica SMTP
├── requirements.txt    # Dependências Python
├── .env.example       # Exemplo de configuração
├── .env              # Suas configurações (não commitar!)
└── README.md         # Esta documentação
```

## ⚙️ Endpoints da API

### `GET /api/health`
Verifica se o servidor está funcionando.

**Resposta:**
```json
{
  "status": "ok",
  "message": "Servidor funcionando corretamente"
}
```

### `POST /api/send-email`
Envia um email e uma confirmação automática.

**Body:**
```json
{
  "name": "Nome do Remetente",
  "email": "email@exemplo.com",
  "subject": "Assunto",
  "message": "Mensagem completa"
}
```

**O que acontece:**
1. ✅ Email é enviado para `RECIPIENT_EMAIL` (você recebe)
2. ✅ Email de confirmação é enviado para o remetente
3. ✅ Ambos com template HTML decorado com o design do portfólio

**Resposta de Sucesso:**
```json
{
  "success": true,
  "message": "Email enviado com sucesso! Verifique sua caixa de entrada para a confirmação."
}
```

**Resposta de Erro:**
```json
{
  "success": false,
  "message": "Descrição do erro"
}
```

## 🔒 Segurança

- ✅ CORS habilitado (ajuste conforme necessário)
- ✅ Validação de campos obrigatórios
- ✅ Validação básica de email
- ✅ Variáveis sensíveis em .env (não commitadas)

## 🐛 Troubleshooting

### "Erro de autenticação SMTP"
- Verifique se a senha de app está correta
- Confirme que a verificação em 2 etapas está ativada
- Tente gerar uma nova senha de app

### "Erro de conexão"
- Verifique se o backend está rodando
- Confirme que a porta 5000 não está sendo usada
- Verifique a URL da API no JavaScript

### Email não chega
- Verifique a pasta de spam
- Confirme o RECIPIENT_EMAIL no .env
- Teste com um email de teste primeiro

## 📚 Outras Opções de SMTP

### Outlook/Hotmail
```env
SMTP_SERVER=smtp-mail.outlook.com
SMTP_PORT=587
```

### Yahoo
```env
SMTP_SERVER=smtp.mail.yahoo.com
SMTP_PORT=587
```

### Outros
Para outros provedores, consulte a documentação do seu serviço de email.

## 🚀 Produção

Para deploy em produção:

1. **Desative o modo debug:**
   ```python
   app.run(host='0.0.0.0', port=5000, debug=False)
   ```

2. **Use um servidor WSGI:**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

3. **Configure HTTPS**

4. **Ajuste o CORS para seu domínio:**
   ```python
   CORS(app, origins=["https://seudominio.com"])
   ```

## 📄 Licença

Este projeto faz parte do portfólio de Enzo Amancio.
