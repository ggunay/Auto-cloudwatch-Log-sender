#file to be zipped for the zip yml
import os
import boto3
import time
from datetime import datetime, timedelta

# Environment variables
query_string = os.getenv('QUERY_STRING')
days_interval = int(os.getenv('DAYS_INTERVAL', '7'))
email_address = os.getenv('EMAIL_ADDRESS')
log_group_names = os.getenv('LOG_GROUP_NAMES').split(',')
time_to_wait = int(os.getenv('TIME_TO_WAIT_FOR_QUERY_COMPLETION', '60'))

def lambda_handler(event, context):
    logs_client = boto3.client('logs')
    ses_client = boto3.client('ses')

    end_time = datetime.now()
    start_time = end_time - timedelta(days=days_interval)

    start_time_ms = int(start_time.timestamp() * 1000)
    end_time_ms = int(end_time.timestamp() * 1000)

    messages = []

    for log_group in log_group_names:
        response = logs_client.start_query(
            logGroupName=log_group,
            startTime=start_time_ms,
            endTime=end_time_ms,
            queryString=query_string,
        )
        query_id = response['queryId']

        # Poll for query completion
        time.sleep(time_to_wait)  # Wait for the specified time before checking the query status

        query_response = logs_client.get_query_results(
            queryId=query_id
        )

        for result in query_response['results']:
            for field in result:
                if field['field'] == '@message':
                    messages.append(field['value'])

    # Compile the email body from the collected messages
    email_body = "\\n".join(messages)

    # Send email via SES
    ses_client.send_email(
        Source=email_address,
        Destination={
            'ToAddresses': [
                email_address
            ]
        },
        Message={
            'Subject': {
                'Data': 'CloudWatch Logs Query Results',
            },
            'Body': {
                'Text': {
                    'Data': email_body,
                }
            }
        }
    )

    return {
        'statusCode': 200,
        'body': 'Email sent successfully!'
    }