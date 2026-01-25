import urllib.parse, os
import pandas  as    pd

# 1. Configuration - MUST MATCH README EXACTLY
DATA      = 'https://github.com/kauefs/DS/raw/refs/heads/@/datasets/tourismBR.csv'
README    = 'README.md'
START_TAG = ''
END_TAG   = ''

def get_badge_url(label, msg, color):
    l_enc = urllib.parse.quote(label)
    m_enc = urllib.parse.quote(msg)
    return f"https://img.shields.io/badge/{l_enc}-{m_enc}-{color}?style=flat-square"

# 2. Load Data & Calculate Metrics
try:
    df = pd.read_csv(DATA)
    df['arrivals'] = pd.to_numeric(df['arrivals'], errors='coerce').fillna(0)
    
    latest_year  = int(df['year'].max())
    total_latest = df[df['year'] == latest_year]['arrivals'].sum()
    total_2019   = df[df['year'] == 2019]['arrivals'].sum()

    prev_year    = latest_year - 1
    total_prev   = df[df['year'] == prev_year]['arrivals'].sum()
    yoy_growth   = ((total_latest - total_prev) / total_prev) * 100 if total_prev > 0 else 0
    recovery     = ((total_latest - total_2019) / total_2019) * 100
    
    yoy_color = "brightgreen" if yoy_growth > 0 else "red"
    badges = (
        f"![Arrivals]({get_badge_url(f'Arrivals {latest_year}', f'{total_latest:,.0f}', '6D6E71')}) "
        f"![YoY]({get_badge_url('YoY Growth', f'{yoy_growth:+.2f}%', yoy_color)}) "
        f"![Recovery]({get_badge_url('vs 2019', f'{recovery:+.2f}%', 'blue')})"
    )
except Exception as e:
    print(f"Calculation Error: {e}")
    exit(1)

# 3. Reconstruct README.md
if os.path.exists(README):
    with open(README, 'r', encoding='utf-8') as f:
        full_text = f.read()

    if START_TAG in full_text and END_TAG in full_text:
        # Split logic: header gets everything BEFORE the first tag, 
        # footer gets everything AFTER the last tag.
        header = full_text.split(START_TAG)[0]
        footer = full_text.split(END_TAG)[-1]
        
        # Assemble fresh content
        new_readme = f"{header}{START_TAG}\n<div align=center>\n\n{badges}\n\n</div>\n{END_TAG}{footer}"
        
        with open(README, "w", encoding="utf-8") as f:
            f.write(new_readme)
        print("README updated successfully.")
    else:
        print(f"Markers not found. Please add {START_TAG} and {END_TAG} to README.")
        exit(1)
else:
    print("README.md not found.")
    exit(1)
