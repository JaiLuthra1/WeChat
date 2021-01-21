from spacy.lang.en.stop_words import STOP_WORDS
import json
from gensim.models import Word2Vec
from gensim.test.utils import datapath, get_tmpfile
from gensim.models import KeyedVectors
from gensim.scripts.glove2word2vec import glove2word2vec
import nltk
import wget
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
ignore_words = STOP_WORDS
stop = stopwords.words('english')
stop = set(stop)
import zipfile
for word in stop:
  ignore_words.add(word)

"""wvUrl = "http://nlp.stanford.edu/data/glove.6B.zip"
zip_file = wget.download(wvUrl)
with zipfile.ZipFile(zip_file, 'r') as zip_ref:
    zip_ref.extractall()"""


glove_file = "glove.6B.100d.txt"
word2vec_glove_file = get_tmpfile("glove.6B.100d.word2vec.txt")
glove2word2vec(glove_file,word2vec_glove_file)
model = KeyedVectors.load_word2vec_format(word2vec_glove_file)
word_vectors = model.wv
data_file = open('IITMandi (1).json').read()
intents = json.loads(data_file)
classno = 0
def f(query):
  fclass = None
  ferr = 0
  fNotFound = 50
  NotFound = 0
  query = nltk.word_tokenize(query)
  query = [lemmatizer.lemmatize(word.lower()) for word in query]
  for intent in intents["QueriesAboutIITMandi"]:
      err = 1
      NotFound = 0
      for qword in query:
          qword = qword.lower()
          if qword in ignore_words:
                continue
          if qword not in word_vectors.vocab:            
            u = False
            for pattern in intent["patterns"]:
                w = nltk.word_tokenize(pattern)
                w = [word.lower() for word in w]
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
                    word = word.lower()
                    if word in ignore_words:
                        continue
                    try:
                      terr = max(terr,model.similarity(lemmatizer.lemmatize(qword),lemmatizer.lemmatize(word)))
                    except:
                      pass
              err *= terr
      if err-NotFound*0.02>ferr-fNotFound*0.02:
          ferr = err
          fNotFound = NotFound
          fclass = intent
  fq,fres = None,None
  fferr = 0
  for i in range(len(fclass["questions"])):
    q = nltk.word_tokenize(fclass["questions"][i])
    ferr = 1
    for qword in query:
      qword = qword.lower()
      err = 0.00000000001
      if qword not in word_vectors.vocab or qword in ignore_words:
        continue
      for word in q:
        word = word.lower()
        if word not in word_vectors.vocab or word in ignore_words:
          continue
        err = max(err,model.similarity(qword,word))
      ferr *= err
    if fferr<ferr:
      fq = fclass["questions"][i]
      fres = fclass["responses"][i]
      fferr = ferr
  return (fq,fres,fclass)

def chatbot_response(query):
    return f(query)
