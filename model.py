import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.utils import shuffle
from sklearn.preprocessing import StandardScaler
from sklearn import tree
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score

# Reading the CSV file
data = pd.read_csv('data.csv')

# Dropping the duplicate tracks
data.drop_duplicates(subset=['track_name', 'first_artist', 'duration_ms'], keep='last', inplace=True)

# Dropping the first 4 columns
data.drop(['track_num', 'track_id', 'track_name', 'first_artist'], axis=1, inplace=True)

# Using Pearson Correlation
plt.figure(figsize=(12, 10))
corr = data.corr()
sns.heatmap(corr, annot=True, cmap=plt.cm.Reds)
# plt.show()

# Correlation with output variable with threshold as 0.1
corr_target = abs(corr['liked'])

# Selecting highly correlated features
relevant_features = corr_target[corr_target > 0.1].index.tolist()

# Shuffling and splitting the dataset into train and test splits
data = shuffle(data)
X = data.loc[:, relevant_features[:-1]].values
y = data.iloc[:, -1].values

# Random state is 0 and test size if 30%
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

sc = StandardScaler()

# Providing the inputs for the scaling purpose
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

# Entropy means information gain
classifier = DecisionTreeClassifier(criterion='entropy', random_state=0)

# Providing the training dataset
classifier.fit(X_train, y_train)

# Predicting the outputs
y_pred = classifier.predict(X_test)

# Evaluation of the model
accuracy = accuracy_score(y_pred, y_test)
print("Accuracy:", accuracy)

clf = DecisionTreeClassifier()

# Output size of decision tree
plt.figure(figsize=(40, 20))

# Providing the training dataset
clf = clf.fit(X_train, y_train)
plot_tree(clf, filled=True)
plt.title("Decision tree of TRAIN set")
# plt.show()

clf = DecisionTreeClassifier()

# Output size of decision tree
plt.figure(figsize=(40, 20))

# Providing the training dataset
clf = clf.fit(X_test, y_test)
plot_tree(clf, filled=True)
plt.title("Decision tree of TEST set")
# plt.show()

# Text based tree
text_representation = tree.export_text(clf)
# print(text_representation)






