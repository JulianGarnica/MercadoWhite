import random
from werkzeug.security import generate_password_hash, check_password_hash

def allowed_file(filename):
  ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

  return '.' in filename and \
    filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def encript_passw(password):
    password = generate_password_hash(password, method='sha256')
    return password


def cod_random(cant):
    array_letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123456789'
    string = ''
    for i in range(cant):
        string = string+random.choice(array_letters)
    return string


def json_convert(datos, indices):
    # main part
    column_list = []
    for i in indices:
        column_list.append(i[0])

    jsonData_list = []
    for row in datos:
        data_dict = {}
        for i in range(len(column_list)):
            data_dict[column_list[i]] = row[i]
        jsonData_list.append(data_dict)

    return jsonData_list