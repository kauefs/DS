import           re
import pandas as pd
# 1. Load Data
DATA='https://github.com/kauefs/DS/raw/refs/heads/@/datasets/tourismBR.csv'
df  = pd.read_csv(DATA)
# 2. Calculate Metrics
latest_year =df['year'].max( )
prev_year   =latest_year -  1
total_latest=df[df['year']==latest_year]['arrivals'].sum( )
total_prev  =df[df['year']==  prev_year]['arrivals'].sum( )
total_2019  =df[df['year']==       2019]['arrivals'].sum( )
yoy_growth  =((total_latest -total_prev)/total_prev)*100
recovery    =((total_latest -total_2019)/total_2019)*100
# 3. Create Markdown Table
metrics_html = f'''
| Metric | Value |
| :----- | :---- |
| **Total Arrivals ({latest_year})**                | {total_latest:,.0f}  |
|     **YoY Growth ({latest_year} vs {prev_year})** |   {yoy_growth:+.2f}% |
|                      **Recovery vs 2019**         |     {recovery:+.2f}% |
'''
# 4. Update README.md
with open('README.md','r', encoding='utf-8') as f:content=f.read( )
# Replace content between markers
new_content=re.sub(r'.*?', f'\n{metrics_html}\n', content, flags=re.DOTALL)
with open('README.md','w', encoding='utf-8') as f:f.write(new_content)
