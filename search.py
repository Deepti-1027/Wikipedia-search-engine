import sys
import math
import operator
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

stop_words = set(stopwords.words('english'))


def get_offset(word,low,high,file_ptr,list_offsets):
  ch=False
  final=False
  while low <= high:
    ch=True
    mid = (high + low)/2
    file_ptr.seek(list_offsets[int(mid)])
    value,offset = file_ptr.readline().strip().split(' ')
    another_value,offset1 = file_ptr.readline().strip().split(' ')
    
    if value == word:
      return list_offsets[int(mid)]
      
    if another_value == word:
      return list_offsets[int(mid) + 1]
      
    if value < word:
      low = mid + 1
      
    else:
      high = mid - 1
  return - 1

def searching_for_all(query,list_of_files,index_file_ptr):
  result={}
  docid=False
  doctitle=False
  docbody=False
  docref=False
  flag=False
  for word in query['all']:
    flag=True
    left=0
    right=len(list_of_files)-1
    while left <= right:
      mid = int(left + (right - left) / 2)
      if list_of_files[mid] < word:
        left=mid + 1
  
      else:
        right=mid - 1

    file_name =list_of_files[left-1]
    file_path=os.path.join('Offset_Partition',file_name)
    offsets=[]
    flag_check=False
    with open(file_path,'r') as file_ptr:
      for line in file_ptr.readlines():
        flag_check=True
        offset_value = int(line.strip().split(' ')[1])
        offsets.append(offset_value)

    offset = get_offset(word,0,len(offsets), index_file_ptr,offsets)
    
    if offset == -1:
      continue
      
    index_file_ptr.seek(offset)
    line = index_file_ptr.readline().strip().split(' ')[1].split('|')
    posting_list=line
    result[word] = {'t':[], 'b':[], 'i':[], 'c':[], 'l':[], 'r':[]}
    for posting in posting_list:
      finding_docid=re.findall('d[0-9]+',posting)
      document_id = int(finding_docid[0][1:])
      if 't' in posting:
        title_reg='t[0-9]+'
        finding_title=re.findall('t[0-9]+', posting)
        title_value = int(finding_title[0][1:])
        result[word]['t'].append([document_id,title_value])

      if 'c' in posting:
        cat_reg='c[0-9]+'
        finding_cat=re.findall('c[0-9]+',posting)
        category_value = int(finding_cat[0][1:])
        result[word]['c'].append([document_id,category_value])

      if 'i' in posting:
        info_reg='i[0-9]+'
        finding_info=re.findall('i[0-9]+',posting)
        infobox_value = int(finding_info[0][1:])
        result[word]['i'].append([document_id,infobox_value])
        
      if 'b' in posting:
        body_reg='b[0-9]+'
        finding_body=re.findall('b[0-9]+',posting)
        body_value = int(finding_body[0][1:])
        result[word]['b'].append([document_id,body_value])
                  
      if 'r' in posting:
        ref_reg='r[0-9]+'
        finding_ref=re.findall('r[0-9]+',posting)
        ref_value = int(finding_ref[0][1:])
        result[word]['r'].append([document_id,ref_value])
        
      if 'l' in posting:
        finding_l=re.findall('l[0-9]+',posting)
        body_value = int(finding_l[0][1:])
        result[word]['l'].append([document_id,body_value])

  return result;

def searching_for_feild(query,list_of_files,index_file_ptr,key):

  result={}
  for word in query[key]:
    left=0
    right=len(list_of_files)-1
    while left <= right:
      mid = int(left + (right - left) / 2)
      if list_of_files[mid] < word:
        left=left+1
      else:
        right=right-1
    file_name =list_of_files[left-1]
    file_path = os.path.join('Offset_Partition',file_name)
    offsets=[]
    with open(file_path,'r') as file_ptr:
      for line in file_ptr.readlines():
        offset_value = int(line.strip().split(' ')[1])
        offsets.append(offset_value)
    offset = get_offset(word,0,len(offsets), index_file_ptr, offsets)
    if offset == -1:
      continue
      
  
    value=list()
    index_file_ptr.seek(offset)
    line = index_file_ptr.readline().strip().split(' ')[1].split('|')
    for v in line:
      if key in v:
        value.append(v)
        
    posting_list=value
    if word not in result:
      result[word] = dict()
    
    result[word][key] = list()
    for posting in posting_list:
      document_id = int(re.findall('d[0-9]+',posting)[0][1:])
      if key == 't':
        title_reg='t[0-9]+'
        findtitle=re.compile('t[0-9]+').findall(posting)
        title_value = int(findtitle[0][1:])
        result[word][key].append([document_id, title_value])
      
      elif key == 'c':
        cat_reg='c[0-9]+'
        findingcat=re.compile('c[0-9]+').findall(posting)
        category_value = int(findingcat[0][1:])
        result[word][key].append([document_id, category_value])
        
      elif key == 'i':
        info_reg='i[0-9]+'
        findinginfo=re.compile('i[0-9]+').findall(posting)
        infobox_value = int(findinginfo[0][1:])
        result[word][key].append([document_id, infobox_value])

      elif key == 'b':
        body_reg='b[0-9]+'
        findingbody=re.compile('b[0-9]+').findall(posting)
        body_value = int(findingbody[0][1:])
        result[word][key].append([document_id, body_value])
        
      elif key == 'l': 
        link_reg='l[0-9]+'
        findinglink=re.compile('l[0-9]+').findall(posting)
        links_value = int(findinglink[0][1:])
        result[word][key].append([document_id, links_value])
        
        
      elif key == 'r':
        ref_reg='r[0-9]+'
        findingref=re.compile('r[0-9]+').findall(posting)
        ref_value = int(findingref[0][1:])
        result[word][key].append([document_id, ref_value])

    return result    

def searching(query,number_document):
  index_path = "index_file.txt"
  index_file_ptr = open(index_path,'r')
  pages=dict()
  list_of_files = []
  for file in os.listdir("Offset_Partition"):
    list_of_files.append(file)
    
  list_of_files.sort()
  for key in query:
    if key in ['all']:
      pages=searching_for_all(query,list_of_files,index_file_ptr)
            
    else:
      pages=searching_for_feild(query,list_of_files,index_file_ptr,key)

  values = dict()

  for page in pages:
    for tag in pages[page]:
      if len(pages[page][tag]) == 0:
        continue
      len_page=len(pages[page][tag])     ## made changes
      for field_value in pages[page][tag]:
        if field_value[0] not in values:
          values[field_value[0]] = 0.0
        
        if tag == 't':
          values[field_value[0]] += math.log(number_document/len_page) *(math.log(field_value[1] + 1)) * .40

        if tag == 'i':
          values[field_value[0]] += math.log(number_document/len_page) *(math.log(field_value[1] + 1)) * .30

        if tag == 'c':
          values[field_value[0]] += math.log(number_document/len_page) *(math.log(field_value[1] + 1)) * .08
          
        if tag == 'b':
          values[field_value[0]] += math.log(number_document/len_page) *(math.log(field_value[1] + 1)) * .08
          
        if tag == 'l':
          values[field_value[0]] += math.log(number_document/len_page) *(math.log(field_value[1] + 1)) * .06
          
        if tag == 'r':
          values[field_value[0]] += math.log(number_document/len_page) *(math.log(field_value[1] + 1)) * .06
          
  result = sorted(values.items(), key= operator.itemgetter(1), reverse=True)
  ranked_result = result
  return ranked_result

def get_titles():
  titles = dict()
  with open('DocID_Title_Map.txt', 'r') as file_ptr:
    for line in file_ptr.readlines():
      line = line.strip().split(' ', 1)
      if len(line) != 1:
        titles[int(line[0])] = line[1]
      else:
        pass
        
        
  return titles

def read_query_file(query_file):
  queries=list()
  search_k=list()
  with open(query_file,'r')as file_:
    for line in file_:
      line=line.strip().split(',')
      search_k.append(line[0])
      queries.append(line[1])

  return search_k,queries

def query_processing(query):
  queries = dict()
  field_list = ['t:', 'b:','c:','i:','r:']
  query = query.lower()
  query_process=False
  
  field_reg = re.finditer('(t:|i:|b:|c:|r:)([\w+\s+]+)(?=(t:|i:|b:|c:|r:|$))',query)
  query_p=True
  
  if any(1 for field in field_list if field in query):
    for elem in field_reg:
      query_process=True
      term = elem.group(0).split(":")
      try:
        term_list=list()
        for word in term[1].split():
          if word not in stop_words:
            term_list.append(stemmer.stem(word.lower()))
            
        for t in term_list:
          queries[term[0]].append(t)
          
      except KeyError:
        queries[term[0]] = list(stemmer.stem(word.lower()) for word in term[1].split() if word not in stop_words)
          
  else:
    words = query.strip().split(' ')
    try:
      term_list=list()
      for word in words:
        if word not in stop_words:
          term_list.append(stemmer.stem(word.lower()))
          
      for t in term_list:
        queries['all'].append(t)
        
    except KeyError:
      ch_all=True
      queries['all'] = list(stemmer.stem(word.lower()) for word in words if word not in stop_words)
      
  return queries

query_file=sys.argv[1]
k_value,query_list=read_query_file(query_file)
print("Loading Titles-Document ID Mappings....")
titles = get_titles()
number_document = len(titles)
print("Loaded...")

output_file="queries_op.txt"

if os.path.exists(output_file):
  os.remove(output_file)

file_op=open(output_file,"w")
for (k,query) in zip(k_value,query_list):
  k=int(k)
  start = time.time()
  processed_queries = query_processing(query)
  print("Modified Query : ", processed_queries)
  result = searching(processed_queries,number_document)

  print("Results : ")
  if len(result) > 0:
    if len(result) > k:
      result = result[:k]
      for r in result:
        file_op.write(str(r[0])+" "+titles[r[0]])
        file_op.write('\n')
        #print(r[0]," ",titles[r[0]])
        
    else:
      result = result[:k]
      for r in result:
        file_op.write(str(r[0])+" "+titles[r[0]])
        file_op.write('\n')
      #print('K results not present!')
    
      
  else:
    print('Result not found')
  end = time.time()
  file_op.write(str(end-start)+" "+str((end-start)/k))
  file_op.write('\n')
  file_op.write('\n')
  print("Response Time for the Query " + query + " is " +  str(end - start) + " seconds")


file_op.close()

