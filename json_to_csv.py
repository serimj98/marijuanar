import json
import csv
import os

def recursively_add_title(start, D, result):
    for key, val in D.items():
        if(isinstance(val, dict)):
            recursively_add_title(start+str(key)+"/", val, result)
        else:
            result.add(start+str(key))
    return result

dir_name = '.'
targets = dict()

for root, dirs, files in os.walk(dir_name, topdown=False):
    for name in files:
        filename = os.path.join(root, name)

        # Get all the csv files (exclude tags.csv)
        if filename.endswith('.json'):
            if root not in targets:
                targets[root] = [filename]
            else:
                targets[root].append(filename)

for dirname, filename in targets.items():
    for file in filename:
        print file
        json_file = open(file, "r")
        target = json.load(json_file)
        if not isinstance(target, list):
            target = [target]

        csv_file = open(file.replace("json", "csv"), "w")
        writer = csv.writer(csv_file)


        titleRow = set()
        rows = []

        for i in range(len(target)):
            recursively_add_title("", target[i], titleRow)
            row = []
            for title in list(titleRow):
                title = title.split("/")
                if title[0] not in target[i]:
                    continue
                val = target[i][title[0]]
                for j in range(1, len(title)):
                    if title[j] not in val:
                        continue
                    val = val[title[j]]
                row.append(val)
            rows.append(row)

        writer.writerow(list(titleRow))
        writer.writerows(rows)