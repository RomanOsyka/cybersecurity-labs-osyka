from PIL import Image
import os

class SteganographyTool:
    def __init__(self):
        self.delimiter = "#####"  # Маркер кінця повідомлення

    def _text_to_bin(self, message):
        """
        ВИПРАВЛЕНО: Конвертує текст у біти через UTF-8 encode.
        Це дозволяє працювати з кирилицею.
        """
        full_message = message + self.delimiter
        # Спочатку кодуємо рядок у байти UTF-8
        message_bytes = full_message.encode('utf-8')
        # Кожен байт (0-255) переводимо у 8 біт
        binary_message = ''.join(format(byte, '08b') for byte in message_bytes)
        return binary_message

    def _bin_to_text(self, binary_data):
        """
        ВИПРАВЛЕНО: Збирає біти назад у байти і декодує через UTF-8.
        """
        # Розбиваємо довгий рядок бітів на шматки по 8
        all_bytes = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
        
        # Перетворюємо біти назад у цілі числа (байти)
        byte_values = []
        for byte_str in all_bytes:
            byte_values.append(int(byte_str, 2))
            
        # Створюємо об'єкт bytes з чисел
        data_bytes = bytes(byte_values)
        
        try:
            # Спробуємо декодувати весь масив байтів
            # (errors='ignore' дозволяє уникнути падіння на "хвості" файлу, де може бути сміття)
            decoded_string = data_bytes.decode('utf-8', errors='ignore')
            
            if self.delimiter in decoded_string:
                return decoded_string.split(self.delimiter)[0]
            else:
                return decoded_string
        except Exception as e:
            return f"Помилка декодування: {e}"

    def hide_message(self, image_path, output_path, secret_message):
        try:
            img = Image.open(image_path)
            img = img.convert("RGB")
            width, height = img.size
            pixels = img.load()

            binary_msg = self._text_to_bin(secret_message)
            msg_len = len(binary_msg)
            
            if msg_len > width * height * 3:
                raise ValueError("Повідомлення занадто довге для цього зображення!")

            data_index = 0
            print(f"[LOG] Довжина бінарних даних: {msg_len} біт")

            for y in range(height):
                for x in range(width):
                    if data_index < msg_len:
                        r, g, b = pixels[x, y]

                        if data_index < msg_len:
                            r = (r & ~1) | int(binary_msg[data_index])
                            data_index += 1
                        if data_index < msg_len:
                            g = (g & ~1) | int(binary_msg[data_index])
                            data_index += 1
                        if data_index < msg_len:
                            b = (b & ~1) | int(binary_msg[data_index])
                            data_index += 1

                        pixels[x, y] = (r, g, b)
                    else:
                        break
                if data_index >= msg_len:
                    break
            
            img.save(output_path, "PNG")
            print(f"[SUCCESS] Повідомлення сховано у {output_path}")

        except Exception as e:
            print(f"[ERROR] Помилка при хованні: {e}")

    def extract_message(self, image_path):
        try:
            img = Image.open(image_path)
            img = img.convert("RGB")
            pixels = img.load()
            
            binary_data = ""
            width, height = img.size
            
            # Для оптимізації не будемо читати ВСЕ зображення, якщо воно велике.
            # Але для лабораторної можна читати все або достатню кількість.
            # Тут читаємо певну кількість пікселів для демонстрації.
            
            # ВАЖЛИВО: Щоб знайти "стоп-слово", нам треба читати поки не знайдемо його
            # або прочитати все зображення. Для надійності прочитаємо перші 4000 пікселів 
            # (це 12000 біт, вистачить на 1.5 кб тексту), або весь файл.
            
            limit_pixels = 4000 # Ліміт, щоб не зависло на 4K картинках
            count = 0

            for y in range(height):
                for x in range(width):
                    r, g, b = pixels[x, y]
                    binary_data += str(r & 1)
                    binary_data += str(g & 1)
                    binary_data += str(b & 1)
                    
                    count += 1
                    if count > limit_pixels: 
                        break
                if count > limit_pixels:
                    break

            return self._bin_to_text(binary_data)

        except Exception as e:
            return f"[ERROR] Помилка при вилученні: {e}"

if __name__ == "__main__":
    tool = SteganographyTool()

    # Створюємо input.png якщо немає
    if not os.path.exists("input.png"):
        img = Image.new('RGB', (200, 200), color = 'red') # Збільшив розмір для надійності
        img.save('input.png')

    my_data = """
    ПІБ: Осика Роман Дмитрович
    Група: 6.04.122.010.22.2
    Предмет: Захист інформації
    Дата народження: 24.05.2005
    """

    print("--- ЕТАП 3: ДЕМОНСТРАЦІЯ ---")
    tool.hide_message("input.png", "secret_image.png", my_data)

    extracted_text = tool.extract_message("secret_image.png")
    
    print("\n--- Результат вилучення ---")
    print(extracted_text.strip()) # strip прибере зайві пробіли
    
    print("\n--- ЕТАП 4: АНАЛІЗ ---")
    orig_size = os.path.getsize("input.png")
    new_size = os.path.getsize("secret_image.png")
    
    print(f"Розмір оригінала: {orig_size} байт")
    print(f"Розмір з секретом: {new_size} байт")
    
    # Порівняння рядків без пробілів по краях
    if extracted_text.strip() == my_data.strip():
        print("Вердикт: Цілісність даних збережена (UTF-8 працює коректно).")
    else:
        print("Вердикт: Дані пошкоджені.")