# Pandas Dataframe Styler
- [visual styling of a DataFrame](https://pandas.pydata.org/pandas-docs/version/1.1/user_guide/style.html) / [visualization of tabular data using the Styler class](https://pandas.pydata.org/pandas-docs/stable/user_guide/style.html)
- [left align the first column and center align the other two columns in a Pandas table](https://stackoverflow.com/questions/59453091/left-align-the-first-column-and-center-align-the-other-columns-in-a-pandas-table)
```
import pandas as pd
df = pd.DataFrame({'Unit': ['Bit', 'Nibble','Byte/Octet', 'Kilobyte', 'Megabyte', 'Gigabyte', 'Terabyte'], 'Abbreviation': ['b', '-', 'B', 'KB', 'MB', 'GB', 'TB'], 'Storage': ['Binary digit, single 0 or 1', '4 bits', '8 bits', '1024 bytes', '1024 KB', '1024 MB', '1024 GB']})
dfStyler = df.style.set_properties(subset=["Abbreviation", "Storage"],**{'text-align': 'center'})
dfStyler = df.style.set_properties(subset=["Unit"],**{'text-align': 'left'})
dfStyler.set_table_styles([dict(selector='th', props=[('text-align', 'center')])])

display(dfStyler.hide_index())
```
- [Apply a CSS-styling function to the index or column headers, level-wise](https://pandas.pydata.org/docs/reference/api/pandas.io.formats.style.Styler.apply_index.html)

# Pandas dataframe to image
- [Crop transparent background using Python(pillow)](https://stackoverflow.com/questions/67665915/cut-transparent-background-using-pythonpillow)
- [pandas to_html using the .style options or custom CSS?](https://stackoverflow.com/questions/36897366/pandas-to-html-using-the-style-options-or-custom-css)
- [Export pandas Styled table to image file with IMGkit](https://stackoverflow.com/questions/45664519/export-pandas-styled-table-to-image-file)
- [Convert styled dataframe to image with dataframe-image / alternatives](https://stackoverflow.com/questions/71955001/option-for-dataframe-image-module-convert-a-styled-dataframe-to-image-that-the) / [dataframe_image has a dependency on Chrome, and a recent Chrome update broke dataframe_image](https://stackoverflow.com/questions/75135530/error-exporting-styled-dataframes-to-image-syntaxerror-not-a-png-file-using)

# Working with Pandas Dataframes
- [pandas.DataFrame.sort_values](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.sort_values.html)
- [How to set Column as Index in Pandas DataFrame?](https://pythonexamples.org/pandas-set-column-as-index/#:~:text=To%20set%20a%20column%20as,index%2C%20to%20set_index()%20method.)
- [Drop specific rows from multiindex Pandas Dataframe](https://www.geeksforgeeks.org/drop-specific-rows-from-multiindex-pandas-dataframe/?ref=rp)
- [MultiIndex / advanced indexing](https://pandas.pydata.org/pandas-docs/version/1.2.0/user_guide/advanced.html)
- [How to extract the index names of a multiindexed dataframe?](https://stackoverflow.com/questions/41674992/how-to-extract-the-index-names-of-a-multiindexed-dataframe)
- [Prepend a level to a pandas MultiIndex](https://stackoverflow.com/questions/14744068/prepend-a-level-to-a-pandas-multiindex)
- [How to set the name of multiindex?](https://stackoverflow.com/questions/49505080/python-pandas-how-to-set-the-name-of-multiindex)
- [How to select top N of two groups and aggregate the rest of the second group into "Others" with Pandas?](https://stackoverflow.com/questions/67720054/how-to-select-top-n-of-two-groups-and-aggregate-the-rest-of-the-second-group-int)
- [Pandas groupby() and sum() With Examples](https://sparkbyexamples.com/pandas/pandas-groupby-sum-examples/)
```
# Use GroupBy() to compute the sum
df2 = df.groupby('Courses').sum()
print(df2)

# Use GroupBy() & compute sum on specific column
df2 = df.groupby('Courses')['Fee'].sum()
print(df2)

# Using GroupBy multiple column
df2 = df.groupby(['Courses','Duration'])['Fee'].sum()
print(df2)

# Groupby and get sum() and count()
df2 = df.groupby('Courses')['Fee'].agg(['sum','count'])
print(df2)

# Pandas groupby get sum() and count()
df2 = df.groupby('Courses').agg({'Fee': ['sum','count']})
print(df2)

# Remove sorting on grouped results
df2=df.groupby(by=['Courses'], sort=False).sum()
print(df2)

# Sorting group keys on descending order
groupedDF = df.groupby('Courses',sort=False).sum()
sortedDF=groupedDF.sort_values('Courses', ascending=False)
print(sortedDF)
```

