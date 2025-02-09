from flask import Flask, render_template, request, jsonify
from ai_bot import *
import logging

app = Flask(__name__)

@app.route('/')
def index():
    title = "Intelli Chat"
    return render_template("index.html", title=title)

@app.route('/generate_response', methods=['POST'])
def handle_generate_response():
    data = request.json
    prompt = data.get('prompt')
    user_id = data.get('user_id', 1)
    system_prompt = data.get('system_prompt', "Отвечай только на русском!")

    try:
        response = generate_response(prompt, user_id, system_prompt)
        return jsonify({'response': response})
    except Exception as e:
        logging.error(f"Ошибка при генерации ответа: {e}")
        return jsonify({'response': "Произошла ошибка при обработке запроса."}), 500


@app.route('/clear_history', methods=['POST'])
def handle_clear_history():
    data = request.json
    user_id = data.get('user_id', 1)
    conversation_history.pop(user_id, None)  # Удаляем историю чата для пользователя
    return jsonify({'success': True})


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app.run(debug=True)