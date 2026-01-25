import urllib.parse, os
import pandas  as    pd
# 1. Configuration
DATA      = 'https://github.com/kauefs/DS/raw/refs/heads/@/datasets/tourismBR.csv'
README    = 'README.md'
START     = ''
END       = ''
def get_badge_url(label, msg, color):
    l_enc = urllib.parse.quote(label)
    m_enc = urllib.parse.quote(msg)
    return f"https://img.shields.io/badge/{l_enc}-{m_enc}-{color}?style=flat-square"
# 2. Load Data & Calculate Metrics
try:
    df = pd.read_csv(DATA)
    df['arrivals']=pd.to_numeric(df['arrivals'], errors='coerce').fillna(0)
    latest_year   =int(df['year'].max( ))
    prev_year     = latest_year  -    1
    total_latest  =df[df['year']==latest_year]['arrivals'].sum( )
    total_prev    =df[df['year']==  prev_year]['arrivals'].sum( )
    total_2019    =df[df['year']==       2019]['arrivals'].sum( )
    yoy_growth    =((total_latest - total_prev)/total_prev)*100
    recovery      =((total_latest - total_2019)/total_2019)*100
    # Format the badge strings
    yoy_color     ="brightgreen" if yoy_growth > 0 else "red"
    badges        =(f"![Arrivals]({get_badge_url(f'Arrivals {latest_year}', f'{total_latest:,.0f}', '6D6E71')}) "
                    f"![YoY]({get_badge_url('YoY Growth', f'{yoy_growth:+.2f}%', yoy_color)}) "
                    f"![Recovery]({get_badge_url('vs 2019', f'{recovery:+.2f}%', 'blue')})")
except Exception as e:
    print(f"Calculation Error: {e}")
    exit(1)
# 3. Reconstruct README.md (The "Safe Sweep" Method)
if os.path.exists(README):
    with open    (README,'r', encoding='utf-8')as f:full_text=f.read( )
    if START in full_text and END in full_text:
        # We split the file into three pieces: 
        # 1. Everything before the START_TAG
        # 2. Everything after the END_TAG
        # We discard whatever was in the middle (the old badges)
        header=full_text.split(START)[0]
        footer=full_text.split (END)[-1]
        # Assemble fresh: No nesting, no repetition
        readme=f"{header}{START}\n<div align=center>\n\n{badges}\n\n</div>\n{END}{footer}"
        with open(README,'w', encoding="utf-8")as f:f.write(readme)
        print("Success: README reconstructed and metrics updated.")
    else:
        print(f"Error: Markers not found. Ensure {START} and {END} are in README.md")
        exit(1)
else:
    print("Error: README.md not found in root directory.")
    exit(1)
