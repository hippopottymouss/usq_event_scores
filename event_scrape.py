import re
import urllib.request
import string
import csv
from bs4 import BeautifulSoup
import os



list_of_dates = ['201709', '201710', '201711', '201712', '201801', '201802', '201803']

list_of_urls = []

for date in list_of_dates:
  url = 'https://www.usquidditch.org/events/calendar/{}'.format(date)
  list_of_urls.append(url)


# print(list_of_urls)

# ^ got a list of calendar urls per month
# now we need to get links to events in each month



# We're gonna define this whole thing below if it works

all_event_ids = []


def geturlsyo(url):
  url_date = url


  # differentiate based on color

  response = urllib.request.urlopen(url_date)

  html = response.read().decode('utf-8')




  resultblock = re.search(r"</div>\s<h2>([^>]*(?:.|\n)*?)<div\sid=\"sidebar_white\">\s<h4>Event Types</h4>", html, re.IGNORECASE)



  if resultblock:
      results = resultblock.group(1)

  file = open('/Users/Work/Desktop/src/usq_eventscrape/every_event_url_test_results.txt','w')
  file.write(results)
  file.close()


  file = open('/Users/Work/Desktop/src/usq_eventscrape/every_event_url_test_results.txt','r')
  soup = BeautifulSoup(file, 'html.parser')


  list_of_events = []
  list_of_eventtype = []


  links = soup.find_all('div', {"class": "event"})
  for a in links:
    href = a['href']
    list_of_events.append(href)


  links2 = soup.find_all('div', {"class": "calendar_box"})
  for a in links2:
    style = a['style']
    list_of_eventtype.append(style)




  list_of_event_ids = []

  for url in list_of_events:
    resultblock = re.findall(r"/events/view/(.*)", url)
    list_of_event_ids.extend(resultblock)


  # GOT IT!!!!! @ list_of_event_ids


  list_of_event_typeids = []

  for url in list_of_eventtype:
    resultblock = re.findall(r"background-color:(.*)", url)
    list_of_event_typeids.extend(resultblock)




  # event_name_and_type = dict(zip(list_of_event_ids, list_of_event_typeids))

  event_name_and_type = {key:value for key, value in zip(list_of_event_ids, list_of_event_typeids)}







  # remove all unofficial events out of list

  # for event,typey in event_name_and_type.items():
  #     if typey == '#1b996a':
  #        del event_name_and_type[event]


  event_name_and_type = { event : typey for event,typey in event_name_and_type.items() if typey != '#1b996a'}
  event_name_and_type = { event : typey for event,typey in event_name_and_type.items() if typey != '#cb7005'}
  event_name_and_type = { event : typey for event,typey in event_name_and_type.items() if event != 'canceled'}


  all_event_ids.extend(event_name_and_type)




for url in list_of_urls:
  geturlsyo(url)


# print(all_event_ids)



# now all the event ids are under all_event_ids






"""








NOW We'll be working on getting data from each url we got above:

















"""





def add_to_csv(eventid):
  urlsource = 'https://www.usquidditch.org/events/view/{}'.format(eventid)


  # /Users/Work/Desktop/src/usq_eventscrape/event_scores_scrape.py

  # urlsource = 'https://www.usquidditch.org/events/view/great-lakes-regional-championship-2017'


  # get url id for tournament

  tournament_id = re.findall('http[s]?://www\.usquidditch\.org/events/view/(.*)', urlsource)
  tournament_id = (tournament_id[0])




  response = urllib.request.urlopen(urlsource)
  # event id after view/








  html = response.read().decode('utf-8')

  # THIS CODE WORKS!!!! Make sure to change url and check test_jawn

  # nyu_scores = open('/Users/Work/Desktop/src/nyuresults.rtf', 'r').read()

  # print(html)




  resultblock = re.search(r"<table>([^>]*(?:.|\n)*?)<\/table>", html, re.IGNORECASE)





  if resultblock:
    results = resultblock.group(1)

  file = open('/Users/Work/Desktop/src/usq_eventscrape/test_results.txt','w')
  file.write(results)
  file.close()


  nyu_res = open('/Users/Work/Desktop/src/usq_eventscrape/test_results.txt', 'r').read()
  #set path

  block_list = re.findall(r"<tr>\s*<td>(\d\d\d\d-\d\d-\d\d)&nbsp;\s*</td>\s*<td>\s*([^<]+)&nbsp;\s*</td>\s*<td>(\d*\W*)&nbsp;-&nbsp;(\d*\W*)&nbsp;</td>\s*<td>([^<]+)&nbsp;</td>\s*<td>(\d\d:\d\d:\d\d)&nbsp;(\(\S*\)*)*&nbsp;</td>\s*</tr>", nyu_res)



  file = open('/Users/Work/Desktop/src/usq_eventscrape/test_jawn.txt','w')
  for block in block_list:
  #', '.join(block)
  #block = block.replace('(', '')
  #block = block.replace(')', '\n')
    file.write(str(block))
    #file.replace('(', '')
    #file.replace(')', '\n')

  file.close()

  # replace OT and 2OT with no parenthesis version

  replacements = {'(OT)':'OT', '(2OT)':'2OT', 'Miami University (OH) Quidditch':'Miami University OH Quidditch'}

  with open('/Users/Work/Desktop/src/usq_eventscrape/test_jawn.txt') as infile, open('/Users/Work/Desktop/src/usq_eventscrape/test_jawn_modified.txt', 'w') as outfile:
      for line in infile:
          for src, target in replacements.items():
              line = line.replace(src, target)
          outfile.write(line)

  outfile.close





  with open('/Users/Work/Desktop/src/usq_eventscrape/test_jawn_modified.txt','r') as myfile:
    data=myfile.read().replace('(', '', 1).replace(')(', '\n').replace(')', '', 1)
    # data=myfile.read().replace('(', '').replace(')', '\n')
    # ^ problem with this: Miami Quidditch (OH) gets triggered


  file = open('/Users/Work/Desktop/src/usq_eventscrape/test_csv.csv','w')
  file.write(str(data))


  file.close()


# v = open('/Users/Work/Desktop/src/usq_eventscrape/test_csv.csv')
# r = csv.reader(v)
# row0 = next(r)
# row0.append(tournament_id)
# for item in r:
#   item.append(tournament_id)







  if os.stat('/Users/Work/Desktop/src/usq_eventscrape/test_csv.csv').st_size > 0:
    with open('/Users/Work/Desktop/src/usq_eventscrape/test_csv.csv','r') as csvinput:
        with open('/Users/Work/Desktop/src/usq_eventscrape/test_csv_complete.csv', 'w') as csvoutput:
            writer = csv.writer(csvoutput, lineterminator='\n')
            reader = csv.reader(csvinput)

            all = []
            row = next(reader)
            row.append(tournament_id)
            all.append(row)

            for row in reader:
              row.append(tournament_id)
              all.append(row)

            writer.writerows(all)

    csvoutput.close()



    with open('/Users/Work/Desktop/src/usq_eventscrape/test_csv_complete.csv','r') as csvinput:
      with open('/Users/Work/Desktop/src/usq_eventscrape/test_csv_ALL.csv', 'a') as csvoutput:
        writer = csv.writer(csvoutput, lineterminator='\n')
        reader = csv.reader(csvinput)

        writer.writerows(all)

    csvoutput.close()

    os.remove('/Users/Work/Desktop/src/usq_eventscrape/test_csv.csv')
    os.remove('/Users/Work/Desktop/src/usq_eventscrape/test_csv_complete.csv')

  else:
    print("No File")


# THIS CODE WORKS!!!! Make sure to change url and check test_jawn




for event in all_event_ids:
  add_to_csv(event)


!gzip -f /Users/Work/Desktop/src/usq_eventscrape/test_csv_ALL.csv




import pandas as pd
import datetime
scores = pd.read_csv("test_csv_ALL.csv.gz", 
                          encoding='utf_8', 
                          dtype = 'unicode',
                          parse_dates = True,
                          infer_datetime_format = True, header = None)

date = "Date"
team_a_name = "Team_A_Name"
team_a_score = "Team_A_Score"
team_b_score = "Team_B_Score"
team_b_name = "Team_B_Name"
time = "Time"
ot = "Overtime_Required"
tournament = "Tournament_Name"




scores.columns = [date, team_a_name, team_a_score, team_b_score, team_b_name, time, ot, tournament]

scores["Date"]=pd.to_datetime(scores["Date"])



scores["Time"] = pd.to_datetime(scores["Time"], format=" \'%H:%M:%S\'")

scores["Time"] = pd.Series([val.time() for val in scores["Time"]])


# scores will now show you every score from every official game recorded

