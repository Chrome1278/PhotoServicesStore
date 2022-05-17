#import Database
#import ORM_Database
from sqlalchemy import create_engine
from ORM_Database import BranchOffice, Customer, Employee, EmployeeLogInfo, Purchase, Service, ServicesList
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker, query
from sqlalchemy.sql import select, text, insert


# engine = create_engine('postgresql+psycopg2://postgres:1278@localhost/postgres')
# # session = Session(bind=engine)
#
# Session = sessionmaker(bind=engine)
# session = Session()

def get_action_number():
    print('- Доступные типы действий:',
          '0 - Выйти из интерфейса',
          '1 - Сменить активную таблицу',
          '- - - - - - - - - - -',
          '2 - Добавить запись',
          '3 - Удалить запись',
          '4 - Вывести записи',
          '5 - Поиск записей по условию',
          sep='\n')
    action_number = int(input('--- Выберите номер действия:'))
    return action_number


def get_table_name():
    input_table_name = ''
    print('- Выберите таблицу:',
          'branch_office',
          'customer',
          'employee',
          'employee_log_info',
          'purchase',
          'service',
          'service_list', sep='\n')
    input_table_name = input('--- Выберите таблицу:')
    return input_table_name


def output_info(engine):
    table_name = get_table_name()
    while True:
        try:
            Session = sessionmaker(bind=engine)
            session = Session()
            action_number = get_action_number()

            if action_number == 0:
                print("Выход из интерфейса...")
                break

            if action_number == 1:
                table_name = get_table_name()
                action_number = get_action_number()

            if action_number != 0:
                print(f'Cтолбцы выбранной таблицы {table_name}:')
                print(*session.execute(select(text(f"* from {table_name}"))).keys())

            if action_number == 2:
                print(f"В соответствие с названиями столбцов таблицы {table_name} введите добавляемые данные:")
                input_insert = str(input())
                q = session.execute(text(f"insert into {table_name} values({input_insert})"))
                session.commit()

            if action_number == 3:
                # print(f"В соответствие с названиями столбцов таблицы {input_table_name} введите удаляемые данные:")
                print(
                    f"Введите условие удаления значений из таблицы {table_name} (в форматах на примере first_name = 'Alex' или id > 5):")
                input_delete = str(input())
                q = session.execute(text(f"delete from {table_name} where {input_delete}"))
                session.commit()

            if action_number == 4:
                q = session.execute(select(text(f"* from {table_name}"))).all()
                for c in q:
                    print(c)

            if action_number == 5:
                print(
                    f"Введите условия фильтрации данных по таблице {table_name} (в форматах на примере first_name = 'Alex' или id > 5):")
                where_input = input()
                q = session.execute(text(f"select * from {table_name} where {where_input}")).all()
                for c in q:
                    print(c)
        except:
            print("\nОШИБКА! Невалидный вид данных! Попробуйте еще раз...\n")
            table_name = get_table_name()







