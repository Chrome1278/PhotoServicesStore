import random

from sqlalchemy import create_engine
from src.ORM_Database import BranchOffice, Customer, Employee, EmployeeLogInfo, Purchase, Service, ServicesList
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker, query
from sqlalchemy.sql import select, text, insert

engine = create_engine('postgresql+psycopg2://postgres:1278@localhost/postgres')
Session = sessionmaker(bind=engine)
session = Session()

q = session.execute(text("select service_name from service")).all()
all_services = [item for sublist in q for item in sublist]

q = session.execute(text("select address from branch_office")).all()
all_offices = [item for sublist in q for item in sublist]


def is_new_customer(full_name, phone_number, e_mail):
    input_customer = session.execute((text(f"select * from customer where "
                                           f"full_name = '{full_name}' and phone_number = '{phone_number}' and e_mail = '{e_mail}'"
                                           # f"{full_name=} and {phone_number=} and {e_mail=}"
                                           ))).fetchone()
    return input_customer


def add_new_customer(full_name, phone_number, e_mail):
    q = session.execute((text("select max(customer_id) from customer"))).fetchone()
    last_customer_id = q[0] + 1
    q = session.execute(text(f"insert into customer(customer_id, full_name, phone_number, e_mail) "
                             f"values('{last_customer_id}','{full_name}', '{phone_number}', '{e_mail}')"))
    session.commit()


def get_service_price(service):
    service_price = session.execute(
        text(f"select service_price from service where service_name = '{service}'")
    ).fetchone()
    return service_price[0]


def get_customer_id(full_name, phone_number, e_mail):
    customer_id = session.execute((text(f"select customer_id from customer where "
                                        f"{full_name=} and {phone_number=} and {e_mail=}"
                                        ))).fetchone()
    return customer_id[0]


def get_branch_office_id(branch_office):
    branch_office_id = session.execute(
        text(f"select branch_office_id from branch_office where address = '{branch_office}'")
    ).fetchone()[0]
    return branch_office_id


def get_random_employee_code(branch_office_id):
    employee_code = session.execute(
        text(f"select employee_code from employee where branch_office_id = '{branch_office_id}'")
    ).all()
    #all_offices = [item for sublist in q for item in sublist]
    return random.choice(employee_code)[0]


def add_new_purchase(customer_id, employee_code, branch_office_id, purchase_amount):
    purchase_number = session.execute((text("select max(purchase_number) from purchase"))).fetchone()[0] + 1

    # сначала создать строку Покупки, после нажатия на кнопку авторизаци и выбора филиала, а потом появляется всю остальное
    # каждый объект корзины добавляется в таблицу services_list, и удаляется оттуда при удалении. И по триггерам общая сумма наполняется


    entry = Purchase(
        purchase_number=purchase_number,
        ##purchase_date,
        customer_id=customer_id,
        employee_code=employee_code,
        branch_office_id=branch_office_id,
        purchase_amount=purchase_amount,
    )
    session.add(entry)
    session.commit()
    
