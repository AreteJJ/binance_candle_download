import pandas as pd
import time
from binance.client import Client
from datetime import datetime

pairs_csv = pd.read_csv('D:/JJ/pairs.txt', delimiter = "\t", names=["pairs"])

pairs = list()
for i in pairs_csv.iloc[:, 0]:
    pairs.append(i)

priv_api = ""
pub_api = ""
client = Client(pub_api, priv_api)

df = pd.DataFrame(columns=pairs)


def price_get():
    count = 0
    while True:
        try: 
            pday = int(time.time())
            pday = datetime.fromtimestamp(pday)
            pday = str(pday).split(" ")[0]
            pday = pday.split("-")
            df = pd.DataFrame(columns=pairs)
            seconds = 60
            while True:
                start =  int(time.time())
                while True:
                    current = int(time.time())
                    elapsed = current-start
                    if elapsed >= seconds:
                        break
                    else: continue
                day = datetime.fromtimestamp(current)
                day = str(day).split(" ")[0]
                day = day.split("-")      
                if day[-1] != pday[-1]:
                    df.to_csv(f"binance_info_{pday[-1]}.{pday[-2]}.{pday[0]}.csv")
                    df = pd.DataFrame(columns=pairs)
                    count=0
                    pass
                else: pass
                s = client.get_all_tickers()
                nl = dict()
                for i in s[:]:
                    if i["symbol"] in pairs:
                        nl[i["symbol"]] = i["price"]
                    else: continue 
                nl["time"]=[current]
                nl = pd.DataFrame(nl)
                df = pd.concat([df, nl], axis=0)
                df = df.reset_index(drop=True)
                pday = day
            return True
        except Exception:
            if len(df.iloc[:,0]) > 300:
                count+=1
                df.to_csv(f"BROKEN{count}_binance_info_{pday[-1]}.{pday[-2]}.{pday[0]}.csv")
                True
            else: True
price_get()
