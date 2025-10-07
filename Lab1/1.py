import re
bd_format = r"^(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[0-2])\.(19[0-9]{2}|20[0-2][0-5])$"
numbers = r"[0-9]"
symbols = r"[!@#$%^&*]"
lowercase = r"[a-z]"
uppercase = r"[A-Z]"


def check_bd_format(birth_date):
    return bool(re.match(bd_format, birth_date))

def input_bd():
    while True:
        birth_date = input("Birthday: ")
        if check_bd_format(birth_date):
            return birth_date
        print("Wrong bd format. Try again")

def split_bd(birth_date):
    return re.split(r"\.", birth_date)



def is_name_in_pw(name, password):
    return name in password

def is_ddmm_in_pw(ddmm, password):
    if ddmm[0] in password:
        return ddmm[1] in password
    return False

def is_yyyy_in_pw(yyyy, password):
    return yyyy in password



def check_pw_length(password, pw_rating, pw_advices):
    pw_length = len(password)
    if 6 <= pw_length and pw_length <= 10:
        pw_rating += 2
        pw_advices += "Password can be longer \n"
    elif pw_length > 10:
        pw_rating += 3
    else:
        pw_advices += "Password is too short \n"
    
    return pw_rating, pw_advices

def check_num_amount(password, pw_rating, pw_advices):
    num_amount = len(re.findall(numbers, password))
    if 2 <= num_amount and num_amount <= 4:
        pw_rating += 1
        pw_advices += "Password can contain more numbers \n"
    elif num_amount > 4:
        pw_rating += 2
    else:
        pw_advices += "Password contains too few numbers \n"

    return pw_rating, pw_advices

def check_symb_amount(password, pw_rating, pw_advices):
    symb_amount = len(re.findall(symbols, password))
    if 1 == symb_amount:
        pw_rating += 2
        pw_advices += "Password can contain more symbols \n"
    elif symb_amount > 1: 
        pw_rating += 3
    else:
        pw_advices += "Password contains too few symbols \n"

    return pw_rating, pw_advices

def check_letters_case(password, pw_rating, pw_advices):
    lowercase_amount = len(re.findall(lowercase, password))
    uppercase_amount = len(re.findall(uppercase, password))
    case_difference = abs(lowercase_amount - uppercase_amount)
    if 0 <= case_difference and case_difference <= 2:
        pw_rating += 2
    elif 3 <= case_difference <= 5:
        pw_rating += 1
        pw_advices += "Difference between the number of uppercase and lowercase letters can be smaller \n"
    else:
        pw_advices += "Difference between the number of uppercase and lowercase letters is too big \n"

    return pw_rating, pw_advices



def check_password(name, bd_items, password):
    try:
        if is_name_in_pw(name, password):
            raise ValueError("Password contains your name. Remove it")

        if is_ddmm_in_pw([bd_items[0], bd_items[1]], password):
            raise ValueError("Password contains your day and month of birth. Remove it")
        
        if is_yyyy_in_pw(bd_items[2], password):
            raise ValueError("Password contains your year of birth. Remove it")

        pw_rating = 0
        pw_advices = ""
        pw_rating, pw_advices = check_pw_length(password, pw_rating, pw_advices)
        pw_rating, pw_advices = check_num_amount(password, pw_rating, pw_advices)
        pw_rating, pw_advices = check_symb_amount(password, pw_rating, pw_advices)
        pw_rating, pw_advices = check_letters_case(password, pw_rating, pw_advices)

        print(f"Password rating is {pw_rating}")
        if pw_advices == "":
            print("Password is OK")
        else:
            print(f"Advices for password improving: \n{pw_advices}")
    except ValueError as e:
        print(e)

def check_new_user():
    name = input("Name: ")
    birth_date = input_bd()
    bd_items = split_bd(birth_date)
    password = input("Password: ")

    check_password(name, bd_items, password)

    return [name, bd_items]

def rewrite_password(old_user_data):
    password = input("Password: ")
    if password == "new":
        return True
    
    check_password(old_user_data[0], old_user_data[1], password)



while True:
    old_user_data = check_new_user()
    while True:
        if rewrite_password(old_user_data):
            break
