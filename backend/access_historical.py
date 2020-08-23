import datetime
import os
import matplotlib.pyplot as plt
import numpy as np

path_to_data_dir = "../data"
path_to_historical_data_dir = "../data/historical"
path_to_live_data_file = "../data/live.csv"
historical_columns = ["date", "county", "state", "fips", "cases", "deaths"]
live_columns = ["date", "county", "state", "fips", "cases", "deaths", "confirmed_cases", "confirmed_deaths", "probable_cases", "probable_deaths"]

FORMAT_STRING = "%Y-%m-%d"

class HistoricalDataAccessor:
    def __init__(self):
        self.historical_data = {}

    def build(self):
        files = os.listdir(path_to_historical_data_dir)

        date_index = historical_columns.index("date")
        county_index = historical_columns.index("county")
        state_index = historical_columns.index("state")
        fips_index = historical_columns.index("fips")
        cases_index = historical_columns.index("cases")
        deaths_index = historical_columns.index("deaths")

        counties_added = 0

        # We set up our dictionary to hold the following key-value pairs:
        # <fips> (as a string) : {"county" : <county name>, "state" : <state>, "data" : {date: (cases, deaths) (for all dates in our data set)} }
        for filename in files:
            # Each file is of the form <date>.csv; we get rid of the .csv part
            i = 0
            while filename[i] != ".":
                i += 1
            date = filename[0:i]

            file = open(path_to_historical_data_dir + "/" + filename, "r")
            for line in file:
                data = line.strip().split(",")
                fips = data[fips_index]

                # It's possible that we have some data that cannot be assigned to a particular county. We identify this
                # by observing an empty string for the fips
                if len(fips) == 0:
                    continue

                # Haven't seen the county before
                if fips not in self.historical_data:
                    counties_added += 1
                    state = data[state_index]
                    self.historical_data[fips] = {"county": data[county_index], "state" : state, "data": {}}

                self.historical_data[fips]["data"][data[date_index]] = (
                        int(data[cases_index]), int(data[deaths_index]))

        date_index = live_columns.index("date")
        county_index = live_columns.index("county")
        state_index = live_columns.index("state")
        fips_index = live_columns.index("fips")
        cases_index = live_columns.index("cases")
        deaths_index = live_columns.index("deaths")

        file = open(path_to_live_data_file, "r")
        for line in file:
            data = line.strip().split(",")
            fips = data[fips_index]

            # Throw away the first line giving column headers and any lines that have no fips (sometimes happens for
            # data logged under "Unknown" county)
            if fips == "fips" or len(fips) == 0:
                continue

            if fips not in self.historical_data:
                counties_added += 1
                self.historical_data[fips] = {"county": data[county_index], "state" : data[state_index], "data": {}}

            try:
                self.historical_data[fips]["data"][data[date_index]] = (
                    int(data[cases_index]), int(data[deaths_index]))
            except ValueError:
                continue

        print(f"Total Counties: {counties_added}")
        now = datetime.datetime.now()
        beginning = datetime.datetime(2020, 1, 21)
        for fips in self.historical_data:
            date = datetime.datetime(2020, 1, 21)

            while date < now:
                key = date.strftime(FORMAT_STRING)
                if key not in self.historical_data[fips]["data"]:
                    if date - datetime.timedelta(1) < beginning:
                        self.historical_data[fips]["data"][key] = (0, 0)
                    else:
                        self.historical_data[fips]["data"][key] = (self.historical_data[fips]["data"][(date - datetime.timedelta(1)).strftime(FORMAT_STRING)][0], self.historical_data[fips]["data"][(date - datetime.timedelta(1)).strftime("%Y-%m-%d")][1])
                date = date + datetime.timedelta(1)

    def total_day(self, cases: bool):
        if cases:
            file = open(path_to_data_dir + "/" + "total_day_cases.csv", "w")
            file.write("fips,cases\n")
        else:
            file = open(path_to_data_dir + "/" + "total_day_deaths.csv", "w")
            file.write("fips,deaths\n")

        now = datetime.datetime.now()
        today = datetime.datetime(2020, 8, 21)
        prev = today - datetime.timedelta(1)
        for fips in self.historical_data:
            if cases:
                prev_val = self.historical_data[fips]["data"][prev.strftime(FORMAT_STRING)][0]
                val = self.historical_data[fips]["data"][today.strftime(FORMAT_STRING)][0]
            else:
                prev_val = self.historical_data[fips]["data"][prev.strftime(FORMAT_STRING)][1]
                val = self.historical_data[fips]["data"][today.strftime(FORMAT_STRING)][1]

            file.write(fips + "," + str(val - prev_val) + "\n")

        file.close()

    def total_week(self, cases: bool):
        if cases:
            file = open(path_to_data_dir + "/" + "total_week_cases.csv", "w")
            file.write("fips,cases\n")
        else:
            file = open(path_to_data_dir + "/" + "total_week_deaths.csv", "w")
            file.write("fips,deaths\n")

        now = datetime.datetime.now()
        today = datetime.datetime(now.year, now.month, now.day)
        for fips in self.historical_data:
            prev = today - datetime.timedelta(7)

            if cases:
                prev_val = self.historical_data[fips]["data"][prev.strftime(FORMAT_STRING)][0]
                val = self.historical_data[fips]["data"][today.strftime(FORMAT_STRING)][0]
            else:
                prev_val = self.historical_data[fips]["data"][prev.strftime(FORMAT_STRING)][1]
                val = self.historical_data[fips]["data"][today.strftime(FORMAT_STRING)][1]

            total_added = val - prev_val
            file.write(fips + "," + str(total_added) + "\n")

        file.close()

    def total_month(self, cases: bool):
        if cases:
            file = open(path_to_data_dir + "/" + "total_month_cases.csv", "w")
            file.write("fips,cases\n")
        else:
            file = open(path_to_data_dir + "/" + "total_month_deaths.csv", "w")
            file.write("fips,deaths\n")

        now = datetime.datetime.now()
        today = datetime.datetime(now.year, now.month, now.day)
        for fips in self.historical_data:
            prev = datetime.datetime(today.year, today.month - 1, today.day-1)

            if cases:
                prev_val = self.historical_data[fips]["data"][prev.strftime(FORMAT_STRING)][0]
                val = self.historical_data[fips]["data"][today.strftime(FORMAT_STRING)][0]
            else:
                prev_val = self.historical_data[fips]["data"][prev.strftime(FORMAT_STRING)][1]
                val = self.historical_data[fips]["data"][today.strftime(FORMAT_STRING)][1]

            total_added = val - prev_val
            file.write(fips + "," + str(total_added) + "\n")

        file.close()

    def total_total(self, cases: bool):
        if cases:
            file = open(path_to_data_dir + "/" + "total_total_cases.csv", "w")
            file.write("fips,cases\n")
        else:
            file = open(path_to_data_dir + "/" + "total_total_deaths.csv", "w")
            file.write("fips,deaths\n")

        now = datetime.datetime.now()
        today = datetime.datetime(now.year, now.month, now.day)
        for fips in self.historical_data:
            if cases:
                file.write(fips + "," + str(self.historical_data[fips]["data"][today.strftime(FORMAT_STRING)][0]) + "\n")
            else:
                file.write(fips + "," + str(self.historical_data[fips]["data"][today.strftime(FORMAT_STRING)][1]) + "\n")

    def getKeyMetrics(self, county, state):
        """
        Given the specified county (we need state because county names are not unique, nationally), return a list with
        the following data:
        [All-time cases, All-time deaths, Daily new cases, Daily new deaths, Weekly new cases, Weekly new deaths, New
        cases in last 30 days, Deaths in last 30 days]

        Returns an empty list if the specified county can't be found.
        """
        data = {}
        for fips in self.historical_data:
            if self.historical_data[fips]["county"] == county and self.historical_data[fips]["state"] == state:
                data = self.historical_data[fips]["data"]
                break

        if not data:
            return []

        now = datetime.datetime.now()
        today = datetime.datetime(now.year, now.month, 21)
        daily_prev = today - datetime.timedelta(1)
        weekly_prev = today - datetime.timedelta(7)
        thirty_day_prev = today - datetime.timedelta(30)

        metrics = []

        metrics.append(data[today.strftime(FORMAT_STRING)][0])
        metrics.append(data[today.strftime(FORMAT_STRING)][1])

        cases_today = data[today.strftime(FORMAT_STRING)][0]
        deaths_today = data[today.strftime(FORMAT_STRING)][1]

        daily_cases_prev = data[daily_prev.strftime(FORMAT_STRING)][0]
        daily_deaths_prev = data[daily_prev.strftime(FORMAT_STRING)][1]

        weekly_cases_prev = data[weekly_prev.strftime(FORMAT_STRING)][0]
        weekly_deaths_prev = data[weekly_prev.strftime(FORMAT_STRING)][1]

        thirty_day_cases_prev = data[thirty_day_prev.strftime(FORMAT_STRING)][0]
        thirty_day_deaths_prev = data[thirty_day_prev.strftime(FORMAT_STRING)][1]

        metrics.extend([cases_today - daily_cases_prev, deaths_today - daily_deaths_prev])
        metrics.extend([cases_today - weekly_cases_prev, deaths_today - weekly_deaths_prev])
        metrics.extend([cases_today - thirty_day_cases_prev, deaths_today - thirty_day_deaths_prev])

        return metrics

    def create_graph(self, county, state, n):
        """
        Creates and saves as a .png a graph displaying the last n days of new cases, including today.

        The saved file is called "<n>_days_graph.png" and is located in the same directory that the program calling this
        method is running in. This filename is returned.
        """
        data = {}
        for fips in self.historical_data:
            if self.historical_data[fips]["county"] == county and self.historical_data[fips]["state"] == state:
                data = self.historical_data[fips]["data"]
                break

        if not data:
            print(f"Couldn't create graph for {county}, {state} because not valid combination")
            return ""

        now = datetime.datetime.now()
        today = datetime.datetime(now.year, now.month, 21)
        date = today - datetime.timedelta(n-1)
        prev = date - datetime.timedelta(1)

        days = []
        vals = []
        while date <= today:
            days.append(date.strftime("%m/%d"))
            vals.append(data[date.strftime(FORMAT_STRING)][0] - data[prev.strftime(FORMAT_STRING)][0])

            date = date + datetime.timedelta(1)
            prev = prev + datetime.timedelta(1)

        x_pos = np.arange(len(days))
        plt.figure(figsize=(10, 7))
        plt.style.use('Solarize_Light2')
        plt.bar(x_pos, vals, color="#CF95D4")
        plt.ylabel("New Cases")
        plt.title(f"New Cases in the Last {n} days")
        plt.xticks(x_pos, [])
        plt.savefig(f"{n}_days_graph.png")
        return f"{n}_days_graph.png"

    def create_all_time_graph(self, county, state):
        """
        Creates and saves as a .png a graph displaying new case data since the beginning of the pandemic, January 21st.

        The saved file is called "all_time_graph.png" and is located in the same directory that the program calling this
        method is running in. This filename is returned.
        """
        data = {}
        for fips in self.historical_data:
            if self.historical_data[fips]["county"] == county and self.historical_data[fips]["state"] == state:
                data = self.historical_data[fips]["data"]
                break

        if not data:
            print(f"Coudln't create graph for {county}, {state} because not valid combination")
            return ""

        now = datetime.datetime.now()
        today = datetime.datetime(now.year, now.month, 21)
        date = datetime.datetime(now.year, 1, 22)
        prev = date - datetime.timedelta(1)

        days = []
        vals = []
        while date <= today:
            days.append(date.strftime("%m/%d"))
            vals.append(data[date.strftime(FORMAT_STRING)][0] - data[prev.strftime(FORMAT_STRING)][0])

            date = date + datetime.timedelta(1)
            prev = prev + datetime.timedelta(1)

        x_pos = np.arange(len(days))
        plt.figure(figsize=(10, 7))
        plt.style.use('Solarize_Light2')
        plt.plot(x_pos, vals, color="#CF95D4")
        plt.ylabel("New Cases")
        plt.title("New Cases All-Time")
        plt.xticks(x_pos, [])
        plt.savefig("all_time_graph.png")
        return "all_time_graph.png"

    def get_graphs(self, county, state):
        """
        Returns the following list:
        [Weekly Graph, Monthly Graph, All-Time Graph]

        """
        return [self.create_graph(county, state, 7), self.create_graph(county, state, 30), self.create_all_time_graph(county, state)]

if __name__ == "__main__":
    acc = HistoricalDataAccessor()
    acc.build()

    bools = [True, False]
    for boolean in bools:
        acc.total_day(boolean)
        acc.total_week(boolean)
        acc.total_month(boolean)
        acc.total_total(boolean)

    acc.get_graphs("Monterey", "California")
