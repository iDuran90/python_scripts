import csv
import yaml
from elements_categories import gameElementsConvention, validationElementsConvention, resultsElementsConvention
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

def homogenizeArticlesElements(articles, key, conventions):
  conventionKeys = conventions.keys()
  articlesHomogenized = []
  for article in articles:
    articleHomogenized = {
      key: []
    }
    if type(article[key]) is list:
      for element in article[key]:
        if type(element) is dict:
          element = list(element.keys())[0]
        if element in conventionKeys:
          articleHomogenized[key].append(element)
        else:
          for elementKey in conventionKeys:
            if element in conventions[elementKey]:
              articleHomogenized[key].append(elementKey)
    articlesHomogenized.append(articleHomogenized)

  return articlesHomogenized

def getElementsUniqueFrequency(articles, key):
  count = {}
  for article in articles:
    for element in article[key]:
      if element in count:
        count[element] += 1
      else:
        count[element] = 1

  return sorted(count.items(), key=lambda kv: kv[1], reverse=True)

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

def getArticlesKeysByAttr(articles, attr):
  validationMethods = {}
  for article in articles:
    if type(article[attr]) is list:
      for element in article[attr]:
        if type(element) is dict:
          element = list(element.keys())[0]
        if element != False:
          if element in validationMethods:
            validationMethods[element] += 1
          else:
            validationMethods[element] = 1

  return sorted(validationMethods.items(), key=lambda kv: kv[1], reverse=True)

articles = loadArticles()

# Lines for elements
# articles = homogenizeArticlesElements(articles)
# elementsCount = getElementsUniqueFrequency(articles)
# # getElementsCountWithCategories(elementsCount)
# articles = getArticlesWithElementsRecombinated(articles, 'Gaming')

# combinationsCounted = getElementsCombinedFrequency(articles)
# combinationsCountedAndSorted = sorted(combinationsCounted.items(), key=lambda kv: kv[1], reverse=True)
# for key, value in combinationsCountedAndSorted:
#   print(key + '\t' + str(value))

# For validation methods
# for key, value in getArticlesKeysByAttr(articles, "validation"):
#   print(key + '\t' + str(value))
articles = homogenizeArticlesElements(articles, "results", resultsElementsConvention)
for key, value in getElementsUniqueFrequency(articles, "results"):
   print(key + '\t' + str(value))

# For results methods
# for key, value in getArticlesKeysByAttr(articles, "results"):
#   print(key + '\t' + str(value))
