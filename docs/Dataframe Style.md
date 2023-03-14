

[left align the first column and center align the other two columns in a Pandas table](https://stackoverflow.com/questions/59453091/left-align-the-first-column-and-center-align-the-other-columns-in-a-pandas-table)

```
import pandas as pd
df = pd.DataFrame({'Unit': ['Bit', 'Nibble','Byte/Octet', 'Kilobyte', 'Megabyte', 'Gigabyte', 'Terabyte'], 'Abbreviation': ['b', '-', 'B', 'KB', 'MB', 'GB', 'TB'], 'Storage': ['Binary digit, single 0 or 1', '4 bits', '8 bits', '1024 bytes', '1024 KB', '1024 MB', '1024 GB']})
dfStyler = df.style.set_properties(subset=["Abbreviation", "Storage"],**{'text-align': 'center'})
dfStyler = df.style.set_properties(subset=["Unit"],**{'text-align': 'left'})
dfStyler.set_table_styles([dict(selector='th', props=[('text-align', 'center')])])

display(dfStyler.hide_index())
```
