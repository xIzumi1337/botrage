import time
import re
import platform
import os
import pyautogui

# --- НАСТРОЙКИ КОДИРОВКИ ---
FILE_ENCODING = "cp1251"  # Кодировка для русской Windows
CHAT_KEY = 't'            # Клавиша открытия чата
DELAY = 0.1               # Задержка между действиями

def solve_expression(expression):
    try:
        expression = expression.replace("^", "**").replace(' ', '')
        return str(round(eval(expression), 2)).rstrip('0').rstrip('.')
    except:
        return None

def send_to_chat(message):
    """Отправка сообщения в активное окно"""
    try:
        # Открываем чат и вводим ответ
        pyautogui.press(CHAT_KEY)
        time.sleep(DELAY)
        pyautogui.write(str(message))
        time.sleep(DELAY)
        pyautogui.press('enter')
        return True
    except Exception as e:
        print(f"Ошибка ввода: {str(e)}")
        return False

def process_log(log_path, last_pos):
    try:
        with open(log_path, "r", encoding=FILE_ENCODING, errors="ignore") as f:
            f.seek(last_pos)
            
            for line in f:
                match = re.search(
                    r"Чат-Игра \| Сколько будет (.+?)\?",
                    line.strip()
                )
                
                if match:
                    task = match.group(1)
                    if answer := solve_expression(task):
                        print(f"Решаем: {task} = {answer}")
                        send_to_chat(answer)
            return f.tell()
    
    except Exception as e:
        print(f"Ошибка: {str(e)}")
        return last_pos

def get_log_path():
    system = platform.system()
    return {
        "Windows": os.path.join(os.getenv('APPDATA'), ".minecraft", "logs", "latest.log"),
        "Darwin": os.path.expanduser("~/Library/Application Support/minecraft/logs/latest.log"),
        "Linux": os.path.expanduser("~/.minecraft/logs/latest.log")
    }.get(system)

if __name__ == "__main__":
    log_file = get_log_path()
    pos = 0
    
    if not log_file or not os.path.exists(log_file):
        print(f"Файл логов не найден: {log_file}")
        exit()
        
    print("Скрипт запущен. Активируйте окно Minecraft!")
    print("Для выхода нажмите Ctrl+C")

    while True:
        pos = process_log(log_file, pos)
        time.sleep(1)
