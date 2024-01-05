
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

csv_file_path = "new_df.csv"
new_df = pd.read_csv(csv_file_path)
tfidf = TfidfVectorizer(max_features=1000, stop_words='english')

vectors =  tfidf.fit_transform(new_df['tags']).toarray()
similarity= cosine_similarity(vectors)

#data = new_df.csv


def recommend(course):
    course_index = new_df[new_df['Course Title'] == course].index[0]
    course_list = sorted(list(enumerate(similarity[course_index])), key=lambda x: x[1], reverse=True)[1:6]
    for i in course_list:
       print(new_df.iloc[i[0]]["Course Title"])
       

recommend("Classical Mechanics")
    

