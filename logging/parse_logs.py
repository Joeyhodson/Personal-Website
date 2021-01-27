import sys

import os
from os import path

import datetime
from dateutil.parser import parse

import pickle


# Data comes from 'logs.txt', a file transferred via ssh from a remote pi periodically over cron
# Script parses all relevant data into a text file, also invokes 'who is' on each IP to generate IP locations & other data.
# All requests are formatted into single line strings, data separated by spaces


# returns a dictionary
def get_whois_dict(client_ip):

    # stream returns a large ass string of stdout from bash
    stream = os.popen(f"whois {client_ip}")
    lines = stream.readlines()

    # list holds lines that don't start w/ # or ' ' of returned string from stream
    filtered_lines = []
    for line in lines:
        #.strip() removes whitespace from both sides of a string
        stripped_line = line.strip()
        if len(stripped_line) != 0 and stripped_line[0] != '#':
            filtered_lines += [stripped_line]

    # dictionary or 'Map' takes keys that return values
    # e.g. key = City -> value = Clearwater
    whois_dict = {}
    for filtered_line in filtered_lines:
        colon_index = filtered_line.find(':')
        key = filtered_line[:colon_index].strip()
        key = key.lower()
        value = [filtered_line[colon_index+1:].strip()]
        
        if key in whois_dict:
            old_value = whois_dict[key]
            old_value += value
            whois_dict[key] = old_value

        else:
            whois_dict[key] = value

    return whois_dict


class Session:
    def __init__(self, ip_address):
        self.ip_address = ip_address
        self.whois_dict = get_whois_dict(ip_address)
        self.requests = []

    def getLocationInfo(self):
        city = self.whois_dict.get("city")
        stateprov = self.whois_dict.get("stateprov")
        country = self.whois_dict.get("country")
        address = self.whois_dict.get("address")

        return f"{city}, {stateprov}, {country}, {address}"
        
    def __str__(self):
        stringified = f"{self.ip_address}, {self.getLocationInfo()}\n"

        for request in self.requests:
            stringified += f"\t{request}\n"

        return stringified


class Request:
    def __init__(self, date_time, status_code, method, resource, process_time, log_line_number):
        self.date_time = parse(date_time)
        #self.date_time = datetime.datetime('%b/%d/%Y %H:%M:S%p')
        self.status_code = status_code
        self.method = method
        self.resource = resource
        self.process_time = process_time
        self.log_line_number = log_line_number

    def __str__(self):
        return f"{self.resource}, {self.status_code}, {self.method}, {self.date_time}"

    def __eq__(self, other):
        if (isinstance(other, Request)):
            return self.date_time == other.date_time and self.status_code == other.status_code \
             and self.method == other.method and self.resource == other.resource and \
             self.process_time == other.process_time and self.log_line_number == other.log_line_number

        return False


def parse_request(line, line_number):

    right_square_bracket = line.find(']')
    date_time = line[1:right_square_bracket]
    
    open_quote_index = line.find('"')
    line = line[open_quote_index + 1:]

    end_quote_index = line.find('"')

    method_resource_protocol = line[:end_quote_index].split(' ')
    if len(method_resource_protocol) == 3:
        method = method_resource_protocol[0]
        resource = method_resource_protocol[1]
    else:
        method = None
        resource = None

    line = line[end_quote_index + 2:]

    space_index = line.find(' ')
    status_code = line[:space_index]

    line = line[space_index + 1:]

    space_index = line.find(' ')
    somme_number = line[:space_index] # non distinct number in log

    line = line[space_index + 1:]

    process_time = line

    request = Request(date_time, status_code, method, resource, process_time, line_number)

    return request


# Called from partition_parsed_logs 
def parse_logs(raw_logs):

    session_dict = {}

    # Deserialize previous session_dict, if exists
    if path.exists("session_dict.obj"):
        session_dict_filehandler = open("session_dict.obj", "rb")
        session_dict = pickle.load(session_dict_filehandler)
        session_dict_filehandler.close()

    # The current log number makes every request distinct
    log_line_number = 0

    raw_logs_filehandler = open(raw_logs, "r")

    for line in raw_logs_filehandler:

        log_line_number += 1

        if not line.startswith("::ffff:"):
            continue
        line = line[7:]
        space_index = line.find(' ')
        ip_address = line[:space_index]

        if ip_address not in session_dict:
            session = Session(ip_address)
            session_dict[ip_address] = session
        else: 
            session = session_dict[ip_address]

        left_bracket_index = line.find('[')
        request = parse_request(line[left_bracket_index:], log_line_number)

        if request not in session.requests:
            session.requests += [request]
        else:
            #print(request)
            #print("\n")
            #for temp in session.requests:
                #print(temp)
            #print("Up to date")
            raw_logs_filehandler.close()
            sys.exit(1)

    raw_logs_filehandler.close()

    # Serialize current state of session_dict
    session_dict_filehandler = open("session_dict.obj", "wb")
    pickle.dump(session_dict, session_dict_filehandler)
    session_dict_filehandler.close()

    return session_dict