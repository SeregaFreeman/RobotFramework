import os

base_url = r"https://accounts.google.com/o/oauth2/"
redirect_uri = "urn:ietf:wg:oauth:2.0:oob"
source_folder = os.path.join(os.path.split(os.path.split(os.path.abspath(__file__))[0])[0], 'resources')
phantomjs_path_win = os.path.join(source_folder, "phantomjs.exe")
phantomjs_path_unix = os.path.join(source_folder, "phantomjs")

max_attempt_number = 5
