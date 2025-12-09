import sqlite3

class SQLInjectionDemo:
    def __init__(self):
        # Використовуємо базу даних в оперативній пам'яті для зручності
        self.conn = sqlite3.connect(":memory:")
        self.cursor = self.conn.cursor()
        self._setup_database()

    def _setup_database(self):
        """Створення таблиці та наповнення тестовими даними"""
        self.cursor.execute("""
            CREATE TABLE users (
                id INTEGER PRIMARY KEY,
                username TEXT,
                password TEXT,
                secret_info TEXT
            )
        """)
        
        # Додаємо "жертв"
        users = [
            (1, "admin", "admin123", "СУПЕР СЕКРЕТНИЙ КЛЮЧ АДМІНА"),
            (2, "ivan", "pass123", "Номер картки Івана: 4141..."),
            (3, "maria", "flower", "Адреса Марії: вул. Шевченка, 10"),
        ]
        self.cursor.executemany("INSERT INTO users VALUES (?, ?, ?, ?)", users)
        self.conn.commit()
        print("[INFO] База даних створена. Користувачі: admin, ivan, maria")

    def vulnerable_search(self, user_input):
        """
        ВРАЗЛИВА ФУНКЦІЯ
        Пряме підставлення вводу в рядок запиту.
        """
        print(f"\n--- [Вразливий пошук] ---")
        
        #Форматування рядка з неперевіреним вводом
        sql_query = f"SELECT * FROM users WHERE username = '{user_input}'"
        
        print(f"[LOG] Виконується SQL: {sql_query}")
        
        try:
            # cur.executescript дозволяє виконати кілька команд, що ще небезпечніше,
            # але для SELECT достатньо звичайного execute, щоб показати витік даних.
            self.cursor.execute(sql_query)
            results = self.cursor.fetchall()
            self._print_results(results)
        except Exception as e:
            print(f"[ERROR] Помилка SQL: {e}")

    def secure_search(self, user_input):
        """
        ЗАХИЩЕНА ФУНКЦІЯ
        Використання параметризованого запиту (Placeholder).
        """
        print(f"\n--- [Захищений пошук] ---")
        
        #Використання знака питання як плейсхолдера
        sql_query = "SELECT * FROM users WHERE username = ?"
        
        print(f"[LOG] Шаблон SQL: {sql_query}")
        print(f"[LOG] Параметри: ('{user_input}',)")
        
        try:
            # Драйвер БД сам екранує ввід, трактуючи його виключно як дані, а не код
            self.cursor.execute(sql_query, (user_input,))
            results = self.cursor.fetchall()
            self._print_results(results)
        except Exception as e:
            print(f"[ERROR] Помилка SQL: {e}")

    def _print_results(self, results):
        if not results:
            print(">> Результат: Нічого не знайдено.")
        else:
            print(f">> Знайдено записів: {len(results)}")
            for row in results:
                print(f"   ID: {row[0]} | User: {row[1]} | Secret: {row[3]}")

# --- ДЕМОНСТРАЦІЯ ---
def run():
    app = SQLInjectionDemo()

    while True:
        print("\n" + "="*50)
        print("МЕНЮ:")
        print("1. Звичайний пошук (наприклад, 'ivan')")
        print("2. АТАКА на вразливу версію")
        print("3. Спроба атаки на захищену версію")
        print("4. Вихід")
        choice = input("Ваш вибір: ")

        if choice == '1':
            name = input("Введіть ім'я: ")
            app.vulnerable_search(name)
        
        elif choice == '2':
            print("\n[HACK] Вводимо пейлоад: ' OR '1'='1")
            # Цей payload робить умову завжди істинною (TRUE)
            payload = "' OR '1'='1" 
            app.vulnerable_search(payload)
            
        elif choice == '3':
            print("\n[TEST] Вводимо той самий пейлоад у захищену систему...") 
            payload = "' OR '1'='1"
            app.secure_search(payload)
            
        elif choice == '4':
            break

if __name__ == "__main__":
    run()