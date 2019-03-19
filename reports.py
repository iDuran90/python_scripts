import csv
import yaml

with open('report_data.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    gameElements = {}
    for row in csv_reader:
        if line_count != 0:
            yamlNotes = yaml.safe_load(row[3])
            if type(yamlNotes) is dict:
                if 'Research Question' in yamlNotes and yamlNotes['Research Question'] != None:
                    elements = yamlNotes['Research Question'][0]['Elements']
                    if type(elements) is list:
                        for element in elements:
                            if element in gameElements:
                                gameElements[element] += 1
                            else:
                                gameElements[element] = 1
        line_count += 1
    gameKeys = list(gameElements.keys())
    gameKeys.sort()
    for gameElement in gameKeys:
        print(gameElement)
        # print(str(gameElement) +': ' + str(gameElements[gameElement]))

gameElementsConvention = {
    'Grammar Skill': []
}
