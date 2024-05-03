import boto3
from botocore.exceptions import ClientError
import requests
import json

# Set up your SQS queue URL and boto3 client
url = "https://sqs.us-east-1.amazonaws.com/440848399208/ryb8jt"
sqs = boto3.client('sqs')

def get_message():
    m_dict = {} # Message Dictionary
    receipts = [] # Receipt List
    try:
        while len(m_dict.items()) <= 11: # <= 10 was not return the correct list size
            response = sqs.receive_message(
                QueueUrl=url,
                AttributeNames=[
                    'All'
                ],
                MaxNumberOfMessages=1,
                MessageAttributeNames=[
                    'All'
                ]
            )
            if "Messages" in response:
                for m in response['Messages']:
                    order = m['MessageAttributes']['order']['StringValue']
                    word = m['MessageAttributes']['word']['StringValue']
                    handle = m['ReceiptHandle']
                    m_dict[order] = word
                    receipts.append(handle)
            else: # Runs once there are no messages left in the queue
                message = ""
                for i in sorted(m_dict.keys()): # Sort dictionary by order
                    message += m_dict[i] + " "
                print(message) # Prints the message
                try:
                    for handle in receipts:
                        # Delete message from SQS queue
                        sqs.delete_message(
                            QueueUrl=url,
                            ReceiptHandle=handle
                        )
                except ClientError as e: # error handling
                    print(e.response['Error']['Message'])
                exit(1)

    # Handle any errors that may occur connecting to SQS
    except ClientError as e:
        print(e.response['Error']['Message'])


# Trigger the function
if __name__ == "__main__":
    get_message()
