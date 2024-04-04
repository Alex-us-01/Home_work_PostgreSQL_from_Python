from Classes.client import Client
from Classes.database import DataBase
from additional import enter_data


def start():
    client_base = DataBase(name='*', user='*', password='*')

    """Для соединения с БД ввести данные * :

    name - Ввести название существующей базы данных
    user - пользователь Postgres
    password - пароль пользователя Postgres"""

    operation = int(input(f'Выберете вид операции с базой данных: \n'
                          f'\n'
                          f'1 - Добавление нового клиента в базу данных\n'
                          f'2 - Добавить телефон для существующего клиента\n'
                          f'3 - Изменить данные для существующего клиента\n'
                          f'4 - Удалить номер телефона существующего клиента\n'
                          f'5 - Удалить существующего клиента из базы данных\n'
                          f'6 - Поиск клиента\n'
                          f''))

    if operation == 1:
        client = Client(last_name=enter_data('last_name'),
                        first_name=enter_data('first_name'),
                        email=enter_data('email'),
                        phone_number=enter_data('phone_number'))

        print(f'{client.last_name}, {client.first_name}, {client.email}, {client.phone_number}')
        client_base.add_new_client(client.last_name, client.first_name, client.email, client.phone_number)
        start()

    elif operation == 2:
        user = client_base.search_client()
        if user is not None:
            client = Client(phone_number=enter_data('phone_number', param_2=1))
            if client_base.check_unique_value('client_phone', 'number', client.phone_number) is None:
                client_base.add_phone_number(user, client.phone_number)
                start()
        else:
            start()

    elif operation == 3:
        user = client_base.search_client()
        if user is None:
            start()
        else:

            edit_param = int(input('Выберите данные для редактирования\n'
                                   '\n'
                                   '1 - Фамилия\n'
                                   '2 - Имя\n'
                                   '3 - Email\n'
                                   '4 - Номер телефона\n'
                                   ''))
            client_3 = Client()
            if edit_param == 1:
                client_3.last_name = enter_data('last_name')
                client_base.edit_data('client', 'last_name', client_3.last_name, 'id', user)
                start()

            elif edit_param == 2:
                client_3.first_name = enter_data('first_name')
                print(client_3.first_name)
                client_base.edit_data('client', 'first_name', client_3.first_name, 'id', user)
                start()
            elif edit_param == 3:
                client_3.email = enter_data('email')
                answer = client_base.check_unique_value('client', 'email', client_3.email)
                if answer is None:
                    client_base.edit_data('client', 'email', client_3.email, 'id', user)
                    start()
                else:
                    print(f'\n'
                          f'КЛИЕНТ С УКАЗАННЫМ EMAIL УЖЕ СУЩЕСТВУЕТ\n'
                          f'')
                    start()
            elif edit_param == 4:
                # client_3.phone_number = enter_data('phone_number', param_2=1)
                list_number = client_base.get_client_phone(user)
                if list_number is None:
                    start()
                else:

                    # print(f' else - {list_number}')

                    if len(list_number) > 0:

                        text = (f'Выберите номер телефона для редактирования\n'
                                '\n')
                        count = 0
                        while count < len(list_number):
                            text += f'{count + 1}  -  {list_number[count]}\n'
                            count += 1
                        print(text)

                        number = int(input(f'Введите порядковый номер телефона для редактирования: '))
                        if 1 <= number <= len(list_number):
                            # print(list_number)
                            client_3.phone_number = enter_data('phone_number', param_2=1)
                            answer = client_base.check_unique_value('client_phone', 'number', client_3.phone_number)
                            if answer is None:
                                client_base.edit_data('client_phone', 'number', int(client_3.phone_number), 'number',
                                                      list_number[number - 1])
                                # client_base.delete_phone_number('client_phone', 'number', list_number[number - 1])
                                start()
                            else:
                                print(f'\n'
                                      f'КЛИЕНТ С УКАЗАННЫМ НОМЕРОМ УЖЕ СУЩЕСТВУЕТ!\n'
                                      f'')
                                start()
                        else:
                            print(f'\n'
                                  f'Такого порядкового номера нет в списке!\n'
                                  f'')
                            start()


    elif operation == 4:
        user = client_base.search_client()
        list_number = client_base.get_client_phone(user)
        if len(list_number) > 1:

            text = (f'Выберите номер телефона для удаления\n'
                    '\n')
            count = 0
            while count < len(list_number):
                text += f'{count + 1}  -  {list_number[count]}\n'
                count += 1
            print(text)

            number = int(input(f'Введите порядковый номер телефона для удаления: '))
            if 1 <= number <= len(list_number):
                client_base.delete_data('client_phone', 'number', list_number[number - 1])
                start()
            else:
                print(f'\n'
                      f'Такого порядкового номера нет в списке!\n'
                      f'')
                start()

        elif len(list_number) == 1:
            client_base.delete_data('client_phone', 'client', user)
            start()

        else:
            print(f'\n'
                  f'У выбранного клиента нет номера телефона!\n'
                  f' ')
            start()



    elif operation == 5:
        user = client_base.search_client()
        if user is not None:
            client_base.delete_data('client_phone', 'client', user)
            client_base.delete_data('client', 'id', user)
            start()
        else:
            start()



    elif operation == 6:
        user = client_base.search_client()


    else:
        return


if __name__ == '__main__':
    start()
