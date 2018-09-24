import requests, sys, time

# need to have each: route, stop & direction
if len(sys.argv) != 4:
    sys.exit("Please be sure to enter a route, stop, and direction.")

route = sys.argv[1]
stop = sys.argv[2]
direction = sys.argv[3]

url = "http://svc.metrotransit.org/NexTrip/"

def getData (uri, key, value, arg):
    resp = requests.get(url + uri + "?format=json")
    data = resp.json()

    # default in case of invalid input 
    dataID = -1

    while True: 
        try: sys.exit(uri + str(resp.status_code))

        except:
            for item in data:
                if item[key].lower().find(arg) > -1:
                    dataID = item[value]
                    break
            return dataID

routeID = getData("Routes", "Description", "Route", route)

if routeID < 0:
    sys.exit(route + " is not a valid route.")

uri = routeID
directionID =  getData("Directions/" + uri, "Text", "Value", direction)

if directionID < 0:
    sys.exit(route + " does not go " + direction + ".")

uri += "/" + directionID 
stopID = getData("Stops/" + uri, "Text", "Value", stop)

if stopID < 0:
    sys.exit(stop + " is not along " + route + " going " + direction + ".")

uri += "/" + stopID
timeID = getData(uri, "RouteDirection", "DepartureTime", direction)

if timeID != -1:
    #Get 10 digit timestamp from response, - from current time, and / by 60 to get minutes as an integer
    time = int((float(timeID[6:16]) - time.time()) // 60)
    if time > 1:
        print str(time) + " minutes"
    else:
        print "1 minute or less"