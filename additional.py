import re


def check_input_data(input_data, check_param: str, param_2=None):
    if check_param == 'last_name':
        if input_data.isalpha() == False:
            print('Не корректно!')
            enter_data(check_param)
        else:
            return input_data.capitalize()
    elif check_param == 'first_name':
        if not input_data.isalpha():
            print('Не корректно!')
            enter_data(check_param)
        else:
            return input_data.capitalize()
    elif check_param == 'email':
        pattern = r'[\w\.-]+@[\w\.-]+(?:\.[\w]+)+'
        result = re.findall(pattern, input_data)
        if len(result) != 0:
            return input_data.lower()
        else:
            print('Не корректно!')
            enter_data(check_param)
    elif check_param == 'phone_number' and param_2 is None:
        if input_data.isnumeric():
            return input_data
        elif input_data == '':
            return
        else:
            print('Введен не корректный номер!')
            enter_data(check_param)
    elif check_param == 'phone_number' and param_2 is not None:
        if input_data.isnumeric():
            return input_data
        elif input_data == '':
            return
        else:
            print('Введен не корректный номер!')
            enter_data(check_param, param_2=1)


def enter_data(param,
               param_2=None):
    if param == 'last_name':
        last_name = input('Введите фамилию клиента: ')
        result = check_input_data(last_name, 'last_name')
        return str(result)
    elif param == 'first_name':
        name = input('Введите имя клиента: ')
        result = check_input_data(name, 'first_name')
        return result
    elif param == 'email':
        email = input('Введите email клиента: ')
        result = check_input_data(email, 'email')
        return result
    elif param == 'phone_number' and param_2 is None:
        phone_number = input('Введите номер телефона клиента (Нажмите ENTER, если номер отсутствует): ')
        result = check_input_data(phone_number, 'phone_number', param_2)
        if result != '':
            return result
        else:
            return
    elif param == 'phone_number' and param_2 != None:
        phone_number = input('Введите номер телефона клиента: ')
        result = check_input_data(phone_number, 'phone_number', param_2)
        return result
    else:
        return
