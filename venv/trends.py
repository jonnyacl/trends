import sys
from pytrends.request import TrendReq
from pytrends.exceptions import ResponseError
import numpy as np
from twowords import *
from datetime import datetime
from time import sleep


# initialise empty 2D array of 172 rows (max number weeks queryable by trends)
# and column size = number of queries + 1 for the date at the start
result = np.empty([172, (len(terms) * 5) + 1], dtype=object)
startTime = datetime.now()
title = ''


# runs the trend query on a row, so 5 queries
def run_trends(a, term, term_no, google_block_count):

    try:
        trender(a, term, term_no)
    except ResponseError:
        print "Google blocking us, try sleeping..."
        google_block_count = google_block_count + 1
        print 'block count: ' + str(google_block_count)
        sleep(60)
        # try again
        try:
            trender(a, term, term_no)
        except ResponseError:
            print "Google still blocking us, skipping term row..."
            google_block_count = google_block_count + 1
            print 'block count: ' + str(google_block_count)
            sleep(60)
    if google_block_count >= 5:
        print_result()
    return google_block_count


def trender(a, term, term_no):
    pytrends = TrendReq(hl='en-US', tz=360)
    pytrends.build_payload(term, cat=0, timeframe='all', geo='GB', gprop='')
    interest = pytrends.interest_over_time()
    b = 0

    # set the values at the correct indices in the 2D result array
    for index, row in interest.iterrows():
        indexstring = str(index)
        result[b][0] = indexstring
        result[b][a + 1] = str(row[term[0]])
        result[b][a + 2] = str(row[term[1]])
        result[b][a + 3] = str(row[term[2]])
        result[b][a + 4] = str(row[term[3]])
        if len(term) == 5:
            result[b][a + 5] = str(row[term[4]])
        b += 1

    print term_no


def print_result():
    # create the column titles

    sys.stdout = open(title + '.csv', 'w')
    headers = 'date'

    for t in terms:
        for item in t:
            headers += ', ' + item
    print headers
    # print the results
    for a in result:
        rowtext = ''
        for w in a:
            if w is not None:
                rowtext += str(w) + ','
        print rowtext[:-1]


if __name__ == "__main__":
    i = 0
    n = 0
    title = sys.argv[1]
    blockcount = 0
    print title
    # loop round the rows of 5 queries at a time and run the trend request
    for term in terms:
        blockcount = run_trends(i, term, n, blockcount)
        i += len(term)
        n += 1
    queryFinish = datetime.now() - startTime

    print_result()
    print 'Query run time: ', queryFinish
    print 'Total run time: ', datetime.now() - startTime


