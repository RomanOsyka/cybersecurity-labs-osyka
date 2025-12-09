
import hashlib
from ecdsa import SigningKey, SECP256k1, VerifyingKey, BadSignatureError

def get_file_hash_bytes(filename):
    with open(filename, "rb") as f:
        return hashlib.sha256(f.read()).digest()  # байтовий digest

def derive_private_key_bytes(name, birthdate, secret_word):
    raw = f"{name}{birthdate}{secret_word}".encode("utf-8")
    full = hashlib.sha256(raw).digest()  # 32 байти -> підходить для SECP256k1
    return full

def generate_keys(name, birthdate, secret_word):
    seed = derive_private_key_bytes(name, birthdate, secret_word)
    sk = SigningKey.from_string(seed, curve=SECP256k1, hashfunc=hashlib.sha256)
    vk = sk.get_verifying_key()
    # серіалізація у файли
    with open("private.key", "wb") as f:
        f.write(sk.to_string())
    with open("public.key", "wb") as f:
        f.write(vk.to_string())
    print("Keys saved: private.key (32 bytes), public.key (64 bytes)")
    return sk, vk

def sign_document(filename, sk: SigningKey):
    h = get_file_hash_bytes(filename)
    signature = sk.sign_digest(h)  # підписуємо дайджест
    sig_file = f"{filename}.sig"
    with open(sig_file, "wb") as f:
        f.write(signature)
    print(f"Signature saved to {sig_file} (len={len(signature)})")
    return signature

def verify_signature(filename, vk: VerifyingKey):
    sig_file = f"{filename}.sig"
    try:
        with open(sig_file, "rb") as f:
            signature = f.read()
    except FileNotFoundError:
        print("Signature file not found.")
        return False
    h = get_file_hash_bytes(filename)
    try:
        vk.verify_digest(signature, h)
        print(" -> РЕЗУЛЬТАТ: [Підпис ДІЙСНИЙ]")
        return True
    except BadSignatureError:
        print(" -> РЕЗУЛЬТАТ: [Підпис ПІДРОБЛЕНИЙ / Документ змінено]")
        return False

def main():
    name = "Roman"
    date = "24052005"
    secret = "music"
    doc = "resume_osyka.txt"

    # Создаємо тест-файл
    with open(doc, "w", encoding="utf-8") as f:
        f.write("Резюме: Досвід роботи 5 років. Навички: Python, Security.")

    sk, vk = generate_keys(name, date, secret)
    sign_document(doc, sk)

    # Перевірка (успішна)
    verify_signature(doc, vk)

    # Змінимо документ — має виявити підробку
    with open(doc, "w", encoding="utf-8") as f:
        f.write("Резюме: Досвід роботи 100 років. Я вмію все!")
    verify_signature(doc, vk)

if __name__ == "__main__":
    main()
