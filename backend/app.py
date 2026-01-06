"""
Backend Flask para envio de emails do portfólio
Configurado com SMTP para Gmail
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configurações SMTP
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
SMTP_EMAIL = os.getenv('SMTP_EMAIL', 'seu-email@gmail.com')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', 'sua-senha-app')
RECIPIENT_EMAIL = os.getenv('RECIPIENT_EMAIL', 'enzoamancio17@gmail.com')


def get_email_template_to_admin(name, email, subject, message):
    """
    Template do email que vai para o ADMIN (você recebe a mensagem)
    """
    return f"""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Nova mensagem do portfólio</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background-color: #f8fafc;
                padding: 20px;
            }}
            
            .email-container {{
                max-width: 600px;
                margin: 0 auto;
                background-color: #ffffff;
                border-radius: 12px;
                overflow: hidden;
                box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            }}
            
            .email-header {{
                background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
                padding: 40px 30px;
                text-align: center;
                color: white;
            }}
            
            .email-header h1 {{
                font-size: 28px;
                font-weight: 700;
                margin-bottom: 8px;
            }}
            
            .email-header p {{
                font-size: 14px;
                opacity: 0.9;
            }}
            
            .email-body {{
                padding: 40px 30px;
            }}
            
            .info-box {{
                background-color: #f1f5f9;
                border-left: 4px solid #2563eb;
                padding: 20px;
                margin-bottom: 24px;
                border-radius: 8px;
            }}
            
            .info-item {{
                margin-bottom: 12px;
            }}
            
            .info-item:last-child {{
                margin-bottom: 0;
            }}
            
            .info-label {{
                font-size: 12px;
                font-weight: 600;
                color: #475569;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                margin-bottom: 4px;
            }}
            
            .info-value {{
                font-size: 15px;
                color: #1e293b;
                font-weight: 500;
            }}
            
            .message-box {{
                background-color: #ffffff;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                padding: 24px;
                margin-bottom: 24px;
            }}
            
            .message-label {{
                font-size: 12px;
                font-weight: 600;
                color: #475569;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                margin-bottom: 12px;
            }}
            
            .message-text {{
                font-size: 15px;
                line-height: 1.7;
                color: #1e293b;
                white-space: pre-wrap;
            }}
            
            .email-footer {{
                background-color: #f8fafc;
                padding: 30px;
                text-align: center;
                border-top: 1px solid #e2e8f0;
            }}
            
            .footer-text {{
                font-size: 13px;
                color: #94a3b8;
                margin-bottom: 16px;
            }}
            
            .footer-brand {{
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 8px;
                font-size: 16px;
                font-weight: 600;
                color: #2563eb;
            }}
            
            .icon {{
                width: 20px;
                height: 20px;
                fill: currentColor;
            }}
            
            .timestamp {{
                display: inline-block;
                background-color: #e2e8f0;
                color: #475569;
                padding: 6px 12px;
                border-radius: 6px;
                font-size: 12px;
                margin-top: 16px;
            }}
        </style>
    </head>
    <body>
        <div class="email-container">
            <div class="email-header">
                <h1>📩 Nova Mensagem</h1>
                <p>Você recebeu uma mensagem do seu portfólio</p>
            </div>
            
            <div class="email-body">
                <div class="info-box">
                    <div class="info-item">
                        <div class="info-label">👤 Nome</div>
                        <div class="info-value">{name}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">📧 Email</div>
                        <div class="info-value">{email}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">📝 Assunto</div>
                        <div class="info-value">{subject}</div>
                    </div>
                </div>
                
                <div class="message-box">
                    <div class="message-label">💬 Mensagem</div>
                    <div class="message-text">{message}</div>
                </div>
                
                <div style="text-align: center;">
                    <div class="timestamp">
                        ⏰ Recebido em: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}
                    </div>
                </div>
            </div>
            
            <div class="email-footer">
                <p class="footer-text">
                    Esta mensagem foi enviada através do formulário de contato do seu portfólio
                </p>
                <div class="footer-brand">
                    <svg class="icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M9 3L5 6.99h3V14h2V6.99h3L9 3zm7 14.01V10h-2v7.01h-3L15 21l4-3.99h-3z" fill="currentColor"/>
                    </svg>
                    Enzo Amancio | Desenvolvedor Full Stack
                </div>
            </div>
        </div>
    </body>
    </html>
    """


def get_confirmation_email_template(name):
    """
    Template de confirmação para o REMETENTE (quem enviou a mensagem)
    """
    return f"""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Mensagem Recebida</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background-color: #f8fafc;
                padding: 20px;
            }}
            
            .email-container {{
                max-width: 600px;
                margin: 0 auto;
                background-color: #ffffff;
                border-radius: 12px;
                overflow: hidden;
                box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            }}
            
            .email-header {{
                background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
                padding: 40px 30px;
                text-align: center;
                color: white;
            }}
            
            .email-header h1 {{
                font-size: 28px;
                font-weight: 700;
                margin-bottom: 8px;
            }}
            
            .email-header p {{
                font-size: 14px;
                opacity: 0.9;
            }}
            
            .email-body {{
                padding: 40px 30px;
                text-align: center;
            }}
            
            .check-icon {{
                width: 80px;
                height: 80px;
                margin: 0 auto 20px;
                background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 40px;
            }}
            
            .confirmation-title {{
                font-size: 24px;
                font-weight: 700;
                color: #1e293b;
                margin-bottom: 12px;
            }}
            
            .confirmation-text {{
                font-size: 15px;
                line-height: 1.7;
                color: #475569;
                margin-bottom: 24px;
            }}
            
            .info-box {{
                background-color: #f1f5f9;
                border-left: 4px solid #2563eb;
                padding: 20px;
                margin-bottom: 24px;
                border-radius: 8px;
                text-align: left;
            }}
            
            .info-label {{
                font-size: 12px;
                font-weight: 600;
                color: #475569;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                margin-bottom: 4px;
            }}
            
            .info-value {{
                font-size: 15px;
                color: #1e293b;
                font-weight: 500;
            }}
            
            .next-steps {{
                background-color: #f8fafc;
                border-radius: 8px;
                padding: 20px;
                margin-bottom: 24px;
                text-align: left;
            }}
            
            .next-steps h3 {{
                font-size: 14px;
                font-weight: 700;
                color: #1e293b;
                margin-bottom: 12px;
            }}
            
            .next-steps ol {{
                margin-left: 20px;
            }}
            
            .next-steps li {{
                font-size: 13px;
                color: #475569;
                margin-bottom: 8px;
                line-height: 1.6;
            }}
            
            .cta-box {{
                background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
                border-radius: 12px;
                padding: 24px;
                margin-bottom: 24px;
            }}
            
            .cta-text {{
                font-size: 14px;
                color: #475569;
                margin-bottom: 8px;
            }}
            
            .cta-links {{
                display: flex;
                gap: 12px;
                justify-content: center;
                flex-wrap: wrap;
            }}
            
            .cta-link {{
                display: inline-flex;
                align-items: center;
                gap: 6px;
                padding: 8px 16px;
                background: white;
                color: #2563eb;
                border-radius: 8px;
                text-decoration: none;
                font-size: 13px;
                font-weight: 600;
                transition: all 0.3s ease;
            }}
            
            .cta-link:hover {{
                background: #2563eb;
                color: white;
            }}
            
            .email-footer {{
                background-color: #f8fafc;
                padding: 30px;
                text-align: center;
                border-top: 1px solid #e2e8f0;
            }}
            
            .footer-text {{
                font-size: 13px;
                color: #94a3b8;
                margin-bottom: 16px;
            }}
            
            .footer-brand {{
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 8px;
                font-size: 14px;
                font-weight: 600;
                color: #2563eb;
            }}
            
            .icon {{
                width: 20px;
                height: 20px;
            }}
        </style>
    </head>
    <body>
        <div class="email-container">
            <div class="email-header">
                <h1>✅ Mensagem Recebida!</h1>
                <p>Obrigado por entrar em contato</p>
            </div>
            
            <div class="email-body">
                <div class="check-icon">✓</div>
                
                <h2 class="confirmation-title">Olá, {name}!</h2>
                
                <p class="confirmation-text">
                    Sua mensagem foi recebida com sucesso. Vou revisar e retornar em breve.
                </p>
                
                <div class="info-box">
                    <div class="info-label">⏰ Data e Hora</div>
                    <div class="info-value">{datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}</div>
                </div>
                
                <div class="next-steps">
                    <h3>📋 Próximos Passos</h3>
                    <ol>
                        <li>Vou ler sua mensagem com atenção</li>
                        <li>Poderei responder em até 24 horas</li>
                        <li>Você receberá minha resposta no email <strong>{RECIPIENT_EMAIL.split('@')[0]}@...</strong></li>
                        <li>Fique atento à pasta de spam caso não encontre</li>
                    </ol>
                </div>
                
                <div class="cta-box">
                    <p class="cta-text">Enquanto isso, conheça meu trabalho:</p>
                    <div class="cta-links">
                        <a href="https://github.com/enzoAmancio" class="cta-link">
                            <span>💻</span> GitHub
                        </a>
                        <a href="https://www.linkedin.com/in/enzoamanciorocha/" class="cta-link">
                            <span>💼</span> LinkedIn
                        </a>
                        <a href="https://wa.me/+5534999173285" class="cta-link">
                            <span>💬</span> WhatsApp
                        </a>
                    </div>
                </div>
            </div>
            
            <div class="email-footer">
                <p class="footer-text">
                    Confirmação automática do portfólio
                </p>
                <div class="footer-brand">
                    <svg class="icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M9 3L5 6.99h3V14h2V6.99h3L9 3zm7 14.01V10h-2v7.01h-3L15 21l4-3.99h-3z" fill="currentColor"/>
                    </svg>
                    Enzo Amancio | Desenvolvedor Full Stack
                </div>
            </div>
        </div>
    </body>
    </html>
    """


@app.route('/api/send-email', methods=['POST'])
def send_email():
    """
    Endpoint para enviar emails
    Envia 2 emails:
    1. Para você (admin) com a mensagem da pessoa
    2. Para a pessoa com confirmação automática decorada
    """
    try:
        data = request.get_json()
        
        # Validação dos campos
        required_fields = ['name', 'email', 'subject', 'message']
        for field in required_fields:
            if field not in data or not data[field].strip():
                return jsonify({
                    'success': False,
                    'message': f'O campo {field} é obrigatório'
                }), 400
        
        name = data['name'].strip()
        email = data['email'].strip()
        subject = data['subject'].strip()
        message = data['message'].strip()
        
        # Validação básica de email
        if '@' not in email or '.' not in email:
            return jsonify({
                'success': False,
                'message': 'Email inválido'
            }), 400
        
        # ===== EMAIL 1: Para você (Admin) =====
        msg_admin = MIMEMultipart('alternative')
        msg_admin['From'] = SMTP_EMAIL
        msg_admin['To'] = RECIPIENT_EMAIL
        msg_admin['Subject'] = f"[Portfólio] {subject}"
        msg_admin['Reply-To'] = email
        
        # Template HTML para admin
        html_content_admin = get_email_template_to_admin(name, email, subject, message)
        
        # Texto alternativo
        text_content_admin = f"""
Nova mensagem do portfólio

Nome: {name}
Email: {email}
Assunto: {subject}

Mensagem:
{message}

---
Recebido em: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}
        """
        
        # Anexar as partes
        part1_admin = MIMEText(text_content_admin, 'plain', 'utf-8')
        part2_admin = MIMEText(html_content_admin, 'html', 'utf-8')
        
        msg_admin.attach(part1_admin)
        msg_admin.attach(part2_admin)
        
        # ===== EMAIL 2: Para o remetente (Confirmação) =====
        msg_user = MIMEMultipart('alternative')
        msg_user['From'] = SMTP_EMAIL
        msg_user['To'] = email
        msg_user['Subject'] = f"✅ Mensagem Recebida - {subject}"
        
        # Template HTML de confirmação
        html_content_user = get_confirmation_email_template(name)
        
        # Texto alternativo
        text_content_user = f"""
Olá, {name}!

Sua mensagem foi recebida com sucesso.

Assunto: {subject}
Data: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}

Vou revisar e retornar em breve.

Obrigado por entrar em contato!

---
Enzo Amancio | Desenvolvedor Full Stack
        """
        
        # Anexar as partes
        part1_user = MIMEText(text_content_user, 'plain', 'utf-8')
        part2_user = MIMEText(html_content_user, 'html', 'utf-8')
        
        msg_user.attach(part1_user)
        msg_user.attach(part2_user)
        
        # Enviar AMBOS os emails
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            
            # Enviar email para admin
            server.send_message(msg_admin)
            
            # Enviar email de confirmação para o remetente
            server.send_message(msg_user)
        
        return jsonify({
            'success': True,
            'message': 'Email enviado com sucesso! Verifique sua caixa de entrada para a confirmação.'
        }), 200
        
    except smtplib.SMTPAuthenticationError:
        return jsonify({
            'success': False,
            'message': 'Erro de autenticação SMTP. Verifique as credenciais.'
        }), 500
        
    except Exception as e:
        print(f"Erro ao enviar email: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Erro ao enviar email. Tente novamente mais tarde.'
        }), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Endpoint para verificar se o servidor está funcionando
    """
    return jsonify({
        'status': 'ok',
        'message': 'Servidor funcionando corretamente'
    }), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
