import time
import re
import platform
import os
import pyautogui  # pip install pyautogui

# Функция для решения математических выражений
def solve_expression(expression):
    try:
        # Заменяем ^ на ** для возведения в степень
        expression = expression.replace("^", "**")
        result = eval(expression)
        return result
    except (SyntaxError, NameError, TypeError, ZeroDivisionError):
        return None  # Возвращаем None в случае ошибки

# Функция для отправки сообщения в чат Minecraft (через pyautogui)
def send_chat_message(message):
    try:
        # Активируем окно Minecraft (требуется, чтобы окно было видно)
        # Попробуйте заменить "Minecraft" на заголовок вашего окна Minecraft, если не работает
        minecraft_window = None
        for window in pyautogui.getAllWindows():
            if "Minecraft" in window.title:
                minecraft_window = window
                break

        if minecraft_window:
            minecraft_window.activate()
        else:
            print("Не удалось найти окно Minecraft. Убедитесь, что оно запущено и видимо.")
            return

        # Открываем чат (обычно кнопка "T")
        pyautogui.press('t')
        time.sleep(0.1)  # Небольшая задержка

        # Вводим сообщение
        pyautogui.typewrite(message)
        time.sleep(0.1)

        # Отправляем сообщение (нажимаем Enter)
        pyautogui.press('enter')
        time.sleep(0.1)

    except Exception as e:
        print(f"Ошибка при отправке сообщения в чат (pyautogui): {e}")


# Функция для чтения файла лога и поиска выражений
def process_log_file(log_file_path, last_position):
    try:
        with open(log_file_path, 'r', encoding='utf-8') as log_file:
            log_file.seek(last_position)  # Переходим к последней обработанной позиции

            for line in log_file:
                # Новое регулярное выражение
                match = re.search(r"\[.*?\] \[.*?\]: \[CHAT\] Чат-Игра \| Сколько будет ([\d\+\-\*\/\^\(\)\s]+)\? Кто первый решит, получит нагрду ₴15000", line)

                if match:
                    expression = match.group(1).strip()

                    result = solve_expression(expression)

                    if result is not None:
                        response = f"{result}" # Только ответ, без "Ответ: "
                        send_chat_message(response)
                    else:
                        print(f"Ошибка: Не удалось решить выражение '{expression}'")

            return log_file.tell()  # Возвращаем текущую позицию в файле

    except FileNotFoundError:
        print(f"Ошибка: Файл лога не найден: {log_file_path}")
        return 0  # Возвращаем 0, чтобы начать с начала в следующий раз
    except Exception as e:
        print(f"Произошла ошибка при чтении файла лога: {e}")
        return last_position  # Возвращаем старую позицию, чтобы не потерять прогресс

# Автоматическое определение пути к файлу лога
system = platform.system()
if system == "Windows":
    log_file_path = "%appdata%\\.minecraft\\logs\\latest.log"
    log_file_path = os.path.expandvars(log_file_path)
    log_file_path = log_file_path.replace("\\", "/") # Заменяем обратные слеши прямыми
elif system == "Darwin":  # macOS
    log_file_path = "~/Library/Application Support/minecraft/logs/latest.log"
    log_file_path = os.path.expanduser(log_file_path)
else:  # Linux (и другие)
    log_file_path = "~/.minecraft/logs/latest.log"
    log_file_path = os.path.expanduser(log_file_path)

# Инициализируем переменную для хранения последней позиции в файле
last_position = 0

# Бесконечный цикл для отслеживания изменений в файле лога
while True:
    last_position = process_log_file(log_file_path, last_position)
    time.sleep(1)  # Проверяем файл лога каждую секунду
