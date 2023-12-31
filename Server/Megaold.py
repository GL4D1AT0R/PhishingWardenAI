import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.compose import ColumnTransformer
import joblib
from Scraper import url, ssl, age, status_code, blacklisted_words
import requests

# Load the dataset
data = pd.read_csv('Shuffled.csv')

# Separate the features and target variable
X = data.iloc[:, :-1]
y = data.iloc[:, -1]

# Define the feature column names expected by the preprocessor
feature_cols = ['url', 'ssl', 'age', 'status_code', 'blacklisted_words']

# Create a DataFrame from the feature data
# url = url
# ssl = ssl
# age = age
# status_code = status_code
# blacklisted_words = blacklisted_words
features = [[url, ssl, age, status_code, blacklisted_words]]
test_data = pd.DataFrame(features, columns=feature_cols)

# Preprocess the numerical features using StandardScaler
numerical_features = ['ssl', 'age', 'status_code']
numerical_transformer = StandardScaler()

# Preprocess the categorical feature using OneHotEncoder
categorical_features = ['url']
categorical_transformer = OneHotEncoder(handle_unknown='ignore')

# Preprocess the text feature using CountVectorizer
text_features = 'blacklisted_words'
text_transformer = CountVectorizer()

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numerical_transformer, numerical_features),
        ('cat', categorical_transformer, categorical_features),
        ('text', text_transformer, text_features)
    ])

# Preprocess the data using the preprocessor
X = preprocessor.fit_transform(X)
test_X = preprocessor.transform(test_data)

# Train the model on the full dataset
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X, y)

# Save the trained model to a file
joblib.dump(clf, 'phishing_model.joblib')

# Predict the phishing status of the test website
test_y_pred = clf.predict(test_X)

is_phish = ""

if test_y_pred[0] == 1:
    print("The website is predicted to be a phishing website.")
    is_phish = "yes"
else:
    print("The website is predicted to be a legitimate website.")
    is_phish = "no"
print(is_phish)
from Encrypt import encrypt_data
result=encrypt_data(is_phish)
cleanedResult = result + "=="
print("Result is ", cleanedResult)

ext_url = 'https://eofn7ve6epuaruq.m.pipedream.net/'
data = {'is_phish': result}

response = requests.post(ext_url, data=data)

print(response.status_code)






















# # Make predictions on the same dataset to evaluate the model performance
# y_pred = clf.predict(X)
# accuracy = accuracy_score(y, y_pred)
# print('Accuracy on the full dataset:', round(accuracy * 100, 2), '%')
#
# # Calculate the F1 score of the model on the full dataset
# f1 = f1_score(y, y_pred)
# print('F1 score on the full dataset:', round(f1 * 100, 2), '%')
