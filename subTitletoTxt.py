"""
Creates readable text file from SRT file.
"""
import re, sys
from googletrans import Translator

srtFileName = "The.Mandalorian.S02E03.Chapter.11.The.Heiress.1080p.WEBRip.DDP5.1.Atmos.x264-MZABI.srt"
def is_time_stamp(l):
  if l[:2].isnumeric() and l[2] == ':':
    return True
  return False

def has_letters(line):
  if re.search('[a-zA-Z]', line):
    return True
  return False

def has_no_text(line):
  l = line.strip()
  if not len(l):
    return True
  if l.isnumeric():
    return True
  if is_time_stamp(l):
    return True
  if l[0] == '(' and l[-1] == ')':
    return True
  if not has_letters(line):
    return True
  return False

def is_lowercase_letter_or_comma(letter):
  if letter.isalpha() and letter.lower() == letter:
    return True
  if letter == ',':
    return True
  return False

def clean_up(lines):
  """
  Get rid of all non-text lines and
  try to combine text broken into multiple lines
  """
  global allWords
  new_lines = []
  for line in lines[1:]:
    if has_no_text(line):
      continue
    elif len(new_lines) and is_lowercase_letter_or_comma(line[0]):
      #combine with previous line
      new_lines[-1] = new_lines[-1].strip() + ' ' + line
    else:
      #append line
      lineSplitted = line.split(" ")
      newLineSplitted = []
      for word in lineSplitted:
        word = word.replace("<i>","")
        word = word.replace("</i>","")
        word = word.replace("\n","")
        newLineSplitted.append(word)
      allWords.extend(newLineSplitted)
      new_lines.append(line)
  print(len(allWords))
  return new_lines
  
allWords = []
def main(args):
  """
    args[1]: file name
    args[2]: encoding. Default: utf-8.
      - If you get a lot of [?]s replacing characters,
      - you probably need to change file_encoding to 'cp1252'
  """
  translator = Translator()
  file_name = "originalSub/" + srtFileName
  file_encoding = 'utf-8'
  with open(file_name, encoding=file_encoding, errors='replace') as f:
    lines = f.readlines()
    new_lines = clean_up(lines)
  new_file_name = srtFileName[:-4] + '.srt'
  tr = translator.translate(allWords[3], src ='he' , dest='en').text
  with open(new_file_name, 'w',encoding=file_encoding) as f:
    for line in lines:
      newText = "<font color=green dir=rtl>" + allWords[3] + "</font>"
      newText =  newText + "<font color=red dir=ltr>" + tr + "</font>"
      line = line.replace(allWords[3],newText)
      f.write(line)
  dbg_file_name ='words.txt'
  with open(dbg_file_name, 'w',encoding=file_encoding) as f:
    for word in allWords:
      f.write(word + "\n")
if __name__ == '__main__':
  main(sys.argv)

"""
NOTES
 * Run from command line as
 ** python srt_to_txt.py file_name.srt cp1252
 * Creates file_name.txt with extracted text from file_name.srt 
 * Script assumes that lines beginning with lowercase letters or commas 
 * are part of the previous line and lines beginning with any other character
 * are new lines. This won't always be correct. 
"""