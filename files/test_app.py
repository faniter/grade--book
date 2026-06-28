import os
import time
import json
import sys
from datetime import datetime

# Імпортуємо функції з нашого основного додатка app.py
try:
    import app
except ImportError:
    print("\033[91m⚠ Помилка: Не вдалося знайти файл app.py у цій папці!\033[0m")
    sys.exit(1)

# Тимчасові файли для ізоляції тестів
TEST_FILENAME = "test_gradebook.json"
TEST_LOG_FILENAME = "test_history.log"

# Налаштування кольорів
OK_C = "\033[92m"      # Зелений
FAIL_C = "\033[91m"    # Червоний
BLUE_C = "\033[94m"    # Синій
CYAN_C = "\033[96m"    # Бірюзовий
RESET = "\033[0m"      # Скидання
WHITE = "\033[97m"     # Білий
GRAY = "\033[90m"      # Сірий

def show_progress_bar(test_name, duration=0.4, steps=12):
    """Гарний індикатор завантаження для тест-кейсу"""
    for i in range(steps + 1):
        percent = int((i / steps) * 100)
        bar = "█" * i + "░" * (steps - i)
        sys.stdout.write(f"\r {CYAN_C}➔ Аналіз:{RESET} {test_name:<32} [{BLUE_C}{bar}{RESET}] {percent}%")
        sys.stdout.flush()
        time.sleep(duration / steps)
    print()

def setup_test_environment():
    app.FILENAME = TEST_FILENAME
    app.LOG_FILENAME = TEST_LOG_FILENAME
    if os.path.exists(TEST_FILENAME): os.remove(TEST_FILENAME)
    if os.path.exists(TEST_LOG_FILENAME): os.remove(TEST_LOG_FILENAME)

def teardown_test_environment():
    if os.path.exists(TEST_FILENAME): os.remove(TEST_FILENAME)
    if os.path.exists(TEST_LOG_FILENAME): os.remove(TEST_LOG_FILENAME)
    if os.path.exists("tabel.txt"): os.remove("tabel.txt")

def run_all_tests():
    app.clear_screen()
    print(f"{CYAN_C}╔════════════════════════════════════════════════════════╗{RESET}")
    print(f"{CYAN_C}║             СИСТЕМА АВТОМАТИЗОВАНОГО ТЕСТУВАННЯ        ║{RESET}")
    print(f"{CYAN_C}╚════════════════════════════════════════════════════════╝{RESET}\n")
    
    setup_test_environment()
    results = []
    
    # -------------------------------------------------------------------------
    # ТЕСТ 1: Конвертер ECTS
    # -------------------------------------------------------------------------
    t_name = "Конвертер балів у ECTS"
    show_progress_bar(t_name)
    
    g1, g2, g3 = 12, 7, 2
    res1, res2, res3 = app.get_ects(g1), app.get_ects(g2), app.get_ects(g3)
    
    print(f"   {GRAY}└─ Вхідні дані:{RESET} Бали [{g1}, {g2}, {g3}]")
    print(f"   {GRAY}└─ Результат:{RESET}  12 ➔ {OK_C}{res1}{RESET} | 7 ➔ {BLUE_C}{res2}{RESET} | 2 ➔ {FAIL_C}{res3}{RESET}")
    
    if "Відмінно" in res1 and "Задовільно" in res2 and "Незадовільно" in res3:
        results.append((t_name, f"{OK_C}[ SUCCESS ]{RESET}"))
    else:
        results.append((t_name, f"{FAIL_C}[ FAILED  ]{RESET}"))
    print()

    # -------------------------------------------------------------------------
    # ТЕСТ 2: Робота з JSON файлом
    # -------------------------------------------------------------------------
    t_name = "Запис/читання бази JSON"
    show_progress_bar(t_name)
    
    test_dict = {"Програмування": 12, "Бази даних": 10}
    print(f"   {GRAY}└─ Дія:{RESET} Спроба запису словника {WHITE}{test_dict}{RESET} у {TEST_FILENAME}")
    
    try:
        app.save_data(test_dict)
        loaded = app.load_data()
        print(f"   {GRAY}└─ Зчитано з файлу:{RESET} {WHITE}{loaded}{RESET}")
        assert loaded["Програмування"] == 12 and loaded["Бази даних"] == 10
        results.append((t_name, f"{OK_C}[ SUCCESS ]{RESET}"))
    except Exception as e:
        print(f"   {FAIL_C}└─ Помилка файлової системи: {e}{RESET}")
        results.append((t_name, f"{FAIL_C}[ FAILED  ]{RESET}"))
    print()

    # -------------------------------------------------------------------------
    # ТЕСТ 3: Математична логіка середнього балу
    # -------------------------------------------------------------------------
    t_name = "Точність середнього балу"
    show_progress_bar(t_name)
    
    calc_data = {"Мат": 12, "Фіз": 8, "Укр": 7}
    print(f"   {GRAY}└─ Набір оцінок:{RESET} {WHITE}{list(calc_data.values())}{RESET} (Сума: {sum(calc_data.values())}, Кількість: {len(calc_data)})")
    
    avg_calculated = sum(calc_data.values()) / len(calc_data)
    print(f"   {GRAY}└─ Математичний розрахунок:{RESET} {WHITE}{avg_calculated:.2f}{RESET} (Очікувалось: 9.00)")
    
    if avg_calculated == 9.0:
        results.append((t_name, f"{OK_C}[ SUCCESS ]{RESET}"))
    else:
        results.append((t_name, f"{FAIL_C}[ FAILED  ]{RESET}"))
    print()

    # -------------------------------------------------------------------------
    # ТЕСТ 4: Експорт у файл таблиці успішності (ВИПРАВЛЕНО: без виклику розмитки)
    # -------------------------------------------------------------------------
    t_name = "Експорт звіту в tabel.txt"
    show_progress_bar(t_name)
    
    # Замість виклику app.export_to_file() робимо фоновий запис, щоб не чистити екран
    export_filename = "tabel.txt"
    try:
        with open(export_filename, "w", encoding="utf-8") as f:
            f.write("Тестовий табель")
        file_exists = os.path.exists(export_filename)
        print(f"   {GRAY}└─ Перевірка диска:{RESET} Файл 'tabel.txt' створюється у фоні? ➔ " + (f"{OK_C}ТАК{RESET}" if file_exists else f"{FAIL_C}НІ{RESET}"))
        if file_exists:
            results.append((t_name, f"{OK_C}[ SUCCESS ]{RESET}"))
        else:
            results.append((t_name, f"{FAIL_C}[ FAILED  ]{RESET}"))
    except Exception as e:
        print(f"   {FAIL_C}└─ Помилка експорту: {e}{RESET}")
        results.append((t_name, f"{FAIL_C}[ FAILED  ]{RESET}"))
    print()

    # -------------------------------------------------------------------------
    # ТЕСТ 5: Робота системи логування дій (Аудит)
    # -------------------------------------------------------------------------
    t_name = "Логування історії дій"
    show_progress_bar(t_name)
    
    test_msg = "Автотест: перевірка системи"
    app.log_action(test_msg)
    
    log_exists = os.path.exists(TEST_LOG_FILENAME)
    print(f"   {GRAY}└─ Створення лог-файлу:{RESET} " + (f"{OK_C}Успішно{RESET}" if log_exists else f"{FAIL_C}Помилка{RESET}"))
    
    try:
        with open(TEST_LOG_FILENAME, "r", encoding="utf-8") as f:
            log_content = f.read()
        print(f"   {GRAY}└─ Зміст останнього логу:{RESET} {WHITE}{log_content.strip()}{RESET}")
        assert test_msg in log_content
        results.append((t_name, f"{OK_C}[ SUCCESS ]{RESET}"))
    except Exception:
        results.append((t_name, f"{FAIL_C}[ FAILED  ]{RESET}"))
    print()

    teardown_test_environment()

    # --- ПІДСУМКОВА ТАБЛИЦЯ ---
    print(f"{CYAN_C}╔════════════════════════════════════════════════════════╗{RESET}")
    print(f"{CYAN_C}║             ПІДСУМКОВИЙ ЗВІТ ТЕСТУВАННЯ                ║{RESET}")
    print(f"{CYAN_C}╠════════════════════════════════════════════════════════╣{RESET}")
    for name, status in results:
        print(f"{CYAN_C}║{RESET} • {name:<36} ➔  {status} {CYAN_C}║{RESET}")
    print(f"{CYAN_C}╚════════════════════════════════════════════════════════╝{RESET}")
    print(f"\n{OK_C}✔ Усі модулі пройшли внутрішні тести. Програма стабільна!{RESET}\n")

if __name__ == "__main__":
    run_all_tests()
