import boto3
from botocore.exceptions import ClientError

# Set up your SQS queue URL and boto3 client
url = "https://sqs.us-east-1.amazonaws.com/440848399208/nem2p"
sqs = boto3.client('sqs')

def delete_message(handle):
    try:
        # Delete message from SQS queue
        sqs.delete_message(
            QueueUrl=url,
            ReceiptHandle=handle
        )
        print("Message deleted")
    except ClientError as e:
        print(e.response['Error']['Message'])

def get_message():
    m_dict = {} # Message Dictionary
    try:
        while True: # Should run until no messages are received
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
            # If there is no message in the queue, print a message and exit    
            else:
                message = ""
                for i in sorted(m_dict.keys()):
                    message += m_dict[i] + " "
                print(message)
                exit(1) # stop this from looping
            
    # Handle any errors that may occur connecting to SQS
    except ClientError as e:
        print(e.response['Error']['Message'])


# Trigger the function
if __name__ == "__main__":
    get_message()
