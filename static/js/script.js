document.addEventListener('DOMContentLoaded', function() {
    const chatHistory = document.getElementById('chat-history');
    const inputText = document.getElementById('input-text');
    const arrowIco = document.querySelector('.arrow-ico');
    const trashIco = document.querySelector('.trash-ico');

    // Функция для отправки сообщения
    function sendMessage() {
        const message = inputText.value.trim();
        if (message) {
            // Добавляем сообщение пользователя
            const userMessage = document.createElement('div');
            userMessage.classList.add('message', 'my-message');
            userMessage.textContent = message;
            chatHistory.appendChild(userMessage);

            // Очищаем поле ввода
            inputText.value = '';

            // Отправляем запрос на сервер для получения ответа от ИИ
            fetch('/generate_response', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    prompt: message,
                    user_id: 1,
                    system_prompt: "Отвечай только на русском!"
                })
            })
            .then(response => response.json())
            .then(data => {
                const botMessage = document.createElement('div');
                botMessage.classList.add('message', 'bot-message');
                botMessage.innerHTML = data.response; // Используем innerHTML для рендеринга Markdown

                // Добавляем кнопки для копирования
                const copyAllButton = document.createElement('button');
                copyAllButton.textContent = 'Copy All';
                copyAllButton.classList.add('copy-button');
                copyAllButton.addEventListener('click', function() {
                    navigator.clipboard.writeText(data.response).then(() => {
                        console.log('Скопировано!');
                    });
                });

                const codeBlocks = botMessage.querySelectorAll('pre code');
                if (codeBlocks.length > 0) {
                    const copyCodeButton = document.createElement('button');
                    copyCodeButton.textContent = 'Copy Code';
                    copyCodeButton.classList.add('copy-button');
                    copyCodeButton.addEventListener('click', function() {
                        const codeText = codeBlocks[0].textContent;
                        navigator.clipboard.writeText(codeText).then(() => {
                            console.log('Код скопирован!');
                        });
                    });

                    botMessage.appendChild(copyAllButton);
                    botMessage.appendChild(copyCodeButton);
                } else {
                    botMessage.appendChild(copyAllButton);
                }

                chatHistory.appendChild(botMessage);

                // Применяем подсветку синтаксиса
                document.querySelectorAll('pre code').forEach((block) => {
                    hljs.highlightBlock(block);
                });

                // Прокручиваем чат вниз
                chatHistory.scrollTop = chatHistory.scrollHeight;
            })
            .catch(error => console.error('Ошибка:', error));
        }
    }

    // Обработчик для кнопки отправки
    arrowIco.addEventListener('click', sendMessage);

    // Обработчик для клавиши Enter
    inputText.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    // Обработчик для кнопки очистки чата
    trashIco.addEventListener('click', function() {
        // Очищаем историю чата на сервере
        fetch('/clear_history', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                user_id: 1
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Очищаем содержимое чата на клиенте
                chatHistory.innerHTML = '';
            }
        })
        .catch(error => console.error('Ошибка:', error));
    });
});
