import requests
import datetime
import json

class Vivacity:
    
    # Call and return the json from the Vivacity API
    def get_results(api_key,start_time, end_time, name,type):
        response = requests.get("https://tfwm.onl/vivacity.json?ApiKey={}&earliest={}&latest={}&name={}&class={}&NullDataPoints=false&to=1684840206".format(api_key,start_time,end_time,name,type))
        response.raise_for_status()
        return response.json()
    
    def filter_results(results: dict):

        out = {}
        records = results.get("Vivacity", {}).get("kids", {})
        
        # Iterate over values and filter out any where the Start, Centre and End values are None
        # Store the output for a given time in a dict
        for value in records.values():
            data = value["kids"]
            if not data:
                continue
            location = data.get("Location", {}).get("kids", {})
            valid_location = location and location.get("Start") is not None
            valid_location = valid_location and location.get("Centre") is not None
            valid_location = valid_location and location.get("End") is not None

            if not valid_location:
                continue

            date_string = data.get("Dates", {}).get("kids", {}).get("From")

            count = data.get("Counts", {}).get("kids", {})

            date_time = datetime.datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S') # Get Unix time

            out[date_time] = count

        return out
    
    def get_counts(name,api_key,type):
        results = Vivacity.get_results(api_key,"today","now",name,type)
        filtered_results = Vivacity.filter_results(results)
        return filtered_results
        
