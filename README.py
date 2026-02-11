import urllib.parse, os
import pandas  as    pd
# Configuration
DATA      ='https://github.com/kauefs/DS/raw/refs/heads/@/datasets/tourismBR.csv'
README    ='README.md'
STATE_FILE='img/last_year.txt'
# Load Data & Calculate Metrics
try:
    df=pd.read_csv(DATA)
    df['arrivals']=pd.to_numeric(df['arrivals'], errors='coerce').fillna(0)
    latest_year   =int(df['year'].max( ))
    # Check if it needs to update
    if os.path.exists(STATE_FILE):
        with open    (STATE_FILE,'r')as f:last_recorded_year=int(f.read( ).strip( ))
        if latest_year <= last_recorded_year:
            print(f'Stats already up to date for {latest_year}; skipping update…')
            exit(0) # Exit successfully without error
    prev_year     =latest_year   -    1
    total_latest  =df[df['year']==latest_year]['arrivals'].sum( )
    total_2019    =df[df['year']==       2019]['arrivals'].sum( )
    total_prev    =df[df['year']==  prev_year]['arrivals'].sum( )
    yoy_growth    =((total_latest - total_prev)/total_prev)*100 # if total_prev > 0 else 0
    recovery      =((total_latest - total_2019)/total_2019)*100
    def get_url(label, msg, color):return f'https://img.shields.io/badge/{urllib.parse.quote(label)}-{urllib.parse.quote(msg)}-{color}?style=flat'
    yoy_color     ='00CD00' if yoy_growth > 0 else 'D22128'
    badges        =(f"![Arrivals ]({get_url(f'Arrivals in {latest_year}',f'{total_latest:,.0f}' ,'808080')})\n\n"
                    f"![YoYgrowth]({get_url( 'Year-over-Year Growth'    ,f'{yoy_growth:+.2f}%', yoy_color)})\n\n"
                    f"![Recovery ]({get_url( 'Recovery from COVID-19'   ,f'{recovery:+.2f}%','0077B5')})")
except Exception as e:
    print(f'Calculation Error: {e}')
    exit(1)
# Safe Reconstruction Logic
if os.path.exists(README):
    with open    (README,'r', encoding='utf-8')as f:full_text=f.read( )
    # Define core tags to look for specifically
    START_TAG='### Live Stats'
    DIV_OPEN ='\n<div align=center>\n'
    DIV_CLOSE='\n</div>\n'
    HR_TAG   ='---'
    if START_TAG in full_text and HR_TAG in full_text:
        # Split header to keep everything above it
        parts_above=full_text.split(START_TAG)
        header     =parts_above[0]+ START_TAG
        # Split horizontal rule to keep everything below it
        parts_below=full_text.split(HR_TAG)
        footer     =HR_TAG +parts_below[-1]
        # Reconstruct with clean spacing
        new_content=[header,'\n'+DIV_OPEN+'\n', badges,'\n'+DIV_CLOSE+'\n', footer]
        new_readme =''.join(new_content)
        with open(README,'w', encoding='utf-8')as f:f.write(new_readme)
        print('Success: README updated with flexible markers.')
    else:
        print(f'Error: Could not find "{START_TAG}" or "{HR_TAG}" in README.md')
        exit(1)
