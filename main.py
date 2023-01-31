import pandas as pd

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
# df.to_csv('final_output.csv')

# -------------------------add data frames, change types---------------------
dfnew = df_sheet_multi[0].add(df_sheet_multi[1], fill_value=int(0)).astype(int)
print("--------------add 2 data frames------------------")
dfnew["E"] = (3, 2, 1)
print(dfnew)
print(dfnew.dtypes)