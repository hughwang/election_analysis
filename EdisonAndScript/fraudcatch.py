import json



def findfraud(NAME):
    with open(NAME + '.json', encoding="utf8") as f:
        x = json.load(f)
    TotalVotesLost = 0
    for i in range(len(x["data"]["races"][0]["timeseries"])):
        if i != 0 and x["data"]["races"][0]["timeseries"][i]["votes"] * x["data"]["races"][0]["timeseries"][i]["vote_shares"]["trumpd"] < x["data"]["races"][0]["timeseries"][i-1]["votes"] * x["data"]["races"][0]["timeseries"][i-1]["vote_shares"]["trumpd"]:
            if x["data"]["races"][0]["timeseries"][i]["votes"] * x["data"]["races"][0]["timeseries"][i]["vote_shares"]["bidenj"] > x["data"]["races"][0]["timeseries"][i-1]["votes"] * x["data"]["races"][0]["timeseries"][i-1]["vote_shares"]["bidenj"]:
                print ("Index : " + str(i) + " Past Index : " + str(i-1))
                print (x["data"]["races"][0]["timeseries"][i]["votes"] * x["data"]["races"][0]["timeseries"][i]["vote_shares"]["trumpd"] - x["data"]["races"][0]["timeseries"][i-1]["votes"] * x["data"]["races"][0]["timeseries"][i-1]["vote_shares"]["trumpd"])
                TotalVotesLost += x["data"]["races"][0]["timeseries"][i]["votes"] * x["data"]["races"][0]["timeseries"][i]["vote_shares"]["trumpd"] - x["data"]["races"][0]["timeseries"][i-1]["votes"] * x["data"]["races"][0]["timeseries"][i-1]["vote_shares"]["trumpd"]
    print (str(str(TotalVotesLost)  + " Flo"))

def findfraud2(NAME):
    with open(NAME + '.json', encoding="utf8") as f:
        x = json.load(f)
    TotalVotesLost = 0
    for i in range(len(x["data"]["races"][0]["timeseries"])):
        if i != 0 and x["data"]["races"][0]["timeseries"][i]["votes"] < x["data"]["races"][0]["timeseries"][i-1]["votes"]:
            TotalVotesLost += x["data"]["races"][0]["timeseries"][i]["votes"] - x["data"]["races"][0]["timeseries"][i-1]["votes"]
    print (TotalVotesLost)
