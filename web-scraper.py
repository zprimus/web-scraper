# create json file with all police departments in US

from selenium import webdriver
import json
import time

url = 'https://en.wikipedia.org/wiki/List_of_United_States_state_and_local_law_enforcement_agencies'

def format_json(agencyName, agencyLocation, agencyType):
    jsonFormat = ',{"name":"' + str(agencyName) + '","location":"' + str(agencyLocation) + '","type":"' + str(agencyType) + '","rating":0.0}'

    return(jsonFormat)

######### Main ########
browser = webdriver.Firefox()
browser2 = webdriver.Firefox()
browser.get(url)

elementState = browser.find_elements_by_tag_name('li')

jsonData = ''

randomIndex = 0

for i in elementState:
    try:
        if(i.text[0:35] == 'List of law enforcement agencies in'):
            #randomIndex += 1
            # get name of state
            stateName = i.text
            if(stateName != 'List of law enforcement agencies in the District of Columbia'):
                newStateName = stateName.replace('List of law enforcement agencies in ', '')
            else:
                newStateName = stateName.replace('List of law enforcement agencies in the ', '')
            
            # open link to list of agencies in state
            elementLinkState = i.find_element_by_tag_name('a')
            hrefState = elementLinkState.get_property('href')
            browser2.get(hrefState)

            # look for agency names in new browser
            elementAgencies = browser2.find_elements_by_tag_name('li')
            
            for j in elementAgencies:
                try:
                    elementAgency = j.find_element_by_tag_name('a')
                    if(elementAgency.get_property('title') != ('' or 'Jump Up')):
                        if(j.text[0] == ('^') or j.text[0].isnumeric() or len(j.text) < 2):
                            continue
                        if(str(j.text[0:4]) == 'Talk' or str(j.text[0:4]) == 'List'):
                            break

                        agencyName = j.text
                        newAgencyName = agencyName
                        
                        if(newAgencyName.find(' (') != -1):
                            newAgencyName = newAgencyName.split(' (', 1)[0]

                        if(newAgencyName.find(', founded') != -1):
                            newAgencyName = newAgencyName.split(', founded', 1)[0]
                        
                        if(newAgencyName.find('[') != -1):
                            newAgencyName = newAgencyName.split('[', 1)[0]

                        if(newAgencyName.find(' "') != -1):
                            newAgencyName = newAgencyName.split(' "', 1)[0]
                        
                        if(newAgencyName.find('\n') != -1):
                            newAgencyName = newAgencyName.split('\n', 1)[0]

                        if(newAgencyName == 'Law enforcement in the United States'):
                            break
                        if(newAgencyName == 'Federal law enforcement in the United States'):
                            break

                        jsonString = format_json(newAgencyName, newStateName, '')
                        jsonData += jsonString
                except:
                    continue
            #if(randomIndex == 20):
                #break
    except:
        continue

# export to file
try:
    jsonData = jsonData.split(',', 1)[1]
    jsonData = '[' + jsonData + ']'

    jsonObject = json.loads(jsonData, strict=False)

    jsonFormattedString = json.dumps(jsonObject, indent=2)

    text_file = open("agency_list.json", "w")
    text_file.write(jsonFormattedString)
    text_file.close()
except Exception as e:
    print(e)

browser.close()
browser2.close()