from sqlalchemy import create_engine, MetaData, Table, Integer, String, Numeric, Column, DateTime, ForeignKey
# from sqlalchemy.dialects.postgresql import psycopg2
import psycopg2
from sqlalchemy.sql import select, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session, sessionmaker, query
from datetime import datetime
from sqlalchemy.sql import func

# session = Session(bind=engine)
Base = declarative_base()
# Session = sessionmaker(bind=engine)
# session = Session()


class BranchOffice(Base):
    __tablename__ = 'branch_office'
    branch_office_id = Column(Integer(), primary_key=True)
    address = Column(String(200), nullable=False)
    full_name_of_owner = Column(String(80), nullable=False)
    branch_office_phone_number = Column(String(18), nullable=False)
    employee = relationship('Employee')
    purchase = relationship('Purchase')


class Customer(Base):
    __tablename__ = 'customer'
    customer_id = Column(Integer(), primary_key=True)
    full_name = Column(String(80), nullable=False)
    phone_number = Column(String(18), nullable=False)
    e_mail = Column(String(80), nullable=False)
    purchase = relationship('Purchase')


class Employee(Base):
    __tablename__ = 'employee'
    employee_code = Column(String(4), primary_key=True)
    full_name = Column(String(80), nullable=False)
    phone_number = Column(String(18), nullable=False)
    e_mail = Column(String(80), nullable=False)
    branch_office_id = Column(Integer(), ForeignKey("branch_office.branch_office_id"), nullable=False)
    # branch_office = relationship("BranchOffice")
    purchase = relationship('Purchase')
    service = relationship('Service')
    # services_list = relationship('ServicesList')


class EmployeeLogInfo(Base):
    __tablename__ = 'employee_log_info'
    log_id = Column(Integer(), primary_key=True)
    employee_code = Column(String(4), nullable=False)
    changed_date = Column(DateTime(), nullable=False)
    operation_type = Column(String(20), nullable=False)


class Purchase(Base):
    __tablename__ = 'purchase'
    purchase_number = Column(Integer(), primary_key=True)
    purchase_date = Column(DateTime(), nullable=False, server_default=func.now()) #возможна проблема с датой и временем
    customer_id = Column(Integer(), ForeignKey("customer.customer_id"), nullable=False)
    # customer = relationship('Customer')
    employee_code = Column(String(4), ForeignKey("employee.employee_code"), nullable=False)
    # employee = relationship('Employee')
    branch_office_id = Column(Integer(), ForeignKey("branch_office.branch_office_id"), nullable=False)
    # branch_office = relationship('BranchOffice')
    purchase_amount = Column(Integer(), nullable=True, default=0)
    services_list = relationship('ServicesList')


class Service(Base):
    __tablename__ = 'service'
    service_code = Column(String(4), primary_key=True)
    service_name = Column(String(80), nullable=False)
    service_price = Column(Integer(), nullable=False)
    employee_code = Column(String(4), ForeignKey("employee.employee_code"), nullable=False)
    services_list = relationship('ServicesList')  ###
    # employee = relationship('Employee')


class ServicesList(Base):
    __tablename__ = 'services_list'
    services_list_number = Column(Integer(), primary_key=True)
    services_amount = Column(Integer(), nullable=False)
    service_code = Column(String(4), ForeignKey("service.service_code"), nullable=False)
    # service = relationship('Employee')
    purchase_number = Column(Integer(), ForeignKey("purchase.purchase_number"), nullable=False)
    # purchase = relationship('Purchase')


if __name__ == '__main__':
    engine = create_engine('postgresql+psycopg2://postgres:1278@localhost/postgres')
    Base.metadata.create_all(engine)

# print(engine)




