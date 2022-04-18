import requests
import hashlib
import sys
import json

def upload_file(file, apikey):
    '''
    Uploads a file and retrieves the associated data_id of the file.

    Parameters
    -------------
    file - The contents of the file being uploaded
    apikey (string) - The apikey of the user running the program

    Returns
    -------------
    The data_id of the file uploaded
    '''

    url = "https://api.metadefender.com/v4/file"
    headers = {
    "apikey": "{key}".format(key=apikey),
    "Content-Type": "application/octet-stream"
    }

    try:
        response = requests.request("POST", url, headers=headers, data=file)
        response = response.json()
    except requests.exceptions.HTTPError as he:
        print("HTTP Error: ", he)
        sys.exit(0)
    except requests.exceptions.ConnectionError as ce:
        print("Connection Error: ", ce)
        sys.exit(0)
    except requests.exceptions.Timeout as to:
        print("Timeout: ", to)
        sys.exit(0)
    except requests.exceptions.InvalidHeader as ih:
        print("Invalid Header: ", ih)
        sys.exit(0)
    except requests.exceptions.RequestException as re:
        print("Request Exception: ", re)
        sys.exit(0)

    return response["data_id"]

def hash_file(file_name):
    '''
    Calculates the hash value of a given file.

    Parameters
    -------------
    file_name (string) - The name of the file

    Output
    -------------
    Hash value of 'file'

    Based on: <https://www.programiz.com/python-programming/examples/hash-file#:~:text=Source%20Code%20to%20Find%20Hash&text=Hash%20functions%20are%20available%20in,and%20update%20the%20hashing%20function>
    '''

    hash = hashlib.sha1()
    with open(file_name, 'rb') as file:
        chunk = 0
        while chunk != b'':
            chunk = file.read(1024)
            hash.update(chunk)
    
    return hash.hexdigest()


def hash_lookup(file_hash, apikey):
    '''
    Looks up a hash value against the API, and returns whether it was successful

    Parameters
    -------------
    file_hash (string) - Hash value of the file being scanned
    apikey (string) - The apikey of the user running the program
    
    Returns
    -------------
    True if the hash lookup was successful, false otherwise
    '''

    url = "https://api.metadefender.com/v4/hash/{hash}".format(hash=file_hash)
    headers = {
    "apikey": "{key}".format(key=apikey)
    }

    try:
        response = requests.request("GET", url, headers=headers)
        response = response.json()
    except requests.exceptions.HTTPError as he:
        print("HTTP Error: ", he)
        sys.exit(0)
    except requests.exceptions.ConnectionError as ce:
        print("Connection Error: ", ce)
        sys.exit(0)
    except requests.exceptions.Timeout as to:
        print("Timeout: ", to)
        sys.exit(0)
    except requests.exceptions.InvalidHeader as ih:
        print("Invalid Header: ", ih)
        sys.exit(0)
    except requests.exceptions.RequestException as re:
        print("Request Exception: ", re)
        sys.exit(0)

    return response

def pull_on_data_id(data_id, apikey):
    '''
    Pulls on 'data_id' to retrieve scanning results after a file with given 'data_id' has been uploaded
    
    Parameters
    -------------
    data_id (string) - The data_id of the file returned after it has been uploaded
    apikey (string) - The apikey of the user running the program

    Returns
    -------------
    The results retrieved from pulling on 'data_id'
    '''

    url = "https://api.metadefender.com/v4/file/{id}".format(id=data_id)
    headers = {
    "apikey": "{key}".format(key=apikey),
    "x-file-metadata": "0"
    }

    try:
        #Repeatedly scans results
        progress = 0
        while progress < 100:
            response = requests.request("GET", url, headers=headers)
            response = response.json()
            progress = (response["scan_results"])["progress_percentage"]
    except requests.exceptions.HTTPError as he:
        print("HTTP Error: ", he)
        sys.exit(0)
    except requests.exceptions.ConnectionError as ce:
        print("Connection Error: ", ce)
        sys.exit(0)
    except requests.exceptions.Timeout as to:
        print("Timeout: ", to)
        sys.exit(0)
    except requests.exceptions.InvalidHeader as ih:
        print("Invalid Header: ", ih)
        sys.exit(0)
    except requests.exceptions.RequestException as re:
        print("Request Exception: ", re)
        sys.exit(0)
    
    return response

def print_output(filename, response_data):
    '''
    Prints the file name, overall status of the file, and the results from different scans performed on given file

    Parameters
    -------------
    filename (string) - The name of the file that was scanned
    response_data - The data retrieved from either performing a hash lookup or from pulling on the file's data_id

    Returns
    -------------
    None
    '''

    overall_status = (response_data["scan_results"])["scan_all_result_a"]
    scans = (response_data["scan_results"])["scan_details"]

    #Prints the name of the file and overall status
    print("filename: {file_name}".format(file_name=filename))
    print("overall status: {status}".format(status=overall_status if overall_status != "No Threat Detected" else "Clean"))

    #Prints information from each of different engines
    for result in scans:
        print("engine: {engine}".format(engine=result))
        result_data = scans[result]
        print("threat_found: {threat}".format(threat=result_data["threat_found"] if result_data["threat_found"] else "Clean"))
        print("scan_result: {result}".format(result=str(result_data["scan_result_i"])))
        print("def_time: {time}".format(time=(result_data["def_time"])))

def get_inputs():
    '''
    Retrieves input from the user. Retrieves the command to be run, the name of the associated file, and the user's apikey.

    Parameters
    -------------
    None

    Returns
    -------------
    None
    '''

    #Retrieves command and associated file name
    command = input("Enter a command: ")
    args = command.split()
    if args[0] != "upload_file":
        print("Unsupported command")
        sys.exit(0)
    file_name = args[1]

    #Retrieves user's apikey
    apikey = input("Enter your apikey: ")
    args = apikey.split()
    apikey = args[0]
    return [file_name, apikey]

#Retrieves inputs and gets the name of the file and user's apikey
inputs = get_inputs()
file_name = inputs[0]
apikey = inputs[1]

#Gets the hash value of the file (Step 1)
file_hash = hash_file(file_name)

#Checks if there are previously cached results for the file (Step 2), and gets associated data if it exists
file_data = hash_lookup(file_hash, apikey)

#Determines whether the file was previously cached
file_found = file_data.__contains__("file_id")

#If file was previously cached, print results (Step 3)
if file_found:
    #Prints output (Step 6)
    print_output(file_name, file_data)

#File was not previously cached
else:
    #Reads and uploads file to retrieve data_id (Step 4)
    with open(file_name, 'rb') as file:
        f = file.read()
    data_id = upload_file(f, apikey)
    
    #Pull on data id to retrieve results (Step 5)
    response_data = pull_on_data_id(data_id, apikey)

    #Prints output (Step 6)
    print_output(file_name, response_data)
