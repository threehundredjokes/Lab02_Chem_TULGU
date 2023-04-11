from faker import Faker
import numpy.random as rd
import pandas as pd
import datetime
import os

# Для уникального набора данных нужно переопределять сид (0 - 4294967296)
SEED = 429496729
# Количество записей в каждой таблице (ибо мне лень делать разные счетчики) (min - 200)
DF_SIZE = 2000
# префикс выходных файлов (чтобы можно было несколько экземплятор генерировать)
PREFIX = 'gen1_'

faker = Faker("Ru_ru")
rd.seed(SEED)
Faker.seed(SEED)
# мне было лень реализовывать распределение, чтобы Начальник был не так часто, так что я просто сделал дубли должностей
JOD_LIST = ['Начальник лаборатории', 'Научный сотрудник', "Младший научный сотрудник", "Младший научный сотрудник",
            "Младший научный сотрудник", "Специалист-биохимик", "Специалист-биохимик",
            "Аналитик химической документации", "Старший лаборант", "Лаборант", "Лаборант", "Лаборант"]

clients_df = pd.DataFrame(columns=['Идентификатор', 'Фамилия', "Имя", "Отчество", "Дата рождения", "Должность"])
shop_df = pd.DataFrame(columns=['Идентификатор', 'Название', "Последняя поставка", "Адрес"])
chemicals_df = pd.DataFrame(columns=['Идентификатор', 'Название', "Формула", "Стоимость за грамм"])
avail_in_shop_df = pd.DataFrame(columns=['Ид. реактива', 'Ид. магазина', "В наличии (грамм)"])
managers_df = pd.DataFrame(columns=['Ид. руководителя', 'Ид. подчиненного'])
orders_df = pd.DataFrame(columns=['Идентификатор', 'Номер заказа', "Ид. реактива", "Ид. заказчика", "Вес в граммах",
                                  "Дата заказа", "Ид. магазина", "Стоимость партии"])


for i in range(DF_SIZE//20):
    ID = i
    NAME = faker.name().split()
    F_NAME, I_NAME, O_NAME = NAME[0], NAME[1], NAME[2]
    DATE_BIRTH = faker.date_between(start_date=datetime.date(1966, 1, 1), end_date=datetime.date(2001, 1, 1))
    JOB = JOD_LIST[rd.randint(0, 12)]
    data = {'Идентификатор':[ID], 'Фамилия':[F_NAME], "Имя":[I_NAME], "Отчество":[O_NAME], "Дата рождения":[DATE_BIRTH],
            "Должность":[JOB]}
    temp_client_df = pd.DataFrame(data=data)
    clients_df = pd.concat([clients_df, temp_client_df])


for i in range(DF_SIZE//200):
    ID = i
    SHOP_NAME = faker.company()
    LAST_INCOME_DT = faker.date_between(start_date=datetime.date(2020, 1, 1), end_date=datetime.date(2023, 1, 1))
    ADDRESS = faker.address()[:-8]
    data = {'Идентификатор':[ID], 'Название':[SHOP_NAME], "Последняя поставка":[LAST_INCOME_DT], "Адрес":[ADDRESS]}
    temp_shop_df = pd.DataFrame(data=data)
    shop_df = pd.concat([shop_df, temp_shop_df])


MANAGERS = clients_df[clients_df["Должность"] == "Начальник лаборатории"]
for i in range(len(clients_df)):
    if not clients_df[(clients_df["Идентификатор"] == i) & (clients_df["Должность"] != "Начальник лаборатории")].empty:
        ID_SLAVE = i
        ID_MASTER = MANAGERS["Идентификатор"].sample(n=1).tolist()[0]
        data = {'Ид. руководителя': [ID_MASTER], 'Ид. подчиненного': [ID_SLAVE]}
        temp_managers_df = pd.DataFrame(data=data)
        managers_df = pd.concat([managers_df, temp_managers_df])


for i in range(DF_SIZE):
    HOW_MANY_SHOPS_HAVE = rd.randint(0, 2)
    for sh in range(HOW_MANY_SHOPS_HAVE):
        ID = i
        ID_SHOP = rd.randint(0, len(shop_df)-1)
        QNT = rd.randint(0, 9999999) / 1000
        data = {'Ид. реактива':[ID], 'Ид. магазина':[ID_SHOP], 'В наличии (грамм)': [QNT]}
        temp_avail_in_shop_df = pd.DataFrame(data=data)
        avail_in_shop_df = pd.concat([avail_in_shop_df, temp_avail_in_shop_df])


chems_raw_df = pd.read_csv("data/chems.csv", delimiter =";", header=None,
                  names=["Название", "Формула"])
raw_size = len(chems_raw_df)
for i in range(DF_SIZE):
    ID = i
    new_chem = chems_raw_df.iloc[rd.randint(0, raw_size-1)]
    CHEM_FORMULA = new_chem["Формула"]
    CHEM_NAME = new_chem["Название"]
    COST = rd.randint(10, 99999)
    data = {'Идентификатор': [ID], 'Название': [CHEM_NAME], 'Формула': [CHEM_FORMULA], 'Стоимость за грамм': [COST]}
    temp_chemicals_df = pd.DataFrame(data=data)
    chemicals_df = pd.concat([chemicals_df, temp_chemicals_df])


ID = 0
CHEM_DF_SIZE = len(chemicals_df)
SHOP_DF_SIZE = len(shop_df)
CLIENTS_DF_SIZE = len(clients_df)
for i in range(DF_SIZE//2):
    ORDER_NUM = faker.bothify(text='??######??', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    CLIENT_ID = rd.randint(0, CLIENTS_DF_SIZE-1)
    ORDER_DT = faker.date_between(start_date=datetime.date(2011, 1, 1), end_date=datetime.date(2023, 1, 1))
    SHOP_ID = rd.randint(0, SHOP_DF_SIZE-1)
    NUM_OF_CHEMS_IN_ORDER = rd.randint(1, 4)
    for chem in range(NUM_OF_CHEMS_IN_ORDER):
        CHEM_ID = rd.randint(0, CHEM_DF_SIZE-1)
        MASS = rd.randint(1, 1000000) / 1000
        COST = MASS * chemicals_df.iloc[CHEM_ID]["Стоимость за грамм"]
        data = {'Идентификатор': [ID],'Номер заказа': [ORDER_NUM],'Ид. реактива': [CHEM_ID],'Ид. заказчика': [CLIENT_ID],
                'Вес в граммах': [MASS], 'Дата заказа': [ORDER_DT], "Ид. магазина": [SHOP_ID], 'Стоимость партии': [COST]}
        ID += 1
        temp_orders_df = pd.DataFrame(data=data)
        orders_df = pd.concat([orders_df, temp_orders_df])


filepath = 'data/'
fileformat = '.csv'

clients_df.to_csv(os.path.join(filepath + PREFIX + 'clients_df' + fileformat), index=False, sep=';')
shop_df.to_csv(os.path.join(filepath + PREFIX + 'shop_df' + fileformat), index=False, sep=';')
chemicals_df.to_csv(os.path.join(filepath + PREFIX + 'chemicals_df' + fileformat), index=False, sep=';')
avail_in_shop_df.to_csv(os.path.join(filepath + PREFIX + 'avail_in_shop_df' + fileformat), index=False, sep=';')
managers_df.to_csv(os.path.join(filepath + PREFIX + 'managers_df' + fileformat), index=False, sep=';')
orders_df.to_csv(os.path.join(filepath + PREFIX + 'orders_df' + fileformat), index=False, sep=';')
