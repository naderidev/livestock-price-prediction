import json
import threading
from scrapper import Scrapper
from rich.pretty import pprint


# scrapper = Scrapper()
# pprint(scrapper.get_data(["گوساله","گوسفند"], [1392, 11, 7]))
# exit()

def get_all_days(from_year:int, to_year:int):
    return dict(
            [
                (
                    i,
                        list(
                            map(
                                lambda y: list(range(1 , 32)) if y < 6 else ( list(range(1 , 30)) if y == 11 else list(range(1 , 31))),
                                range(12)
                            )
                        )
                ) for i in list(range(from_year , to_year + 1))
        ]
    )

inflations:dict = json.loads(open("tavarom.json" , "r").read())
dataset_file = open("dataset.csv" , "w+",encoding='utf-8')

# Wrtiing the Header
dataset_file.write("PROVINCE,PRICE,TYPE,YEAR,MONTH,DAY,INFLATION_RATE\n")

# Settingup Threads
saved_dates:list[list[int]] = []
thread_list:list[threading.Thread] = []

# Settingup Scrapper
dates = get_all_days(1392, 1403)
count_all =  sum(list( map(lambda x: len(x) , sum(list(dates.values()) , [])) ))
scrapper = Scrapper()
types = ["گوساله", "گوسفند"]



for year, months in dates.items():
    for month, days in enumerate(months):
        for day in days:
            date = [year, (month + 1), day]
            def thread(d):
                try:
                    models = scrapper.get_data(types,d)
                    if models:
                        inflation_rate = inflations[str(year)][d[1] - 1] if str(year) in list(inflations.keys()) else ''
                        for model in models:
                            dataset_file.write(model.to_csv_row() + f",{inflation_rate}\n")
                        saved_dates.append(saved_dates)
                except:
                    pass
                    

            th = threading.Thread(target=thread, args=(date, ))
            thread_list.append(th)
            th.start()

            if len(thread_list) % 60 == 0:
                for t in thread_list:
                    t.join()
                    print(f"\r--> Saved Dates Count: {len(saved_dates)} of {count_all} | %{round((len(saved_dates) / count_all)*100, 2)}", end="") 
