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
                <div class="app-icon">📅</div>
                <div>
                    <h1 id="title">PPL Assistant</h1>
                    <p class="subtitle">Lịch họp · Thời tiết · Sắp xếp</p>
                </div>
            </div>
            <div class="toggles">
                <button class="language-toggle" id="lang-toggle" onclick="toggleLanguage()">EN</button>
                <button class="mode-toggle" id="mode-toggle" onclick="toggleMode()">🌙</button>
            </div>
        </div>
        <div class="quick-actions" id="quick-actions">
            <button class="quick-chip" onclick="sendQuickAction('Thời tiết hôm nay')">Thời tiết hôm nay</button>
            <button class="quick-chip" onclick="sendQuickAction('Thêm lịch họp')">Thêm lịch họp</button>
            <button class="quick-chip" onclick="sendQuickAction('Xem lịch tuần')">Xem lịch tuần</button>
            <button class="quick-chip" onclick="sendQuickAction('Nhắc nhở')">Nhắc nhở</button>
        </div>
        <div class="chat-box" id="chat-box"></div>
        <div class="input-group">
            <button class="input-icon" id="attach-btn" title="Attach">📎</button>
            <button class="input-icon" id="mic-btn" title="Voice input">🎙</button>
            <input type="text" id="user-input" placeholder="Nhập lệnh hoặc câu hỏi...">
            <button class="send-button" onclick="sendMessage()" id="send-btn">➤</button>
        </div>
    </div>

    <script>
        const chatBox = document.getElementById('chat-box');
        const userInput = document.getElementById('user-input');
        const title = document.getElementById('title');
        const langToggle = document.getElementById('lang-toggle');
        const modeToggle = document.getElementById('mode-toggle');

        let isEnglish = false;
        let isDarkMode = true;
        const translations = {
            en: {
                title: 'PPL Assistant',
                placeholder: 'Type your message...',
                toggle: 'VN',
                subtitle: 'Meeting planner · Weather · Organization'
            },
            vn: {
                title: 'PPL Assistant',
                placeholder: 'Nhập lệnh hoặc câu hỏi...',
                toggle: 'EN',
                subtitle: 'Lịch họp · Thời tiết · Sắp xếp'
            }
        };

        function toggleLanguage() {
            isEnglish = !isEnglish;
            const lang = isEnglish ? 'en' : 'vn';
            title.textContent = translations[lang].title;
            userInput.placeholder = translations[lang].placeholder;
            langToggle.textContent = translations[lang].toggle;
            document.querySelector('.subtitle').textContent = translations[lang].subtitle;
            document.documentElement.lang = isEnglish ? 'en' : 'vi';
            langToggle.classList.toggle('active', !isEnglish);
        }

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
            if (/sorry|không hiểu|không nhận ra|i don't understand|don\'t understand|cannot understand|unable to understand|xin lỗi/.test(lowered)) {
                return 'error';
            }
            if (/\d+°c|°c|weather|thời tiết|temperature|nhiệt độ/.test(lowered)) {
                return 'weather';
            }
            if (/đã tạo|tạo thành công|confirmed|success|hoàn thành|đã lưu/.test(lowered)) {
                return 'success';
            }
            if (/lịch|sự kiện|cuộc họp|reminder|nhắc/.test(lowered) && !/thời tiết/.test(lowered)) {
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
                addMessage(isEnglish ? 'Sorry, an error occurred.' : 'Xin lỗi, có lỗi xảy ra.', 'bot');
            });
        }

        function sendQuickAction(text) {
            userInput.value = text;
            sendMessage();
        }

        userInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });

        document.getElementById('mic-btn').addEventListener('click', () => {
            addMessage(isEnglish ? 'Voice input is not enabled yet.' : 'Chức năng giọng nói chưa mở.', 'bot');
        });

        document.getElementById('attach-btn').addEventListener('click', () => {
            addMessage(isEnglish ? 'Attachment support is not available yet.' : 'Chưa hỗ trợ đính kèm.', 'bot');
        });

        document.body.classList.add('dark-mode');
        toggleLanguage();
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