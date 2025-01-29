import boto3
from boto3.dynamodb.conditions import Key, Attr
from dotenv import load_dotenv
import os
import time
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

# Load environment variables from a .env file
load_dotenv()
# Retrieve the environment variables
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
aws_session_token = os.getenv('AWS_SESSION_TOKEN')
region_name = os.getenv('AWS_REGION')

# Initialize a session using Amazon DynamoDB
session = boto3.Session(
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    aws_session_token=aws_session_token,
    region_name=region_name
)

dynamodb = session.resource('dynamodb')
print("CONEXION EXITOSA")



# Conectamos con DynamoDB
dynamodb = boto3.resource("dynamodb")

# Crear tablas
def create_tables():
    tables = [("Usuarios", "UserID"), ("Productos", "ProductoID"), ("Pedidos", "PedidoID")]
    for table_name, pk in tables:
        try:
            table = dynamodb.create_table(
                TableName=table_name,
                KeySchema=[{"AttributeName": pk, "KeyType": "HASH"}],
                AttributeDefinitions=[{"AttributeName": pk, "AttributeType": "S"}],
                ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5}
            )
            table.wait_until_exists()
            print(f"Tabla {table_name} creada correctamente.")
        except Exception as e:
            print(f"Error creando tabla {table_name}: {e}")

# Insertar datos
def insert_data():
    data = {
        "Usuarios": {"UserID": "U1", "Nombre": "Alice"},
        "Productos": {"ProductoID": "P1", "Nombre": "Laptop"},
        "Pedidos": {"PedidoID": "O1", "Cliente": "Alice"}
    }
    for table_name, item in data.items():
        try:
            table = dynamodb.Table(table_name)
            table.put_item(Item=item)
            print(f"Datos insertados en {table_name}.")
        except Exception as e:
            print(f"Error insertando datos en {table_name}: {e}")

# Obtener registros
def get_records():
    tables = ["Usuarios", "Productos", "Pedidos"]
    for table_name in tables:
        try:
            table = dynamodb.Table(table_name)
            response = table.get_item(Key={f"{table_name[:-1]}ID": f"{table_name[0]}1"})
            print(f"Registro en {table_name}: {response.get('Item')}")
        except Exception as e:
            print(f"Error obteniendo datos de {table_name}: {e}")

# Actualizar registros
def update_records():
    try:
        table = dynamodb.Table("Usuarios")
        table.update_item(
            Key={"UserID": "U1"},
            UpdateExpression="SET Nombre = :new",
            ExpressionAttributeValues={":new": "Alice Updated"}
        )
        print("Usuario actualizado.")
    except Exception as e:
        print(f"Error actualizando usuario: {e}")

# Eliminar registros
def delete_records():
    try:
        dynamodb.Table("Usuarios").delete_item(Key={"UserID": "U1"})
        dynamodb.Table("Productos").delete_item(Key={"ProductoID": "P1"})
        dynamodb.Table("Pedidos").delete_item(Key={"PedidoID": "O1"})
        print("Registros eliminados.")
    except Exception as e:
        print(f"Error eliminando registros: {e}")

# Obtener todos los registros
def get_all_records():
    for table_name in ["Usuarios", "Productos", "Pedidos"]:
        try:
            table = dynamodb.Table(table_name)
            response = table.scan()
            print(f"Todos los registros en {table_name}: {response.get('Items')}")
        except Exception as e:
            print(f"Error obteniendo todos los registros de {table_name}: {e}")

# Filtrar registros
def filter_records():
    try:
        table = dynamodb.Table("Usuarios")
        response = table.scan(FilterExpression="Nombre = :name", ExpressionAttributeValues={":name": "Alice Updated"})
        print(f"Filtrado en Usuarios: {response['Items']}")
    except Exception as e:
        print(f"Error filtrando registros: {e}")

# Eliminación condicional
def conditional_delete():
    try:
        table = dynamodb.Table("Usuarios")
        table.delete_item(Key={"UserID": "U1"}, ConditionExpression="attribute_exists(UserID)")
        print("Usuario eliminado condicionalmente.")
    except Exception as e:
        print(f"Error eliminando usuario condicionalmente: {e}")

# Filtrar con múltiples condiciones
def multi_filter():
    try:
        table = dynamodb.Table("Productos")
        response = table.scan(FilterExpression="Nombre = :n", ExpressionAttributeValues={":n": "Laptop"})
        print(f"Filtrado múltiple en Productos: {response['Items']}")
    except Exception as e:
        print(f"Error filtrando múltiples condiciones: {e}")

# Consulta PartiQL
def partiql_query():
    try:
        client = boto3.client("dynamodb")
        query = "SELECT * FROM Usuarios WHERE UserID = 'U1'"
        response = client.execute_statement(Statement=query)
        print(f"Resultado de consulta PartiQL: {response['Items']}")
    except Exception as e:
        print(f"Error ejecutando consulta PartiQL: {e}")

# Crear backup
def create_backup():
    try:
        client = boto3.client("dynamodb")
        for table_name in ["Usuarios", "Productos", "Pedidos"]:
            response = client.create_backup(
                TableName=table_name,
                BackupName=f"Backup-{table_name}"
            )
            print(f"Backup creado para {table_name}: {response['BackupDetails']['BackupArn']}")
    except Exception as e:
        print(f"Error creando backup: {e}")

# Menú principal
def main():
    while True:
        print("\nSeleccione una operación:")
        print("1. Crear tablas")
        print("2. Insertar registros")
        print("3. Obtener un registro")
        print("4. Actualizar un registro")
        print("5. Eliminar registros")
        print("6. Obtener todos los registros")
        print("7. Filtrar registros")
        print("8. Eliminación condicional")
        print("9. Filtrado múltiple")
        print("10. Consulta PartiQL")
        print("11. Crear backup")
        print("12. Salir")
        
        opcion = input("Ingrese una opción: ")

        if opcion == "1":
            create_tables()
        elif opcion == "2":
            insert_data()
        elif opcion == "3":
            get_records()
        elif opcion == "4":
            update_records()
        elif opcion == "5":
            delete_records()
        elif opcion == "6":
            get_all_records()
        elif opcion == "7":
            filter_records()
        elif opcion == "8":
            conditional_delete()
        elif opcion == "9":
            multi_filter()
        elif opcion == "10":
            partiql_query()
        elif opcion == "11":
            create_backup()
        elif opcion == "12":
            break
        else:
            print("Opción no válida. Inténtelo de nuevo.")

if __name__ == "__main__":
    main()