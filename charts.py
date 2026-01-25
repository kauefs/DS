import                          os
import     pandas          as   pd
import    seaborn          as   sns
import matplotlib.pyplot   as   plt
import matplotlib.cm       as   cm
import matplotlib.ticker   as   ticker
from   matplotlib.colors import Normalize
from   adjustText        import adjust_text
# Configuration
DATA      ='https://github.com/kauefs/DS/raw/refs/heads/@/datasets/tourismBR.csv'
DIR       ='img'
STATE_FILE='img/last_year.txt'
def load_data( ):
    df    = pd.read_csv(DATA)
    df['arrivals']=pd.to_numeric(df['arrivals'], errors='coerce').fillna(0)
    return df
def should_update(current_max_year):
    if not os.path.exists(STATE_FILE):return True
    with open(STATE_FILE,'r')as f:
        try:last_year=int(f.read( ).strip( ))
        except ValueError:return True
    return current_max_year > last_year
def save_heatmap(df):
    heatmap_data=df.groupby(['year','month'])['arrivals'].sum( ).reset_index( )
    heatmap_data['month']=pd.Categorical(heatmap_data['month'], categories=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'], ordered=True)
    pivot=heatmap_data.pivot_table(index='year', columns='month', values='arrivals', observed=False)
    fig,ax=plt.subplots(figsize=(12, 8), frameon=True, tight_layout=True)
    def fmt(x, pos):return f'{x/1e6:.1f}M' if x >= 1e6 else f'{x/1e3:.0f}K'
    sns.heatmap(pivot, cmap='RdYlGn_r', linewidths=.5, cbar_kws={'format':ticker.FuncFormatter(fmt)})
    plt.title('Monthly Arrivals Intensity per Year', fontsize=15, fontweight='bold')
    plt.ylabel('')
    plt.xlabel('')
    plt.yticks(fontsize=10, fontweight='semibold')
    plt.xticks(fontsize=10, fontweight='semibold')
    plt.tick_params(axis='both', which=    'both', length=0)
    plt.savefig(f'{DIR}/HeatMap.png')
    plt.close(fig)
def save_annual(df):
    annual =df.groupby('year')    ['arrivals']      .sum( ).reset_index( )
    values =annual['arrivals'].groupby(annual.index).sum( ).values
    norm   =Normalize (     annual['arrivals'].min( ), annual['arrivals'].max( ))
    palette=cm.viridis(norm(annual['arrivals'])).tolist( )
    fig, ax=plt.subplots(figsize=(15, 8), frameon=True, tight_layout=True)
    sns.barplot(x=annual.index, y='arrivals', data=annual, palette=palette, hue=values, saturation=.75, legend=False)
    plt.title('Annual InterNational Tourist Arrivals in Brazil ({}–{})'.format(annual['year'].min( ), annual['year'].max( )), fontsize=20, fontweight='bold')
    plt.xticks(fontsize=13 ,fontweight='semibold' ,          rotation='vertical'  )
    for spine in ax.spines.values( ):spine.set_visible(False)
    ax.yaxis.set_visible(False)
    plt.ylabel(None)
    plt.xlabel(None)
    plt.legend( [], frameon= False)
    plt.grid(       visible= False)
    for c in ax.containers:ax.bar_label(container=c, labels=values, fmt='{:,.0f}', fontsize=11, padding=-80, fontweight='bold', rotation='vertical', color='#FFFFFF')
    plt.savefig(f'{DIR}/AnnualTimeSeries.png')
    plt.close(fig)
def save_by_country(df):
    sort=df.groupby('country')['arrivals'].sum( ).sort_values(ascending=False)[:12]
    values=sort['arrivals'].groupby(sort.index, observed= True).sum( ).values
    fig,ax=plt.subplots(frameon=True, tight_layout=True)
    sns.barplot(x=sort.index, y='arrivals', data=sort, palette='Blues_r', hue=sort.index, saturation=.75, legend=False)
    plt.title('Top InterNational Tourist Arrivals in Brazil ({}–{}) by Country'.format(sort['year'].min( ), sort['year'].max( )),   fontsize=20, fontweight='bold')
    plt.yticks(fontsize=13, fontweight='semibold', rotation='horizontal')
    plt.xticks( [] )
    plt.ylabel(None)
    plt.xlabel(None)
    plt.legend( [], frameon= False)
    plt.grid(       visible= False)
    for spine in ax.spines.values( ):spine.set_visible(False)
    ax.xaxis.set_visible    (False)
    for c in ax.containers:ax.bar_label(container=c, labels=values, fmt='{:,.0f}', fontsize=11, padding=10, fontweight='bold', rotation='horizontal', color='#000000')
    plt.savefig(f'{DIR}/TopArrivals.png')
    plt.close(fig)
def save_timeseries(df, countries, filename, title):
    group =df.groupby(['country','year'])['arrivals'].sum( ).reset_index( )
    subset=group[group['country'].isin(countries)]
    piv   =subset.pivot_table(index='year', columns='country', values='arrivals')
    fig   =plt.figure(figsize=(10, 5), tight_layout=True)
    texts =[]
    colors=sns.color_palette('tab10', len(countries)) if len(countries) > 4 else ['#00BFFF','#FF4500','#0065FF','#4CAF50']
    for i, country in enumerate(countries):
        if country in piv.columns:
            plt.plot(piv.index, piv[country], label=country, color=colors[i], linewidth=2.25)
            y_end=piv[country].iloc[-1]
            texts.append(plt.annotate(f'{country} {y_end:,.0f}', xy=(piv.index[-1], y_end), color=colors[i], fontsize=8, fontweight='semibold'))
    adjust_text(texts, autoalign='y', only_move={'text':'y','static':'x'})
    plt.title(title, fontsize=15, fontweight='bold', loc='left')
    plt.yscale('log')
    plt.box(False)
    plt.savefig(f'{DIR}/{filename}.png')
    plt.close(fig)
if __name__=='__main__':
    if not os.path.exists(DIR): os.makedirs(DIR)
    df       =load_data( )
    max_year =int(df['year'].max( ))
    if should_update(max_year):
        print(f'Updating charts for: {max_year}')
        save_heatmap   (df)
        save_annual    (df)
        save_by_country(df)
        # Top 10 Arrivals
        top10=df.groupby('country')['arrivals'].sum( ).nlargest(10).index.tolist( )
        save_timeseries(df, top10,'Top10','Top 10 Arrivals')
        # Selected Countries
        selected=['Austrália','Canadá','Estados Unidos','Japão']
        save_timeseries(df, selected,'Selected','Selected Countries')
        with open(STATE_FILE,'w')as f:f.write(str(max_year))
    else:print('No year change detected; skipping…')
