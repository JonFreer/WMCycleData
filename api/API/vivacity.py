import datetime

import requests


class Vivacity:
    # Call and return the json from the Vivacity API
    def get_results(api_key, start_time, end_time, identity):
        if identity == None:
            response = requests.get(
                "https://tfwm.onl/vivacity_counts.json?ApiKey={}&earliest={}&period=hour&EndPeriod=hour&meta=true".format(
                    api_key, start_time
                )
            )
        else:
            response = requests.get(
                    "https://tfwm.onl/vivacity_counts.json?ApiKey={}&earliest={}&period=hour&EndPeriod=hour&meta=true&identity={}".format(
                    api_key, start_time, identity
                )
            )
        response.raise_for_status()
        return response.json()

    def filter_results(results: dict):
        counters = {}
        out = []
        records = results.get("Vivacity", {}).get("kids", {})

        # Iterate over values and filter out any where the Start, Centre and End values are None
        # Store the output for a given time in a dict
        for value in records.values():
            data = value["kids"]
            if not data:
                continue

            location = data.get("Location", {}).get("kids", {})
            valid_location = location.get("Centre") is not None

            if not valid_location:
                continue

            date_string = data.get("Date").get("value")
            count_in = data.get("CountIn")
            count_out = data.get("CountOut")

            out.append(
                {
                    "timestamp": datetime.datetime.strptime(
                        date_string, "%Y-%m-%d %H"
                    ),
                    "counts": {"In":count_in,"Out" : count_out},
                    "mode": data.get("Class", {}),
                    "identity": data.get("Identity", {}),
                }
            )

            counters[int(data.get("Identity", {}))] =  data.get("Location", {}).get("kids", {}).get("Centre", {})
        return out, counters

    def get_counts(api_key, delta_t, identity=None):
        time = int(datetime.datetime.now().timestamp()) - delta_t
        results = Vivacity.get_results(api_key, time, "now", identity)
        filtered_results, counters = Vivacity.filter_results(results)
        return filtered_results, counters
