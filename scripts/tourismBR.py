# Libraries
import      numpy          as   np
import     pandas          as   pd
import    seaborn          as   sns
import  streamlit          as   st
import     plotly.express  as   px
import matplotlib.cm       as   cm
import matplotlib.pyplot   as   plt
import matplotlib.ticker   as   ticker
from   matplotlib.colors import Normalize
from   adjustText        import adjust_text
from     datetime        import date
st.set_page_config(page_title='TourismBR', page_icon='🇧🇷', layout='wide', initial_sidebar_state='collapsed')
# DATA
DATA     =           'https://github.com/kauefs/DS/raw/refs/heads/@/datasets/tourismBR.csv'
@st.cache_data
def LoadData( ):
    DF   = pd.read_csv(DATA)
    return DF
DF       = LoadData   (    )
FontT={'family':'sans-serif','color':'#000000','size':19,'fontweight':'bold'}
# SIDE
st.sidebar.title    ('ƊⱭȾɅViƧi🧿Ƞ&trade;'     )
st.sidebar.divider  (                          )
st.sidebar.header   ('Brazil 🇧🇷 InterNational Tourist Arrivals')
st.sidebar.subheader('Time Series Data Analysis'               )
st.sidebar.divider  (                          )
# Year Range Slider
min=int(DF['year'].min( ))
max=int(DF['year'].max( ))
selected_years=st.sidebar.slider('Year Range', min, max, (min, max))
country_totals=DF.groupby('country')['arrivals'].sum( )
country='Estados Unidos'
arrivals=country_totals[country]
st.sidebar.divider  (                          )
st.sidebar.markdown ('Source: [Ministry of Tourism](https://dados.turismo.gov.br/dataset/chegada-de-turistas-internacionais)')
st.sidebar.write    (          'Annual Reports from {} to {}'                .format(DF['year'] .min( )   ,  DF['year'].max( )                                                                     ))
st.sidebar.info     (            'Total Arrivals ({}–{}): {}'                .format(DF['year'] .min( )   ,  DF['year'].max( )          , f"{DF                   ['arrivals'].sum( )       :,.0f}"))
st.sidebar.success  ('Year with highest visitors: {} with {} arrivals.'      .format(DF.groupby('year')    ['arrivals'].sum( ).idxmax( ), f"{DF.groupby('year')   ['arrivals'].sum( ).max( ):,.0f}"))
st.sidebar.warning  (      'Top visiting country: {} with {} total arrivals.'.format(DF.groupby('country') ['arrivals'].sum( ).idxmax( ), f"{DF.groupby('country')['arrivals'].sum( ).max( ):,.0f}"))
st.sidebar.error    (  f'Second visiting country: {country} with {arrivals:,.0f} total arrivals.')
st.sidebar.divider  (                          )
st.sidebar.markdown ('''
![2024.10.17  ](https://img.shields.io/badge/2024.10.17-000000)
![2026.01.21  ](https://img.shields.io/badge/2026.01.21-000000)

[![License    ](https://img.shields.io/badge/Apache--2.0-D22128?&logo=apache&logoColor=CB2138&label=License&labelColor=6D6E71)](https://www.apache.org/licenses/LICENSE-2.0)

[![GitHub     ](https://img.shields.io/badge/-000000?logo=github&logoColor=FFFFFF)](https://github.com/kauefs/)
[![Medium     ](https://img.shields.io/badge/-000000?logo=medium&logoColor=FFFFFF)](https://medium.com/@kauefs)
[![LinkedIn   ](https://img.shields.io/badge/in-0077B5?logo=linkedin&logoColor=FFFFFF)](https://www.linkedin.com/in/kauefs/)
[![Python     ](https://img.shields.io/badge/3-646464?logo=python&logoColor=FFDE57&labelColor=4584B6)](https://www.python.org/)

[![ƊⱭȾɅViƧi🧿Ƞ](https://img.shields.io/badge/ƊⱭȾɅViƧi🧿Ƞ&trade;-0065FF?style=plastic&logoColor=0065FF&label=&copy;2026&labelColor=0065FF)](https://datavision.one/)
                     ''')
# MAIN
st.title   ('Brazil 🇧🇷 InterNational Tourist Arrivals')
st.divider (                                          )
st.markdown('''
Brazil's rich tapestry of cultures, breathtaking landscapes, and iconic landmarks, has long captivated a dynamic fluctuation of millions of visitors each year.
In recent times, Brazil has seen a resurgence in tourist arrivals, as travelers seek to explore its rich heritage, vibrant festivals, and culinary delights,
from the lush Amazon rainforest to the sun-kissed beaches of Rio de Janeiro, the country offers a diverse array of experiences.

As the country enhances its infrastructure and promotes sustainable travel, it stands as an interesting destination for international visitors,
showcasing the warmth and diversity of its people and landscapes. While 2024 marked a triumphant recovery from COVID-19 pandemic
– surpassing the 2018 record – 2025 has truly shattered the ceiling, setting an entirely new benchmark for arrivals.
            ''')
st.divider( )
# KPI
#st.subheader('KPI Metrics')
mask=(DF['year']>=selected_years[0])&(DF['year']<=selected_years[1])
filtered_data =DF[mask]
current_total =filtered_data['arrivals'].sum( )
# Year-Over-Year Logic (comparing max selected year vs previous year)
latest_year   =selected_years[1]
prev_year     =  latest_year -1
total_latest  =DF[DF['year'] == latest_year]['arrivals'].sum( )
total_prev    =DF[DF['year'] ==   prev_year]['arrivals'].sum( )
if total_prev > 0:yoy_growth=((total_latest-total_prev)/total_prev)*100
else             :yoy_growth=0
yoy_pct=(total_latest/total_prev)*100   if  total_prev     > 0 else 0
# Record Growth
total2024     =DF[DF['year']==2024]['arrivals'].sum( )
total2018     =DF[DF['year']==2018]['arrivals'].sum( )
record        =(( total_latest-total2018)/total2018)*100
record_pct    =(  total_latest/total2018)*100 if total2018 > 0 else 0
record_delta  =  record_pct              -100
# Pandemic Recovery (comparing latest vs 2019)
total2019     = DF[DF['year']==2019]['arrivals'].sum( )
recovery      =(( total_latest-total2019)       /total2019)*100
recovery_pct  =(  total_latest/total2019)*100 if total2019 > 0 else 0
recovery_delta=recovery_pct              -100
col1,col2,col3=st.columns(3)
with col1:
    st.metric(label= 'Total Arrivals from Selected Range',
              value=f'{current_total:,.0f}',
              help = 'Sum of all international arrivals within the slider range.')
with col2:
    st.metric(label=f'{latest_year} $vs.$ {prev_year}', # YoY Growth
              value=f'{yoy_growth    :+.2f}%',
              delta=f'{yoy_growth    :+.2f}%',
              help = 'Percentage change compared to the previous calendar year.')
with col3:
    st.metric(label=f'Recovery from COVID-19', 
              value=f'{recovery      :+.2f}%',
              delta=f'{recovery_delta:+.2f}%',
              help = 'Compares current year arrivals to 2019 pre-pandemic benchmark.')
# with col4:
#     st.metric(label=f'2024 $vs.$ 2018', 
#               value=f'{record        :+.2f}%',
#               delta=f'{record_delta  :+.2f}%',
#               help = 'Percentage change compared to the previous record year.')
plt.close('all')
st.divider(   )
# HeatMap
df=DF.copy(   )
def WorldWideHeatMap(df):
    data=df.groupby('ISO')['arrivals'].sum( ).reset_index( )
    fig =px.choropleth(data, color='arrivals', color_continuous_scale='sunsetdark',
                       title=f"<b>InterNational Tourist Arrivals in Brazil ({DF['year'].min( )}–{DF['year'].max( )})</b>",
                       locations='ISO', locationmode='ISO-3', #hover_name='country', #hover_data={'arrivals':':,.0f'},
                       projection='natural earth', scope='world') # Provides a classic rounded world view
    fig.update_layout(margin={'r':0,'t':50,'l':0,'b':0}, title={'x':.43,'xanchor':'center','font':{'size':20}},
                      coloraxis_colorbar=dict(title={'text':'Total Arrivals','font':{'size':15}}),
                      geo=dict(showframe=False, showcoastlines=True, showcountries=True, countrycolor='#F0F0F0'))
    st.plotly_chart(fig, use_container_width=True)
WorldWideHeatMap(df)
st.divider      (  )
# InterActive Seasonality HeatMap
st.subheader(f'Seasonality HeatMap ({selected_years[0]}–{selected_years[1]})')
filter=DF[(DF['year']>=selected_years[0])&(DF['year']<=selected_years[1])]
data=filter.groupby(['year','month'])['arrivals'].sum( ).reset_index( )
data['month']=pd.Categorical(data['month'], categories=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'], ordered=True)
pivot=data.pivot_table(index='year', columns='month', values='arrivals', observed=False)
def fmt(x, pos):return f'{x/1e6:.1f}M' if x >= 1e6 else f'{x/1e3:.0f}K'
fig,ax=plt.subplots(figsize=(12, 8), frameon=True   , tight_layout=True)
sns.heatmap(pivot,
            annot= False ,
            cmap ='RdYlGn_r', # Spectral_r
           #center=pivot_heatmap.stack( ).mean( ), # Colors shift at the average value
            linewidths=.5,
            cbar_kws={'format':ticker.FuncFormatter(fmt)})
ax.collections[0].colorbar.ax.tick_params(length=0)
plt.title ('Monthly Arrivals Intensity per Year', fontdict=FontT)
plt.ylabel('')
plt.xlabel('')
plt.yticks(fontsize =  13, fontweight='semibold')
plt.xticks(fontsize =  13, fontweight='semibold')
plt.tick_params(axis='both',   which =    'both', length=0)
st.pyplot(fig)
plt.close(fig)
st.divider(  )
# Seasonality Index
st.subheader(f'Seasonality Index ({selected_years[0]}–{selected_years[1]})')
# Total Arrivals for Every Year–Month Combination
yearly_monthly_totals=filtered_data.groupby(['year','month'])['arrivals'].sum( ).reset_index( )
# Average of Totals Arrivals for Each Month
months=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
monthly_avg=yearly_monthly_totals.groupby('month')['arrivals'].mean( ).reindex(months)
# The Index (Monthly Mean/Grand Mean)
overall_mean=monthly_avg.mean( )
seasonality_index=(monthly_avg/overall_mean).reset_index( )
# Ensure Chronological Order
# seasonality_index['month']=pd.Categorical(seasonality_index['month'], categories=months, ordered=True)
# seasonality_index=seasonality_index.sort_values('month')
# Visualization
norm   =Normalize(seasonality_index['arrivals'].min( ), seasonality_index['arrivals'].max( ))
season_palette=cm.RdYlGn_r(norm(seasonality_index['arrivals'].values)).tolist( ) # (RdYlGn_r) Red for High & Green for Low
fig, ax=plt.subplots(figsize=(12, 8), frameon=True, tight_layout=True)
sns.barplot(x='month', y='arrivals', data=seasonality_index, palette=season_palette, hue='month', legend=False)
# BaseLine@1.0
baseline=ax.axhline(y=1., color='#000000', linestyle=':', linewidth=1.25, alpha=.75, label='Annual BaseLine Average')
ax.text(x=5.5, y=1.025, s='Annual BaseLine Average', fontsize=13, fontweight='regular', ha='center')
# ax.legend (handles=[baseline], frameon=False, loc='upper right', prop={'size':13,'weight':'regular'})
plt.title (f'Seasonality Index ({selected_years[0]}–{selected_years[1]})', fontdict=FontT)
plt.text  (x=.51, y=.91, s=f'total monthly volume averaged across years' , fontsize= 13, fontweight= 'regular', ha='center', transform=plt.gcf( ).transFigure)
plt.ylabel('')
plt.xlabel('')
plt.ylim(0, seasonality_index['arrivals'].max( )+.2 )
plt.yticks(   fontsize= 13, fontweight='semibold')
plt.xticks(   fontsize= 13, fontweight='semibold')
plt.tick_params(  axis='both',  which =    'both', length=0)
for spine in ax.spines.values( ):spine.set_visible(False)
for p in ax.patches:ax.annotate(f'{p.get_height( ):.2f}',(p.get_x( )+p.get_width( )/2., p.get_height( )), ha='center', va='center', xytext=(0,9), textcoords='offset points', fontsize=11, fontweight='semibold')
st.pyplot(fig)
plt.close(fig)
# check=filtered_data.groupby('month')['arrivals'].agg(['count','sum','mean'])
# st.write(check.reindex(['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']))
st.divider(  )
# Annual
st.subheader('Annual Time Series')
annual=DF.groupby('year')['arrivals'].sum(   ).reset_index( )
values=    annual        ['arrivals'].values
norm=Normalize(values.min( ),         values  .max ( ) )
annual_palette=cm.viridis(norm       (values)).tolist( )
fig,ax=plt.subplots(figsize=(12,12), frameon= True , tight_layout=True)
sns.barplot(y='arrivals', x='year' ,    data=annual, palette=annual_palette,  hue='year', saturation=.75, legend=False)
plt.title(f'Annual InterNational Tourist Arrivals in Brazil ({annual['year'].min( )}–{annual['year'].max( )})', fontdict=FontT)
plt.yticks(ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}')))
plt.xticks(fontsize=13 ,fontweight='semibold' ,          rotation='vertical'  )
plt.ylabel                                        ( None)
plt.xlabel                                        ( None)
plt.legend([ ],                            frameon=False)
plt.grid(                                  visible=False)
for spine in ax.spines.values( ):spine.set_visible(False)
ax.yaxis                              .set_visible(False)
plt.tick_params(axis='both', which='both', length=0)
labels=[f'{v:,.0f}' for v in annual['arrivals']]
for i, patch in enumerate(ax.patches):ax.text(x=patch.get_x( )+patch.get_width( )/2., y=patch.get_height( )-50000, s=labels[i], ha='center', va='top', fontsize=11, fontweight='bold', rotation='vertical', color='#FFFFFF')
st.pyplot ( fig )
plt.close ( fig )
st.divider(     )
# Monthly
st.subheader('Monthly Arrivals')
monthly=DF.groupby('month')['arrivals'].sum( ).reindex(months).reset_index( )
values=monthly['arrivals'].values
norm=Normalize(values.min( ),    values  .max ( ) )
monthly_palette=cm.RdYlGn_r(norm(values)).tolist( ) # brg_r
fig,ax=plt.subplots(figsize=(12, 12), frameon=True, tight_layout=True)
sns.barplot(data=monthly, y='arrivals',  x='month', hue='month', palette=monthly_palette, saturation=.75, legend=False)
plt.title(f'Monthly InterNational Tourist Arrivals in Brazil ({DF['year'].min( )}–{DF['year'].max( )})', fontdict=FontT)
plt.yticks(ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}')))
plt.xticks(fontsize=13, fontweight='semibold' ,          rotation='horizontal')
plt.ylabel                                         (None)
plt.xlabel                                         (None)
plt.legend([ ],                            frameon=False)
plt.grid(                                  visible=False)
for spine in ax.spines.values( ):spine.set_visible(False)
plt.gca( ).axes.get_yaxis    ( )      .set_visible(False)
plt.tick_params(axis='both', which ='both', length=0)
labels=[f'{v:,.0f}' for v in monthly['arrivals']]
for i, patch in enumerate(ax.patches):ax.text(x=patch.get_x( )+patch.get_width( )/2., y=patch.get_height( )-100000, s=labels[i], ha='center', va='top', fontsize=13, fontweight='bold', rotation='vertical', color='#FFFFFF')
st.pyplot ( fig )
plt.close ( fig )
st.divider(     )
# Means of Travel
st.subheader('Means of Travel')
DD=DF['arrivals'].groupby(DF['via']).sum( )
df=pd.DataFrame(DD)
values=df['arrivals'].groupby(df.index, observed= True).sum( ).values
sort=df.sort_values(by='arrivals'     ,ascending=False)
fig,ax=plt.subplots(figsize=(12, 6), frameon=True, tight_layout=True)
sns.barplot(y=sort.index, x='arrivals', data=sort, hue=sort.index, palette='GnBu_r',saturation=.75, legend=False)
plt.title(f'InterNational Tourist Arrivals in Brazil ({DF['year'].min( )}–{DF['year'].max( )}) Means of Travel', fontdict=FontT)
plt.yticks(fontsize=13, fontweight='semibold', rotation='horizontal')
plt.xticks( [] )
plt.ylabel                                         (None)
plt.xlabel                                         (None)
plt.legend( [],                            frameon=False)
plt.grid(                                  visible=False)
for spine in ax.spines.values( ):spine.set_visible(False)
plt.tick_params(   axis='both', which ='both', length= 0)
for i, patch in enumerate(ax.patches):
    width=patch.get_width( )                      # get_width( ): find the end of the horizontal bar
    if width > 0:
        ax.text(width+500000,                     # X-pos: just past the end of the bar
            patch.get_y( )+patch.get_height( )/2, # Y-pos: center of the bar
            f'{width:,.0f}',                      # number format
            va        ='center',
            ha        ='left',
            fontsize  =  13,
            fontweight='bold')
st.pyplot ( fig )
plt.close ( fig )
st.divider(     )
# Continents
st.subheader('Continents')
DD=DF['arrivals'].groupby(DF['continent']).sum( )
df=pd.DataFrame(DD)
values=df['arrivals'].groupby(df.index, observed= True).sum( ).values
sort=df.sort_values(by='arrivals'     ,ascending=False)
fig,ax=plt.subplots(figsize=(12 , 6)  ,  frameon= True, tight_layout=True)
sns.barplot(y=sort.index, x='arrivals',     data= sort, hue=sort.index, palette='autumn', saturation=.75, legend=False)
plt.title(f'International Tourist Arrivals in Brazil ({DF['year'].min( )}–{DF['year'].max( )}) Continents', fontdict=FontT, loc='right')
plt.yticks(fontsize=13, fontweight='semibold', rotation='horizontal')
plt.xticks( [] )
plt.ylabel                                         (None)
plt.xlabel                                         (None)
plt.legend( [],                            frameon=False)
plt.grid(                                  visible=False)
for spine in ax.spines.values( ):spine.set_visible(False)
plt.tick_params(   axis='both', which ='both', length= 0)
for i, patch in enumerate(ax.patches):
    width=patch.get_width( )                      # get_width( ): find the end of the horizontal bar
    if width > 0:
        ax.text(width+500000,                     # X-pos: just past the end of the bar
            patch.get_y( )+patch.get_height( )/2, # Y-pos: center of the bar
            f'{width:,.0f}',                      # number format
            va        ='center',
            ha        ='left',
            fontsize  =  13,
            fontweight='bold')
st.pyplot ( fig )
plt.close ( fig )
st.divider(     )
# Countries
st.subheader   ('Countries')
sort=DF.groupby('country')['arrivals'].sum( ).sort_values(ascending=False)[:12].reset_index( )
values =sort  ['arrivals'].groupby(sort.index, observed= True).sum( ).values
fig,ax=plt.subplots(figsize=(12, 6),  frameon= True,     tight_layout= True)
sns.barplot(y='country', x='arrivals',   data= sort, palette='Blues_r', hue='country', saturation=.75, legend=False)
plt.title(f'Top InterNational Tourist Arrivals in Brazil ({DF['year'].min( )}–{DF['year'].max( )}) Countries', fontdict=FontT)
plt.yticks(fontsize=13, fontweight='semibold', rotation='horizontal')
plt.xticks( [] )
plt.ylabel                                        ( None)
plt.xlabel                                        ( None)
plt.legend( [],                            frameon=False)
plt.grid  (                                visible=False)
plt.tick_params(   axis='both', which ='both', length= 0)
for spine in ax.spines.values( ):spine.set_visible(False)
for i, patch in enumerate(ax.patches):
    width=patch.get_width( )                      # get_width( ): find the end of the horizontal bar
    if width > 0:
        ax.text(width+500000,                     # X-pos: just past the end of the bar
            patch.get_y( )+patch.get_height( )/2, # Y-pos: center of the bar
            f'{width:,.0f}',                      # number format
            va        ='center',
            ha        ='left',
            fontsize  =  13,
            fontweight='bold')
st.pyplot ( fig )
plt.close ( fig )
st.divider(     )
# Arrival Estates
st.subheader('Arrival Estates')
DD=DF['arrivals'].groupby(DF['UF']).sum( )
df=pd.DataFrame(DD)
values=df['arrivals'].groupby(df.index, observed= True).sum( ).values
sort=df.sort_values(by='arrivals'     ,ascending=False)
fig,ax=plt.subplots(figsize=(12, 8),  frameon= True, tight_layout=True)
sns.barplot(y=sort.index, x='arrivals', data=sort, hue=sort.index, palette='Purples_r', saturation=.75, legend=False )
plt.title(f'InterNational Tourist Arrivals in Brazil ({DF['year'].min( )}–{DF['year'].max( )}) Arrival Estates', fontdict=FontT, loc='right')
plt.yticks(fontsize=13, fontweight='semibold', rotation='horizontal')
plt.xticks( [] )
plt.ylabel                                         (None)
plt.xlabel                                         (None)
plt.legend( [],                            frameon=False)
plt.grid(                                  visible=False)
plt.tick_params(   axis='both', which ='both', length= 0)
for spine in ax.spines.values( ):spine.set_visible(False)
for i, patch in enumerate(ax.patches):
    width=patch.get_width( )                      # get_width( ): find the end of the horizontal bar
    if width > 0:
        ax.text(width+500000,                     # X-pos: just past the end of the bar
            patch.get_y( )+patch.get_height( )/2, # Y-pos: center of the bar
            f'{width:,.0f}',                      # number format
            va        ='center',
            ha        ='left',
            fontsize  =  13,
            fontweight='bold')
st.pyplot ( fig )
plt.close ( fig )
st.divider(     )
# Monthly Arrivals
latest=DF['year'].max( )
filter=DF[(DF['year']>=latest-15)]
st.subheader(f'Monthly Arrivals ({filter['year'].min( )}–{filter['year'].max( )})')
start=filter['year'].min( )
end  =filter['year'].max( )+1
years         =range(start, end)
fig, axes     =plt.subplots(8, 2, figsize=(12, 50), tight_layout=True)
for i, year in enumerate(years):
    df_year   =filter[filter['year']==year]
    group= df_year.groupby('month')['arrivals'].sum( ).reset_index( )
    group['month']=pd.Categorical(group['month'], categories=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'], ordered=True)
    group= group.sort_values('month')
    norm=plt.Normalize(vmin=group['arrivals'].min( ), vmax=group['arrivals'].max( ), clip=False)
    cmap=cm.cividis_r
    palette=cmap(norm(group['arrivals'])).tolist( )
    data   =     norm(group['arrivals'] ).tolist( )
    ax=axes[i // 2, i % 2]
    sns.barplot(x='month' , y='arrivals', hue='month', data=group, ax=ax, palette=palette, legend=False)
    ax.set_title(f'{year}', fontsize=15, fontweight='bold',   pad=60)
    labels=ax.get_xticklabels( )
    plt.setp(labels, rotation=0, ha='center')
    ax.tick_params(axis='both', which='both', length= 0)
    ax.set_xlabel('')
    ax.set_ylabel('')
    ax.set_yticks([])
    for spine in ax.spines.values( ):spine.set_visible(False)
    for   c   in ax.containers:
        values=df_year.value_counts(ascending=False).iloc[0:0].values
        ax.bar_label(container=c, labels=values, fmt='{:,.0f}', fontsize=11, padding=5, fontweight='bold', rotation='vertical', color='#000000')
st.pyplot (fig)
plt.close (fig)
st.divider(   )
# Top Countries
st.subheader(f'Top Countries ({filter['year'].min( )}–{filter['year'].max( )})')
group =filter.groupby(   ['year','country'])['arrivals']  .sum( )        .reset_index( )
group =group.sort_values(['year',            'arrivals'], ascending=[True, False])
fig   ,axes=plt.subplots(8,    2,                           figsize=(12,    25), tight_layout=True)
axes  =axes.flatten( )
for i ,year in enumerate(range(start, end)):
    df_year=group[group['year'] == year].head(11)
    sns.barplot(x='arrivals', y='country', hue='country', data=df_year, ax=axes[i], orient='h', palette='Blues_r', legend=False)
    axes[i].set_title(f'Top Arrivals in {year}', fontsize=15, fontweight='bold')
    axes[i].set_xlabel('')
    axes[i].set_ylabel('')
    axes[i].set_xticks([])
    axes[i].set_yticks(range(len(df_year)))
    axes[i].set_yticklabels(df_year['country'], fontsize=11, fontweight='semibold')
    axes[i].tick_params(axis='both', which='both', length=0)
    for spine in axes[i].spines.values( ):spine.set_visible(False)
    for patch in axes[i].patches:
        width=patch.get_width( )                      # get_width( ): find the end of the horizontal bar
        if width > 0:
            axes[i].text(width+1000,                  # X-pos: just past the end of the bar
                patch.get_y( )+patch.get_height( )/2, # Y-pos: center of the bar
                f'{width:,.0f}',                      # number format
                va        ='center',
                ha        ='left',
                fontsize  =  11,
                fontweight='semibold')
st.pyplot       (   fig  )
plt.close       (   fig  )
st.divider      (        )
# Top 10 Arrivals
st.subheader(f'Top 10 Arrivals ({filter['year'].min( )}–{filter['year'].max( )})')
def Arrivals(df, countries, filename, title, linestyle=None, palette='tab10', labels=None):
    group =filter.groupby(['country','year'])['arrivals'].sum( ).reset_index( )
    top   =group [group   ['country'].isin(countries)]
    piv   =  top.pivot_table(index  ='year', columns='country', values='arrivals')
    if isinstance(palette, list):colors=palette
    else                        :colors=sns.color_palette(palette, len(countries))
    fig,ax   =plt.subplots(figsize=(12, 6), frameon=True, tight_layout=True)
    fig. subplots_adjust  (left   =.08,   right=.72, top=.88,   bottom= .12)
    values   =piv.iloc[-1].sort_values(ascending=False)
    min_gap_multiplier=.75
    last_y_pos=float('inf')
    for country, y_end in values   .items ( ):
        if country in piv.columns:
            valid_data=piv[country].dropna( )
            color     =colors[countries.index(country)]
            ax.plot(valid_data.index, valid_data.values, color=color, linewidth=1.5, alpha=.75, linestyle=linestyle)
            # Use Custom Label if Provided:
            name=labels.get(country, country)if labels else country
            text=f'{name} {y_end:,.0f}'
            # If y_end is too close to previous label, push it down (calculating non-overlapping position):
            suggested_y    =     y_end
            if  suggested_y>last_y_pos*min_gap_multiplier:
                suggested_y=last_y_pos*min_gap_multiplier
            ax.text(valid_data.index[-1]+.15,
                    suggested_y,
                    text       ,
                    color      = color,
                    fontsize   =   11 ,
                    fontweight ='bold',
                   #fontname   ='Segoe UI Emoji',
                    va         ='center')
            # Drawing tiny connector line if label is pushed significantly if abs(suggested_y-y_end)/y_end>.05:
            # ax.plot([valid_data.index[-1], valid_data.index[-1]+.15],   [y_end, suggested_y], color=color, linestyle=':', linewidth=1)
            last_y_pos=suggested_y
    ax.set_title(f'{title} ({latest-15}–{latest})', fontdict=FontT, loc='left')
    ax.set_yscale('log')
    ax.set_ylim(piv.min( ).min( )*.5, piv.max( ).max( )*2.5)
    ax.xaxis.set_major_locator(ticker.MaxNLocator        (integer= True))
    for spine in ax.spines.values( ):            spine.set_visible(False)
    plt.tick_params(axis='both',     which=    'both', length=0, labelleft=False)
    plt.xticks( fontsize=  13  ,fontweight='semibold')
    st.pyplot (      fig  )
    plt.close (      fig  )
top10  =filter.groupby('country')     ['arrivals'].sum( ).nlargest(10).index.tolist( )
names  ={'Argentina':'Argentina',   'Chile':'Chile'   ,'Estados Unidos':'United States','Paraguai':'Paraguay',    'Uruguai':'Uruguay'       ,
            'França':'France'   ,'Portugal':'Portugal',      'Alemanha':'Germany'      ,  'Itália':'Italy'   ,'Reino Unido':'United Kingdom'}
palette=[  '#0065FF','#4CAF50'  , '#FF4500','#00BFFF' ,       '#F030E0','#7B70EE'      , '#800000','#BCBD11' ,    '#FF7F0E','#808080'       ]
Arrivals(filter, top10,'Top10','Top 10 InterNational Tourist Arrivals in Brazil',':', palette, labels=names)
st.divider(           )
# Selected Countries
st.subheader(f'Selected Countries ({filter['year'].min( )}–{filter['year'].max( )})')
selected=['Austrália'     ,'Canadá'     ,'China'     ,'Estados Unidos'      ,'Japão'     ]
flags   ={'Austrália':'🇦🇺','Canadá':'🇨🇦','China':'🇨🇳','Estados Unidos':'🇺🇸','Japão':'🇯🇵'}
names   ={'Austrália':'Australia','Canadá':'Canada','China':'China','Estados Unidos':'United States','Japão':'Japan'}
custom  =[  '#F030E0'     ,'#FF4500'    ,'#4CAF50'   ,    '#0065FF'         ,'#00BFFF'   ]
Arrivals(filter, selected,'Selected','InterNational Tourist Arrivals in Brazil for Selected Countries','--', custom, labels=names)
st.divider (          )
plt.close  (    'all' )
st.toast   ('Travel!', icon='😎')
