import sys
import datetime
from pyspark import SparkContext
from pyspark.streaming import StreamingContext


def get_goog(x):
    line = x.split(" ")
    goog_price = line[1]
    return (goog_price)


def get_msft(x):
    line = x.split(" ")
    msft_price = line[2]
    return (msft_price)


def goog_trade(x):
    tenDay_before = x[0][0]
    fortyDay_before = x[0][1]
    tenDay_after = x[1][0]
    fortyDay_after = x[1][1]
    date = x[2]

    if tenDay_before < fortyDay_before and tenDay_after > fortyDay_after:
        # BUY
        return (date, " buy goog")
    if tenDay_before > fortyDay_before and tenDay_after < fortyDay_after:
        # SELL
        return (date, "sell msft")

if __name__ == "__main__":
    # Setup
    #conf = (SparkConf().setMaster("local").setAppName("StockAnalysis").set("spark.shuffle.service.enabled", "false").set("spark.dynamicAllocation.enabled", "false"))
    sc = SparkContext()
    ssc = StreamingContext(sc, 1)

    lines = ssc.socketTextStream(sys.argv[1], int(sys.argv[2]))
    googPrice = lines.map(lambda l: get_goog(l))
    msftPrice = lines.map(lambda l: get_msft(l))
    dates = lines.map(lambda l: l.split(" ")[0])


    googLast10 = googPrice.window(10, 1)
    googLast10 = googLast10.map(lambda k: (float(k), 1))
    googLast10 = googLast10.map(lambda k: k[1])
#    googLast10 = googLast10.reduce(lambda k, j: (k[0] + j[0], k[1] + j[1]))
    googLast10.pprint()
#    googLast10 = googLast10.filter(lambda k: k[1] == 10)
    goog10Day = googLast10.map(lambda k: float(k[0]) / 10)

    googLast40 = googPrice.window(40, 1)
    googLast40 = googLast40.map(lambda k: (float(k), 1))
    googLast40 = googLast40.reduce(lambda k, j: (k[0] + j[0], k[1] + j[1]))
    googLast40 = googLast40.filter(lambda k: k[1] == 10)
    goog40Day = googLast40.map(lambda k: float(k[0]) / 40)

#       googLast10 = googLast10.filter(lambda l: len(l) >= 10) wondering if this would work just fine
#       googLast40 = googLast40.filter(lambda l: len(l) >= 40)
#       goog10Day = googLast10.map(lambda l: float(l)).reduce(lambda x, y: x + y).map(lambda sum: float(sum) / 10)
#       goog40Day = googLast40.map(lambda l: float(l)).reduce(lambda x, y: x + y).map(lambda sum: float(sum) / 40)

    msftLast10 = msftPrice.window(10, 1)
    msftLast10 = msftLast10.map(lambda k: (float(k), 1))
    msftLast10 = msftLast10.reduce(lambda k, j: (k[0] + j[0], k[1] + j[1]))
    msftLast10 = msftLast10.filter(lambda k: k[1] == 10)
    msft10Day = msftLast10.map(lambda k: float(k[0]) / 10)

    msftLast40 = msftPrice.window(40, 1)
    msftLast40 = msftLast40.map(lambda k: (float(k), 1))
    msftLast40 = msftLast40.reduce(lambda k, j: (k[0] + j[0], k[1] + j[1]))
    msftLast40 = msftLast40.filter(lambda k: k[1] == 40)
    msft40Day = msftLast40.map(lambda k: float(k[0]) / 40)


    goog_join = goog10Day.join(goog40Day)
    goog_join_2 = goog_join.window(2, 1) # (10Day.before, 40Day.before), (10Day.after, 40Day.after)
    goog_buy_sell = goog_join_2.join(dates).map(lambda t: goog_trade(t))

#   goog_buy_sell.pprint()

    msft_join = msft10Day.join(msft40Day)
    msft_join_2 = msft_join.window(2, 1)
    msft_buy_sell = msft_join_2.join(dates).map(lambda t: msft_trade(t))

#   msft_buy_sell.pprint()
    googPrice.pprint()

    ssc.start()
    ssc.awaitTermination()