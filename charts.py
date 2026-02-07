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
FontT={'family':'sans-serif','color':'#000000','size':20,'fontweight':'bold'}
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
    data=df.groupby(['year','month'])['arrivals'].sum( ).reset_index( )
    data['month']=pd.Categorical(data['month'], categories=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'], ordered=True)
    pivot=data.pivot_table(index='year', columns='month', values='arrivals', observed=False)
    def fmt(x, pos):return f'{x/1e6:.1f}M' if x >= 1e6 else f'{x/1e3:.0f}K'
    fig,ax=plt.subplots(figsize=(12, 8), frameon=True, tight_layout=True)
    sns.heatmap(pivot, cmap='RdYlGn_r', linewidths=.5, cbar_kws={'format':ticker.FuncFormatter(fmt)})
    ax.collections[0].colorbar.ax.tick_params(length=0)
    plt.title('Monthly Arrivals Intensity per Year', fontsize=15, fontweight='bold')
    plt.ylabel('')
    plt.xlabel('')
    plt.yticks(fontsize=10, fontweight='semibold')
    plt.xticks(fontsize=10, fontweight='semibold')
    plt.tick_params(axis='both', which=    'both', length=0)
    plt.savefig(f'{DIR}/HeatMap.png')
    plt.close(fig)
def save_annual(df):
    annual =df.groupby('year')['arrivals'].sum( ).reset_index( )
    values =annual['arrivals'].values
    norm   =Normalize (values.min( ), values.max( ))
    palette=cm.viridis(norm(values)).tolist( )
    fig, ax=plt.subplots(figsize=(15, 15), frameon=True, tight_layout=True)
    sns.barplot(x='year', y='arrivals', data=annual, palette=palette, hue='year', saturation=.75, legend=False)
    plt.title(f'Annual InterNational Tourist Arrivals in Brazil ({annual['year'].min( )}–{annual['year'].max( )})', fontdict=FontT)
    plt.xticks(fontsize=13 ,fontweight='semibold' ,          rotation='vertical'  )
    for spine in ax.spines.values( ):spine.set_visible(False)
    ax.yaxis.set_visible(False)
    plt.ylabel(None)
    plt.xlabel(None)
    plt.legend( [], frameon= False)
    plt.grid  (     visible= False)
    labels=[f'{v:,.0f}' for v in annual['arrivals']]
    for i, patch in enumerate(ax.patches):
        height=patch.get_height( )
        if height > 0:
            ax.text(patch.get_x( )+patch.get_width( )/2, # X-coordinate: center of bar
                height   -50000,                         # Y-coordinate: inside the top (adjust -50000 as needed)
                labels[i],
                ha        ='center'  ,
                va        =   'top'  ,
                fontsize  =  11      ,
                fontweight='bold'    ,
                rotation  ='vertical',
                color     ='#FFFFFF')
    plt.savefig(f'{DIR}/AnnualTimeSeries.png')
    plt.close(fig)
def save_by_country(df):
    sort=df.groupby('country')['arrivals'].sum( ).sort_values(ascending=False)[:12]
    values=sort['arrivals'].groupby(sort.index, observed= True).sum( ).values
    fig,ax=plt.subplots(frameon=True, tight_layout=True)
    sns.barplot(x=sort.index, y='arrivals', data=sort, palette='Blues_r', hue=sort.index, saturation=.75, legend=False)
    plt.title(f'Top InterNational Tourist Arrivals in Brazil ({df['year'].min( )}–{df['year'].max( )}) by Country', fontdict=FontT)
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
    # Filter
    latest_year=df['year'].max( )
    start_year =latest_year - 15
    df_filtered=df[df['year']>=start_year]
    # Data Processing
    group =df_filtered.groupby(['country','year'])['arrivals'].sum( ).reset_index( )
    subset=group[group         ['country'].isin(countries)]
    piv   =subset.pivot_table(index=      'year', columns='country', values='arrivals')
    # Figure
    fig,ax=plt.subplots(figsize=(10, 5))
    fig.subplots_adjust(left=.08, right=.72, top=.88, bottom=.12)
    colors = sns.color_palette('tab10', len(countries))if len(countries)> 4 else['#00BFFF','#FF4500','#0065FF','#4CAF50']
    # Plotting
    # Sort countries by the last year value
    last_values = piv.iloc[-1].sort_values(ascending=False)
    # Defining minimum "multiplier" gap for the log scale
    # 0.85 means the next label must be at least 15% lower than the previous one
    min_gap_multiplier =.75
    last_y_pos = float('inf')
    for country, y_end in last_values.items( ):
        if country in piv.columns:
            valid_data=piv[country] .dropna( )
            color     =colors[countries.index(country)]
            ax.plot(valid_data.index, valid_data.values, color=color, linewidth=2.25, alpha=.75)
            # Calculating non-overlapping position – if current y_end is too close to the previous label, push it down
            suggested_y    =     y_end
            if  suggested_y>last_y_pos*min_gap_multiplier:
                suggested_y=last_y_pos*min_gap_multiplier
            ax.text(valid_data.index[-1]+.15,
                    suggested_y,
                    f'{country} {y_end:,.0f}',
                    color      = color,
                    fontsize   =    9 ,
                    fontweight ='bold',
                    va         ='center')
            # Drawing a tiny connector line if the label was pushed significantly if abs(suggested_y-y_end)/y_end>.05
            #     ax.plot([valid_data.index[-1], valid_data.index[-1]+.15],
            #             [y_end,  suggested_y], color=color, linestyle=':', linewidth=1)
            last_y_pos=suggested_y
    # Styling
    ax.set_title(f'{title} ({start_year}–{latest_year})', fontsize=15, fontweight='bold', loc='left', pad=25)
    ax.set_yscale('log')
    # Strictly controling limits to prevent "Enormous Height"
    ax.set_ylim(piv.min( ).min( )*.5, piv.max( ).max( )*2.5)
    ax.xaxis.set_major_locator( ticker.MaxNLocator        (integer=True))
    plt.tick_params(axis='both', which='both', length=0, labelleft=False)
    for spine in ax.spines.values( ):            spine.set_visible(False)
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
