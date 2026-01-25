import urllib.parse,re
import pandas  as   pd
# 1. Load Data
DATA='https://github.com/kauefs/DS/raw/refs/heads/@/datasets/tourismBR.csv'
df  = pd.read_csv(DATA)
# 2. Calculate Metrics
latest_year =df['year'].max( )
total_latest=df[df['year']==latest_year]['arrivals'].sum( )
# Calculating YoY Growth
prev_year   =latest_year -  1
total_prev  =df[df['year']==  prev_year]['arrivals'].sum( )
yoy_growth  =((total_latest -total_prev)/total_prev)*100
# total_2019  =df[df['year']==       2019]['arrivals'].sum( )
# recovery    =((total_latest -total_2019)/total_2019)*100
# 3. Formating strings for Badges
total_str   = f'{total_latest:,.0f}'
yoy_str     = f'{yoy_growth:+.2f}%'
yoy_color   = 'green' if yoy_growth > 0 else 'red'
# metrics_html = f'''
# | Metric | Value |
# | :----- | :---- |
# | **Total Arrivals ({latest_year})**                | {total_latest:,.0f}  |
# |     **YoY Growth ({latest_year} vs {prev_year})** |   {yoy_growth:+.2f}% |
# |                      **Recovery vs 2019**         |     {recovery:+.2f}% |
# '''
# 4. Create Shields.io Markdown
# Format: https://img.shields.io/badge/<LABEL>-<MESSAGE>-<COLOR>
def make_badge(label, message, color):
    label_enc=urllib.parse.quote(label)
    msg_enc  =urllib.parse.quote(message)
    return f'![{label}](https://img.shields.io/badge/{label_enc}-{msg_enc}-{color}?style=flat-square)'
badges       =(make_badge(f'Total Arrivals ({latest_year})', total_str,'blue')+ ' ' +make_badge('YoY Growth', yoy_str, yoy_color))
# 4. Inject into README
with open('README.md','r', encoding='utf-8') as f:content=f.read( )
# Replace content between markers
# new_content=re.sub(r'.*?', f'\n{metrics_html}\n', content, flags=re.DOTALL)
new_content=re.sub(r'.*?', f'\n{badges}\n', content, flags=re.DOTALL)
with open('README.md','w', encoding='utf-8') as f:f.write(new_content)
