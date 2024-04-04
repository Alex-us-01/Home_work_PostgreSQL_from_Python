import psycopg2
from Classes.client import Client
from additional import enter_data


class DataBase:
    def __init__(self, name, user, password):
        self.name = name
        self.user = user
        self.password = password
        self.connect = psycopg2.connect(database=self.name, user=self.user, password=self.password)

    def create_db_structure(self):

        with self.connect.cursor() as cursor:
            cursor.execute("""CREATE TABLE IF NOT EXISTS client (
                    id SERIAL PRIMARY KEY,
                    last_name VARCHAR(60) NOT NULL,
                    first_name VARCHAR(60) NOT NULL,
                    email VARCHAR(60) UNIQUE NOT NULL

                );
                """)

            cursor.execute("""CREATE TABLE IF NOT EXISTS client_phone (
                    id SERIAL PRIMARY KEY,
                    number BIGINT UNIQUE,
                    client INTEGER REFERENCES client(id)
                );
                """)

            self.connect.commit()

    def get_client_phone(self, client_id):
        with self.connect.cursor() as cursor:
            cursor.execute(f"""SELECT number FROM client_phone WHERE client =%s;
                                                                                              """, (client_id,))
            result_2 = (cursor.fetchall())
            # print(result_2)
            if result_2 is None:
                print('Клиента с таким номером не нашлось!')
            else:

                list_result = []

                for el in result_2:
                    for el_2 in el:
                        list_result.append(el_2)

                return list_result

    def delete_tables(self):
        with self.connect.cursor() as cursor:
            cursor.execute("""
                DROP TABLE client_phone, client ;
                """)
            self.connect.commit()

    def add_new_client(self, last_name, first_name, email, phone=None):
        if self.check_unique_value(table='client', column='email', value=email) is None:

            if phone is not None:
                if self.check_unique_value(table='client_phone', column='number', value=phone) is None:
                    with self.connect.cursor() as cursor:
                        cursor.execute(f"""
                              INSERT INTO client(last_name, first_name, email )
                              VALUES('{last_name}', '{first_name}','{email}' )
                              RETURNING id;
                              """)
                        id_ = (cursor.fetchone())[0]
                        cursor.execute(f"""INSERT INTO client_phone(number, client)
                                                            VALUES('{int(phone)}', '{id_}' );
                                                                            """)
                        self.connect.commit()
                        print(f'\n'
                              f'КЛИЕНТ ДОБАВЛЕН\n'
                              f'')
                else:
                    print(f'\n'
                          f'Клиент с указанным номером телефона уже существует\n'
                          f'')
            else:
                with self.connect.cursor() as cursor:
                    cursor.execute(f"""
                          INSERT INTO client(last_name, first_name, email )
                          VALUES('{last_name}', '{first_name}','{email}' )
                          RETURNING id;
                          """)
                    self.connect.commit()
                    print(f'\n'
                          f'КЛИЕНТ ДОБАВЛЕН\n'
                          f'')
        else:
            print(f'\n'
                  f'Клиент с указанным email уже существует\n'
                  f'')

    def edit_data(self, table, column, value, criterion, value_2):
        print(f'Edit_data - {value_2}')
        with self.connect.cursor() as cursor:
            cursor.execute(f"""UPDATE {table}
                            SET {column} = '{value}'
                            WHERE {criterion} = '{value_2}';
                            """)
            self.connect.commit()
            print(f'\n'
                  f'ДАННЫЕ ИЗМЕНЕНЫ\n'
                  f'')

    def check_unique_value(self, table, column, value):
        with self.connect.cursor() as cursor:
            cursor.execute(f"""
                SELECT {column} FROM {table} WHERE {column}=%s;
            """, (value,))
            return cursor.fetchone()

    def add_phone_number(self, id_, value):
        with self.connect.cursor() as cursor:
            cursor.execute(f"""INSERT INTO client_phone(number, client)
                            VALUES('{value}', '{id_}' );
                            """)
            self.connect.commit()
            print(f'\n'
                  f'НОМЕР ДОБАВЛЕН!\n'
                  f'')

    def delete_data(self, table, column, value):
        with self.connect.cursor() as cursor:
            if table != 'client':
                cursor.execute(f"""DELETE FROM {table} WHERE {column} = {value};
                                               """)
                print(f'\n'
                      f'НОМЕР УДАЛЕН\n'
                      f'')
                self.connect.commit()
            else:
                cursor.execute(f"""DELETE FROM {table} WHERE {column} = {value};
                                                               """)
                print(f'\n'
                      f'КЛИЕНТ УДАЛЕН\n'
                      f'')
                self.connect.commit()

    def choose_client(self, list_client, number):

        client = (list_client[number])
        print(
            f'{client[0]}   -   {client[1][0]} - {client[1][1]} - {client[1][2]} - {client[1][3]} - {client[2]}\n')
        return client[1][0]

    def get_list_clients(self, column=None, value=None):
        if column is None and value is None:
            with self.connect.cursor() as cursor:
                cursor.execute(f"""SELECT * FROM client;                
                                            """)
                result = list(cursor.fetchall())
                # print(result)
                return_list = []
                for element in enumerate(result):
                    print(
                        f'{element[0]}   -   {element[1][0]} -  {element[1][1]}  -  {element[1][2]}  -  {element[1][3]}  -  {self.get_client_phone(element[1][0])}')
                    list_2 = list(element)
                    list_2.append(self.get_client_phone(element[1][0]))
                    return_list.append(list_2)
                return return_list

        elif column is not None and column != 'number':
            with self.connect.cursor() as cursor:
                cursor.execute(f"""SELECT * FROM client 
                                WHERE {column} = %s;
                                """, (value,))
                result = list(cursor.fetchall())
                return_list = []
                for element in enumerate(result):
                    print(
                        f'{element[0]}   -   {element[1][0]} -  {element[1][1]}  -  {element[1][2]}  -  {element[1][3]}  -   {self.get_client_phone(element[1][0])}')
                    list_2 = list(element)
                    list_2.append(self.get_client_phone(element[1][0]))
                    return_list.append(list_2)
                return return_list

        elif column != None and column == 'number':
            # print('Вход в Column != None and column == phone')
            with self.connect.cursor() as cursor:
                cursor.execute(f"""SELECT * FROM client_phone 
                                WHERE number = %s;
                                """, (value,))
                # print('Сформироан запрос. Ответ получен')
                result = (cursor.fetchone())
                if result is None:
                    print('Клиента с таким номером не нашлось!')

                else:
                    result_1 = list(result)

                    return_list = []
                    client_id = result_1[-1]
                    cursor.execute(f"""SELECT * FROM client
                                                    WHERE id = %s;
                                                    """, (client_id,))
                    result = list(cursor.fetchall())
                    # print(result)
                    for element in enumerate(result):
                        print(
                            f'{element[0]}   -   {element[1][0]} -  {element[1][1]}  -  {element[1][2]}  -  {element[1][3]}  -  {self.get_client_phone(element[1][0])}')
                        list_2 = list(element)
                        list_2.append(self.get_client_phone(element[1][0]))
                        return_list.append(list_2)
                    return return_list[0][1][0]

    def search_client(self):
        param = int(input('Выберите вид поиска клиента:\n'
                          '\n'
                          '1 - Из списка\n'
                          '2 - По параметру\n'
                          ''))
        # Поиск по списку
        if param == 1:
            clients_list = self.get_list_clients()
            # print(clients_list)
            if len(clients_list) > 0:
                client = int(input('Введите порядковый номер клиента: \n'
                                   ''))
                if 0 <= client <= len(clients_list):
                    return self.choose_client(clients_list, client)
                else:
                    print('Клиента с указанным порядковым номером нет в списке!')
            else:
                print(f'\n'
                      f'СПИСОК КЛИЕНТОВ ПУСТ!\n'
                      f'')

        # Поиск по параметру
        elif param == 2:
            operation = int(input(f'Выберете вид поиска: \n'
                                  f'\n'
                                  f'1 - Поиск по фамилии\n'
                                  f'2 - Поиск по имени\n'
                                  f'3 - Поиск по Email\n'
                                  f'4 - Поиск по номеру телефона\n'
                                  '\n'
                                  f''))

            if operation == 1:
                client = Client(last_name=enter_data('last_name'))
                clients_list = self.get_list_clients(column='last_name', value=client.last_name)
                if len(clients_list) > 0:
                    client = int(input('Введите порядковый номер клиента: \n'
                                       ''))
                    if 0 <= client <= len(clients_list):
                        return self.choose_client(clients_list, client)
                    else:
                        print('Клиента с указанным порядковым номером нет в списке!')
                else:
                    print(f'КЛИЕНТ НЕ НАЙДЕН!')
                    return

            elif operation == 2:
                client = Client(first_name=enter_data('first_name'))
                clients_list = self.get_list_clients(column='first_name', value=client.first_name)
                if len(clients_list) > 0:
                    client = int(input('Введите порядковый номер клиента: \n'
                                       ''))
                    if 0 <= client <= len(clients_list):
                        return self.choose_client(clients_list, client)
                    else:
                        print('Клиента с указанным порядковым номером нет в списке!')
                else:
                    print(f'КЛИЕНТ НЕ НАЙДЕН!')
                    return
            elif operation == 3:
                client = Client(email=enter_data('email'))
                clients_list = self.get_list_clients(column='email', value=client.email)
                if len(clients_list) == 1:
                    return clients_list[0][1][0]
                else:
                    print('\n'
                          'Клиент с указанным Email не найден!\n'
                          '')
                    return

            elif operation == 4:
                client = Client(phone_number=enter_data('phone_number', param_2=1))
                clients_list = self.get_list_clients(column='number', value=client.phone_number)
                if clients_list is None:
                    return None
                else:
                    return clients_list
