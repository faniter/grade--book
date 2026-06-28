import json
import os
import time
import random
from datetime import datetime

if os.name == 'nt':
    os.system('')

FILENAME = "gradebook_data.json"
LOG_FILENAME = "history.log"

# Кольорова схема
CYAN = "\033[96m"         # Бірюзовий
BLUE = "\033[94m"         # Синій
GREEN = "\033[92m"        # Зелений
RESET = "\033[0m"         # Скидання
WHITE = "\033[97m"         # Білий
PURPLE = "\033[35m"        # Фіолетовий
GRAY = "\033[90m"          # Сірий колір для порожніх поділок графіка

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_ects(grade):
    if 10 <= grade <= 12: return f"(A) - Відмінно"
    elif grade == 9: return f"(B) - Дуже добре"
    elif grade == 8: return f"(C) - Добре"
    elif grade == 7: return f"(D) - Задовільно"
    elif grade == 6: return f"(E) - Достатньо"
    elif grade in [4, 5]: return f"(FX) - Незадовільно (з перездачею)"
    else: return f"(F) - Незадовільно (з повторним курсом)"

def log_action(action_text):
    now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    with open(LOG_FILENAME, "a", encoding="utf-8") as f:
        f.write(f"[{now}] {action_text}\n")

def load_data():
    if os.path.exists(FILENAME):
        with open(FILENAME, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(FILENAME, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def add_record(data):
    clear_screen()
    print(f"{CYAN}┌────────────────────────────────────────┐{RESET}")
    print(f"{CYAN}│        ДОДАВАННЯ НОВОГО ПРЕДМЕТА       │{RESET}")
    print(f"{CYAN}└────────────────────────────────────────┘{RESET}\n")
    subject = input(f"{BLUE}➔ Введіть назву предмета:{RESET} ").strip()
    
    if not subject:
        print(f"\n{PURPLE}⚠ Назва предмета не може бути порожньою!{RESET}")
        time.sleep(2)
        return

    while True:
        try:
            grade = int(input(f"{BLUE}➔ Введіть оцінку (1-12):{RESET} "))
            if 1 <= grade <= 12:
                data[subject] = grade
                save_data(data)
                log_action(f"Додано предмет '{subject}' з оцінкою {grade}")
                print(f"\n{GREEN}✔ Запис успішно додано!{RESET}")
                break
            else:
                print(f"{PURPLE}⚠ Оцінка повинна бути в межах від 1 до 12.{RESET}")
        except ValueError:
            print(f"{PURPLE}⚠ Необхідно ввести ціле число.{RESET}")
    
    input(f"\n{CYAN}Натисніть Enter, щоб повернутися в меню...{RESET}")

def view_all(data):
    clear_screen()
    print(f"{CYAN}┌────────────────────────────────────────┐{RESET}")
    print(f"{CYAN}│          УСІ ОЦІНКИ ТА СИСТЕМА ECTS    │{RESET}")
    print(f"{CYAN}└────────────────────────────────────────┘{RESET}\n")
    if not data:
        print(f"{PURPLE}Журнал порожній.{RESET}\n")
    else:
        for subject, grade in data.items():
            print(f" {BLUE}• {subject:<20}{RESET} ➔  {WHITE}{grade:<2}{RESET} {GREEN}{get_ects(grade)}{RESET}")
    print(f"\n{CYAN}──────────────────────────────────────────{RESET}")
    input(f"{CYAN}Натисніть Enter, щоб повернутися в меню...{RESET}")

def calc_average(data):
    clear_screen()
    print(f"{CYAN}┌────────────────────────────────────────┐{RESET}")
    print(f"{CYAN}│          ПІДРАХУНОК СЕРЕДНЬОГО БАЛУ    │{RESET}")
    print(f"{CYAN}└────────────────────────────────────────┘{RESET}\n")
    if not data:
        print(f"{PURPLE}Немає даних для підрахунку.{RESET}\n")
    else:
        avg = sum(data.values()) / len(data)
        print(f" {BLUE}Ваш поточний середній бал:{RESET} {WHITE}{avg:.2f}{RESET}\n")
    print(f"{CYAN}──────────────────────────────────────────{RESET}")
    input(f"{CYAN}Натисніть Enter, щоб повернутися в меню...{RESET}")

def find_worst(data):
    clear_screen()
    print(f"{CYAN}┌────────────────────────────────────────┐{RESET}")
    print(f"{CYAN}│         ПОШУК НАЙГІРШОГО ПРЕДМЕТА      │{RESET}")
    print(f"{CYAN}└────────────────────────────────────────┘{RESET}\n")
    if not data:
        print(f"{PURPLE}Журнал порожній.{RESET}\n")
    else:
        worst_subject = min(data, key=data.get)
        grade = data[worst_subject]
        print(f" {BLUE}Найгірший предмет:{RESET} {WHITE}{worst_subject}{RESET}")
        print(f" {BLUE}Оцінка:{RESET}            {PURPLE}{grade}{RESET} {GREEN}{get_ects(grade)}{RESET}\n")
    print(f"{CYAN}──────────────────────────────────────────{RESET}")
    input(f"{CYAN}Натисніть Enter, щоб повернутися в меню...{RESET}")

def find_best(data):
    clear_screen()
    print(f"{CYAN}┌────────────────────────────────────────┐{RESET}")
    print(f"{CYAN}│         ПОШУК НАЙКРАЩОГО ПРЕДМЕТА      │{RESET}")
    print(f"{CYAN}└────────────────────────────────────────┘{RESET}\n")
    if not data:
        print(f"{PURPLE}Журнал порожній.{RESET}\n")
    else:
        best_subject = max(data, key=data.get)
        grade = data[best_subject]
        print(f" {GREEN}Найкращий предмет:{RESET} {WHITE}{best_subject}{RESET}")
        print(f" {GREEN}Оцінка:{RESET}            {GREEN}{grade}{RESET} {CYAN}{get_ects(grade)}{RESET}\n")
    print(f"{CYAN}──────────────────────────────────────────{RESET}")
    input(f"{CYAN}Натисніть Enter, щоб повернутися в меню...{RESET}")

def view_history_and_manage():
    while True:
        clear_screen()
        print(f"{CYAN}┌────────────────────────────────────────┐{RESET}")
        print(f"{CYAN}│       ІСТОРІЯ ДІЙ ТА КЕРУВАННЯ ЛОГАМИ  │{RESET}")
        print(f"{CYAN}└────────────────────────────────────────┘{RESET}\n")
        
        if not os.path.exists(LOG_FILENAME) or os.stat(LOG_FILENAME).st_size == 0:
            print(f"{PURPLE}Історія дій порожня.{RESET}\n")
            print(f"{CYAN}[0]{RESET} Назад до головного меню")
            choice = input(f"\n{CYAN}➔ Ваш вибір:{RESET} ")
            if choice == '0': break
            continue
            
        with open(LOG_FILENAME, "r", encoding="utf-8") as f:
            logs = f.readlines()
            
        for idx, log_line in enumerate(logs, start=1):
            print(f" {CYAN}[{idx}]{RESET} {WHITE}{log_line.strip()}{RESET}")
        
        print(f"\n{CYAN}──────────────────────────────────────────{RESET}")
        print(f"{CYAN}[D]{RESET} {PURPLE}Видалити конкретний запис{RESET}  {CYAN}[C]{RESET} {PURPLE}Очистити все{RESET}  {CYAN}[0]{RESET} {BLUE}Назад{RESET}")
        
        choice = input(f"\n{CYAN}➔ Ваш вибір:{RESET} ").strip().lower()
        
        if choice == '0': break
        elif choice == 'c':
            confirm = input(f"{PURPLE}Ви впевнені? (д/н):{RESET} ").strip().lower()
            if confirm in ['д', 'так', 'y']:
                open(LOG_FILENAME, 'w', encoding='utf-8').close()
                print(f"{GREEN}Історію очищено!{RESET}")
                time.sleep(1)
        elif choice == 'd':
            try:
                num = int(input(f"{CYAN}Номер запису для видалення:{RESET} "))
                if 1 <= num <= len(logs):
                    logs.pop(num - 1)
                    with open(LOG_FILENAME, "w", encoding="utf-8") as f:
                        f.writelines(logs)
                    print(f"{GREEN}Запис видалено!{RESET}")
                else:
                    print(f"{PURPLE}Неправильний номер!{RESET}")
                time.sleep(1)
            except ValueError:
                print(f"{PURPLE}Введіть число!{RESET}")
                time.sleep(1)

def delete_records(data):
    while True:
        clear_screen()
        print(f"{CYAN}┌────────────────────────────────────────┐{RESET}")
        print(f"{CYAN}│           ВИДАЛЕННЯ ТА СКИДАННЯ        │{RESET}")
        print(f"{CYAN}└────────────────────────────────────────┘{RESET}\n")
        print(f" {CYAN}[1]{RESET} {GREEN}Видалити один конкретний предмет{RESET}")
        print(f" {CYAN}[2]{RESET} {GREEN}Повністю очистити журнал оцінок{RESET}")
        print(f" {CYAN}[0]{RESET} {PURPLE}Назад до головного меню{RESET}")
        print(f"\n{CYAN}──────────────────────────────────────────{RESET}")
        
        choice = input(f"{CYAN}➔ Ваш вибір:{RESET} ")
        
        if choice == '1':
            clear_screen()
            if not data:
                print(f"{PURPLE}Журнал порожній.{RESET}\n")
                time.sleep(1)
                continue
            print(f"{CYAN}--- Список предметів ---{RESET}")
            for subject in data.keys(): print(f" • {BLUE}{subject}{RESET}")
            print(f"────────────────────────\n")
            del_subject = input(f"{CYAN}Введіть назву предмета:{RESET} ").strip()
            if del_subject in data:
                old_grade = data[del_subject]
                del data[del_subject]
                save_data(data)
                log_action(f"Видалено предмет '{del_subject}' (була оцінка {old_grade})")
                print(f"\n{GREEN}✔ Предмет успішно видалено!{RESET}")
            else:
                print(f"\n{PURPLE}⚠ Предмет не знайдено.{PURPLE}")
            time.sleep(1.5)
        elif choice == '2':
            clear_screen()
            confirm = input(f"{PURPLE}Видалити ВСІ оцінки? (д/н):{RESET} ").strip().lower()
            if confirm in ['д', 'y', 'так']:
                data.clear()
                save_data(data)
                log_action("Повне скидання журналу")
                print(f"\n{GREEN}✔ Усі оцінки видалено!{RESET}")
            else:
                print(f"\n{BLUE}Скасовано.{RESET}")
            time.sleep(1.5)
            break
        elif choice == '0': break

def edit_record(data):
    clear_screen()
    print(f"{CYAN}┌────────────────────────────────────────┐{RESET}")
    print(f"{CYAN}│          РЕДАГУВАННЯ ОЦІНКИ            │{RESET}")
    print(f"{CYAN}└────────────────────────────────────────┘{RESET}\n")
    if not data:
        print(f"{PURPLE}Журнал порожній.{RESET}\n")
        input(f"{CYAN}Натисніть Enter для повернення...{RESET}")
        return

    for subject, grade in data.items():
        print(f" • {BLUE}{subject:<20}{RESET} (Поточна: {WHITE}{grade}{RESET})")
    print(f"──────────────────────────────────────────\n")
    
    subject = input(f"{CYAN}➔ Введіть назву предмета для зміни:{RESET} ").strip()
    if subject in data:
        old_grade = data[subject]
        while True:
            try:
                new_grade = int(input(f"{BLUE}➔ Введіть НОВА оцінку (1-12):{RESET} "))
                if 1 <= new_grade <= 12:
                    data[subject] = new_grade
                    save_data(data)
                    log_action(f"Змінено '{subject}' з {old_grade} на {new_grade}")
                    print(f"\n{GREEN}✔ Оцінку успішно оновлено!{RESET}")
                    break
                else:
                    print(f"{PURPLE}⚠ Оцінка має бути від 1 до 12.{RESET}")
            except ValueError:
                print(f"{PURPLE}⚠ Введіть ціле число.{RESET}")
    else:
        print(f"\n{PURPLE}⚠ Предмет '{subject}' не знайдено!{RESET}")
    input(f"\n{CYAN}Натисніть Enter, щоб повернутися в меню...{RESET}")

def view_sorted(data):
    clear_screen()
    print(f"{CYAN}┌────────────────────────────────────────┐{RESET}")
    print(f"{CYAN}│        СОРТУВАННЯ (ВІД ВИЩОЇ ДО НИЖЧОЇ)│{RESET}")
    print(f"{CYAN}└────────────────────────────────────────┘{RESET}\n")
    if not data:
        print(f"{PURPLE}Журнал порожній.{RESET}\n")
    else:
        sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)
        for subject, grade in sorted_data:
            color = GREEN if grade >= 10 else (BLUE if grade >= 7 else PURPLE)
            print(f" {BLUE}• {subject:<20}{RESET} ➔  {color}{grade:<2}{RESET} {GREEN}{get_ects(grade)}{RESET}")
    print(f"\n{CYAN}──────────────────────────────────────────{RESET}")
    input(f"{CYAN}Натисніть Enter, щоб повернутися в меню...{RESET}")

def show_statistics(data):
    clear_screen()
    print(f"{CYAN}┌────────────────────────────────────────┐{RESET}")
    print(f"{CYAN}│          СТАТИСТИКА ТА АНАЛІТИКА       │{RESET}")
    print(f"{CYAN}└────────────────────────────────────────┘{RESET}\n")
    if not data:
        print(f"{PURPLE}Немає даних для аналізу.{RESET}\n")
        input(f"{CYAN}Натисніть Enter для повернення...{RESET}")
        return

    total = len(data)
    exc = sum(1 for g in data.values() if 10 <= g <= 12)
    gd = sum(1 for g in data.values() if 7 <= g <= 9)
    sat = sum(1 for g in data.values() if 4 <= g <= 6)
    bad = sum(1 for g in data.values() if 1 <= g <= 3)

    print(f" {BLUE}Всього предметів у журналі:{RESET} {WHITE}{total}{RESET}\n")
    print(f" {GREEN}● Відмінно (10-12):{RESET}  {WHITE}{exc}{RESET}")
    print(f" {BLUE}● Добре (7-9):{RESET}      {WHITE}{gd}{RESET}")
    print(f" {CYAN}● Задовільно (4-6):{RESET} {WHITE}{sat}{RESET}")
    print(f" {PURPLE}● Борги (1-3):{RESET}      {WHITE}{bad}{RESET}")
    print(f"\n{CYAN}──────────────────────────────────────────{RESET}")
    input(f"{CYAN}Натисніть Enter, щоб повернутися в меню...{RESET}")

def search_subject(data):
    clear_screen()
    print(f"{CYAN}┌────────────────────────────────────────┐{RESET}")
    print(f"{CYAN}│             ПОШУК ПРЕДМЕТА             │{RESET}")
    print(f"{CYAN}└────────────────────────────────────────┘{RESET}\n")
    if not data:
        print(f"{PURPLE}Журнал порожній.{RESET}\n")
        input(f"{CYAN}Натисніть Enter для повернення...{RESET}")
        return

    query = input(f"{CYAN}➔ Введіть назву (або частину назви):{RESET} ").strip().lower()
    found = False
    print(f"\n{CYAN}--- Результати пошуку ---{RESET}")
    for subject, grade in data.items():
        if query in subject.lower():
            print(f" {BLUE}• {subject:<20}{RESET} ➔  {WHITE}{grade:<2}{RESET} {GREEN}{get_ects(grade)}{RESET}")
            found = True
    if not found: print(f"{PURPLE}Збігів не знайдено.{RESET}")
    print(f"{CYAN}──────────────────────────────────────────{RESET}\n")
    input(f"{CYAN}Натисніть Enter, щоб повернутися в меню...{RESET}")

def check_scholarship(data):
    clear_screen()
    print(f"{CYAN}┌────────────────────────────────────────┐{RESET}")
    print(f"{CYAN}│          СТИПЕНДІАЛЬНИЙ СТАТУС         │{RESET}")
    print(f"{CYAN}└────────────────────────────────────────┘{RESET}\n")
    if not data:
        print(f"{PURPLE}Немає даних.{RESET}\n")
        input(f"{CYAN}Натисніть Enter для повернення...{RESET}")
        return

    avg = sum(data.values()) / len(data)
    has_debts = any(g < 4 for g in data.values())

    print(f" {BLUE}Ваш точний середній бал:{RESET} {WHITE}{avg:.2f}{RESET}")
    print(f"{CYAN}──────────────────────────────────────────{RESET}")
    if has_debts: print(f" {PURPLE}Вердикт: Немає стипендії (наявні борги 1-3 бали).{RESET}")
    elif avg >= 10.0: print(f" {GREEN}Вердикт: Ви проходите на ПІДВИЩЕНУ стипендію! 🎉{RESET}")
    elif avg >= 7.5: print(f" {GREEN}Вердикт: Ви проходите на ЗВИЧАЙНУ стипендію. 👍{RESET}")
    else: print(f" {PURPLE}Вердикт: Немає стипендії (бал нижче ніж 7.5).{RESET}")
    print(f"{CYAN}──────────────────────────────────────────{RESET}\n")
    input(f"{CYAN}Натисніть Enter, щоб повернутися в меню...{RESET}")

# [13] МОДИФІКОВАНИЙ ГРАФІК УСПІШНОСТІ (Шкала на 12 поділок з кольоровим заповненням)
def view_graph(data):
    clear_screen()
    print(f"{CYAN}┌────────────────────────────────────────┐{RESET}")
    print(f"{CYAN}│      ГРАФІК УСПІШНОСТІ (ШКАЛА 1-12)    │{RESET}")
    print(f"{CYAN}└────────────────────────────────────────┘{RESET}\n")
    if not data:
        print(f"{PURPLE}Журнал порожній, немає даних для графіка.{RESET}\n")
    else:
        for subject, grade in data.items():
            # Визначаємо колір заповненої частини залежно від оцінки
            color = GREEN if grade >= 10 else (BLUE if grade >= 7 else PURPLE)
            
            filled_bar = color + "█" * grade + RESET       # Кольорові заповнені поділки
            empty_bar = GRAY + "░" * (12 - grade) + RESET  # Сірі порожні поділки (завжди до 12)
            
            print(f" {WHITE}{subject:<18}{RESET} [{filled_bar}{empty_bar}] {color}{grade:>2} балів{RESET}")
            
    print(f"\n{CYAN}──────────────────────────────────────────{RESET}")
    input(f"{CYAN}Натисніть Enter, щоб повернутися в меню...{RESET}")

# [14] ГЕНЕРАТОР ДЕМО-ДАНИХ ДЛЯ ШВИДКОГО ТЕСТУ
def generate_demo_data(data):
    clear_screen()
    print(f"{CYAN}┌────────────────────────────────────────┐{RESET}")
    print(f"{CYAN}│       ГЕНЕРАЦІЯ ДЕМО-ОЦІНОК            │{RESET}")
    print(f"{CYAN}└────────────────────────────────────────┘{RESET}\n")
    
    confirm = input(f"{BLUE}➔ Додати 6 випадкових предметів для тесту? (д/н):{RESET} ").strip().lower()
    if confirm in ['д', 'y', 'так']:
        demo_subjects = ["Математика", "Програмування", "Фізика", "Історія", "Англійська мова", "Бази даних"]
        for sub in demo_subjects:
            data[sub] = random.randint(3, 12) # Генеруємо бали від 3 до 12
        save_data(data)
        log_action("Згенеровано демо-дані для тестування програми")
        print(f"\n{GREEN}✔ Демо-дані успішно створено! Перевірте список або графік.{RESET}")
    else:
        print(f"\n{PURPLE}Скасовано.{RESET}")
        
    print(f"\n{CYAN}──────────────────────────────────────────{RESET}")
    input(f"{CYAN}Натисніть Enter, щоб повернутися в меню...{RESET}")

# [15] ЕКСПОРТ У ТАБЕЛЬ (Гарний текстовий файл)
def export_to_file(data):
    clear_screen()
    print(f"{CYAN}┌────────────────────────────────────────┐{RESET}")
    print(f"{CYAN}│          ЕКСПОРТ У ТАБЕЛЬ УСПІШНОСТІ   │{RESET}")
    print(f"{CYAN}└────────────────────────────────────────┘{RESET}\n")
    
    if not data:
        print(f"{PURPLE}⚠ Помилка: Журнал порожній. Немає даних для експорту!{RESET}\n")
        print(f"{CYAN}──────────────────────────────────────────{RESET}")
        input(f"{CYAN}Натисніть Enter для повернення в меню...{RESET}")
        return

    export_filename = "tabel.txt"
    avg = sum(data.values()) / len(data)
    
    # Миттєвий запис у файл
    with open(export_filename, "w", encoding="utf-8") as f:
        f.write("==================================================\n")
        f.write("                ТАБЕЛЬ УСПІШНОСТІ                 \n")
        f.write("==================================================\n\n")
        f.write(f" Дата генерації: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n")
        f.write("--------------------------------------------------\n")
        f.write(f" {'Назва предмета':<25} | {'Бал':<4} | {'Система ECTS'}\n")
        f.write("--------------------------------------------------\n")
        for subject, grade in data.items():
            f.write(f" {subject:<25} | {grade:<4} | {get_ects(grade)}\n")
        f.write("--------------------------------------------------\n")
        f.write(f" Середній академічний бал: {avg:.2f}\n")
        f.write("==================================================\n")

    # --- ОДРАЗУ ВИВОДИМО РЕЗУЛЬТАТ ВИКОНАННЯ ---
    print(f"{GREEN}✔ Табель успішно збережено у файл '{export_filename}'!{RESET}")
    print(f"{BLUE}Ви можете відкрити його через Блокнот та роздрукувати.{RESET}\n")

    print(f"{CYAN}┌────────────────────────────────────────┐{RESET}")
    print(f"{CYAN}║         РЕЗУЛЬТАТ ОПЕРАЦІЇ             ║{RESET}")
    print(f"{CYAN}╠════════════════════════════════════════╣{RESET}")
    print(f"{CYAN}║{RESET} • Кількість предметів: {WHITE}{len(data):<15}{RESET}{CYAN}║{RESET}")
    print(f"{CYAN}║{RESET} • Підсумковий бал:     {WHITE}{avg:<15.2f}{RESET}{CYAN}║{RESET}")
    print(f"{CYAN}║{RESET} • Статус запису:       {GREEN}{'УСПІШНО ЗАПИСАНО':<15}{RESET}{CYAN}║{RESET}")
    print(f"{CYAN}╚════════════════════════════════════════╝{RESET}")
    
    print(f"\n{CYAN}──────────────────────────────────────────{RESET}")
    input(f"{CYAN}Натисніть Enter, щоб повернутися в меню...{RESET}")

def main():
    data = load_data()
    while True:
        clear_screen()
        print(f"{CYAN}╔════════════════════════════════════════╗{RESET}")
        print(f"{CYAN}║             ЖУРНАЛ ОЦІНОК              ║{RESET}")
        print(f"{CYAN}╠════════════════════════════════════════╣{RESET}")
        print(f"{CYAN}║ [ БАЗОВІ ОПЕРАЦІЇ ]                    ║{RESET}")
        print(f"{CYAN}║{RESET}  {CYAN}[1]{RESET}  {BLUE}Додати предмет і оцінку{RESET}        {CYAN}  ║{RESET}")
        print(f"{CYAN}║{RESET}  {CYAN}[2]{RESET}  {BLUE}Переглянути всі оцінки + ECTS{RESET}  {CYAN}  ║{RESET}")
        print(f"{CYAN}║{RESET}  {CYAN}[3]{RESET}  {BLUE}Підрахувати середній бал{RESET}       {CYAN}  ║{RESET}")
        print(f"{CYAN}║{RESET}  {CYAN}[4]{RESET}  {BLUE}Знайти найгірший предмет{RESET}       {CYAN}  ║{RESET}")
        print(f"{CYAN}║                                        ║{RESET}")
        print(f"{CYAN}║ [ ДОДАТКОВІ ОПЕРАЦІЇ ]                 ║{RESET}")
        print(f"{CYAN}║{RESET}  {CYAN}[5]{RESET}  {GREEN}Знайти найкращий предмет{RESET}       {CYAN}  ║{RESET}")
        print(f"{CYAN}║{RESET}  {CYAN}[6]{RESET}  {GREEN}Редагувати оцінку{RESET}              {CYAN}  ║{RESET}")
        print(f"{CYAN}║{RESET}  {CYAN}[7]{RESET}  {GREEN}Сортування оцінок{RESET}              {CYAN}  ║{RESET}")
        print(f"{CYAN}║{RESET}  {CYAN}[8]{RESET}  {GREEN}Статистика та аналітика{RESET}        {CYAN}  ║{RESET}")
        print(f"{CYAN}║{RESET}  {CYAN}[9]{RESET}  {GREEN}Пошук предмета{RESET}                 {CYAN}  ║{RESET}")
        print(f"{CYAN}║{RESET}  {CYAN}[10]{RESET} {GREEN}Розрахунок стипендії{RESET}           {CYAN}  ║{RESET}")
        print(f"{CYAN}║{RESET}  {CYAN}[11]{RESET} {GREEN}Історія дій та логування{RESET}       {CYAN}  ║{RESET}")
        print(f"{CYAN}║{RESET}  {CYAN}[12]{RESET} {GREEN}Очищення журналу / видалення{RESET}   {CYAN}  ║{RESET}")
        print(f"{CYAN}║{RESET}  {CYAN}[13]{RESET} {GREEN}Графік успішності (Шкала 1-12){RESET} {CYAN}  ║{RESET}")
        print(f"{CYAN}║{RESET}  {CYAN}[14]{RESET} {GREEN}Згенерувати демо-оцінки{RESET}        {CYAN}  ║{RESET}")
        print(f"{CYAN}║{RESET}  {CYAN}[15]{RESET} {GREEN}Експорт у файл \"tabel.txt\"{RESET}      {CYAN} ║{RESET}")
        print(f"{CYAN}║                                        ║{RESET}")
        print(f"{CYAN}║{RESET}  {CYAN}[0]{RESET}  {PURPLE}Вийти з програми{RESET}               {CYAN}  ║{RESET}")
        print(f"{CYAN}╚════════════════════════════════════════╝{RESET}")
        
        choice = input(f"{CYAN}➔ Ваш вибір:{RESET} ").strip()
        
        if choice == '1': add_record(data)
        elif choice == '2': view_all(data)
        elif choice == '3': calc_average(data)
        elif choice == '4': find_worst(data)
        elif choice == '5': find_best(data)
        elif choice == '6': edit_record(data)
        elif choice == '7': view_sorted(data)
        elif choice == '8': show_statistics(data)
        elif choice == '9': search_subject(data)
        elif choice == '10': check_scholarship(data)
        elif choice == '11': view_history_and_manage()
        elif choice == '12': delete_records(data)
        elif choice == '13': view_graph(data)
        elif choice == '14': generate_demo_data(data)
        elif choice == '15': export_to_file(data)
        elif choice == '0':
            clear_screen()
            print(f"{PURPLE}Вихід з програми...{RESET}")
            time.sleep(1)
            break
        else:
            print(f"{PURPLE}Неправильний вибір!{RESET}")
            time.sleep(0.7)

if __name__ == "__main__":
    main()