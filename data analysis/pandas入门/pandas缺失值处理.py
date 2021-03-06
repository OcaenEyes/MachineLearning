#pandas缺失值处理

import numpy as np
import pandas as pd

# 1、什么是缺失值
## 缺失值，表示的是"缺失的数据"
### 示例
index = pd.Index(data=["A", "B", "C", "D", "E", "F"], name="name")

data = {
    "age": [18, 30, np.nan, 40, np.nan, 30],
    "city": ["BeiJing", "ShangHai", "GuangZhou", "ShenZhen", np.nan, " "],
    "sex": [None, "male", "female", "male", np.nan, "unknown"],
    "birth": ["2000-02-10", "1988-10-17", None, "1978-08-08", np.nan, "1988-10-17"],

}

user_info = pd.DataFrame(data=data,index=index)
print(user_info)

print('-------------------------------------------------')
#### 将出生日期转为时间戳 to_datetime
user_info["birth"] =pd.to_datetime(user_info.birth)
print(user_info)
print('-------------------------------------------------')
# None ,np.nan ,NaT 在pandas内均为缺失值
#### 识别哪些是缺失值， 哪些是非缺失值 isnull() 或 notnull()
print(user_info.isnull())
print('-------------------------------------------------')
print(user_info.notnull())
print('-------------------------------------------------')

#### 过滤到值缺失的行
print(user_info[user_info.age.notnull()])
print('-------------------------------------------------')


# 2、丢弃缺失值
# dropna
## Series内
print(user_info.age.dropna())
print('-------------------------------------------------')

## DataFrame内 丢弃缺失值，需要多种参数
### axis参数，控制行／列， axis=0(默认) 表示行， axis=1，表示列
### how参数，any(默认) ／all ； any 表示一行／列有任意元素为空时即丢弃； all表示一行／列 全部为空时丢弃
### subset 参数表示删除时，只考虑的索引或者列名
### thresh 参数，类型为整数，比如thresh=3，会在一行/列中至少有 3 个非空值时将其保留

##### 一行数据只要有一个字段为空值即删除
print(user_info.dropna(axis=0,how="any"))
print('------------------------')

#### 一行数据所有字段都为空值才删除
print(user_info.dropna(axis=0,how="all"))
print('-------------------------')
#### 一行数据中只要city/sex 存在空值即删除
print(user_info.dropna(axis=0,how="any",subset=["city","sex"]))
print('-------------------------')

# 3、填充缺失值
## 常使用fillna填充缺失值
### 使用标量填充
print(user_info.age.fillna(0))
print('---------------------')
### 使用前一个有效值来填充 method='pad' / method='ffill'
print(user_info.age.fillna(method='pad'))
print('------------------')

### 使用后一个有效值来填充 method='bfill' / method='backfill'
print(user_info.age.fillna(method='backfill'))
print('--------------------')

### 使用interpolate 来填充，默认情况使用线性差值
print(user_info.age.interpolate())
print('-------------------------')

# 4、替换缺失值
## 某些异常值也被视作 缺失值来处理; unknown 也被视作缺失值 ; 有时候出现空白字符串，也被视作缺失值
## Series
## 使用replace替换缺失值
print(user_info.age.replace(40,np.nan))
print('-------------------------')
## 也可以指定一个映射字典
print(user_info.age.replace({40:np.nan}))
print('-------------------------')

## DataFrame
## 指定每列需要替换的值
print(user_info.replace({"age":40,"birth":pd.Timestamp("1978-08-08")},np.nan))

# 5、使用其他对象填充
## 可以将没有缺失值的series中的元素传给有缺失值的
age_new = user_info.age.copy()
age_new.fillna(20,inplace=True)
print(age_new)
print('-----------------')

print(user_info.age.combine_first(age_new))