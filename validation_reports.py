import csv
import yaml
from elements_categories import gameElementsConvention
from categories import categoriesConvention

def loadArticles():
  with open('slr_report_data.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    articles = []
    line_count = 0
    for row in csv_reader:
      if line_count != 0:
        if row[2] == 'INC':
          yamlNotes = yaml.safe_load(row[1])
          articles.append({
            "elements": yamlNotes['Research Question'][0]['Elements'],
            "validation": yamlNotes['Research Question'][1]['Validation'],
            "results": yamlNotes['Research Question'][2]['Results']
          })

      line_count += 1

    return articles

def homogenizeArticlesElements(articles):
  gameElementsConventionKeys = gameElementsConvention.keys()
  articlesHomogenized = []
  for article in articles:
    articleHomogenized = {
      "elements": []
    }
    if type(article["elements"]) is list:
      for element in article["elements"]:
        if element in gameElementsConventionKeys:
          articleHomogenized["elements"].append(element)
        else:
          for elementKey in gameElementsConventionKeys:
            if element in gameElementsConvention[elementKey]:
              articleHomogenized["elements"].append(elementKey)
    articlesHomogenized.append(articleHomogenized)

  return articlesHomogenized

def getElementsUniqueFrequency(articles):
  gameElements = {}
  for article in articles:
    for element in article["elements"]:
      if element in gameElements:
        gameElements[element] += 1
      else:
        gameElements[element] = 1

  return (gameElements)

def getElementsCountWithCategories(elements):
  elementsCategorized = []
  for element in elements.keys():
    for category in categoriesConvention.keys():
      if element in categoriesConvention[category]:
        elementsCategorized.append({
          "element": element,
          "category": category,
          "count": elements[element]
        })
  
  elementsCategorized.sort(reverse=True, key=lambda element: element["count"])
  for element in elementsCategorized:
    print(element["category"] + '\t' + element["element"] + '\t' + str(element["count"]))

def getArticlesWithElementsRecombinated(articles, byCategory):
  newArticles = []
  for article in articles:
    elements = list(set(article["elements"]))
    elements.sort()

    if byCategory != None:
      elements = list(filter(lambda x: x in categoriesConvention[byCategory], elements))

    combinations = []
    
    for pivot in elements:
      listClone = list(elements)
      listClone.remove(pivot)
      combinationLevel = len(elements)

      for i in range(1, combinationLevel):
        for idx, item in enumerate(listClone):
          if i == 1:
            temp = [pivot, item]
            temp.sort()
            combinations.append(", ".join([*temp]))
          else:
            temp = [pivot, *listClone[idx:idx+i]]
            temp.sort()
            combinations.append(", ".join([*temp]))

    
    # print(*sort_and_deduplicate(combinations), sep='\n')
    
    newArticles.append({
      **articles[0],
      "combinations": sort_and_deduplicate(combinations)
    })

  return newArticles

def uniq(lst):
    last = object()
    for item in lst:
        if item == last:
            continue
        yield item
        last = item

def sort_and_deduplicate(l):
    return list(uniq(sorted(l)))

def getElementsCombinedFrequency(articles):
  combinations = {}
  for article in articles:
    for combination in article["combinations"]:
      if combination in combinations:
        combinations[combination] += 1
      else:
        combinations[combination] = 1

  return (combinations)

articles = loadArticles()
articles = homogenizeArticlesElements(articles)
elementsCount = getElementsUniqueFrequency(articles)
# getElementsCountWithCategories(elementsCount)
articles = getArticlesWithElementsRecombinated(articles, 'Gaming')

combinationsCounted = getElementsCombinedFrequency(articles)
combinationsCountedAndSorted = sorted(combinationsCounted.items(), key=lambda kv: kv[1], reverse=True)
for key, value in combinationsCountedAndSorted:
  print(key + '\t' + str(value))

# getElementsCombinedFrequencyByCategory()
