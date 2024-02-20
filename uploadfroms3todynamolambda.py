import json
import boto3

s3_client = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("Customer")

def lambda_handler(event, context):
    # Extracting information from the S3 event
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_name = event['Records'][0]['s3']['object']['key']

    # Reading data from the S3 object
    response = s3_client.get_object(Bucket=bucket_name, Key=file_name)
    data = response['Body'].read().decode("utf-8")

    # Splitting data into lines and excluding the header
    customers = data.split("\n")[1:]

    for customer in customers:
        # Splitting each line into individual data points
        customer_data = customer.split(",")

        # Adding data to DynamoDB
        try:
            table.put_item(
                Item={
                    "Day": customer_data[0],
                    "Customers": customer_data[1],
                    "Gross": customer_data[2],
                    "Expenses": customer_data[3]
                }
            )
        except Exception as e:
            print(f"Error adding item to DynamoDB: {e}")

    print("Processing completed.")
