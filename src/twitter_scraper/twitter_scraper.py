import csv
import time
import tweepy
import os

def get_docs_abs_path():
    docs_path = os.path.join(r'C:\Dev\bootcamp\twitter_api_exercise','docs')
    return docs_path

# Define batch size for processing
BATCH_SIZE = 100
RESULTS_CSV_FILE_NAME = 'results.csv'
EXCEL_RESULTS_FILE = os.path.join(get_docs_abs_path(),'excel_results.xlsx')
REQUEST_THROTTLE_IN_SECONDS = 0.2


CREDENTIALS_TXT = get_docs_abs_path() + r'\api_credentials.txt'
RESULTS_CSV_FILE_NAME = get_docs_abs_path() + r'\results.csv'

def get_credentials_as_dict():

    credendials_dict = {}
    with open(CREDENTIALS_TXT, 'r') as file:
        for line in file:
            key = line.split('=')[0].strip()
            value = line.split('=')[1].strip()
            credendials_dict[key] = value
    return credendials_dict


def get_ids_and_labels_as_lists():
    '''
    Reads the text file including the ids and their sentiment labels for processing.
    Returns two lists.
    '''
    ids = []
    sentiment_labels = []

    with open(os.path.join(get_docs_abs_path(),'BIDU.txt'), 'r') as file:

        for line in file:

            # Split line in to 2 fields
            split_records = line.split('\t')
            print(split_records)
            # Add to result lists
            ids.append(split_records[0].strip())
            sentiment_labels.append(split_records[1].strip())

    return ids, sentiment_labels


def get_batch_to_process() -> list:
    # Read data to lists for processing
    ids, sentiment_labels = get_ids_and_labels_as_lists()

    while len(ids) >= BATCH_SIZE and len(sentiment_labels) >= BATCH_SIZE:

        id_processing_batch, ids = ids[0:BATCH_SIZE], ids[BATCH_SIZE:]

        sentiment_labels_processing_batch, sentiment_labels = \
                sentiment_labels[0:BATCH_SIZE], sentiment_labels[BATCH_SIZE:]

        yield id_processing_batch, sentiment_labels_processing_batch

    return ids, sentiment_labels


# Read credentials from api_credentials_file
credentials = get_credentials_as_dict()

# Create tweepy authorization as object
auth = tweepy.OAuthHandler(
    credentials['CONSUMER_KEY'], credentials['CONSUMER_SECRET'])
auth.set_access_token(
    credentials['ACCESS_TOKEN'], credentials['ACCESS_TOKEN_SECRET'])
TWEEPY_API_INSTANCE = tweepy.API(auth)




def main():

    import pandas as pd

    df = pd.DataFrame(columns=['ID','Text','SentimentLabel'])

    with open(RESULTS_CSV_FILE_NAME, 'w', newline='\n') as csvfile:
        results_writer = csv.writer(csvfile, delimiter='\t',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)

        for id_proc_batch, sent_proc_batch in get_batch_to_process():


            try:
                # Recover the full text
                results = TWEEPY_API_INSTANCE.statuses_lookup(id_proc_batch)
                
                for index, tweet in enumerate(results):


                    tweet_id = str(tweet.id)

                    try:
                        tweet_text = str(tweet.text)
                    except:
                        tweet_text = "No text attribute on this tweet"

                    tweet_sentiment_label = str(sent_proc_batch[index])

                    # Write the results to a csv, using the tracked index to find the related sentiment label
                    results_writer.writerow([tweet_id, tweet_text, tweet_sentiment_label])

                    df = df.append({'ID':tweet_id, 'Text': tweet_text, 'SentimentLabel': tweet_sentiment_label}, ignore_index=True)

            except Exception as e:



                print("Unable to retrieve -> \n"+str(e))
                print(tweet_id)
                print(dir(tweet))
                print("...............")
                continue

            # Wait to avoid making too many requests too rapidly
            time.sleep(REQUEST_THROTTLE_IN_SECONDS)
    df.to_excel(r'C:\Dev\bootcamp\twitter_api_exercise\docs\excel_pandas_out.xlsx')

if __name__ == "__main__":
    main()  