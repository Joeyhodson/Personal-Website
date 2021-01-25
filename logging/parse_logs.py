import os
import datetime
from dateutil.parser import parse

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
    # e.g. key = City -> value = clearwater
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
    def __init__(self, date_time, status_code, method, resource):
        self.date_time = parse(date_time)
        #self.date_time = datetime.datetime('%b/%d/%Y %H:%M:S%p')
        self.status_code = status_code
        self.method = method
        self.resource = resource

    def __str__(self):
        return f"{self.resource}, {self.status_code}, {self.method}, {self.date_time}"


def parse_request(line):

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

    request = Request(date_time, status_code, method, resource)

    return request


if __name__ == "__main__":

    in_file = open("logs.txt", "r")
    session_dict = {}

    for line in in_file:
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
        request = parse_request(line[left_bracket_index:])
        session.requests += [request]

    in_file.close()


    out_file = open("parsed_logs.txt", "w") # change to "a" -> kept "w" since appending would add onto already parsed logs (i.e. duplicates)

    for session in session_dict.values():
        out_file.write(str(session) + "\n\n")

    out_file.close()

# IDEA 1:
# POTENTIAL UPDATES -> ADD TO IP DICTIONARY, COUNT PROPER REQUESTS (SEE IF REAL PERSON ACCESSING SITE, NOT BOT)
# CONT. -> LOOK AT WHAT URLS THEY WERE ACCESSING (E.G. TRAVERSED THROUGH MY PROJECT URLS, MOST LIKELY REAL PERSON)
# CREATE GLOBAL LIST OF AUTHENTIC PATHS

# IDEA 2:
# RATHER THAN CREATING PARSEDLOGS.TXT FROM SCRATCH EVERYTIME, MAYBE TAKE DIFF OF NEW LOG FROM OLD LOG AND APPEND IT TO PARSEDLOGS.TXT