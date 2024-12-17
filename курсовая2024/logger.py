from datetime import datetime

class Logger:
    """Класс для логирования ошибок."""
    @staticmethod
    def log_error(operation, error_message):
        try:
            with open("error_log.txt", "a") as log_file:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_message = f"{timestamp} - Операция: {operation} - Ошибка: {error_message}\n"
                log_file.write(log_message)
        except Exception as e:
            print(f"Не удалось записать в лог-файл: {e}")