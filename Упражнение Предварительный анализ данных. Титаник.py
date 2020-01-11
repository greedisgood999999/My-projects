import pandas as pd


data = pd.read_csv('C:\\Users\\Сергей\\Desktop\\ДУШИМ ЗМЕЮ\\DATA SCIENCE BITCH!\\mail.ru\\data\\titanic_train.csv',
                  index_col='PassengerId')
# посмотреть верхние пять строк
print(data.head(5))
# посмотреть основные статистические шутки
print(data.describe())
# отобрать людей, которые сели в С и заплатили больше 200
print(data[(data['Embarked'] == 'C') & (data['Fare'] > 200)].head(5))
# отсортировать их по убыванию платы за билет
print(data[(data['Embarked'] == 'C') & (data['Fare'] > 200)].sort_values(by='Fare', ascending=False).head(5), '\n')

# ПРАКТИКА
# посчитаем количество мужчин и женщин на борту
print('На борту было', data[data['Sex'] == 'male']['Sex'].count(), 'мужчин')
print('На борту было', data[data['Sex'] == 'female']['Sex'].count(), 'женщин\n')

# найдем мужчин, которые купили каюты второго класса
print(data[(data['Sex'] == 'male') & (data['Pclass'] == 2)]['Pclass'].count(), 'мужчин взяло каюты второго класса\n')

# найдем медиану и cтандартное отклонение платежей
print('Медиана цен за билет:', data['Fare'].median())
print('Стандартное отклонение:', data['Fare'].std(), '\n')

# Правда ли, что люди моложе 30 лет выживали чаще, чем люди старше 60 лет?
print('Люди моложе 30 выживали чаще, чем люди старше 60:',
      data[(data['Age'] < 30) & (data['Survived'] == 1)]['Survived'].count() >
      data[(data['Age'] > 60) & (data['Survived'] == 1)]['Survived'].count(), '\n')

# найдем доли выживших
print('Выжило среди молодых:',
      data[(data['Age'] < 30) & (data['Survived'] == 1)]['Survived'].count() /
      data[data['Age'] < 30]['Survived'].count() * 100, '%')
print('Выжило среди старых:',
      data[(data['Age'] > 60) & (data['Survived'] == 1)]['Survived'].count() /
      data[data['Age'] > 60]['Survived'].count() * 100, '%', '\n')

# Правда ли, что женщины выживали чаще мужчин?
print('Женщины выживали чаще мужчин:',
      data[(data['Sex'] == 'female') & (data['Survived'] == 1)]['Survived'].count() >
      data[(data['Sex'] == 'male') & (data['Survived'] == 1)]['Survived'].count(), '\n')

# найдем доли выживших
print('Выжило среди женщин:',
      data[(data['Sex'] == 'female') & (data['Survived'] == 1)]['Survived'].count() /
      data[data['Sex'] == 'female']['Survived'].count() * 100, '%')
print('Выжило среди мужчин:',
      data[(data['Sex'] == 'male') & (data['Survived'] == 1)]['Survived'].count() /
      data[data['Sex'] == 'male']['Survived'].count() * 100, '%', '\n')

# самое популярное имя среди мужчин
first_names = {}
for i in data[data['Sex'] == 'male']['Name']:
    if i.split()[2] in first_names:
        first_names[i.split()[2]] += 1
    else:
        first_names[i.split()[2]] = 1
m = max(first_names.values())
for name, freq in first_names.items():
    if freq == m:
        print('Самое популярное мужское имя на корабле:', name, '\n')

# Cредний возраст погибших выше спасенных, верно?
print('Средний возраст погибших выше спасенных:',
      data[data['Survived'] == 0]['Age'].mean() > data[data['Survived'] == 1]['Age'].mean(), '\n'
      )

# Выберите верные утверждения
print('Средний возраст мужчины 1-го класса больше 40:',
      data[(data['Sex'] == 'male') & (data['Pclass'] == 1)]['Age'].mean() > 40
      )
print('Средний возраст женщины 1-го класса больше 40:',
      data[(data['Sex'] == 'female') & (data['Pclass'] == 1)]['Age'].mean() > 40
      )
q = True
for cls in range(1, 4, 1):
    q = q and (data[(data['Sex'] == 'male') & (data['Pclass'] == cls)]['Age'].mean() >
                data[(data['Sex'] == 'female') & (data['Pclass'] == cls)]['Age'].mean())
print('Мужчины всех классов старше женщин того же класса:', q)
print('В среднем люди в 1 классе старше, чем люди во 2-ом, а те старше представителей 3-го класса:',
      data[data['Pclass'] == 1]['Age'].mean() >
      data[data['Pclass'] == 2]['Age'].mean() >
      data[data['Pclass'] == 3]['Age'].mean()
      )
