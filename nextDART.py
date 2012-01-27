#!/usr/bin/env python

import sys
from optparse import OptionParser
import urllib2

try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    print "Requires BeautifulSoup module"
    sys.exit(0)
    
# Global data

# dict for dart station rss IDs
stations = {
    'pearse'           : 'PERSE',
    'blackrock'        : 'BROCK',
    'grand canal dock' : 'GCDK',
    'tara'             : 'TARA',
    'tara street'      : 'TARA',
}   

def set_args():
    """
    Set up options
    """


    # set up arguments, take any immediate action required
    parser = OptionParser()

    parser.add_option("-s", "--station", dest="start_station", help="starting station")

    parser.add_option("-d", "--direction", dest="direction", help="direction of travel" )

    parser.add_option("-l", "--list", action="store_true", dest="list_stations", help="list available stations" )

    (options, args) = parser.parse_args()   

    if options.list_stations:
        print "Possible options for starting station:"
        print "\n".join(stations.keys())  
        sys.exit()
    
    # assign arguments as required
    try:
        start_station = options.start_station.lower()
        direction = options.direction.lower()
    except Exception, e:
        parser.error("Problem with arguments, see -h --help for help")
        print e                 

    return (start_station, direction)

def main():

    start_station, direction = set_args()

    try:
        raw_response = urllib2.urlopen("http://www.irishrail.ie/realtime/station_details.jsp?ref=" + stations[start_station], )
    except urllib2.HTTPError:
        print "Unable to connect"
        sys.exit(0)  

    # terminating stations
    if direction == 'south':
        targets = ['Bray', 'Greystones']
    elif direction == 'north':
        targets = ['Howth', 'Malahide']

    tables = BeautifulSoup(raw_response.read()).findAll('table')

    trains = []
    for tb in tables:
        rows = tb.findAll('tr')
        for tr in rows:
            train = []
            cols = tr.findAll('td')
            for td in cols:
                text_ = td.find(text=True)
                if text_ is not None:
                    text = ''.join(text_)
                    train.append(text)
            if "DART" in train: trains.append(train)                   

    for train in trains:
        if train[2] in targets:
            print("[ arriving in %s]  %s" % (train[6], train[3]+" "+train[0])) 

if __name__ == '__main__':
    main()
