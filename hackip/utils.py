import configparser


def load_configuration():
    config = configparser.ConfigParser()
    # Read the config.ini file
    config.read("hackip/config.ini")
    return config
