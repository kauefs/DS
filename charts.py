import                      os
import pandas            as pd
import matplotlib.pyplot as plt
# Configuration
DATA      ='https://github.com/kauefs/DS/raw/refs/heads/@/datasets/tourismBR.csv'
DIR       ='img'
STATE_FILE='img/last_year.txt'
def get_latest_year(df):return int(df['year'].max( ))
def should_update(current_max_year):
    if not os.path.exists(STATE_FILE):return True
    with open(STATE_FILE,'r')as f:last_year=int(f.read( ).strip( ))
    return current_max_year >     last_year
def charts(df):
    if not os.path.exists(DIR):os.makedirs(DIR)
    # Example: Annual Time Series
    fig,ax=plt.subplots(figsize=(10, 6))
    df.groupby('year')['arrivals'].sum( ).plot(kind='line', ax=ax)
    plt.savefig(f'{DIR}/AnnualTimeSeries.png')
    plt.close(fig)
    # ... add your other 3 charts here ...
if __name__=='__main__':
    df=pd.read_csv(DATA)
    df['arrivals']=pd.to_numeric(df['arrivals'], errors='coerce').fillna(0)
    current_year=get_latest_year(df)
    if should_update(current_year):
        print(f'New year detected ({current_year}). Updating charts…')
        save_charts(df)
        # Update the state file
        with open(STATE_FILE,'w')as f:f.write(str(current_year))
    else:
        print(f'Max year ({current_year}) has not changed. Skipping chart update.')
