import pandas as pd


data = pd.read_csv('C:\\Users\\Сергей\\Desktop\\ДУШИМ ЗМЕЮ\\DATA SCIENCE BITCH!\\mail.ru\\data\\adult.data.csv')

# Сколько мужчин и женщин представленно в этом наборе данных?
print('В этом наборе данных', data[data['sex'] == 'Male']['age'].count(), 'мужчин')
print('В этом наборе данных', data[data['sex'] == 'Female']['age'].count(), 'женщин', '\n')

# Cредний возраст женщин?
print('Средний возраст женщин', data[data['sex'] == 'Female']['age'].mean())

# Доля граждан Германии
print('Граждан Германии', data[data['native-country'] == 'Germany']['age'].count() /
                            data['age'].count() * 100, '%')

# средние и среднеквадратичные отклонения возраста тех, кто получает более 50K в год
print('Возраст тех, кто получает больше 50К в год', data[data['salary'] == '>50K']['age'].mean(), '+-',
      data[data['salary'] == '>50K']['age'].std()
      )
# средние и среднеквадратичные отклонения возраста тех, кто получает менее 50K в год
print('Возраст тех, кто получает меньше 50К в год', data[data['salary'] == '<=50K']['age'].mean(), '+-',
      data[data['salary'] == '<=50K']['age'].std()
      )

# Правда ли, что люди, которые получают больше 50k, имеют как минимум высшее образование?
good_education = ('Bachelors', 'Prof-school', 'Assoc-acdm', 'Assoc-voc', 'Masters', 'Doctorate')
print('Люди, которые получают больше 50k, имеют как минимум высшее образование: ', end='')
for edu_lvl in data[(data['salary'] == '>50K')]['education']:
    if edu_lvl not in good_education:
        print(False)
        break
else:
    print(True)

# Каков максимальный возраст мужчин расы Amer-Indian-Eskimo?
print('Максимальный возраст мужчин расы Amer-Indian-Eskimo',
      max(list(data[(data['race'] == 'Amer-Indian-Eskimo') & (data['sex'] == 'Male')]['age'])))

# Среди кого больше доля зарабатывающих много (>50K): среди женатых или холостых мужчин?
married = ('Married-civ-spouse', 'Married-spouse-absent', 'Married-AF-spouse')
m = nm = 0
for status in data[(data['sex'] == 'Male') & (data['salary'] == '>50K')]['marital-status']:
    if status in married:
        m += 1
    else:
        nm += 1
print('Среди мужчин, которые зарабатывают более 50К больше женатых:', (m/(m+nm)) > (nm/(m+nm)))

# Какое максимальное число часов человек работает в неделю?
# Сколько людей работают такое количество часов и каков среди них процент зарабатывающих много?
maximum = max(list(data['hours-per-week']))
print('Максимальное число часов работы в неделю', maximum)
print('Всего', maximum, 'часов в неделю работает', data[data['hours-per-week'] == maximum]['age'].count(), 'человек')
print('Из них богатых', data[(data['hours-per-week'] == maximum) & (data['salary'] == '>50K')]['age'].count() /
      data[data['hours-per-week'] == maximum]['age'].count() * 100, '%')

# Cреднее время работы при разной зарплате в Японии
print('Среднее время работы японца с маленькой зарплатой',
      data[(data['salary'] == '<=50K') & (data['native-country'] == 'Japan')]['hours-per-week'].mean(),
      '\nСреднее время работы японца с большой зарплатой',
      data[(data['salary'] == '>50K') & (data['native-country'] == 'Japan')]['hours-per-week'].mean()
      )
