import time
import re
import platform
import os
import pyautogui 

def solve_expression(expression):
    try:
        expression = expression.replace("^", "**")
        result = eval(expression)
        return result
    except (SyntaxError, NameError, TypeError, ZeroDivisionError):
        return None 

def send_chat_message(message):
    try:
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

        pyautogui.press('t')
        time.sleep(0.1)  

       
        pyautogui.typewrite(message)
        time.sleep(0.1)

      
        pyautogui.press('enter')
        time.sleep(0.1)

    except Exception as e:
        print(f"Ошибка при отправке сообщения в чат (pyautogui): {e}")


def process_log_file(log_file_path, last_position):
    try:
        with open(log_file_path, 'r', encoding='utf-8') as log_file:
            log_file.seek(last_position) 

            for line in log_file:
                match = re.search(r"\[.*?\] \[.*?\]: \[CHAT\] Чат-Игра \| Сколько будет ([\d\+\-\*\/\^\(\)\s]+)\? Кто первый решит, получит нагрду ₴15000", line)

                if match:
                    expression = match.group(1).strip()

                    result = solve_expression(expression)

                    if result is not None:
                        response = f"{result}"
                        send_chat_message(response)
                    else:
                        print(f"Ошибка: Не удалось решить выражение '{expression}'")

            return log_file.tell()

    except FileNotFoundError:
        print(f"Ошибка: Файл лога не найден: {log_file_path}")
        return 0 
    except Exception as e:
        print(f"Произошла ошибка при чтении файла лога: {e}")
        return last_position

system = platform.system()
if system == "Windows":
    log_file_path = "%appdata%\\.minecraft\\logs\\latest.log"
    log_file_path = os.path.expandvars(log_file_path)
    log_file_path = log_file_path.replace("\\", "/")
elif system == "Darwin":
    log_file_path = "~/Library/Application Support/minecraft/logs/latest.log"
    log_file_path = os.path.expanduser(log_file_path)
else:
    log_file_path = "~/.minecraft/logs/latest.log"
    log_file_path = os.path.expanduser(log_file_path)

last_position = 0

while True:
    last_position = process_log_file(log_file_path, last_position)
    time.sleep(1)  
