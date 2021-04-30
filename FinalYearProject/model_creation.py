import pandas as pd
from Foodie.models import Blogs
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import sqlalchemy

def create():
	blogs = Blogs.objects.all()
	foodlist = []

	for blog in blogs:
		foodlist.append(blog.ingredients)

	ingredients = pd.Series(foodlist)
	print(ingredients.size)

	#genres = genres.apply(lambda x: x.split(" "))
	print(ingredients.head(n=20))

	vectorizer = TfidfVectorizer(analyzer="word",min_df=0,ngram_range=(1,2),stop_words="english")
	tfidf_matrix = vectorizer.fit_transform(ingredients)
	cosine_sim = linear_kernel(tfidf_matrix,tfidf_matrix)
	cosine_pd = pd.DataFrame(cosine_sim)

	with open("modelfile.pickle","wb") as f:
		pickle.dump(cosine_sim,f)

	print(cosine_pd.head(n = 20))