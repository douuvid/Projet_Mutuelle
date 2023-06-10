import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import nltk
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn import metrics

data = pd.read_csv("mutuelle_tableau_A.csv",sep=";")



print(data.isna().sum())
print(data.shape)

data['label'].value_counts().plot.bar()
#plt.show()

text = list(data['text'])

lemmatizer = WordNetLemmatizer()

corpus = []

for i in range(len(text)):

    r = re.sub('[^a-zA-Z]', ' ', text[i])

    r = r.lower()

    r = r.split()

    r = [word for word in r if word not in stopwords.words('english')]

    r = [lemmatizer.lemmatize(word) for word in r]

    r = ' '.join(r)

    corpus.append(r)

data['text'] = corpus

print(data.head())

X = data['text']

y = data['label']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=123)

print('Training Data :', X_train.shape)

print('Testing Data : ', X_test.shape)


cv = CountVectorizer()

X_train_cv = cv.fit_transform(X_train)

print(X_train_cv.shape)

lr = LogisticRegression()

lr.fit(X_train_cv, y_train)




# transform X_test using CV

X_test_cv = cv.transform(X_test)




# generate predictions

predictions = lr.predict(X_test_cv)

print(predictions)

df = pd.DataFrame(metrics.confusion_matrix(y_test,predictions), 
    index=["Null","hospitalisation","soins courants","aides auditives","optique","dentaire","medecine douce","fonds social","service"],
    columns=["Null","hospitalisation","soins courants","aides auditives","optique","dentaire","medecine douce","fonds social","service"])

print(df)
    
