import pandas as pd
import pickle
from text_cleaner import text_cleaner
from sklearn.feature_extraction.text import CountVectorizer

df = pd.read_excel("dataset.xlsx")
df = df.dropna()

df['cleaned'] = df["text"].apply(text_cleaner)

X = df.cleaned
y = df.label

vect = CountVectorizer(max_features = 20000 , lowercase=False , ngram_range=(1,2))
X_cv =vect.fit_transform(X).toarray()

def vectorize(clean_text):
    model = pickle.load(open('CV_BestModel.sav', 'rb'))
    single_prediction = model.predict(vect.transform([clean_text]).toarray())[0]

    output = {0:"No Anxiety/Depression",
          1:"Anxiety/Depression"}
    
    return output[single_prediction]
