from flask import Flask, render_template_string, request, jsonify
from assistant.response_engine import ResponseEngine

app = Flask(__name__, static_folder='static')
engine = ResponseEngine()

HTML_TEMPLATE = r"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PPL Assistant</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}">
</head>
<body class="dark-mode">
    <div class="container">
        <div class="header">
            <div class="title-block">
                <div class="app-icon">🗓️</div>
                <div>
                    <h1 id="title">PPL Assistant</h1>
                    <p class="subtitle">Meeting planner · Weather · Organization</p>
                </div>
            </div>
            <div class="toggles">
                <button class="mode-toggle" id="mode-toggle" onclick="toggleMode()">🌙</button>
            </div>
        </div>
        <div class="quick-actions" id="quick-actions">
            <div class="quick-example">Show calendar 30/12/2024</div>
            <div class="quick-example">Show meeting 30/12/2024</div>
            <div class="quick-example">Show event 31/12/2024</div>
            <div class="quick-example">Show weather vung tau 16/12/2024</div>
        </div>
        <div class="chat-box" id="chat-box"></div>
        <div class="input-group">
            <input type="text" id="user-input" placeholder="Type your message...">
            <button class="send-button" onclick="sendMessage()" id="send-btn">➤</button>
        </div>
    </div>

    <script>
        const chatBox = document.getElementById('chat-box');
        const userInput = document.getElementById('user-input');
        const title = document.getElementById('title');
        const modeToggle = document.getElementById('mode-toggle');

        let isDarkMode = true;

        function toggleMode() {
            isDarkMode = !isDarkMode;
            document.body.classList.toggle('dark-mode', isDarkMode);
            document.body.classList.toggle('light-mode', !isDarkMode);
            modeToggle.textContent = isDarkMode ? '🌙' : '☀️';
        }

        function getTimestamp() {
            const now = new Date();
            return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        }

        function classifyBotMessage(text) {
            const lowered = text.toLowerCase();
            if (/sorry|i don't understand|don\'t understand|cannot understand|unable to understand/.test(lowered)) {
                return 'error';
            }
            if (/\d+°c|°c|weather|temperature/.test(lowered)) {
                return 'weather';
            }
            if (/confirmed|success/.test(lowered)) {
                return 'success';
            }
            if (/reminder/.test(lowered)) {
                return 'event';
            }
            return 'normal';
        }   

        function renderMessage(text, sender, variant = 'normal', time = getTimestamp()) {
            const wrapper = document.createElement('div');
            wrapper.className = `message ${sender} ${variant}`;
            const bubble = document.createElement('div');
            bubble.className = 'bubble';

            if (sender === 'bot' && variant === 'weather') {
                bubble.innerHTML = `
                    <div class="weather-card">
                        <div class="weather-icon">☀️</div>
                        <div>
                            <strong>${text}</strong>
                        </div>
                    </div>
                `;
            } else if (sender === 'bot' && variant === 'success') {
                bubble.innerHTML = `
                    <div class="success-card">
                        <span class="success-icon">✓</span>
                        <div>${text}</div>
                    </div>
                `;
            } else {
                bubble.textContent = text;
            }

            const timestamp = document.createElement('div');
            timestamp.className = 'timestamp';
            timestamp.textContent = time;
            wrapper.appendChild(bubble);
            wrapper.appendChild(timestamp);
            chatBox.appendChild(wrapper);
            chatBox.scrollTop = chatBox.scrollHeight;
        }

        function addMessage(message, sender) {
            const variant = sender === 'bot' ? classifyBotMessage(message) : 'user';
            renderMessage(message, sender, variant);
        }

        function sendMessage() {
            const message = userInput.value.trim();
            if (!message) return;
            addMessage(message, 'user');
            userInput.value = '';

            fetch('/get_response', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message }),
            })
            .then(response => response.json())
            .then(data => {
                const botText = data.response;
                addMessage(botText, 'bot');
            })
           .catch(error => {
                console.error('Error:', error);
                addMessage('Sorry, an error occurred.', 'bot');
            });
        }

        userInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });

        document.body.classList.add('dark-mode');
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/get_response', methods=['POST'])
def get_response():
    data = request.get_json()
    message = data.get('message', '')
    response = engine.get_response(message)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
