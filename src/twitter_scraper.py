import csv
import time
import tweepy

# Define batch size for processing
BATCH_SIZE = 20
RESULTS_CSV_FILE_NAME = 'results.csv'
REQUEST_THROTTLE_IN_SECONDS = 1


def get_credentials_as_dict():

    credendials_dict = {}
    with open('docs\\api_credentials', 'r') as file:
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

    with open('docs\\BIDU.txt', 'r') as file:

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
    with open(RESULTS_CSV_FILE_NAME, 'w', newline='') as csvfile:
        results_writer = csv.writer(csvfile, delimiter=' ',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)

        for id_proc_batch, sent_proc_batch in get_batch_to_process():

            # Iterate through the id_processing_batch keeping track of the index
            for index, tweep_id in enumerate(id_proc_batch):
                # True refers to recovering the full text or limited no. of chars
                text = TWEEPY_API_INSTANCE.get_direct_message([tweep_id, True])
                # Write the results to a csv, using the tracked index to find the related sentiment label
                results_writer.writerow(
                    [tweep_id, text, sent_proc_batch[index]])

                # Wait to avoid making too many requests too rapidly
                time.sleep(REQUEST_THROTTLE_IN_SECONDS)
