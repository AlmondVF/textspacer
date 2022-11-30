# Imports
import re
import numpy as np
from wordfreq import get_frequency_dict

# Variables
word_prob = get_frequency_dict(lang='en', wordlist='large')
max_word_len = max(map(len, word_prob))  # 34

# Text cleaning
inputtext = input("Enter text to space:") # gets text from user
despacedtext = inputtext.replace(" ","")
lowercasetext = despacedtext.lower() # makes it all lowercase
cleantext = re.sub(r"(@\[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", "", lowercasetext) # cleans out any non ASCII/letter characters :D

# Subroutine for something (viterbi algorithm) 
def viterbi_segment(text, debug=False):
  probs, lasts = [1.0], [0]
  for i in range(1, len(text) + 1):
    new_probs = []
    for j in range(max(0, i - max_word_len), i):
      substring = text[j:i]
      length_reward = np.exp(len(substring))
      freq = word_prob.get(substring, 0) * length_reward
      compounded_prob = probs[j] * freq
      new_probs.append((compounded_prob, j))

      if debug:
        print(f'[{j}:{i}] = "{text[lasts[j]:j]} & {substring}" = ({probs[j]:.8f} & {freq:.8f}) = {compounded_prob:.8f}')

    prob_k, k = max(new_probs)  # max of a touple is the max across the first elements, which is the max of the compounded probabilities
    probs.append(prob_k)
    lasts.append(k)

    if debug:
      print(f'i = {i}, prob_k = {prob_k:.8f}, k = {k}, ({text[k:i]})\n')

  # when text is a word that doesn't exist, the algorithm breaks it into individual letters.
  # in that case, return the original word instead
  if len(set(lasts)) == len(text):
    return text

  words = []
  k = len(text)
  while 0 < k:
    word = text[lasts[k]:k]
    words.append(word)
    k = lasts[k]
  words.reverse()
  return ' '.join(words)


# Subroutine for splitting words
def split_message(message):
  new_message = ' '.join(viterbi_segment(wordmash, debug=False) for wordmash in message.split())
  return new_message

# List
messages = [cleantext]

# Print outputs
for message in messages:
  print("\nInput text: ")
  print(f'{inputtext}')
  print("\nClean text: ")
  print(f'{message}')
  print("\nSpaced text: ")
  new_message = split_message(message)
  print(f'{new_message}\n')