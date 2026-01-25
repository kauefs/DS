import urllib.parse, os
import pandas  as    pd

# 1. Configuration
DATA      = 'https://github.com/kauefs/DS/raw/refs/heads/@/datasets/tourismBR.csv'
README    = 'README.md'

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
    
    def get_url(label, msg, color):
        return f"https://img.shields.io/badge/{urllib.parse.quote(label)}-{urllib.parse.quote(msg)}-{color}?style=flat-square"

    yoy_color = "brightgreen" if yoy_growth > 0 else "red"
    badges = (
        f"![Arrivals]({get_url(f'Arrivals {latest_year}', f'{total_latest:,.0f}', '6D6E71')}) "
        f"![YoY]({get_url('YoY Growth', f'{yoy_growth:+.2f}%', yoy_color)}) "
        f"![Recovery]({get_url('vs 2019', f'{recovery:+.2f}%', 'blue')})"
    )
except Exception as e:
    print(f"Calculation Error: {e}")
    exit(1)

# 3. Safe Reconstruction Logic
if os.path.exists(README):
    with open(README, 'r', encoding='utf-8') as f:
        full_text = f.read()

    # DO NOT CHANGE THESE STRINGS
    S_MARKER = ''
    E_MARKER = ''

    if S_MARKER in full_text and E_MARKER in full_text:
        # We use the literal strings here to avoid "empty separator" errors
        header = full_text.split(S_MARKER)[0]
        footer = full_text.split(E_MARKER)[-1]
        
        # Assemble
        new_readme = f"{header}{S_MARKER}\n<div align=center>\n\n{badges}\n\n</div>\n{E_MARKER}{footer}"
        
        with open(README, "w", encoding="utf-8") as f:
            f.write(new_readme)
        print("Success: README updated.")
    else:
        print(f"Error: Markers {S_MARKER} or {E_MARKER} not found in README.md")
        exit(1)
else:
    print("Error: README.md not found.")
    exit(1)
