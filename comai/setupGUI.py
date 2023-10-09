from tkinter import *
import sys
import json
import os
from tqdm import tqdm
from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files.file import File
from office365.runtime.client_request_exception import ClientRequestException


def createJSONold(client_id, client_secret, ip, site_url, folder_url):
    if not os.path.isfile('config.json'):
        config_data = {
            'clientID': client_id,
            'clientSecret': client_secret,
            'ip': ip,
            'siteURL': site_url,
            'folderURL': folder_url
            }
    
        with open('config.json', 'w') as file:
            json.dump(config_data, file)


def createJSON(client_id, client_secret, ip, site_url, folder_url):

        config_data = {
            'clientID': client_id,
            'clientSecret': client_secret,
            'ip': ip,
            'siteURL': site_url,
            'folderURL': folder_url
            }
    
        with open('config.json', 'w') as file:
            json.dump(config_data, file)


def loadJSON():
    try:
        with open('config.json', 'r') as file:
            config = json.load(file)
        return config
    except FileNotFoundError:
        print("file not found")
        return False


def cls():
    #Clear console, cross plattform
    os.system('cls' if os.name=='nt' else 'clear')


def authAndDownloadPDF(client_id, client_secret, site_url, folder_url):
    # Create Folder if not already existing

    if os.path.exists("PDFStore") == False:
        current_directory = os.getcwd() + "/PDFStore" #In linux /PDFStore
        os.mkdir(current_directory)

    try:
        # Get authenticated using context
        context_auth = AuthenticationContext(site_url)
        context_auth.acquire_token_for_app(client_id, client_secret)
        ctx = ClientContext(site_url, context_auth)

        folder = ctx.web.get_folder_by_server_relative_url(folder_url)

    # Load folder properties and get all files
        ctx.load(folder)
        files = folder.get_files()
        ctx.load(files)
        ctx.execute_query()

        # Get the total number of files first
        total_files = len(files)

        # Initialize a counter
        downloaded_files = 0

        # Download all files
        for file in tqdm(files, desc="Downloading files", unit="file"):

            # Setup path's an prepare download folder for each file 
            download_path = f"{file.properties['Name']}"
            current_directory = os.getcwd() + "\\PDFStore" #Full folder Path #In Linux /PDFStore
            
            final_path = os.path.join(current_directory, download_path)
            file_content = File.open_binary(ctx, file.serverRelativeUrl)
            ctx.execute_query()

            with open(final_path, "wb") as local_file:
                local_file.write(file_content.content)

            print(f"\rDownloaded file: {file.properties['Name']}", end='')
        cls()
        return True
    
    # For any exceptions regarding "wrong spelling"
    except ClientRequestException as e:
        print("There is an Error with the folder URL, please check for any typos")
        return False
    except ValueError as e:
        cls()
        if 'unauthorized_client' in str(e):
            print("There is an Error with your clientID please check for any typos and correct spelling")
        elif 'invalid_client' in str(e):
            print("There is an Error with your clientSecret(Value) please check for any typos and correct spelling")
        elif 'invalid_request' in str(e):
            print("There is an Error with your site URL please check for any typos and correct spelling")
        else:
            print(e)
        return False
    
      
def createPDFStore():
    if os.path.exists("PDFStore") == False:
        current_directory = os.getcwd()
        os.mkdir( os.path.join(current_directory, r"PDFStore"))
        print("newFolder PDFStore has been created")


def ipFinder():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 1))  # connect() for UDP doesn't send packets
    local_ip_address = s.getsockname()[0]
    return local_ip_address


def ipSetup():
    ipv4 = ipFinder()
    print("For automatic setup enter 1 (Default)\n or")
    print("Enter IPv4:")

    # Unecessary (?) DELETE WHEN DONE
    if len(sys.argv) > 1:
        enteredIP = sys.argv[1]
    else:
        enteredIP = input()

    if enteredIP == '1':
        IP = ipv4
        print("Server is being hosted under: " + IP + "\n")
        print("Please wait...")
    else:
        IP = enteredIP

    return IP


def setFieldsFromConfig(client_id_entry, client_secret_entry, ip_entry, site_url_entry, folder_url_entry):
    config =  loadJSON()
    client_ID = config['clientID']
    client_Secret = config['clientSecret']
    site_URL = config['siteURL']
    folder_URL = config['folderURL']
    ip = config['ip']
    

    client_id_entry.insert(0, client_ID)
    client_secret_entry.insert(0, client_Secret)
    ip_entry.insert(0, ip)
    site_url_entry.insert(0, site_URL)
    folder_url_entry.insert(0, folder_URL)


def convert_to_path(url, folder_url_entry):
    # Find the position of "/sites/"
    idx = url.find("/sites/")
    if idx == -1:  # "/sites/" not found in the url
        print("/sites/ was not found inside the URL, this will throw an exception. please check your pasted URL")
        return ""
    
    # Extract the part of the URL from "/sites/" onwards
    path = url[idx:]
    # Replace "%20" with spaces
    path = path.replace("%20", " ")
    folder_url_entry.delete(0, 'end')
    return path


def main():
    # Create main window
    root = Tk()

    # Set window size
    root.geometry('700x150')

    root.resizable(width=False,height=False)

    # Add a title
    root.title("Setup")

    # Create labels and entries
    client_id_label = Label(root, text="Client ID:")
    client_secret_label = Label(root, text="Client Secret:")
    ip_label = Label(root, text="IP: (autofilled, change if needed)")
    site_url_label = Label(root, text="Site URL:")
    folder_url_label = Label(root, text="Folder URL (e.g., /sites/myfolder/subfolder1/subfolder2):")

    # Create StringVar() variables
    client_id_var = StringVar()
    client_secret_var = StringVar()
    ip_var = StringVar()
    site_url_var = StringVar()
    folder_url_var = StringVar()

    # Create Entry widgets, passing the StringVar() variables to the textvariable parameter
    client_id_entry = Entry(root, textvariable=client_id_var)
    client_secret_entry = Entry(root, textvariable=client_secret_var)
    ip_entry = Entry(root, textvariable=ip_var)
    site_url_entry = Entry(root, textvariable=site_url_var)
    folder_url_entry = Entry(root, textvariable=folder_url_var)

    # Checkbox to trigger IP finder
    ip_auto_check = BooleanVar()
    ip_checkbutton = Checkbutton(root, 
                                 text='Auto-Find IP', 
                                 variable=ip_auto_check, 
                                 command= lambda: (ip_entry.delete(0, 'end'),
                                                    ip_entry.insert(0,  ipFinder()))
                                                    if ip_auto_check.get() else None)
    ip_checkbutton.grid(row=2, column=2)

    # Checkbox to convert folder link to folder_URL 
    convert_to_path_check = BooleanVar()
    convert_to_path_checkbutton = Checkbutton(root, 
                                            text='Convert to Path', 
                                            variable=convert_to_path_check, 
                                            command= lambda: (
                                                                folder_url_entry.insert(0, convert_to_path(folder_url_entry.get(), folder_url_entry)) 
                                                                if convert_to_path_check.get() else None)
                                            )
    convert_to_path_checkbutton.grid(row=4, column=2)

    config =  loadJSON()
    try:
        if config: # Is there any config file already ? yes ? then use it.
            setFieldsFromConfig(client_id_entry, client_secret_entry, ip_entry, site_url_entry, folder_url_entry)    
        else:
             # Autofill Ip
            ip_entry.insert(0,  ipFinder())
    except FileNotFoundError:
        print("no config, skipping.")
    except TypeError:
        print("The config.json might be corrupted, try deleting the config.JSON and repeat the setup process.")
   
    def submit():
        createJSON(client_id_entry.get(), 
                client_secret_entry.get(),
                ip_entry.get(), 
                site_url_entry.get(), 
                folder_url_entry.get())
    
        # Check if there was any exception, if not, close GUI. Otherwise loop back
        done = authAndDownloadPDF(client_id_entry.get(), 
                    client_secret_entry.get(), 
                    site_url_entry.get(), 
                    folder_url_entry.get())
        if done is True:
        #Reason: If called, it cant create chunks since no data is present on initial start
        #Solution: move the loose code into function(s)
        #So far its just a "hacky" solution.
            import LChainTest
            root.destroy()
        
    # Create submit button
    submit_button = Button(root, text="Save", command=submit, height=2, width=10)
    submit_button.grid(row=5, column=1)
    

    # Grid system
    client_id_label.grid(row=0, column=0,sticky='w')
    client_id_entry.grid(row=0, column=1, sticky='nsew')
    client_secret_label.grid(row=1, column=0,sticky='w')
    client_secret_entry.grid(row=1, column=1, sticky='nsew')
    ip_label.grid(row=2, column=0,sticky='w')
    ip_entry.grid(row=2, column=1, sticky='nsew')
    site_url_label.grid(row=3, column=0,sticky='w')
    site_url_entry.grid(row=3, column=1, sticky='nsew')
    folder_url_label.grid(row=4, column=0,sticky='w')
    folder_url_entry.grid(row=4, column=1, sticky='nsew')

    # Allow the second column to expand
    root.grid_columnconfigure(1, weight=1)

    # Start the GUI
    root.mainloop()

main()