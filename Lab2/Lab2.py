ua_alphabet = ['а', 'б', 'в', 'г', 'ґ', 
               'д', 'е', 'є', 'ж', 'з', 
               'и', 'і', 'ї', 'й', 'к', 
               'л', 'м', 'н', 'о', 'п', 
               'р', 'с', 'т', 'у', 'ф', 
               'х', 'ц', 'ч', 'ш', 'щ', 
               'ь', 'ю', 'я']

def caesar_cipher(message, key, is_encryption):
    try:
        key = int(key)
        result = ""

        for letter in message:
            if letter.lower() in ua_alphabet:
                letter_index = ua_alphabet.index(letter.lower())
                if is_encryption:
                    shifted_letter_index = (letter_index + key) % len(ua_alphabet)
                else:
                    shifted_letter_index = (letter_index - key) % len(ua_alphabet)
                shifted_letter = ua_alphabet[shifted_letter_index]
                result += shifted_letter
            else:
                result += letter
        return result
    
    except ValueError as e:
        print("Caesar key must be a number")
        key = input("Key: ")
        return caesar_cipher(message, key, is_encryption)


def vigenere_cipher(message, key, is_encryption):

    try:
        is_key_correct = False
        for key_letter in key:
            if key_letter.lower() in ua_alphabet:
                is_key_correct = True
                break
        
        if is_key_correct == False:
            raise ValueError("Vigenere key must contain ua alphabet letters")

        result = ""

        key_start = -1
        key_len = len(key)
        for letter in message:
            if letter.lower() in ua_alphabet:
                letter_index = ua_alphabet.index(letter.lower())

                while True:
                    key_start += 1
                    if key_start == key_len:
                        key_start = 0
                    if key[key_start].lower() in ua_alphabet:
                        key_letter_index = ua_alphabet.index(key[key_start].lower())

                        if is_encryption:
                            shifted_letter_index = (letter_index + key_letter_index) % len(ua_alphabet)
                        else:
                            shifted_letter_index = (letter_index - key_letter_index) % len(ua_alphabet)
                        result += ua_alphabet[shifted_letter_index]
                        break
            else:
                result += letter
        return result

    except ValueError as e:
        print(e)
        key = input("Key: ")
        return vigenere_cipher(message, key, is_encryption)
            

def enter_data():
    message = input("\nMessage: ")
    key = input("Key: ")
    return message, key

def print_table():
    print(f"\n{"Параметр":<25} | {"Шифр Цезаря":<30} | {"Щифр Віженера":<30}")
    print(f"{"Довжина результату":<25} | {"Не змінюється":<30} | {"Не змінюється":<30}")
    print(f"{"Читабельність":<25} | {"Результат виглядає однорідно":<30} | {"Результат виглядає більш випадковим":<30}")
    print(f"{"Складність ключа":<25} | {"Дуже низька":<30} | {"Вища":<30}")

def compare():
    message = input("\nMessage: ")

    caesar_key = input("Caesar key: ")
    vigenere_key = input("Vigenere key: ")

    print("Caesar cipher result: ", caesar_cipher(message, caesar_key, True))
    print("Vigenere cipher result: ", vigenere_cipher(message, vigenere_key, True))

while True:
    print("\n1 - encrypt with Caesar \n"
    "2 - decrypt with Caesar \n"
    "3 - encrypt with Vigenere \n"
    "4 - decrypt with Vigenere \n"
    "5 - compare ciphers")
    option = input("Choice: ")

    match option:
        case "1":
            print("Результат:", caesar_cipher(*enter_data(), True))
        case "2":
            print("Результат:", caesar_cipher(*enter_data(), False))
        case "3":
            print("Результат:", vigenere_cipher(*enter_data(), True))
        case "4":
            print("Результат:", vigenere_cipher(*enter_data(), False))
        case "5":
            compare()
            print_table()
        case _:
            print("Unknown option")

# https://itnauka.org/services/caesar_decrypt.html