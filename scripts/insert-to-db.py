import sys
import os
import psycopg2
import psycopg2.extras
import pandas as pd


USEFUL_COLUMNS = [
    'DepCode',
    'DepLib',
    'ComLib',
    'InsNom',
    'InsNumeroInstall',
    'EquipementId',
    'EquNom',
    'EquipementTypeCode',
    'EquipementTypeLib',
    'EquipementFamille',
    'EquipementCateg'
]

TABLE_COLUMNS = (
    "DEPARTMENT_CODE",
    "DEPARTMENT_NAME",
    "CITY_NAME",
    "LOCATION_NAME",
    "LOCATION_ID",
    "EQUIPMENT_ID",
    "EQUIPMENT_NAME",
    "EQUIPMENT_TYPE_ID",
    "EQUIPMENT_TYPE_NAME",
    "EQUIPMENT_FAMILY",
    "EQUIPMENT_CATEGORY",
    "GPS_LOCATION"
)

def usage():
    print('lol')

def connect_to_db():
    return psycopg2.connect(
        user='saucisse',
        password='saucisse',
        host='127.0.0.1',
        port='5432',
        database='esp'
    )

def create_table(cursor):
    create_table_query = """
        DROP TABLE IF EXISTS test;
        CREATE TABLE IF NOT EXISTS test (
            ID                  SERIAL              PRIMARY KEY,
            DEPARTMENT_CODE     CHAR(2)             NOT NULL,
            DEPARTMENT_NAME     VARCHAR(64)         NOT NULL,
            CITY_NAME           VARCHAR(64)         NOT NULL,
            LOCATION_NAME       VARCHAR(128)        NOT NULL,
            LOCATION_ID         VARCHAR(64)         NOT NULL,
            EQUIPMENT_ID        VARCHAR(64)         NOT NULL,
            EQUIPMENT_NAME      VARCHAR(128)        NOT NULL,
            EQUIPMENT_TYPE_ID   SMALLINT            NOT NULL,
            EQUIPMENT_TYPE_NAME VARCHAR(128)        NOT NULL,
            EQUIPMENT_FAMILY    VARCHAR(128)        NOT NULL,
            EQUIPMENT_CATEGORY  VARCHAR(128)        NOT NULL,
            GPS_LOCATION        GEOGRAPHY(POINT)    NOT NULL
        );
    """
    cursor.execute(create_table_query)

def get_data_frame_from_file(file_path):
    return pd.read_excel(file_path)

def row_to_tuple(row):
    value_list = [row[col] for col in USEFUL_COLUMNS]
    value_list.append(f"POINT({row['EquGPSX']}, {row['EquGPSY']}")
    return tuple(value_list)

def insert_df_into_db(cursor, df):
    query = "INSERT INTO test " + str(TABLE_COLUMNS) + "VALUES %s"
    values = [row_to_tuple(row) for _, row in df.iterrows()]
    psycopg2.extras.execute_values(cursor, query, values)

def main(file_path):
    connection = None
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        create_table(cursor)
        df = get_data_frame_from_file(file_path)
        insert_df_into_db(cursor, df)
        connection.commit()
    except (Exception, psycopg2.Error) as err:
        print(err)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print('connection closed')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
        exit(1)
    file_path = sys.argv[1]
    if file_path and file_path.endswith('.xlsx') and os.path.exists(file_path):
        main(file_path)
    else:
        usage()
        exit(1)
