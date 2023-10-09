from setupGUI import *


def main():
    createPDFStore
    config =  loadJSON()
    try:
        if config: # Is there any config file already ? yes ? then use it.
            print("config file found. proceeding to fetch data")
            client_ID = config['clientID']
            client_Secret = config['clientSecret']
            site_URL = config['siteURL']
            folder_URL = config['folderURL']
            done = authAndDownloadPDF(client_ID, client_Secret,site_URL,folder_URL)
            if done is True:
                print("PDF download completed")
                
    except FileNotFoundError:
        print("no config, skipping.")
    except TypeError:
        print("The config.json might be corrupted, try deleting the config.JSON and repeat the setup process.")

main()