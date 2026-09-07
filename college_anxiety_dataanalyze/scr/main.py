import pandas as pd
from pandas.core.reshape.pivot import crosstab

df=pd.read_excel(r'C:\Users\白玉琦\PycharmProjects\PythonProject\.venv\运动习惯与焦虑情绪现状调研.xlsx')
drop_columns=['序号', '提交答卷时间', '来源', '来源详情', '来自IP']
df=df.drop(columns=drop_columns)
##数据清洗
df['所用时间']=df['所用时间'].str.replace("秒","").astype(int)
df=df[df["所用时间"]>=15]
##数据文本编码
map_5 = {
    "0次":1,
    "1-2次":2,
    "2-3次":3,
    "3-4次":4,
    "4-5次":5,
    "5次及以上":6
}
df["5、每周运动次数（快走/跑步/球类/健身等）"] = df["5、每周运动次数（快走/跑步/球类/健身等）"].map(map_5)

# --------6题 单次运动时长--------
map_6 = {
    "30分钟以内":1,
    "30‑60分钟":2,
    "60分钟以上":3
}
df["6、单次运动时长"] = df["6、单次运动时长"].map(map_6)
# --------7题 容易心慌、烦躁--------
map_7 = {
    "完全没有":1,
    "偶尔":2,
    "经常":3,
    "总是":4
}
df["7、容易心慌、烦躁"] = df["7、容易心慌、烦躁"].map(map_7)


# --------8题 莫名担心很多事情--------
map_8 = {
    "完全没有":1,
    "偶尔":2,
    "经常":3,
    "总是":4
}
df["8、莫名担心很多事情"] = df["8、莫名担心很多事情"].map(map_8)


# --------9题 入睡困难，容易失眠--------
map_9 = {
    "完全没有":1,
    "偶尔":2,
    "经常":3,
    "总是":4
}
df["9、入睡困难，容易失眠"] = df["9、入睡困难，容易失眠"].map(map_9)

# --------10题 精神紧绷，难以放松--------
map_10 = {
    "完全没有":1,
    "偶尔":2,
    "经常":3,
    "总是":4
}
df["10、精神紧绷，难以放松"] = df["10、精神紧绷，难以放松"].map(map_10)
anxiety_cols=['7、容易心慌、烦躁', '8、莫名担心很多事情',
       '9、入睡困难，容易失眠', '10、精神紧绷，难以放松']
df['焦虑总分']=df[anxiety_cols].sum(axis=1)
##描述性统计
gender_anxiety=df.groupby("1、您的性别")["焦虑总分"].agg(
    ["count",
     'mean',
     'std',
     'min',
     'max' ]
).round(2)
sport_anxiety=df.groupby("5、每周运动次数（快走/跑步/球类/健身等）")['焦虑总分'].agg(
    ["count",
     'mean',
     'std',
     'min',
     'max'
     ]
).round(2)
##可视化
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
print(df["焦虑总分"])
anxiety_goal=df["焦虑总分"].dropna()
##焦虑总分直方图
plt.figure(figsize=(10,5))
plt.hist(anxiety_goal, bins=20,color="blue", edgecolor="black")
plt.title("焦虑总分直方分布图")
plt.xlabel("焦虑得分")
plt.ylabel("频率")
plt.grid(True)
##可视化直观图保存
plt.savefig("焦虑总分直方图分布.png",dpi=300,bbox_inches='tight')
##箱线图
import seaborn as sns
plt.figure(figsize=(10,5))
sns.boxplot(data=df,x="5、每周运动次数（快走/跑步/球类/健身等）",y="焦虑总分")
plt.title("不同的每周运动次数的焦虑总分箱线图")
plt.xlabel("每周运动次数编码")
plt.ylabel("焦虑总分")
plt.grid(axis="y",alpha=0.3)
##箱线图保存
plt.savefig("周运动频率_焦虑总分箱线图.png",dpi=300,bbox_inches='tight')
##清洗后数据保存
df.to_csv("clean_data.csv",index=False,encoding='utf-8')
##描述性统计结果保存
with pd.ExcelWriter('descriptive_stats.xlsx') as writer:
    gender_anxiety.to_excel(writer, sheet_name='性别分组')
    sport_anxiety.to_excel(writer, sheet_name='运动次数分组')











