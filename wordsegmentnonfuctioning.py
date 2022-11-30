# this doesn't work at the monent but am trying to find a solution.

import wordsegment as ws
import re
ws.load()
inputtext = input("Enter text to space:") # gets text from user
cleantext = ws.clean(inputtext)
textlist = ws.segment('spamihatespam')
endtext = re.sub(r"(@\[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", "", textlist) # cleans out commas from list

# List
messages = [textlist]
print(textlist)
# Print outputs
for message in messages:
  print("\nOld text: ")
  print(f'{message}')
  print("\nNew text: ")
  print(f'{endtext}\n')


