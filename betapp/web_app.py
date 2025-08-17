from flask import Flask, render_template_string, request, jsonify, redirect, url_for
import requests
import json

app = Flask(__name__)

# API Client
class ApiClient:
    def __init__(self):
        self.base_url = "http://127.0.0.1:8000"
        self.token = None

    def set_token(self, token):
        self.token = token

    def _headers(self):
        headers = {"Accept": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def register(self, email: str, password: str):
        r = requests.post(
            f"{self.base_url}/auth/register",
            json={"email": email, "password": password},
            headers=self._headers(),
            timeout=15,
        )
        r.raise_for_status()
        return r.json()

    def login(self, email: str, password: str) -> str:
        r = requests.post(
            f"{self.base_url}/auth/login",
            json={"email": email, "password": password},
            headers=self._headers(),
            timeout=15,
        )
        r.raise_for_status()
        data = r.json()
        return data["access_token"]

    def list_matches(self):
        r = requests.get(f"{self.base_url}/matches", headers=self._headers(), timeout=15)
        r.raise_for_status()
        return r.json()

api = ApiClient()

# HTML Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>BetApp - Maç Tahminleri</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 2px solid #eee;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        input[type="email"], input[type="password"] {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 16px;
        }
        .btn {
            padding: 12px 24px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            margin-right: 10px;
        }
        .btn-primary {
            background-color: #007bff;
            color: white;
        }
        .btn-success {
            background-color: #28a745;
            color: white;
        }
        .btn-secondary {
            background-color: #6c757d;
            color: white;
        }
        .match-card {
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 15px;
            background: #f9f9f9;
        }
        .match-title {
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 5px;
        }
        .match-details {
            color: #666;
            font-size: 14px;
        }
        .premium-badge {
            background: #ffc107;
            color: #000;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: bold;
        }
        .free-badge {
            background: #28a745;
            color: white;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: bold;
        }
        .alert {
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 15px;
        }
        .alert-success {
            background-color: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        .alert-danger {
            background-color: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        .hidden {
            display: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>⚽ BetApp - Maç Tahminleri</h1>
            <p>En güncel maç tahminleri ve analizler</p>
        </div>

        {% if message %}
        <div class="alert alert-{{ message_type }}">
            {{ message }}
        </div>
        {% endif %}

        {% if not logged_in %}
        <!-- Login Form -->
        <div id="login-form">
            <h2>Giriş Yap</h2>
            <form method="POST" action="/login">
                <div class="form-group">
                    <label for="email">Email:</label>
                    <input type="email" id="email" name="email" required>
                </div>
                <div class="form-group">
                    <label for="password">Şifre:</label>
                    <input type="password" id="password" name="password" required>
                </div>
                <button type="submit" class="btn btn-primary">Giriş Yap</button>
                <button type="button" class="btn btn-success" onclick="showRegister()">Kayıt Ol</button>
            </form>
        </div>

        <!-- Register Form -->
        <div id="register-form" class="hidden">
            <h2>Kayıt Ol</h2>
            <form method="POST" action="/register">
                <div class="form-group">
                    <label for="reg-email">Email:</label>
                    <input type="email" id="reg-email" name="email" required>
                </div>
                <div class="form-group">
                    <label for="reg-password">Şifre:</label>
                    <input type="password" id="reg-password" name="password" required>
                </div>
                <button type="submit" class="btn btn-success">Kayıt Ol</button>
                <button type="button" class="btn btn-secondary" onclick="showLogin()">Giriş Yap</button>
            </form>
        </div>
        {% else %}
        <!-- Matches List -->
        <div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                <h2>Maçlar ({{ matches|length }})</h2>
                <div>
                    <span class="free-badge">Ücretsiz</span>
                    <span class="premium-badge">Premium</span>
                    <a href="/logout" class="btn btn-secondary">Çıkış Yap</a>
                </div>
            </div>
            
            {% for match in matches %}
            <div class="match-card">
                <div class="match-title">
                    {{ match.home_team }} vs {{ match.away_team }}
                    {% if match.is_premium %}
                        <span class="premium-badge">Premium</span>
                    {% else %}
                        <span class="free-badge">Ücretsiz</span>
                    {% endif %}
                </div>
                <div class="match-details">
                    <strong>Lig:</strong> {{ match.league }}<br>
                    <strong>Tarih:</strong> {{ match.kickoff_utc }}<br>
                    {% if match.prediction %}
                        <strong>Tahmin:</strong> {{ match.prediction.tip_value }}<br>
                        <strong>Güven:</strong> {{ match.prediction.confidence_percent }}%<br>
                        <strong>Oran:</strong> {{ match.prediction.odds_decimal }}
                    {% else %}
                        <strong>Tahmin:</strong> <em>Giriş yapın</em>
                    {% endif %}
                </div>
            </div>
            {% endfor %}
        </div>
        {% endif %}
    </div>

    <script>
        function showRegister() {
            document.getElementById('login-form').classList.add('hidden');
            document.getElementById('register-form').classList.remove('hidden');
        }
        
        function showLogin() {
            document.getElementById('register-form').classList.add('hidden');
            document.getElementById('login-form').classList.remove('hidden');
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    try:
        if api.token:
            matches = api.list_matches()
            return render_template_string(HTML_TEMPLATE, logged_in=True, matches=matches)
        else:
            return render_template_string(HTML_TEMPLATE, logged_in=False, matches=[])
    except:
        return render_template_string(HTML_TEMPLATE, logged_in=False, matches=[])

@app.route('/login', methods=['POST'])
def login():
    try:
        email = request.form['email']
        password = request.form['password']
        
        token = api.login(email, password)
        api.set_token(token)
        
        return redirect('/')
    except Exception as e:
        return render_template_string(HTML_TEMPLATE, 
                                    logged_in=False, 
                                    matches=[], 
                                    message=f"Giriş hatası: {str(e)}", 
                                    message_type="danger")

@app.route('/register', methods=['POST'])
def register():
    try:
        email = request.form['email']
        password = request.form['password']
        
        api.register(email, password)
        
        return render_template_string(HTML_TEMPLATE, 
                                    logged_in=False, 
                                    matches=[], 
                                    message="Kayıt başarılı! Giriş yapabilirsiniz.", 
                                    message_type="success")
    except Exception as e:
        return render_template_string(HTML_TEMPLATE, 
                                    logged_in=False, 
                                    matches=[], 
                                    message=f"Kayıt hatası: {str(e)}", 
                                    message_type="danger")

@app.route('/logout')
def logout():
    api.set_token(None)
    return redirect('/')

if __name__ == '__main__':
    print("🌐 Web uygulaması başlatılıyor...")
    print("📱 Tarayıcıda http://127.0.0.1:5000 adresine gidin")
    app.run(debug=True, host='127.0.0.1', port=5000)
