from sklearn import tree
from sklearn import linear_model
import xgboost as xgb
import sys
import numpy as np
from sklearn.cross_validation import train_test_split

# Data 

data_2017 = [24.29, 90.21, 12.46, 80.08], [19.74, 87.95, 12.61, 79.53], [16.00, 89.55, 14.95, 81.51], [23.45, 84.89, 13.31, 83.83]
results_2017 = 5, 5, 12, 5


# For the 5v12 seed starting with 2018 and ending with 2008
# Format: Kenpom, Sagarin
features = [[20.44, 88.22, 14.7, 82.16], [21.16, 86.49, 10.2, 78.54], [22.44, 90.26, 12.19, 78.6], [21.65, 86.7, 12.92, 80.06],
			[24.29, 90.21, 12.46, 80.08], [19.74, 87.95, 12.61, 79.53], [16.00, 89.55, 14.95, 81.51], [23.45, 84.89, 13.31, 83.83],
			[20.25, 87.26, 9.57, 78.38], [19.06, 85.79, 14.33, 81.77], [23.85, 89.27, 13.24, 76.00], [23.05, 89.24, 6.50, 80.13],
			[17.64, 86.02, 11.87, 80.45], [16.44, 84.71, 6.72, 77.98], [27.24, 86.37, 13.64, 76.69], [20.98, 90.82, 5.67, 82.36],
			[19.80, 85.81, 10.83, 79.83], [19.24, 86.32, 17.58, 84.88], [15.72, 84.69, 11.60, 80.59], [17.90, 84.29, 11.76, 81.12],
			[18.69, 85.60, 16.78, 85.88], [22.57, 87.56, 16.95, 85.26], [16.07, 87.08, 13.11, 80.11], [20.28, 83.93, 11.52, 81.88],
			[22.36, 87.37, 13.45, 75.62], [19.45, 80.06, 69.14, 15.27], [20.90, 79.14, 14.34, 74.74], [14.49, 78.48, 13.13, 65.56],
			[20.11, 86.63, 18.16, 84.09], [19.65, 88.35, 6.98, 79.94], [17.33, 84.59, 16.01, 84.88], [17.42, 85.22, 19.32, 85.01],
			[20.12, 86.33, 15.92, 84.86], [20.13, 87.59, 6.03, 77.18], [22.45, 89.57, 16.53, 83.76], [21.33, 87.28, 19.9, 83.33],
			[17.8, 83.79, 15.96, 83.75], [21.84, 88.71, 9.7, 78.73], [15.76, 84.62, 17.62, 84.65], [18.72, 86.25, 8.1, 79.02],
			[19.07, 86.18, 9.68, 77.73], [22.03, 86.18, 14.21, 83.25], [21.15, 88.58, 12.37, 80.15], [21.46, 85.93, 14.6, 84.03]
]

labels = [5, 5, 5, 5,
		  5, 5, 12, 5,
		  5, 12, 12, 5,
		  5, 5, 5, 5,
		  12, 12, 5, 12,
		  12, 12, 12, 5,
		  12, 5, 5, 12,
		  5, 5, 12, 5,
		  12, 5, 5, 5,
		  12, 5, 12, 12,
		  5, 12, 5, 12
]

correct = 0
total_tested = 0
for i in range(0,1000):	
	X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=.2, random_state=i, stratify=labels)

	# print X_test, "\n", y_test

	index = 0
	total = 0

	# clf = tree.DecisionTreeClassifier()
	clf = linear_model.LogisticRegression()
	# clf = xgb.XGBClassifier()
	# clf = clf.fit(np.array(features),np.array(labels))

	clf = clf.fit(np.array(X_train), np.array(y_train))

	for element in X_test:
		prediction = clf.predict(np.array(element).reshape(1,-1))
		# print prediction, y_test[index]
		if prediction == y_test[index]:
			correct +=1 
		index +=1
		total_tested+=1


print "Accuracy: ", correct/float(total_tested)


# print clf.predict(sys.argv[1], sys.argv[2])

# print clf.predict([[float(sys.argv[1]), float(sys.argv[2])]])

# 2018
# print clf.predict(np.array([[20.44, 88.22, 14.70, 82.16]])), 5
# print clf.predict(np.array([[21.16, 86.49, 10.20, 78.54]])), 5
# print clf.predict(np.array([[22.44, 90.26, 12.19, 78.60]])), 5
# print clf.predict(np.array([[21.65, 86.70, 12.92, 80.06]])), 5

# # 2012
# #print clf.predict(np.array([[22.36, 87.37, 13.45, 75.62]])), 12
# #print clf.predict(np.array([[19.45, 80.06, 69.14, 15.27]])), 5
# #print clf.predict(np.array([[20.90, 79.14, 14.34, 74.74]])), 5
# # print clf.predict(np.array([[14.49, 78.48, 13.13, 65.56]])), 12

# # 2011
# # print clf.predict(np.array([[20.11, 86.63, 18.16, 84.09]])), 5
# # print clf.predict(np.array([[19.65, 88.35, 6.98, 79.94]])), 5
# # print clf.predict(np.array([[17.33, 84.59, 16.01, 84.88]])), 12
# # print clf.predict(np.array([[17.42, 85.22, 19.32, 85.01]])), 5

# #2010
# print clf.predict(np.array([[20.12, 86.33, 15.92, 84.86]])), 12
# print clf.predict(np.array([[20.13, 87.59, 6.03, 77.18]])), 5
# print clf.predict(np.array([[22.45, 89.57, 16.53, 83.76]])), 5
# print clf.predict(np.array([[21.33, 87.28, 19.9, 83.33]])), 5
