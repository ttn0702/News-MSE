from settings import RSS_FEEDS
from utils import get_article_content
import csv
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import numpy as np


ps = PorterStemmer()
# Xử lý văn bản
stop_words = set()
# read vietnamese stopwords from file txt
with open("vi_stopwords.txt", "r", encoding="utf-8") as f:
    stop_words = f.read().splitlines()


def preprocess_text(text):
    words = text.split()
    words = [ps.stem(word) for word in words if word not in stop_words]
    return " ".join(words)


class RecommendArticles:
    def __init__(self, file_name="train_data.csv"):
        self.file_name = file_name

    def get_train_data(self):
        train_headers = [
            "id",
            "title",
            "link",
            "url",
            "category",
            "description",
            "published",
            "image_link",
        ]
        train_csv_file = open(self.file_name, "w", encoding='utf-8')

        train_writer = csv.DictWriter(
            train_csv_file, fieldnames=train_headers, delimiter=";"
        )
        train_writer.writeheader()

        index = 1
        for category_name in RSS_FEEDS:
            print(category_name)
            category = RSS_FEEDS[category_name]
            # request to get rss feed
            articles = get_article_content(category["url"])
            for article in articles:
                train_writer.writerow(
                    {
                        "id": index,
                        "title": article["title"].strip(),
                        "link": article["link"].strip(),
                        "url": article["url"].strip(),
                        "category": category_name,
                        "description": article["description"].strip(),
                        "published": article["published"].strip(),
                        "image_link": article["image_link"].strip(),
                    }
                )
                index += 1

        train_csv_file.close()

    def train_model(self):
        data = pd.read_csv(self.file_name, delimiter=";")
        df = pd.DataFrame(data)
        df["processed_content"] = df["title"].apply(preprocess_text)
        # Tạo ma trận đặc trưng TF-IDF cho nội dung
        tfidf_content = TfidfVectorizer()
        print('data: ',data)
        tfidf_matrix_content = tfidf_content.fit_transform(df["processed_content"])

        # Tạo ma trận đặc trưng TF-IDF cho thể loại
        tfidf_category = TfidfVectorizer()
        tfidf_matrix_category = tfidf_category.fit_transform(df["category"])

        # Kết hợp ma trận nội dung và thể loại
        self.combined_features = np.hstack(
            (tfidf_matrix_content.toarray(), tfidf_matrix_category.toarray())
        )

        # Sử dụng KNN để tìm các bài báo tương tự
        knn = NearestNeighbors(metric="cosine", algorithm="brute")
        knn.fit(self.combined_features)

        self.knn = knn
        self.df = df

    def recommend(self, read_articles, num_recommendations=3):
        read_indices = [
            self.df.index[self.df["link"] == article_id].tolist()[0]
            for article_id in read_articles
        ]
        distances, indices = self.knn.kneighbors(
            self.combined_features[read_indices].reshape(len(read_articles), -1),
            n_neighbors=num_recommendations + 1,
        )
        all_recommendations = indices.flatten()[1:]
        unique_recommendations = list(set(all_recommendations) - set(read_indices))
        return self.df.iloc[unique_recommendations[:num_recommendations]]
