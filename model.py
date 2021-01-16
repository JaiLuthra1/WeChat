
from spacy.lang.en.stop_words import STOP_WORDS
import json
from gensim.models import Word2Vec
from gensim.test.utils import datapath, get_tmpfile
from gensim.models import KeyedVectors
from gensim.scripts.glove2word2vec import glove2word2vec
import nltk
import wget
nltk.download('stopwords','./nltk_data/')
nltk.data.path.append('./nltk_data/')
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
ignore_words = STOP_WORDS
stop = stopwords.words('english')
stop = set(stop)
import zipfile
for word in stop:
  ignore_words.add(word)

# wvUrl = "http://nlp.stanford.edu/data/glove.6B.zip"
# zip_file = wget.download(wvUrl, './')
# with zipfile.ZipFile(zip_file, 'r') as zip_ref:
#     zip_ref.extractall()


glove_file = "glove.6B.100d.txt"
word2vec_glove_file = get_tmpfile("glove.6B.100d.word2vec.txt")
glove2word2vec(glove_file,word2vec_glove_file)
model = KeyedVectors.load_word2vec_format(word2vec_glove_file)
word_vectors = model.wv
data_file = open('QueriesAboutIITMandi.json').read()
intents = json.loads(data_file)
classno = 0

def f(query):
  fclass = None
  ferr = 0
  query = nltk.word_tokenize(query)
  query = [lemmatizer.lemmatize(word.lower()) for word in query]
  for intent in intents["QueriesAboutIITMandi"]:
      err = 1
      NotFound = 0
      for qword in query:
          if qword in ignore_words:
                continue
          if qword not in word_vectors.vocab:              
            u = False
            for pattern in intent["patterns"]:
                w = nltk.word_tokenize(pattern)
                if qword in w:
                    u = True
                    break
            if not u:
                NotFound +=1
          else:
              terr = 0.00001
              for pattern in intent["patterns"]:
                  w = nltk.word_tokenize(pattern)
                  for word in w:
                    if word in ignore_words:
                        continue
                    try:
                      terr = max(terr,model.similarity(lemmatizer.lemmatize(qword),lemmatizer.lemmatize(word.lower())))
                    except:
                      pass
              err *= terr
      if err>ferr:
          ferr = err
          fclass = intent
  return fclass

def chatbot_response(query):
    return f(query)
