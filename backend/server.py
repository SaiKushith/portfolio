import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app, origins=["*"])

@app.route('/', methods=['GET'])
def health():
    return jsonify({'status': 'ok'}), 200

@app.route('/send-email', methods=['POST'])
def send_email():
    data    = request.get_json()
    name    = data.get('name', '').strip()
    email   = data.get('email', '').strip()
    message = data.get('message', '').strip()

    if not name or not email or not message:
        return jsonify({'success': False, 'error': 'All fields are required.'}), 400

    host     = os.getenv('EMAIL_HOST')
    port     = int(os.getenv('EMAIL_PORT'))
    user     = os.getenv('EMAIL_HOST_USER')
    password = os.getenv('EMAIL_HOST_PASSWORD')

    msg = MIMEMultipart()
    msg['From']     = user
    msg['To']       = user
    msg['Subject']  = f'Portfolio Inquiry from {name}'
    msg['Reply-To'] = email
    msg.attach(MIMEText(f"Name: {name}\nEmail: {email}\n\n{message}", 'plain'))

    try:
        with smtplib.SMTP(host, port) as server:
            server.ehlo()
            server.starttls()
            server.login(user, password)
            server.sendmail(user, user, msg.as_string())
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
