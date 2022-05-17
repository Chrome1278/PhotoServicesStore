from sqlalchemy import create_engine, MetaData, Table, Integer, String, Column, DateTime, ForeignKey
# from sqlalchemy.dialects.postgresql import psycopg2
import psycopg2

metadata = MetaData()
engine = create_engine('postgresql+psycopg2://postgres:1278@localhost/postgres')

# table_name = Table('table_name', metadata,
#                    Column('id', Integer(), primary_key=True)
#                    )


branch_office = Table('branch_office', metadata,
                      Column('branch_office_id', Integer(), primary_key=True),
                      Column('address', String(200), nullable=False),
                      Column('full_name_of_owner', String(80), nullable=False),
                      Column('branch_office_phone_number', String(18), nullable=False)
                   )

customer = Table('customer', metadata,
                      Column('customer_id', Integer(), primary_key=True),
                      Column('full_name', String(80), nullable=False),
                      Column('phone_number', String(18), nullable=False),
                      Column('e_mail', String(80), nullable=False)
                   )

employee = Table('employee', metadata,
                      Column('employee_code', String(4), primary_key=True),
                      Column('full_name', String(80), nullable=False),
                      Column('phone_number', String(18), nullable=False),
                      Column('e_mail', String(80), nullable=False),
                      Column('branch_office_id', Integer(), ForeignKey("branch_office.branch_office_id"), nullable=False)
                   )

employee_log_info = Table('employee_log_info', metadata,
                      Column('log_id', Integer(), primary_key=True),
                      Column('employee_code', String(4), nullable=False),
                      Column('changed_date', DateTime(), nullable=False),
                      Column('operation_type', String(20), nullable=False)
                   )

purchase = Table('purchase', metadata,
                      Column('purchase_number', Integer(), primary_key=True),
                      Column('purchase_date', DateTime(), nullable=False),
                      Column('customer_id', Integer(), ForeignKey("customer.customer_id"), nullable=False),
                      Column('employee_code', String(4), ForeignKey("employee.employee_code"), nullable=False),
                      Column('branch_office_id', Integer(), ForeignKey("branch_office.branch_office_id"), nullable=False),
                      Column('purchase_amount', Integer(), nullable=True)
                   )

service = Table('service', metadata,
                      Column('service_code', String(4), primary_key=True),
                      Column('service_name', String(80), nullable=False),
                      Column('service_price', Integer(), nullable=False),
                      Column('employee_code', String(4), ForeignKey("employee.employee_code"), nullable=False)
                   )

services_list = Table('services_list', metadata,
                      Column('services_list_number', Integer(), primary_key=True),
                      Column('services_amount', Integer(), nullable=False),
                      Column('service_code', String(4), ForeignKey("service.service_code"), nullable=False),
                      Column('purchase_number', Integer(), ForeignKey("purchase.purchase_number"), nullable=False)
                   )

metadata.create_all(engine)


print(engine)

#conn = engine.connect()
#r = conn.execute() # insert


# s = customers.select() # input_table_name.select()
# print(s)


# Read
# result_set = conn.execute("SELECT * FROM customer")
# for r in result_set:
#     print(r)


# Update
#conn.execute("UPDATE films SET title='Some2016Film' WHERE year='2016'")


# Delete
#conn.execute("DELETE FROM films WHERE year='2016'")

# 	добавление записей в таблицы; Insert
# 	удаление записей из таблиц; Delete
# 	вывод всех записей выбранной таблицы; Select
# 	поиск записей по некоторому условию. Выберите, поиск по числу (<>=), или по фразе через Like %
# 	дополнительные операции, зависящие от вашей предметной области (обсуждается с преподавателем). Вывод суммы






