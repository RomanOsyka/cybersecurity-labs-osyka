import hashlib
import base64
from cryptography.fernet import Fernet
import os

class SecureMessenger:
    def __init__(self, personal_data: str):
        """
        Ініціалізація месенджера.
        Ключ генерується на основі персональних даних (симетричний алгоритм).
        """
        self.key = self._generate_key(personal_data)
        self.cipher = Fernet(self.key)

    def _generate_key(self, raw_data: str) -> bytes:
        """
        Генерація 32-байтного URL-safe ключа для Fernet
        на основі хешу (SHA-256) від вхідного рядка.
        """
        # 1. Отримуємо хеш SHA-256 від даних (це дає 32 байти)
        digest = hashlib.sha256(raw_data.encode('utf-8')).digest()
        
        # 2. Fernet вимагає base64 кодування ключа
        return base64.urlsafe_b64encode(digest)

    def encrypt_message(self, message: str) -> str:
        """Шифрує повідомлення"""
        if not message:
            return ""
        # Fernet працює з байтами, тому кодуємо рядок
        encrypted_bytes = self.cipher.encrypt(message.encode('utf-8'))
        # Повертаємо як рядок для зручності читання
        return encrypted_bytes.decode('utf-8')

    def decrypt_message(self, encrypted_token: str) -> str:
        """Розшифровує повідомлення"""
        try:
            decrypted_bytes = self.cipher.decrypt(encrypted_token.encode('utf-8'))
            return decrypted_bytes.decode('utf-8')
        except Exception as e:
            return f"[ПОМИЛКА] Невірний ключ або пошкоджені дані: {e}"

    def get_key_display(self) -> str:
        """Повертає ключ у читабельному вигляді"""
        return self.key.decode('utf-8')


# --- ДЕМОНСТРАЦІЯ ---
def run():
    print("="*60)
    print("      СИСТЕМА ЗАХИЩЕНОГО ОБМІНУ ПОВІДОМЛЕННЯМИ")
    print("="*60)

    # 1. Етап налаштування відправника
    print("\n[КРОК 1] Налаштування Відправника")
    sender_data = "RomanOsyka2005"  # Персональні дані для генерації ключа
    sender = SecureMessenger(sender_data)
    
    print(f"Дані для ключа: '{sender_data}'")
    print(f"Згенерований симетричний ключ: {sender.get_key_display()}")

    # 2. Етап шифрування
    print("\n[КРОК 2] Шифрування повідомлення")
    email_body = "Зустрічаємося завтра о 15:00"
    print(f"Оригінальний текст: \"{email_body}\"")
    
    encrypted_msg = sender.encrypt_message(email_body)
    print(f"Зашифровані дані (ciphertext):\n{encrypted_msg}")

    # 3. Етап отримання (Спроба розшифрувати правильним ключем)
    print("\n[КРОК 3] Отримувач (з правильним ключем)")
    # У симетричному шифруванні отримувач повинен мати той самий секрет 
    receiver_correct = SecureMessenger("RomanOsyka2005") 
    decrypted_msg = receiver_correct.decrypt_message(encrypted_msg)
    
    print(f"Спроба розшифрування: \"{decrypted_msg}\"")
    
    if decrypted_msg == email_body:
        print(">> УСПІХ: Повідомлення прочитано коректно.")
    
    # 4. Етап спроби злому (неправильний ключ)
    print("\n[КРОК 4] Перехоплювач (з неправильним ключем)")
    hacker = SecureMessenger("HackerData123") # Інший ключ
    hacker_result = hacker.decrypt_message(encrypted_msg)
    print(f"Спроба злому: {hacker_result}")

if __name__ == "__main__":
    run()