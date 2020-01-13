import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


data = pd.read_csv(r'C:\Users\Сергей\Desktop\ДУШИМ ЗМЕЮ\DATA SCIENCE BITCH!\mail.ru\data\titanic_train.csv')
print(data.head(2))
print(data.describe(include='all'))
print(data.info())
data = data.drop('Cabin', axis=1).dropna()
print(data.info())
print(data.columns)

feat = ['Age', 'Fare', 'Pclass', 'Sex', 'SibSp', 'Parch', 'Embarked', 'Survived']
sns.pairplot(data[feat])
plt.show()

fare_pclass1 = data[data['Pclass'] == 1]['Fare']
fare_pclass2 = data[data['Pclass'] == 2]['Fare']
fare_pclass3 = data[data['Pclass'] == 3]['Fare']
fare_pclass1_no_out = fare_pclass1[fare_pclass1.apply(lambda x: abs(fare_pclass2.mean()-x)) < 2 * fare_pclass1.std()]
fare_pclass2_no_out = fare_pclass2[fare_pclass2.apply(lambda x: abs(fare_pclass2.mean()-x)) < 2 * fare_pclass2.std()]
fare_pclass3_no_out = fare_pclass3[fare_pclass3.apply(lambda x: abs(fare_pclass3.mean()-x)) < 2 * fare_pclass3.std()]
data['Fare_no_out'] = fare_pclass1_no_out.append(fare_pclass2_no_out).append(fare_pclass3_no_out)
sns.boxplot(x='Pclass', y='Fare_no_out', data=data)
plt.show()

sns.countplot(hue='Sex', x='Survived', data=data)
plt.show()

sns.countplot(hue='Pclass', x='Survived', data=data)
plt.show()

for i in data['Age'].index:
    if data['Age'][i] < 30:
        data['Age'][i] = 'Young'
    elif 30 < data['Age'][i] < 60:
        data['Age'][i] = 'Middle'
    else:
        data['Age'][i] = 'Old'
sns.countplot(hue='Age', x='Survived', data=data)
plt.show()
