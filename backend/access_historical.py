import datetime
import os

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
        fips_index = historical_columns.index("fips")
        cases_index = historical_columns.index("cases")
        deaths_index = historical_columns.index("deaths")

        counties_added = 0

        # We set up our dictionary to hold the following key-value pairs:
        # <fips> (as a string) : {"county" : <county name>, "data" : {date: (cases, deaths) (for all dates in our data set)} }
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
                    self.historical_data[fips] = {"county": data[county_index], "data": {}}

                self.historical_data[fips]["data"][data[date_index]] = (
                        int(data[cases_index]), int(data[deaths_index]))

        date_index = live_columns.index("date")
        county_index = live_columns.index("county")
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
                self.historical_data[fips] = {"county": data[county_index], "data": {}}

            try:
                self.historical_data[fips]["data"][data[date_index]] = (
                    int(data[cases_index]), int(data[deaths_index]))
            except ValueError:
                print(f"One of \"{data[cases_index]}\" or \"{data[deaths_index]}\" couldn't be converted to int. Skipping,"
                      f"and will assume that values are the same as the day before")

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
        else:
            file = open(path_to_data_dir + "/" + "total_day_deaths.csv", "w")

        now = datetime.datetime.now()
        today = datetime.datetime(now.year, now.month, now.day)
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
        else:
            file = open(path_to_data_dir + "/" + "total_week_deaths.csv", "w")

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
        else:
            file = open(path_to_data_dir + "/" + "total_month_deaths.csv", "w")

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
        else:
            file = open(path_to_data_dir + "/" + "total_total_deaths.csv", "w")

        now = datetime.datetime.now()
        today = datetime.datetime(now.year, now.month, now.day)
        for fips in self.historical_data:
            if cases:
                file.write(fips + "," + str(self.historical_data[fips]["data"][today.strftime(FORMAT_STRING)][0]) + "\n")
            else:
                file.write(fips + "," + str(self.historical_data[fips]["data"][today.strftime(FORMAT_STRING)][1]) + "\n")


if __name__ == "__main__":
    acc = HistoricalDataAccessor()
    acc.build()

    bools = [True, False]
    for boolean in bools:
        acc.total_day(boolean)
        acc.total_week(boolean)
        acc.total_month(boolean)
        acc.total_total(boolean)
