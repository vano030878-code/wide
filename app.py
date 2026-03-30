from flask import Flask, request, jsonify

from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

def init_db():
    conn = sqlite3.connect('data.db')
    conn.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        contact TEXT,
        description TEXT,
        image TEXT      
                   )
    ''')
    conn.commit()
    conn.close()

# id INTEGER PRIMARY KEY AUTOINCREMENT,  база данных сама назначит id каждому объявлению


@app.route('/messages', methods=['GET'])
def get_messages():
    conn = sqlite3.connect('data.db')
    conn.row_factory = sqlite3.Row
    rows = conn.execute('SELECT * FROM messages ORDER BY id DESC').fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])


@app.route('/messages', methods=['POST'])
def add_message():
    data = request.json
    title = data.get('title')
    contact = data.get('contact')
    description = data.get('description')      
    image = data.get('image')     

    # if not text:
    #     return jsonify({'error': 'Текст обязателен'}), 400  #скорее всего тут не нужна проверка, потому что она есть в js коде
    
    conn = sqlite3.connect('data.db')
    sql = 'INSERT INTO messages (title, description, contact, image) VALUES (?, ?, ?, ?)'
    conn.execute(sql, (title, description, contact, image))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Сохранено'}), 201

@app.route('/messages/<int:msg_id>', methods=['DELETE'])
def delete_message(msg_id):
    conn = sqlite3.connect('data.db')
    conn.execute('DELETE FROM messages WHERE id = ?', (msg_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Удалено'}), 200

if __name__ == '__main__':
    init_db()
    print('API запущен на http://localhost:5000')
    app.run(port=5000, debug=True)


# Коды статуса (например, `200` или `201`) — это часть HTTP-ответа. Они говорят клиенту (браузеру, скрипту), как прошла операция.

# - **200 OK** – стандартный код для успешного запроса. Если не указать код, Flask вернёт `200` по умолчанию.
# - **201 Created** – специальный код, который означает, что ресурс успешно создан (например, добавлено новое сообщение). Используется по соглашению в REST API.

# **Можно ли без них?**  
# Технически можно написать просто `return jsonify(...)`, и Flask сам подставит `200`. Но для `POST` лучше явно вернуть `201`, чтобы клиент знал, что объект создан. Это делает API более правильным и предсказуемым. К тому же, если у клиента есть обработка ошибок, коды помогают отличить успех от ошибки (например, `400`, `404`).

# Если вы пишете простой сервер для себя, можете временно не указывать коды, но в будущем привыкайте их ставить — это хороший тон.