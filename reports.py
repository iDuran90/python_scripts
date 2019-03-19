import csv
import yaml

with open('report_data.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        elif line_count == 1:
            yamlNotes = yaml.safe_load(row[3])
            print(f'{yamlNotes}')
            print(f'{yamlNotes["Inclusion"]}')
            print(f'{yamlNotes["Exclusion"]}')
            print(f'{yamlNotes["Research Question"]}')
            line_count += 1
