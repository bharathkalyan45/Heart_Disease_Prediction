import pandas as pd
import numpy as np

df = pd.read_csv("dataset.csv")

print("EDA for the Heart Disease Dataset")
print(df.info())
print("\n")
print(df.describe())
print("\n")
print(df.shape)
print("\n")
print(df.corr()['target'])

import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(20,15))
sns.heatmap(df.corr(),annot=True,cmap="coolwarm")
plt.title("Correlation of each columns with Target")
plt.show()

# finding outliers

for i in df.columns:
    Q1 = df[i].quantile(0.25)
    Q3 = df[i].quantile(0.75)
    IQR = Q3 - Q1

    outliers = df[(df[i] < Q1 - 1.5 * IQR) | (df[i] > Q3 + 1.5 * IQR)]
    print("\n")
    print("Outliers for each columns")
    print(i, len(outliers))

df = df.drop(columns=['sex', 'fasting blood sugar', 'resting ecg'], axis=1, errors='ignore')

# cleaning outliers with capping method

for i in df.columns:

    Q1 = df[i].quantile(0.25)
    Q3 = df[i].quantile(0.75)

    IQR = Q3 - Q1

    lower_limit = Q1 - 1.5 * IQR
    upper_limit = Q3 + 1.5 * IQR

    outliers = df[(df[i] < Q1 - 1.5 * IQR) | (df[i] > Q3 + 1.5 * IQR)]

    if len(outliers) > 0:
        df[i] = df[i].clip(lower=lower_limit, upper=upper_limit)

    outliers = df[(df[i] < Q1 - 1.5 * IQR) | (df[i] > Q3 + 1.5 * IQR)]
    print("\n")
    print("Outliers After Clipping")
    print(i, len(outliers))

X = df.drop('target', axis=1)
Y = df['target']

print("\n")
print("Checking if target is imbalanced")
print(Y.value_counts(normalize=True))

from sklearn.model_selection import train_test_split

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, train_size=0.7, random_state=42)

from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier

voting = VotingClassifier(estimators=[
    ('rfc', RandomForestClassifier(bootstrap=True)),
    ('xgb', XGBClassifier()),
    ('lgb', LGBMClassifier())
], voting="soft")

from sklearn.pipeline import Pipeline

pipe = Pipeline([
    ('voting', voting)
])

from scipy.stats import randint, uniform

param_dist = {
    "voting__rfc__n_estimators": [300, 500, 700],
    "voting__rfc__max_depth": [10, 20, 30],
    "voting__rfc__min_samples_split": [4, 8, 10, 20],
    "voting__rfc__max_samples": [None, 0.6, 0.7, 0.8, 0.9],
    "voting__rfc__min_samples_leaf": [1, 2, 5, 10],
    'voting__rfc__max_features': ['sqrt', 'log2', 0.5],

    'voting__xgb__n_estimators': randint(100, 600),
    'voting__xgb__max_depth': randint(3, 10),
    'voting__xgb__learning_rate': uniform(0.01, 0.2),
    'voting__xgb__subsample': uniform(0.6, 0.4),
    'voting__xgb__colsample_bytree': uniform(0.6, 0.4),
    'voting__xgb__min_child_weight': randint(1, 15),
    'voting__xgb__gamma': uniform(0, 1),
    'voting__xgb__reg_alpha': uniform(0, 1),
    'voting__xgb__reg_lambda': uniform(0.5, 2),

    "voting__lgb__n_estimators": randint(200, 800),
    "voting__lgb__learning_rate": uniform(0.01, 0.2),
    "voting__lgb__num_leaves": randint(20, 150),
    "voting__lgb__max_depth": randint(-1, 20),
    "voting__lgb__min_child_samples": randint(5, 50),
    "voting__lgb__subsample": uniform(0.6, 0.4),
    "voting__lgb__colsample_bytree": uniform(0.6, 0.4),
    "voting__lgb__reg_alpha": uniform(0, 1),
    "voting__lgb__reg_lambda": uniform(0.5, 2)
}

from sklearn.model_selection import RandomizedSearchCV

randomized = RandomizedSearchCV(
    estimator=pipe,
    param_distributions=param_dist,
    verbose=0,
    n_jobs=-1,
    n_iter=30,
    cv=5,
    scoring="roc_auc"
)

randomized.fit(X_train, Y_train)

Y_pred = randomized.predict(X_test)

from sklearn.metrics import accuracy_score, precision_score, recall_score
print("\n")
print("Accuracy_score", accuracy_score(Y_test, Y_pred))
print("Precision_Score",precision_score(Y_test, Y_pred))
print("recall_score",recall_score(Y_test, Y_pred))

import pickle
pickle.dump(randomized.best_estimator_, open("heart_disease.pkl", "wb"))