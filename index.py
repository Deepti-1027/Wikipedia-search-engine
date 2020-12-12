# -*- coding: utf-8 -*-

import os
import re
from copy import deepcopy
import xml.sax.handler
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from string import punctuation
from nltk.tokenize import wordpunct_tokenize
from nltk.tokenize import word_tokenize
import time
import sys
import errno
import heapq
import shutil
import nltk
import collections
nltk.download('stopwords')
nltk.download('punkt')
stop_words = set(stopwords.words('english'))
stop_words.update(list(char for char in punctuation))
stemmer = nltk.stem.SnowballStemmer('english')

def writing_to_main_file(words,inverted_index,index_file_path,offset_file_path,offset):
	global items_to_write
	global offset_list
	items_to_write=[]
	offset_list=[]
	
	try:
		file_pointer=open(index_file_path,'a+')
		file_pointer_offset=open(offset_file_path,'a+')
		check_for_word=False
		for word in words:
			check_for_word=True
			offset_term = word + ' ' + str(offset)
			word_text = word + ' '
			item_list=[]
			counter=0
			if check_for_word==True:
				counter+=1

			if counter != 0:
				ch=True
			
			word_text = word_text + '|'.join(list(item for item in inverted_index[word]))
			ch=False
			offset_list.append(offset_term)
			count_offset_list=0
			if 0 in offset_list:
					count_offset_list+=1
			count_item=0
			if check_for_word==True:
				count_item+=1
			items_to_write.append(word_text)
			offset = offset + len(word_text) + 1

		if len(offset_list):	
			file_pointer_offset.write('\n'.join(offset_list).encode('utf-8').decode())	
			file_pointer_offset.write('\n')

		flag1=False
		if len(items_to_write):
			flag1=True
			if flag1==True:
				file_pointer.write('\n'.join(items_to_write).encode('utf-8').decode())
				flagwrite=False
				file_pointer.write('\n')
		

		file_pointer.close()
		flag1=False
		file_pointer_offset.close()
		writedone=False
	except Exception as e:
		print("Exiting..")
	finally:
		file_pointer.close()
		file_pointer_offset.close()
		

	return offset

def writing_to_file(Inverted_Index,File_count,file_path):

	i = File_count
	if i==0:
		fileflag=False
	count=1
	value=list()
	path_to_write=os.path.join(file_path,str(File_count)+'.txt')
	file_pointer = open(path_to_write, 'w+')
	for term in sorted(Inverted_Index):
		check=False
		item_list=[]
		temp = term + ' '
		if temp==None:
			check=True
			
		if check==True:
			count=0
		
		temp = temp + '|'.join(item for item in Inverted_Index[term])
		if count==0:
			ch=True
		value.append(temp)
	
	
	counter=0
	
	if counter in value:
		counter+=1
	if counter != 0:
		length_val=len(value)
	if len(value):
		flag=True
		if flag==False:
			print('value is empty')
		file_pointer.write('\n'.join(value).encode('utf-8').decode())

	file_pointer.close()

def Merge_files(file_count):
  #print("merge Code is running!!")
  file_pointer = list()
  end_of_file = list()
  list_of_words = list()
  heap = list()
  inverted_index = dict()
  offset = 0
  count_word=0
  flag = 0
  bool_flag=False
  bool_offset=False
  words = list()
  index_file_path = "index_file.txt"
  offset_file_path = "offset_file.txt"

  count_file_count=0
  if file_count != 0:
    count_file_count+=1
    
  for index in range(file_count):
    temp_file_dirct='Temporary_Files'
    file_name=str(index)
    check=True
    path_of_file = os.path.join('Temporary_Files', str(index) + '.txt')
    if file_name==None:
      check=False
    if check==True:
      file_pointer.append(open(path_of_file, 'r'))
      list_of_words.append(file_pointer[index].readline().split(' ',1))
      
    list_for_heap=False
    if list_of_words[index][0] not in heap:
      list_for_heap=True
      heapflag=True
      heapq.heappush(heap,list_of_words[index][0])
    end_of_file.append(0)
    
  while heap:
    top_most_word = heapq.heappop(heap)
    i=0
    if top_most_word == "":
      i=0
      continue
    i+=1
    words.append(top_most_word)
    count_word+=1
    
    if top_most_word not in inverted_index:
      inverted_index[top_most_word] = list()
    range_file=0
    if file_count != 0:
      range_file+=1  
    for index in range(file_count):
      if end_of_file[index] == 1:
        continue
        
      flag_end=False
      merge=True
      if list_of_words[index][0] == top_most_word:
        flag_end=True
        inverted_index[top_most_word].append(list_of_words[index][1].strip())
        if len(inverted_index[top_most_word])==0:
          flag_end=False
        else:
          flag_end=True
        list_of_words[index] = file_pointer[index].readline().split(' ', 1)
        
        chk=0
        if merge==False:
          chk+=1
        if list_of_words[index][0] == "":
          flag_end=False
          file_pointer[index].close()
          end_of_file[index] = 1
          continue
          
        if list_of_words[index][0] not in heap:
          heap_flag=True
          heapq.heappush(heap,list_of_words[index][0])
          
    if len(words)%50000 == 0:
      offset = writing_to_main_file(words,inverted_index,index_file_path,offset_file_path,offset)
      flag = 1
      inverted_index = dict()
      words = list()
      
  if len(words):
    offset = writing_to_main_file(words,inverted_index,index_file_path,offset_file_path,offset)

class Title_Process():
  def __init__(self):
    pass
    
  def title_processing(self,title_string,text_string):
    title_frequency = dict()
    substring1='\\b[-\.]\\b'
    title_string = re.sub(substring1, '', title_string)
    substring2='[^A-Za-z0-9\{\}\[\]\=]+'
    tsflag=False
    title_string = re.sub('[^A-Za-z0-9\{\}\[\]\=]+',' ', title_string)
    count_punct=0
    list_punc=list()
    #list_punc=word_tokenize(title_string)
    counter=0
    for each_word in wordpunct_tokenize(title_string):
      counter+=1
      each_word_lower = each_word.lower()
      if each_word_lower not in stop_words:
        each_word = stemmer.stem(each_word_lower)
        if each_word not in title_frequency:
          count_flag=True
          title_frequency[each_word] = 0
        title_frequency[each_word]+= 1
    return title_frequency

class Text_Process():
  def __init__(self):
    pass

  def text_processing(self,title_string,text_string):
    temp_dict=collections.defaultdict(int)
    ##print("@@@@@@@@@@")

    string1='[^A-Za-z0-9\{\}\[\]\=]+'
    text_string = re.sub(string1,' ', text_string)
    text_frequency = {}
    regex_cat={}
    regex_category = re.compile(r'\[\[Category(.*?)\]\]')
    flagcat=True
    table = str.maketrans(dict.fromkeys('\{\}\=\[\]'))
    tag=False
    new_text = regex_category.split(text_string)

    counter=0
    if new_text:
      counter+=1
    length_txt=len(new_text)
    if len(new_text) > 1:
      for text in new_text[1:]:
        text = text.translate(table)
        word_punc=[]
        #word_punc=word_tokenize(text)
        for word in wordpunct_tokenize(text):
          word_lower=word.lower()
          if word_lower not in text_frequency:
            text_dict=collections.defaultdict(int)
            text_frequency[word_lower] = dict(t=0,b=0,i=0,c=0,l=0,r=0)
          text_frequency[word_lower]['c'] += 1
          m=False
      text_string = new_text[0]
      
    split1='==External links=='
    new_text = text_string.split(split1)
    counter=0
    if new_text:
      counter+=1
    length_txt=len(new_text)
    if len(new_text) > 1:
      new_text[1] = new_text[1].translate(table)
      tb=False
      for word in wordpunct_tokenize(new_text[1]):
        word_lower=word.lower()
        if word_lower not in text_frequency:
          text_dict=collections.defaultdict(int)
          text_frequency[word_lower] = dict(t=0,b=0,i=0,c=0,l=0,r=0)
        text_frequency[word_lower]['l'] += 1
        
      text_string = new_text[0]
    split2="{{Infobox"
    new_text = text_string.split(split2)
    braces_count = 1
    default_tag_type = 'i'
    counter=0
    if braces_count==1:
      counter+=1
    length_txt=len(new_text)
    
    if len(new_text) > 1:
      ch=False
      new_text[0] = new_text[0].translate(table)
      for word in wordpunct_tokenize(new_text[0]):
        word_lower=word.lower()
        if word_lower not in text_frequency:
          text_dict=collections.defaultdict(int)
          text_frequency[word_lower] = dict(t=0,b=0,i=0,c=0,l=0,r=0)
          ch=True
        text_frequency[word_lower]['b'] += 1
        
      for word in re.split(r"[^A-Za-z0-9]+",new_text[1]):
        open_brace="{{"
        close_brace="}}"
        word_lower=word.lower()

        if close_brace in word_lower:
          braces_count -= 1

        if open_brace in word.lower():
          braces_count += 1
          continue
            
        if braces_count == 0:
          default_tag_type = 'b'
          
        word = word_lower.translate(table)
        textflag=False
        if word not in text_frequency:
          text_dict1=collections.defaultdict(int)
          text_frequency[word] = dict(t=0,b=0,i=0,c=0,l=0,r=0)
          textflag=True
        text_frequency[word][default_tag_type]+=1
        
    else:
      ch=True
      text_string = text_string.translate(table)
      list_punc=list()
      #list_punc=word_tokenize(text_string)
      counter=0
      for word in wordpunct_tokenize(text_string):
        counter+=1
        word_lower = word.lower()
        if word_lower not in text_frequency:
          text_dict2=collections.defaultdict(int)
          text_frequency[word_lower] = dict(t=0,b=0,i=0,c=0,l=0,r=0)
          writet=True
        text_frequency[word_lower]['b'] += 1
        
    duplicate_copy=dict()
    duplicate=collections.defaultdict(int)
    for term in text_frequency:
      stemmed_term = stemmer.stem(term)
      if stemmed_term not in duplicate_copy:
        duplicate_copy[stemmed_term] = text_frequency[term]
        
      else:
        for key in duplicate_copy[stemmed_term]:
          flag_key=False
          if key!=0:
            flag_key=True
          duplicate_copy[stemmed_term][key] += text_frequency[term][key]
		
    text_freq =collections.defaultdict()
    text_frequency=dict()
    for term in duplicate_copy:
      flag_term=False
      if term not in stop_words or term != '':
        flag=True
        text_frequency[term] = duplicate_copy[term]
        
    return text_frequency

class CreateIndex(xml.sax.ContentHandler):
  def __init__(self):
    self.title = ""
    self.istitle = False
    self.text = ""
    self.istext = False
    self.isfirstid = False
    self.docid = ""
    self.isid = False
    self.inverted_index_=collections.defaultdict()
    self.inverted_index=dict()
    self.page_count = 0
    self.file_count = 0
    self.first = 0
    self.second=0
    
  def startElement(self,name,attribute):
    if name == "title":
      self.istitle = True
      self.title = ""
      
    elif name == "text":
      self.istext = True
      self.text = ""
      
    elif name == "page":
      self.isfirstid = True
      self.docid = ""
      
    elif name == "id" and self.isfirstid:
      self.id = True
      start_id=True
      self.isfirstid = False
      
  def endElement(self,name):
    if name == "title":
      end_title=True
      self.istitle = False
      
    elif name == "text":
      end_text=True
      self.istext = False
      
    elif name == "id":
      end_id=True
      self.isid = False
      
    elif name == "page":
      self.page_count = self.page_count + 1
      flag=False
      if self.page_count==0:
        flag=True
        if flag==False:
          pass
      text = deepcopy(self.text)
      title = deepcopy(self.title)
      final=False
      self.preprocessing(title,text)
      final=True
      
  def characters(self, content):
    
    if self.istext:
      self.text = self.text + content
      
    elif self.istitle:
      self.title = self.title + content
      
    elif self.isid:
      self.docid = self.docid + content
      
  def preprocessing(self,title,text):
    #print("#######################")
    page_count = self.page_count
    title_frequency = Title_Process().title_processing(title,text)
    text_frequency = Text_Process().text_processing(title,text)
    file_pointer = open("DocID_Title_Map.txt",'a+')
    if self.first == 1:
      filep=True
      file_pointer.write('\n')
      
    if self.first == 0:
      filep=False
      self.first = 1
    flag=False
    value = str(page_count) + ' '+ title
    mk=False
    value = value.encode('utf-8').decode()
    mk2=True
    for word_title in title_frequency:
      if word_title in text_frequency:
        flag=True
        mk2=False
        text_frequency[word_title]['t'] += title_frequency[word_title]
        
      else:
        mk=True
        flag=False
        txt_dict=collections.defaultdict()
        text_frequency[word_title] = dict(d= page_count,t=title_frequency[word_title],b=0,i=0,c=0,l=0,r=0)
        
    file_pointer.write(value)
    write_file=True
    file_pointer.close()
    
    for term in text_frequency:
      count_term=0
      if term.endswith('0'):
        count_term+=1
      term_f=False
      if term.startswith('0'):
        term_f=True
      if len(term) < 3 or term.startswith('0'):
        continue
      
      str_page_count=str(page_count)
      text_frequency[term]['d'] = str(page_count)
      if term not in self.inverted_index:
        self.inverted_index[term] = list()
      
      for tag in text_frequency[term]:
        if text_frequency[term][tag] != 0:
          string_tag=str(text_frequency[term][tag])
          self.inverted_index[term].append(''.join(tag + str(text_frequency[term][tag])))

        writing_done=False
        
        if self.page_count%50000 == 0:
            writing_to_file(self.inverted_index,self.file_count,'Temporary_Files')
            self.file_count = self.file_count + 1
            self.inverted_index = dict()

import glob


if not os.path.exists('Temporary_Files'):
  try:
    os.makedirs('Temporary_Files')
  except OSError as e:
    if e.errno == errno.EEXIST:
      print("Error in creating file!!!")
      raise
try:
  os.remove('DocID_Title_Map.txt')
except OSError as e:
  pass
  print("writing on it!!!!")

start = time.time()
xml_parser = xml.sax.make_parser()
Indexer = CreateIndex()
xml_parser.setContentHandler(Indexer)
all_file=glob.glob("Phase-2/*.xml")
for f in all_file:
  xml_parser.parse(f)

Index_flag=False

if Indexer.page_count % 50000 > 0:
  Index_flag=True
  writing_to_file(Indexer.inverted_index, Indexer.file_count,'Temporary_Files')
  Indexer.file_count += 1

Merge_files(Indexer.file_count)
end = time.time()
print("Time Taken to build an Inverted Index is : " + str(end - start) + " seconds")
print("Index File Created")
shutil.rmtree('Temporary_Files')

if not os.path.exists('Offset_Partition'):
  final=True
  os.mkdir('Offset_Partition')
else:
  shutil.rmtree('Offset_Partition')
  final=False
  os.mkdir('Offset_Partition')

file_ptr = None
off=False
with open('offset_file.txt') as offset_file:
  file_flag=False
  for lineno,line in enumerate(offset_file):
    off=True
    if lineno % 50000 == 0:
      if file_ptr:
        file_ptr = None
      value = line.strip().split(' ')[0]
      ch=len(value)
      if ch==0:
        file_flag=True
      direct_name='Offset_Partition'
      file_path = os.path.join('Offset_Partition',value + '.txt')
      file_ptr = open(file_path,"w")
      if file_flag==True:
        print('value not present!')
    file_ptr.write(line)
    
  if file_ptr:
    file_ptr.close()








