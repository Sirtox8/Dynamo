import boto3
from boto3.dynamodb.conditions import Key, Attr
from dotenv import load_dotenv
import os

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