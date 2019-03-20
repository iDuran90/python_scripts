import csv
import yaml
from elements_categories import gameElementsConvention

with open('report_data.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    gameElements = {}
    gameElementsConventionKeys = gameElementsConvention.keys()
    for row in csv_reader:
        if line_count != 0:
            yamlNotes = yaml.safe_load(row[3])
            if type(yamlNotes) is dict:
                if 'Research Question' in yamlNotes and yamlNotes['Research Question'] != None:
                    elements = yamlNotes['Research Question'][0]['Elements']
                    if type(elements) is list:
                        for element in elements:
                            if element in gameElementsConventionKeys:
                                if element in gameElements:
                                    gameElements[element] += 1
                                else:
                                    gameElements[element] = 1
                            else:
                                elementAdded = False
                                for elementKey in gameElementsConventionKeys:
                                    if element in gameElementsConvention[elementKey]:
                                        if elementKey in gameElements:
                                            elementAdded = True
                                            gameElements[elementKey] += 1
                                        else:
                                            elementAdded = True
                                            gameElements[elementKey] = 1
                                if not elementAdded:
                                    print('Elemento huerfano:' + str(element))
        line_count += 1
    print()

    sorted_by_value = sorted(gameElements.items(), key=lambda kv: kv[1])
    for key, value in reversed(sorted_by_value):
        print(key + '\t' + str(value))
