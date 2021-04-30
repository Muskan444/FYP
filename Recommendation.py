import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import sqlalchemy
engine = sqlalchemy.create_engine('mysql+pymysql://root:@localhost:3306/Foodie')
food = pd.read_sql_table('foodie_blogs',engine)
Reviews = pd.read_sql_table('foodie_review',engine)
Data = pd.merge(Reviews, food)

from sklearn.model_selection import train_test_split
Xtrain, Xtest = train_test_split(Data, test_size=0.2, random_state=1)

tfidfvec = TfidfVectorizer()
tfidf_recipe_id = tfidfvec.fit_transform(Xtrain['ingredients'])
cosine_sim = cosine_similarity(tfidf_recipe_id)
job_id = Xtrain[Xtrain.title == 'Turkey Ragu'].index
list(Xtrain[Xtrain.title == 'Turkey Ragu'].index)

def Recommendations(title):
	index = list(Xtrain[Xtrain.title == 'Turkey Ragu'].index)
	print(index)
	scores = list(enumerate(cosine_sim[index]))
	similarity_scores = sorted(scores, key=lambda x: x[1], reverse=True)
	similarity_scores = similarity_scores[:4]
	food = [i[0] for i in similarity_scores]
	return Data['title'].iloc[food]
