import json
import boto3
from datetime import datetime, timedelta

def lambda_handler(event, context):

    # Configure DynamoDB client
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('your_table_name')  # Replace with your table name

    # Get contact ID from event (assuming it's present)
    contact_id = event.get('ContactId')
    if not contact_id:
        print("Error: ContactId not found in event")
        return {
            'statusCode': 400,
            'body': 'Missing ContactId in event'
        }

    # Get preferred callback time from DynamoDB
    response = table.get_item(Key={'ContactId': contact_id})
    preferred_callback_time_str = response.get('Item', {}).get('preferred_callback_time')
    
    if not preferred_callback_time_str:
        print("Error: preferred_callback_time not found for contact")
        return {
            'statusCode': 400,
            'body': 'preferred_callback_time not found for contact'
        }

    # Parse preferred callback time string (adjust format as needed)
    try:
        preferred_callback_time = datetime.strptime(preferred_callback_time_str, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        print("Error: Invalid format for preferred_callback_time")
        return {
            'statusCode': 400,
            'body': 'Invalid format for preferred_callback_time'
        }

    # Get current time with 15 minute buffer (adjust as needed)
    current_time = datetime.utcnow() + timedelta(minutes=15)  # Add a buffer to account for processing time

    # Compare times
    if preferred_callback_time <= current_time:
        # Initiate outbound call using Amazon Connect Streams API
        # Replace the following with your specific configuration and logic
        connect_client = boto3.client('connectstreams')
        response = connect_client.start_outbound_voice_contact(
            ContactId=contact_id,
            QueueName='your_queue_name',  # Replace with your queue name
            InstanceId='your_instance_id',  # Replace with your instance ID
        )
        print(f"Outbound call initiated for contact: {contact_id}")
        return {
            'statusCode': 200,
            'body': 'Outbound call initiated successfully'
        }
    else:
        print(f"Preferred callback time ({preferred_callback_time}) has not arrived yet.")
        return {
            'statusCode': 200,
            'body': 'Preferred callback time has not arrived yet'
        }

# Replace placeholders with your actual values:
# * your_table_name: Name of your DynamoDB table
# * your_queue_name: Name of your Amazon Connect queue
# * your_instance_id: ID of your Amazon Connect instance
