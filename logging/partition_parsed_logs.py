from parse_logs import parse_logs


valid_urls = {'/resume', '/3DPrinting', '/ElectricSkateboard',
'/Fishing', '/FishTank', '/LEDCube', '/LEDFootwells', '/Website',
'/Photography', '/RoboticQuadruped', '/JosephHodsonResume.pdf', '/static/style.css',
'/static/cursor.gif', '/static/logo.png', '/favicon.ico'}

if __name__== "__main__":

    session_dict = parse_logs("logs.txt")

    valid_requests = open("valid_requests.txt", "w")
    malicious_requests = open("malicious_requests.txt", "w")

    for session in session_dict.values():

        countries = session.whois_dict.get("country")
        valid_path = False

        if all(request.resource == "/" for request in session.requests) and all(country == "US" for country in countries):
            valid_path = True
        else:
            for request in session.requests:
                if request.resource in valid_urls:
                    valid_path = True
                    break

        if valid_path == True:
            valid_requests.write(str(session) + "\n\n")
        else:
            malicious_requests.write(str(session) + "\n\n")

    valid_requests.close()
    malicious_requests.close()