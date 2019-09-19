Simple app which reads the tweet ids in a text file and extracts the
tweeted text using the twitter api (and the tweepy wrapper around it).

After extracting the text, the results are compiled with the initial info
and written to a csv file.


STEPS TO USE:

1. Add the necessary credentials in docs/api_credentials
2. Check all dependencies are loaded (check the requirements.txt). Install any missing dependencies.
2. Type  "python -m __init__.py" from its directory