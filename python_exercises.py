from typing import List,Dict, Callable ,Any
def count_event_type(logs):
    event_counts={}
    for log in logs:
        user_id=log.get("user_id")
        event=log.get("event")
        if event is None or user_id is None:
            continue
        if user_id not in event_counts :
            event_counts[user_id]={event:1}
        else:
            event_counts[user_id][event] = event_counts[user_id].get(event,0) + 1

    return event_counts

def count_events_def_dict(logs):
    from collections import defaultdict
    event_counts= defaultdict(lambda:defaultdict(int))
    for log in logs:
        user_id = log.get("user_id")
        event = log.get("event")
        event_counts[user_id][event] += 1
    return {k:dict(v) for (k,v) in event_counts.items()}

def read_csv(file_path):
    import csv
    
    with open(file_path,mode="r",encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        fieldnames_len = len(csv_reader.fieldnames)
        for row in csv_reader:
            if None in row.values() or None in row:
                continue
            if row["event"] == "click":
                yield {**row, 'filtered':True}

def build_pipeline(funct_list:List[Callable]) ->Callable:
    if not funct_list :
        raise ValueError("No function passed to pipeline")
    def process_data(initial_result:List[Dict[str,Any]])->List[Dict[str,Any]]:
        result = initial_result
        for funct in funct_list:
            result = funct(result)
        return result
    return process_data

def trim_fields(rows: List[Dict])->List[Dict]:
    return  [{k:v.strip() if isinstance(v,str) else v for (k,v) in row.items()}
             for row in rows]    
def captialise_fields(rows:List[Dict])->List[Dict]:
    return [{k:v.upper()  if isinstance(v,str) else v for (k,v) in row.items() } 
            for row in rows]

from typing import List,DefaultDict,Any
from collections import defaultdict
import bisect

class SlidingWindowCounter():
    def __init__(self, N:int):
        self.window_size = N
        self.user_events :DefaultDict[str,List[Any]]= defaultdict(list)

    def record(self,user_id:str,timestamp:int)->None:
        bisect.insort_left(self.user_events[user_id],timestamp)
    
    def window_cleanup(self,user_id:str,cutoff:int)->None:
        if cutoff > 0:
            del self.user_events[user_id][:cutoff]
    
    def count(self,user_id:str,timestamp:int)->int:
        if user_id not in self.user_events:
            return 0
        window_start_idx = bisect.bisect_left(self.user_events[user_id],timestamp - self.window_size)
        window_end_idx = bisect.bisect_right(self.user_events[user_id],timestamp)
        window_count = window_end_idx - window_start_idx
        self.window_cleanup(user_id,window_start_idx)
        return window_count

        




                    

if __name__=="__main__":
    logs = [
    {"user_id": 101, "event": "click", "timestamp": "2024-01-15 08:23:11"},
    {"user_id": 102, "event": "view",  "timestamp": "2024-01-15 08:24:05"},
    {"user_id": 101, "event": "view",  "timestamp": "2024-01-15 08:25:30"},
    {"user_id": 103, "event": "click", "timestamp": "2024-01-15 08:26:00"},
    {"user_id": 101, "event": "click", "timestamp": "2024-01-15 08:27:45"},
    {"user_id": 102, "event": "click", "timestamp": "2024-01-15 08:28:10"},
    ]
    event_counts = count_events_def_dict(logs)
    print(event_counts)
    csv_reader= read_csv('csv_sample.txt')
    input_list=[]
    for line in csv_reader:
        input_list.append(line)
    process_csv_files = build_pipeline([])
    cleaned_data = process_csv_files(input_list)
    print(cleaned_data)