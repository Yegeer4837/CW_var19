import random
import requests
import string

# Генерация паролей
def generate_password(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))

# Генерация студентов
def generate_student_data():
    surnames = [
    'Ivanov', 'Petrov', 'Sidorov', 'Alexeev', 'Pavlov', 'Nikolaev', 'Vasilyev', 'Smirnov', 'Mikhailov',
    'Fedorov', 'Orlov', 'Kuznetsov', 'Popov', 'Zakharov', 'Morozov', 'Romanov', 'Voronov', 'Lebedev',
    'Grigoryev', 'Kovalev', 'Volkov', 'Baranov', 'Dyakov', 'Filippov', 'Klimov', 'Schmidt', 'Kravtsov',
    'Kiselev', 'Demidov', 'Solovyev', 'Slobodchikov', 'Yakovlev', 'Sheremetev', 'Trofimov', 'Golubev',
    'Zhuravlev', 'Matveev', 'Belyakov', 'Korolev', 'Cherepanov', 'Bashirov', 'Chudinov', 'Popov', 'Frolov',
    'Fedoseev', 'Golovin', 'Zharkov', 'Kulikov', 'Peshkov', 'Rudnev'
    ]

    groups = [
    'Group1', 'Group2', 'Group3', 'Group4', 'Group5', 'Group6', 'Group7', 'Group8', 'Group9', 'Group10',
    'Group11', 'Group12', 'Group13', 'Group14', 'Group15', 'Group16', 'Group17', 'Group18', 'Group19',
    'Group20', 'Group21', 'Group22', 'Group23', 'Group24', 'Group25', 'Group26', 'Group27', 'Group28',
    'Group29', 'Group30', 'Group31', 'Group32', 'Group33', 'Group34', 'Group35', 'Group36', 'Group37',
    'Group38', 'Group39', 'Group40', 'Group41', 'Group42', 'Group43', 'Group44', 'Group45', 'Group46',
    'Group47', 'Group48', 'Group49', 'Group50'
    ]
    
    surname = random.choice(surnames)
    group = random.choice(groups)
    list_number = random.randint(1, 100)
    password = generate_password()
    
    return {
        'surname': surname,
        'group': group,
        'list_number': list_number,
        'password': password
    }

# куда отправлять запрос
url = "http://127.0.0.1:8000/students/add"

# Кол-во сгенерированных студентов(можно менять)
num_students = 50

for _ in range(num_students):
    student_data = generate_student_data()
    response = requests.post(url, data=student_data)
    print("Ok")
    

