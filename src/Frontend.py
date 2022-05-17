import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, query
from ORM_Database import BranchOffice, Customer, Employee, EmployeeLogInfo, Purchase, Service, ServicesList
from Data_listing import all_services, all_offices, get_service_price, is_new_customer, add_new_customer, \
    get_customer_id, get_random_employee_code, get_branch_office_id, add_new_purchase
import hydralit_components as hc

engine = create_engine('postgresql+psycopg2://postgres:1278@localhost/postgres')
Session = sessionmaker(bind=engine)
session = Session()


@st.experimental_singleton
class Total:
    def __init__(self):
        self.services_list = []
        self.services_amount = []
        self.services_price = []

# Делаем синглтон с флагом на отключение логинга в условие после срабатывание флага на авторизациюк

@st.experimental_singleton
class Login:
    def __init__(self):
        # self.full_name = col_login_1.text_input("Full name")
        # self.phone_number = col_login_2.text_input("Phone number")
        # self.e_mail = col_login_3.text_input("Email")
        self.is_login = False

st.set_page_config(
    page_title="PhotoLibra",
    page_icon=":camera:",
    layout="wide",
)


st.markdown("<h1 style='text-align: center;"
            "color: #03fc98;"
            "margin-bottom: 1rem'>Салон фотоуслуг PhotoLibra</h1", unsafe_allow_html=True)

container = st.container()
col_login_0, col_login_1, col_login_2, col_login_3, col_login_4 = container.columns((2, 3, 3, 3, 2))

full_name = col_login_1.text_input("Full name")
phone_number = col_login_2.text_input("Phone number")
e_mail = col_login_3.text_input("Email")


if col_login_2.button("Авторизироваться!"):
    if not is_new_customer(full_name, phone_number, e_mail):
        add_new_customer(full_name, phone_number, e_mail)
        container.info(f"Добро пожаловать, {full_name}!")
    else:
        container.info(f"Рады вас снова видеть, {full_name}!")
    Login().is_login = True

if Login().is_login:
    customer_id = get_customer_id(full_name, phone_number, e_mail)

    container.markdown("---")





    _, col_l, _, col_r, col_del, _ = container.columns((2, 6, 3, 6, 1, 2))
    branch_office = col_l.selectbox("Выбор филлиала:", all_offices)
    col_l.markdown("---")
    service = col_l.selectbox("Выбор услуги:", all_services)
    service_amount = col_l.number_input("Количество выбранной услуги:", min_value=1, max_value=1000, value=1)
    service_price = get_service_price(service) * service_amount
    col_l.write(f"**Стоимость выбранной услуги:** {service_price}")
    add_to_total = col_l.button("Добавить в корзину")

    col_r.subheader("**Выбранные услуги:**")
    col_del.markdown("&nbsp;")

    if add_to_total:
        added_warning = False
        for item in Total().services_list:
            if item == service:
                container.warning("Услуга уже добавлена! Если хотите изменить количество выбранной услуги,"
                           " то необходимо сначала её удалить.")
                added_warning = True
                break
        if not added_warning:
            Total().services_list.append(service)
            print(Total().services_list)
            Total().services_amount.append(service_amount)
            print(Total().services_amount)
            Total().services_price.append(service_price)
            print(Total().services_price)
    purchase_amount = 0


    for service, service_amount, service_price in zip(Total().services_list, Total().services_amount,
                                                      Total().services_price):
        purchase_amount += service_price
        col_r.markdown("""
        <style>
        .e16nr0p33 {
        line-height: 3.2;
        font-weight: bold;
        }
      </style>"""
                       f""" {Total().services_list.index(service) + 1}. "{service}", {service_amount}шт, всего {service_price}""",
                       unsafe_allow_html=True)

        if col_del.button('DELETE', key=str(service)):
            Total().services_list.remove(service)
            Total().services_amount.remove(service_amount)
            Total().services_price.remove(service_price)
            st.experimental_rerun()

    container.markdown("---")
    col_last_1, col_last_2, col_last_3 = container.columns((3.5, 1, 3.5))
    total_sum = col_last_2.markdown(f"#### Итог: {purchase_amount}")
    accept_purchase = col_last_2.button("Оформить заказ!")

    branch_office_id = get_branch_office_id(branch_office)
    employee_code = get_random_employee_code(branch_office_id)


    if accept_purchase and branch_office:  # and other
        try:
            add_new_purchase(customer_id, employee_code, branch_office_id, purchase_amount)
            st.success(f"Заказ оформлен! Спасибо что выбрали нас, {full_name}!")
        except Exception as e:
            st.error(f"Ошибка офорлмения заказа! Подробнее: {e}")
