import configparser
"""
Variables for streamer_process.py. wait_time defined in seconds.

"""
config = configparser.ConfigParser()
config['DEFAULT'] = {"path_to_rec" : "/mnt/f/IISc_Big/recordings",
    				"wait_time" : "5",
    				"list_length":100}
with open('config.ini', 'w') as configfile:
  config.write(configfile)