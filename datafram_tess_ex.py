import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import PIL
import pytesseract
import os


os.environ['TESSDATA_PREFIX'] = r'C:\Program Files (x86)\Tesseract-OCR\tessdata'

special_config = '--psm 12 --oem 1'
languages_ = "eng" # For multiple language use like "eng+rus+swe" and so on

image_path = "data/new_lb_rimini_croped.jpg" # Any image format will do
img_pl=PIL.Image.open(image_path) # You can use opencv for that option too

data = pytesseract.image_to_data(
                        img_pl,
                        lang=languages_,
                        output_type='data.frame',
                        config=special_config)

def optimizeDf(old_df: pd.DataFrame) -> pd.DataFrame:
    df = old_df[["left", "top", "width", "text"]]
    df['left+width'] = df['left'] + df['width']
    df = df.sort_values(by=['top'], ascending=True)
    df = df.groupby(['top', 'left+width'], sort=False)['text'].sum().unstack('left+width')
    df = df.reindex(sorted(df.columns), axis=1).dropna(how='all').dropna(axis='columns', how='all')
    df = df.fillna('')
    return df

data_imp_sort = optimizeDf(data)


def mergeDfColumns(old_df: pd.DataFrame, threshold: int = 10, rotations: int = 5) -> pd.DataFrame:
    df = old_df.copy()
    for j in range(0, rotations):
        new_columns = {}
        old_columns = df.columns
        i = 0
        while i < len(old_columns):
            if i < len(old_columns) - 1:
                # If the difference between consecutive column names is less than the threshold
                if any(old_columns[i + 1] == old_columns[i] + x for x in range(1, threshold)):
                    new_col = df[old_columns[i]].astype(str) + df[old_columns[i + 1]].astype(str)
                    new_columns[old_columns[i + 1]] = new_col
                    i = i + 1
                else:  # If the difference between consecutive column names is greater than or equal to the threshold
                    new_columns[old_columns[i]] = df[old_columns[i]]
            else:  # If the current column is the last column
                new_columns[old_columns[i]] = df[old_columns[i]]
            i += 1
        df = pd.DataFrame.from_dict(new_columns).replace('', np.nan).dropna(axis='columns', how='all')
    return df.replace(np.nan, '')


def mergeDfRows(old_df: pd.DataFrame, threshold: int = 10) -> pd.DataFrame:
    new_df = old_df.iloc[:1]
    for i in range(1, len(old_df)):
        # If the difference between consecutive index values is less than the threshold
        if abs(old_df.index[i] - old_df.index[i - 1]) < threshold:
            new_df.iloc[-1] = new_df.iloc[-1].astype(str) + old_df.iloc[i].astype(str)
        else:  # If the difference is greater than the threshold, append the current row
            new_df = new_df._append(old_df.iloc[i])
    return new_df.reset_index(drop=True)


df_new_col = mergeDfColumns(data_imp_sort)
merged_row_df = mergeDfRows(df_new_col)


def clean_df(df):
    # Remove columns with all cells holding the same value and its length is 0 or 1
    df = df.loc[:, (df != df.iloc[0]).any()]
    # Remove rows with empty cells or cells with only the '|' symbol
    df = df[(df != '|') & (df != '') & (pd.notnull(df))]
    # Remove columns with only empty cells
    df = df.dropna(axis=1, how='all')
    return df.fillna('')

cleaned_df = clean_df(merged_row_df.copy())