import pandas as pd
from sqlalchemy import create_engine, text
import logging
from config import DATABASE_CONFIG, CSV_FILES, LOG_FILE

# Configuración de logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def create_db_engine(config):
    """
    Crea y prueba la conexión a MySQL.
    """
    try:
        engine = create_engine(
            f"mysql+mysqlconnector://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}",
            echo=False
        )

        # Probar conexión real
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))

        logging.info("Conexión a la base de datos establecida correctamente.")
        print("Conexión a MySQL exitosa.")
        return engine

    except Exception as e:
        logging.error(f"Error al conectar a la base de datos: {e}")
        print(f"Error al conectar a la base de datos: {e}")
        raise


def read_csv(file_path):
    """
    Lee un CSV y devuelve un DataFrame.
    """
    try:
        df = pd.read_csv(file_path)
        logging.info(f"Archivo leído exitosamente: {file_path}")
        print(f"Archivo leído: {file_path}")
        return df

    except Exception as e:
        logging.error(f"Error al leer el archivo {file_path}: {e}")
        print(f"Error al leer el archivo {file_path}: {e}")
        raise


def transform_departments(df):
    """
    Transformaciones para departments.
    """
    if 'department_name' not in df.columns:
        raise ValueError("La columna 'department_name' no existe en departments.")

    if df['department_name'].duplicated().any():
        logging.warning("Hay departamentos duplicados en departments.")
        print("Advertencia: hay departamentos duplicados en departments.")

    return df


def transform_categories(df, departments_df):
    """
    Transformaciones para categories.
    """
    required_cols = ['category_id', 'category_department_id', 'category_name']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"La columna '{col}' no existe en categories.")

    if 'department_id' not in departments_df.columns:
        raise ValueError("La columna 'department_id' no existe en departments.")

    valid_ids = set(departments_df['department_id'])
    invalid_rows = df[~df['category_department_id'].isin(valid_ids)]

    if not invalid_rows.empty:
        raise ValueError(
            f"Hay category_department_id que no existen en departments. "
            f"Ejemplos: {invalid_rows['category_department_id'].drop_duplicates().tolist()[:10]}"
        )

    return df


def transform_customers(df):
    """
    Transformaciones para customers.
    """
    required_cols = [
        'customer_id', 'customer_fname', 'customer_lname', 'customer_email',
        'customer_password', 'customer_street', 'customer_city',
        'customer_state', 'customer_zipcode'
    ]

    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"La columna '{col}' no existe en customers.")

    df['customer_email'] = df['customer_email'].astype(str).str.lower().str.strip()

    if df[['customer_fname', 'customer_lname', 'customer_email']].isnull().any().any():
        raise ValueError("Hay datos faltantes en customer_fname, customer_lname o customer_email.")

    return df


def transform_products(df, categories_df):
    required_cols = [
        'product_id', 'product_category_id', 'product_name',
        'product_description', 'product_price', 'product_image'
    ]
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"La columna '{col}' no existe en products.")

    if 'category_id' not in categories_df.columns:
        raise ValueError("La columna 'category_id' no existe en categories.")

    valid_ids = set(categories_df['category_id'])
    invalid_rows = df[~df['product_category_id'].isin(valid_ids)]

    if not invalid_rows.empty:
        raise ValueError(
            f"Hay product_category_id que no existen en categories. "
            f"Ejemplos: {invalid_rows['product_category_id'].drop_duplicates().tolist()[:10]}"
        )

    # Rellenar nulos en product_description
    df['product_description'] = df['product_description'].fillna('Sin descripción')

    return df
    


def transform_orders(df, customers_df):
    """
    Transformaciones para orders.
    """
    required_cols = ['order_id', 'order_date', 'order_customer_id', 'order_status']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"La columna '{col}' no existe en orders.")

    df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')

    if df['order_date'].isnull().any():
        invalid_count = df['order_date'].isnull().sum()
        raise ValueError(f"Hay {invalid_count} valores inválidos en order_date.")

    if 'customer_id' not in customers_df.columns:
        raise ValueError("La columna 'customer_id' no existe en customers.")

    valid_ids = set(customers_df['customer_id'])
    invalid_rows = df[~df['order_customer_id'].isin(valid_ids)]

    if not invalid_rows.empty:
        raise ValueError(
            f"Hay order_customer_id que no existen en customers. "
            f"Ejemplos: {invalid_rows['order_customer_id'].drop_duplicates().tolist()[:10]}"
        )

    return df


def transform_order_items(df, orders_df, products_df):
    """
    Transformaciones para order_items.
    """
    required_cols = [
        'order_item_id', 'order_item_order_id', 'order_item_product_id',
        'order_item_quantity', 'order_item_subtotal', 'order_item_product_price'
    ]
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"La columna '{col}' no existe en order_items.")

    if 'order_id' not in orders_df.columns:
        raise ValueError("La columna 'order_id' no existe en orders.")

    if 'product_id' not in products_df.columns:
        raise ValueError("La columna 'product_id' no existe en products.")

    valid_order_ids = set(orders_df['order_id'])
    invalid_orders = df[~df['order_item_order_id'].isin(valid_order_ids)]
    if not invalid_orders.empty:
        raise ValueError(
            f"Hay order_item_order_id que no existen en orders. "
            f"Ejemplos: {invalid_orders['order_item_order_id'].drop_duplicates().tolist()[:10]}"
        )

    valid_product_ids = set(products_df['product_id'])
    invalid_products = df[~df['order_item_product_id'].isin(valid_product_ids)]
    if not invalid_products.empty:
        raise ValueError(
            f"Hay order_item_product_id que no existen en products. "
            f"Ejemplos: {invalid_products['order_item_product_id'].drop_duplicates().tolist()[:10]}"
        )

    calculated_subtotal = df['order_item_quantity'] * df['order_item_product_price']
    if not (df['order_item_subtotal'] == calculated_subtotal).all():
        logging.info("Recalculando order_item_subtotal.")
        print("Recalculando order_item_subtotal.")
        df['order_item_subtotal'] = calculated_subtotal

    return df


def truncate_tables(engine):
    """
    Limpia las tablas antes de volver a cargar.
    """
    try:
        with engine.begin() as conn:
            conn.execute(text("SET FOREIGN_KEY_CHECKS=0"))
            conn.execute(text("TRUNCATE TABLE order_items"))
            conn.execute(text("TRUNCATE TABLE orders"))
            conn.execute(text("TRUNCATE TABLE products"))
            conn.execute(text("TRUNCATE TABLE customers"))
            conn.execute(text("TRUNCATE TABLE categories"))
            conn.execute(text("TRUNCATE TABLE departments"))
            conn.execute(text("SET FOREIGN_KEY_CHECKS=1"))

        logging.info("Tablas truncadas correctamente.")
        print("Tablas limpiadas correctamente.")

    except Exception as e:
        logging.error(f"Error al truncar tablas: {e}")
        print(f"Error al truncar tablas: {e}")
        raise


def load_data(engine, table_name, df):
    """
    Carga un DataFrame a MySQL.
    """
    try:
        df.to_sql(name=table_name, con=engine, if_exists='append', index=False)
        logging.info(f"Datos cargados exitosamente en la tabla {table_name}.")
        print(f"Carga exitosa: {table_name} ({len(df)} filas)")

    except Exception as e:
        logging.error(f"Error al cargar datos en la tabla {table_name}: {e}")
        print(f"Error al cargar datos en la tabla {table_name}: {e}")
        raise


def main():
    try:
        print("Iniciando pipeline...")

        engine = create_db_engine(DATABASE_CONFIG)

        # Leer y transformar
        departments_df = transform_departments(read_csv(CSV_FILES['departments']))
        categories_df = transform_categories(read_csv(CSV_FILES['categories']), departments_df)
        customers_df = transform_customers(read_csv(CSV_FILES['customers']))
        products_df = transform_products(read_csv(CSV_FILES['products']), categories_df)
        orders_df = transform_orders(read_csv(CSV_FILES['orders']), customers_df)
        order_items_df = transform_order_items(
            read_csv(CSV_FILES['order_items']),
            orders_df,
            products_df
        )

        # Limpiar tablas antes de cargar
        truncate_tables(engine)

        # Cargar en orden correcto
        load_data(engine, 'departments', departments_df)
        load_data(engine, 'categories', categories_df)
        load_data(engine, 'customers', customers_df)
        load_data(engine, 'products', products_df)
        load_data(engine, 'orders', orders_df)
        load_data(engine, 'order_items', order_items_df)

        logging.info("Pipeline ejecutado exitosamente.")
        print("Pipeline ejecutado exitosamente.")

    except Exception as e:
        logging.error(f"Fallo general del pipeline: {e}")
        print(f"Fallo general del pipeline: {e}")
        raise


if __name__ == "__main__":
    main()