import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_excel("testdata.xlsx")

print("-------------read first sheet-------------------")
print(df)

df_sheet_index = pd.read_excel("testdata.xlsx", sheet_name=1)
print("-------------read sheet via index-------------------")
print(df_sheet_index)

df_sheet_name = pd.read_excel("testdata.xlsx", sheet_name="Tabelle2")
print("-------------read sheet via name-------------------")
print(df_sheet_name)

df_sheet_multi = pd.read_excel("testdata.xlsx", sheet_name=[0, 1])
print("-------------read multiple sheets-------------------")
print(df_sheet_multi)

print("-------------address sheet in  multiple sheets dataframe-------------------")
# ---------find column name------------
# print(df_sheet_multi[0].columns.str.match("A"))
# -----------drop column (2 methods)------------------------
# df_sheet_multi[0] = df_sheet_multi[0].loc[:,~df_sheet_multi[0].columns.str.match("Unnamed")]
#
df_sheet_multi[0] = df_sheet_multi[0].drop("Unnamed: 0",axis=1)
df_sheet_multi[1] = df_sheet_multi[1].drop("Unnamed: 0",axis=1)
print(df_sheet_multi[0])
print(df_sheet_multi[1])

# ---------print to csv-----------
# df.to_csv('out.csv')

# -------------------------add data frames, change types---------------------
dfnew = df_sheet_multi[0].add(df_sheet_multi[1], fill_value=0)

print("--------------add column, add 2 data frames------------------")
dfnew["E"] = (3, 2, 1)
dfnew = dfnew.astype(int)
print(dfnew)
print(dfnew.dtypes)

print("-------------------mean function on whole df----------------")
print(dfnew.mean())

print("-------------------manual mean column A----------------")
meanA = (dfnew.iat[0,0] + dfnew.iat[1,0] + dfnew.iat[2,0]) / 3
print(meanA)

print("----------dataframe.info()------------------")
print(dfnew.info())

print("----------Number of rows, columns------------------")
print(str(len(dfnew)) + ", " + str(len(dfnew.columns)))

print("----------shape and size------------------")
print("df.shape: " + str(dfnew.shape))
print("df.size: " + str(dfnew.size))

print("-------------------some manipulations-----------------------")
dfnewbool = dfnew[dfnew > 70]

dfnewbool.iat[1,4] = 76
dfnewbool.iat[2,4] = 77
dfnewbool.iat[1,3] = 66
dfnewbool.iat[2,3] = 67
print(dfnewbool)
print(pd.isna(dfnewbool))

print(dfnewbool.dropna())


print("------------------plotting----------------")
plt.close("all")
ts = pd.Series(np.random.randn(1000), index=pd.date_range("1/1/2000", periods=1000))
print(ts)
print(ts.cumsum())

ts = ts.cumsum()

# ----------------------print html table------------------------
print(dfnewbool.to_html())
with open("test.html", "w") as file_out:
    print(dfnewbool.to_html(), file=file_out)

# -----------------------print plot----------------------------
fig = ts.plot().get_figure()
fig.savefig('test.png')