from confluent_kafka import Producer
import json
import time
import logging
import pandas as pd


#Configure logger
logging.basicConfig(format='%(asctime)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='producer.log',
                    filemode='w')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

#Create Kafka Producer
p=Producer({'bootstrap.servers':'localhost:9092'})

#Callback function
def receipt(err,msg):
    if err is not None:
        print('Failed to deliver message: {}'.format(err))
    else:
        message = 'Produced message on topic {} with value of {}\n'.format(msg.topic(), msg.value().decode('utf-8'))
        logger.info(message)
        print(message)

#Write Producer loop that acts like user activity
def main():
    df = pd.read_csv('export_data.csv',error_bad_lines=False)
    df = df.to_json(orient = 'split')
    for i in range(5):
        m=json.dumps(df)
        p.produce('indian-exports-store', m.encode('utf-8'),callback=receipt)
        p.poll(1) # Polls/checks the producer for events and calls the corresponding callback functions.
        p.flush() #Wait for all messages in the Producer queue to be delivered. Should be called prior to shutting down the producer to ensure all outstanding/queued/in-flight messages are delivered.
        time.sleep(3)

if __name__ == '__main__':
    main()