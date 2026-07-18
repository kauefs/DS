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
arrivals=country_totals[country]if country in country_totals else 0
st.sidebar.divider  (   )
st.sidebar.markdown ('Source: [Ministry of Tourism](https://dados.turismo.gov.br/dataset/chegada-de-turistas-internacionais)')
st.sidebar.write    (f"Annual Reports from {DF['year'].min( )} to {DF['year'].max( )}")
st.sidebar.info     (f"Total Arrivals ({DF['year'].min( )}–{DF['year'].max( )}): {DF['arrivals'].sum( ):,.0f}")
st.sidebar.success  (f"Year with highest visitors: {DF.groupby('year')['arrivals'].sum( ).idxmax( )} with {DF.groupby('year')   ['arrivals'].sum( ).max( ):,.0f} arrivals.")
st.sidebar.warning  (f"Top visiting country: {DF.groupby('country')   ['arrivals'].sum( ).idxmax( )} with {DF.groupby('country')['arrivals'].sum( ).max( ):,.0f} total arrivals.")
st.sidebar.error    (f"Second most visiting country: {country} with {arrivals:,.0f} total arrivals.")
st.sidebar.divider  (   )
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
mask  =(DF['year']>=selected_years[0])&(DF['year']<=selected_years[1])
filter= DF[ mask ]
current_total =filter['arrivals'].sum( )
# Year-Over-Year Logic (comparing max selected year vs previous year)
latest_year   =selected_years[1]
prev_year     =  latest_year -1
total_latest  =DF[DF['year'] == latest_year]['arrivals'].sum( )
total_prev    =DF[DF['year'] ==   prev_year]['arrivals'].sum( )
yoy_growth=((total_latest-total_prev)/total_prev)*100 if total_prev > 0 else 0
yoy_pct   = (total_latest/total_prev)            *100 if total_prev > 0 else 0
# Record Growth
total2024     =DF[DF['year']==2024]['arrivals'].sum( )
total2018     =DF[DF['year']==2018]['arrivals'].sum( )
record        =(( total2024-total2018)/total2018)*100 if total2018 > 0 else 0
record_pct    =(  total2024/total2018)           *100 if total2018 > 0 else 0
record_delta  =      record_pct                  -100
# Pandemic Recovery (comparing latest vs 2019)
total2019     = DF[DF['year']==2019]['arrivals'].sum( )
recovery      =(( total_latest-total2019)/total2019)*100 if total2019 > 0 else 0
recovery_pct  =(  total_latest/total2019)           *100 if total2019 > 0 else 0
recovery_delta=       recovery_pct                  -100
col1,col2,col3,col4=st.columns(4)
col1.metric(label=f'Total Arrivals ({selected_years[0]}–{selected_years[1]})',
              value=f'{current_total:,.0f}',
              help = 'Sum of all international arrivals within the slider range.')
col2.metric(label=f'{latest_year} $vs.$ {prev_year}',
              value=f'{yoy_growth    :+.2f}%',
              delta=f'{yoy_growth    :.2f}%',
              help = 'Percentage change compared to the previous calendar year.')
col3.metric(label=f'COVID-19 Recovery', 
              value=f'{recovery      :+.2f}%',
              delta=f'{recovery_delta:.2f}%',
              help = 'Compares current year arrivals to 2019 pre-pandemic benchmark.')
col4.metric(label=f'2024 $vs.$ 2018', 
              value=f'{record        :+.2f}%',
              delta=f'{record_delta  :.2f}%',
              help = 'Percentage change compared to the previous record year.')
plt.close('all')
st.divider(   )
# HeatMap
df=DF.copy(   )
def WorldWideHeatMap(df):
    data=df.groupby('ISO')['arrivals'].sum( ).reset_index( )
    fig =px.choropleth(data, color='arrivals', color_continuous_scale='sunsetdark',
                       title=f"<b>InterNational Tourist Arrivals in Brazil ({selected_years[0]}–{selected_years[1]})</b>",
                       locations='ISO', locationmode='ISO-3', custom_data=['ISO'], #hover_name='country', #hover_data={'arrivals':':,.0f'},
                       projection='natural earth', scope='world') # Provides a classic rounded world view
    fig.update_traces(hovertemplate='<b>%{customdata[0]}</b> %{z:,.0f} arrivals<extra></extra>')
    fig.update_layout(margin={'r':0,'t':50,'l':0,'b':0}, title={'x':.43,'xanchor':'center','font':{'size':20}},
                      coloraxis_colorbar=dict(title={'text':'Total Arrivals','font':{'size':15}}),
                      geo=dict(showframe=False, showcoastlines=True, showcountries=True, countrycolor='#F0F0F0'))
    st .plotly_chart (fig, width='stretch')
WorldWideHeatMap(filter)
st.divider      (      )
# InterActive Seasonality HeatMap
st.subheader(f'Seasonality HeatMap ({selected_years[0]}–{selected_years[1]})')
months=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
data=filter.groupby(['year','month'])['arrivals'].sum( ).reset_index( )
data['month']=pd.Categorical(data['month']  ,     categories=   months ,  ordered= True)
pivot=data.pivot_table(index='year', columns='month', values='arrivals', observed=False)
def fmt(x, pos):return f'{x/1e6:.1f}M'if x >= 1e6 else  f'{x/1e3:.0f}K'
fig,ax=plt.subplots(figsize=(12, 8), frameon=True   ,  tight_layout=False)
sns.heatmap(pivot, annot= False, cmap='RdYlGn_r', # Spectral_r
           #center=pivot_heatmap.stack( ).mean( ), # Colors shift at the average value
            linewidths=.5, cbar_kws={'format':ticker.FuncFormatter(fmt)}, ax=ax)
ax.collections[0].colorbar.ax.tick_params(length=0)
plt.title ('Monthly Arrivals Intensity per Year', fontdict=FontT)
plt.ylabel('')
plt.xlabel('')
plt.yticks(fontsize =  13, fontweight='semibold')
plt.xticks(fontsize =  13, fontweight='semibold')
plt.tick_params(axis='both',   which =    'both', length=0)
st.pyplot(fig, width='stretch')
plt.close(fig)
st.divider(  )
# Seasonality Index
st.subheader(f'Seasonality Index ({selected_years[0]}–{selected_years[1]})')
# Total Arrivals for Every Year–Month Combination
yearly_monthly_totals=filter.groupby(['year','month'])['arrivals'].sum( ).reset_index( )
# Average of Totals Arrivals for Each Month
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
fig, ax=plt.subplots(figsize=(12, 8), frameon=True, tight_layout=False)
sns.barplot(x='month', y='arrivals', data=seasonality_index, palette=season_palette, hue='month', legend=False, ax=ax)
# BaseLine@1.0
ax.axhline(y=1., color='#000000', linestyle=':', linewidth=1.25, alpha=.75, label='Annual BaseLine Average')
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
st.pyplot(fig, width='stretch')
plt.close(fig)
# check=filtered_data.groupby('month')['arrivals'].agg(['count','sum','mean'])
# st.write(check.reindex(['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']))
st.divider(  )
# Annual
st.subheader('Annual Time Series')
annual=filter.groupby('year')['arrivals'].sum( ).reset_index( )
norm  =Normalize(annual['arrivals'].min( ), annual['arrivals'].max( ))
annual_palette=cm.viridis(norm(annual['arrivals'].values)).tolist ( )
fig,ax=plt.subplots(figsize=(12,12), frameon= True , tight_layout=False)
sns.barplot(y='arrivals', x='year' ,    data=annual, palette=annual_palette,  hue='year', saturation=.75, legend=False, ax=ax)
plt.title(f"Annual InterNational Tourist Arrivals in Brazil ({annual['year'].min( )}–{annual['year'].max( )})", fontdict=FontT)
plt.yticks(ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}')))
plt.xticks(fontsize=13 ,fontweight='semibold', rotation='vertical')
plt.ylabel                                        ( None)
plt.xlabel                                        ( None)
plt.legend([ ],                            frameon=False)
plt.grid(                                  visible=False)
for spine in ax.spines.values( ):spine.set_visible(False)
ax.yaxis                              .set_visible(False)
ax.tick_params(axis='both', which='both', length=0)
labels=[f'{v:,.0f}'for v in annual['arrivals']]
for i, patch in enumerate(ax.patches):ax.text(x=patch.get_x( )+patch.get_width( )/2., y=patch.get_height( )-50000, s=labels[i], ha='center', va='top', fontsize=11, fontweight='bold', rotation='vertical', color='#FFFFFF')
st.pyplot ( fig, width='stretch')
plt.close ( fig )
st.divider(     )
# Monthly
st.subheader('Monthly Arrivals')
monthly=filter.groupby('month')['arrivals'].sum( ).reindex(months).reset_index( )
values=monthly['arrivals'].values
norm=Normalize(values.min( ),    values  .max ( ) )
monthly_palette=cm.RdYlGn_r(norm(values)).tolist( ) # brg_r
fig,ax=plt.subplots(figsize=(12, 12), frameon=True, tight_layout=False)
sns.barplot(data=monthly, y='arrivals',  x='month', hue='month', palette=monthly_palette, saturation=.75, legend=False)
plt.title(f'Monthly InterNational Tourist Arrivals in Brazil ({selected_years[0]}–{selected_years[1]})', fontdict=FontT)
plt.yticks(ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}')))
plt.xticks(fontsize=13, fontweight='semibold', rotation='horizontal')
plt.ylabel                                         (None)
plt.xlabel                                         (None)
plt.legend([ ],                            frameon=False)
plt.grid(                                  visible=False)
for spine in ax.spines.values( ):spine.set_visible(False)
plt.gca( ).axes.get_yaxis    ( )      .set_visible(False)
plt.tick_params(axis='both', which ='both', length=0)
labels=[f'{v:,.0f}' for v in monthly['arrivals']]
for i, patch in enumerate(ax.patches):ax.text(x=patch.get_x( )+patch.get_width( )/2., y=patch.get_height( )-100000, s=labels[i], ha='center', va='top', fontsize=13, fontweight='bold', rotation='vertical', color='#FFFFFF')
st.pyplot ( fig, width='stretch')
plt.close ( fig )
st.divider(     )
# Means of Travel
st.subheader('Means of Travel')
def PlotBarsH(df, column, title, palette, loc=None):
    data=df.groupby(column)['arrivals'].sum( ).sort_values(ascending=False).reset_index( )
    if column=='country':data=data.head(12)
    fig,ax=plt.subplots(figsize=(12, 6), frameon=True , tight_layout=False)
    sns.barplot(data=data, y=column, x='arrivals', hue=column, palette=palette, saturation=.75, legend=False, ax=ax)
    plt.title  (f'InterNational Tourist Arrivals in Brazil ({selected_years[0]}–{selected_years[1]}) {title}', fontdict=FontT, loc=loc)
    plt.yticks (fontsize=13, fontweight='semibold', rotation='horizontal')
    plt.xticks ([ ])
    plt.ylabel                                         (None)
    plt.xlabel                                         (None)
    plt.legend( [ ],                           frameon=False)
    plt.grid(                                  visible=False)
    for spine in ax.spines.values( ):spine.set_visible(False)
    plt.tick_params(   axis='both', which ='both', length= 0)
    for p in ax.patches:
        width=p.get_width( )
        if width > 0:ax.text(width+(data['arrivals'].max( )*.02), p.get_y( )+p.get_height( )/2,f'{width:,.0f}', va='center', ha='left', fontsize=13, fontweight='bold')
    st.pyplot(fig, width='stretch')
    plt.close(fig)
PlotBarsH(filter,'via','Means of Travel',   'GnBu_r')
st.divider   (   )
# Continent
st.subheader('Continent')
PlotBarsH(filter,'continent','Continent',   'autumn', loc='right')
st.divider   (   )
# Country
st.subheader('Country')
PlotBarsH(filter,'country',    'Country',  'Blues_r', loc= 'left')
st.divider   (   )
# Arrival Estates
st.subheader('Arrival States')
PlotBarsH(filter,'UF',  'Arrival States','Purples_r', loc='right')
st.divider   (   )
# Monthly Arrivals
latest  =DF['year'].max( )
filter15=DF[(DF['year']>=latest-15)]
st.subheader(f'Monthly Arrivals ({filter15['year']. min  ( )}–{filter15['year'].max( )})')
period=sorted(filter15['year'].unique( ))
years =len   (period)
# start=filter15['year'].min( )
# end  =filter15['year'].max( )+1
# years         =range(start, end)
cols=2
rows=(years+1)//cols
fig, axes     =plt.subplots(rows, cols, figsize=(cols*6, rows*5), frameon=True, tight_layout=False)
axes=axes.flatten( )
for i, year in enumerate(period):
    df_year   =filter15[filter15['year']==year]
    group= df_year.groupby('month')['arrivals'].sum( ).reset_index( )
    group['month']=pd.Categorical(group['month'], categories=months, ordered=True)
    group= group.sort_values('month')
    norm=plt.Normalize(vmin=group['arrivals'].min( ), vmax=group['arrivals'].max( ), clip=False)
    palette=cm.cividis_r(norm(group['arrivals'])).tolist( )
    ax=axes[i]
    sns.barplot(x='month' , y='arrivals', hue='month', data=group, ax=ax, palette=palette, legend=False)
    ax.set_title(f'{year}', fontsize=15, fontweight='bold',   pad=60)
    plt.setp(ax.get_xticklabels( ), rotation=0, ha='center')
    ax.tick_params(axis='both', which='both', length= 0)
    ax.set_xlabel('')
    ax.set_ylabel('')
    ax.set_yticks([])
    for spine in ax.spines.values( ):spine.set_visible(False)
    for   c   in ax.containers:
       #values=df_year.value_counts(ascending=False).iloc[0:0].values
       #ax.bar_label(container=c, labels=values, fmt='{:,.0f}', fontsize=11, padding=5, fontweight='bold', rotation='vertical', color='#000000')
        ax.bar_label(container=c, fmt='{:,.0f}', fontsize=11, padding=5, fontweight='bold', rotation='vertical', color='#000000')
for j in range(i+1, len(axes):fig.delaxes(axes[j])
# fig.subplots_adjust(hspace=.4, wspace=.15)
st.pyplot (fig, width='stretch')
plt.close (fig)
st.divider(   )
# Top Countries
st.subheader(f'Top Countries ({filter15['year'].min( )}–{filter15['year'].max( )})')
group =filter15.groupby(   ['year','country'])['arrivals']  .sum( )        .reset_index( )
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
st.pyplot       (fig,width='stretch' )
plt.close       (fig)
st.divider      (   )
# Top 10 Arrivals
st.subheader(f'Top 10 Arrivals ({filter['year'].min( )}–{filter['year'].max( )})')
def PlotlyArrivals(df, countries, title, palette, labels=None, dash=None):
    group =df.groupby(['country','ISO','year'])['arrivals'].sum( ).reset_index( )
    subset=group[group['country'].isin(countries)].copy(  )
    if labels:
        subset['country']=subset['country'].map(lambda x:labels.get(x,x))
        cmap ={labels.get(c,c):p for c,p in zip(countries, palette)}
    else:cmap={             c :p for c,p in zip(countries, palette)}
    last_year     =        subset['year'].max( )
    final_values  = subset[subset['year']==last_year].sort_values('arrivals', ascending=False)
    sorted        =  final_values['country'].tolist( )
    fig=   px.line(subset, x='year', y='arrivals', color='country', custom_data=['ISO'], category_orders={'country':sorted}, title=f'<b>{title} ({subset['year'].min( )}–{subset['year'].max( )})</b>', color_discrete_map=cmap, template='none')
    fig.update_traces(line=dict(width=1.75, dash=dash), hoverlabel=dict(namelength=1), hovertemplate='<b>%{customdata[0]}</b> %{y:,.0f} arrivals<extra></extra>', hoveron='points+fills', mode='lines')
    annotations=[ ]
    last_points=[ ]
    for country in sorted:
        country_df=subset[subset['country']==country]
        last_row  =country_df.sort_values('year').iloc[-1]
        last_points.append({'name':country,'year':last_row['year'],'val':np.log10(last_row['arrivals']),'color':cmap.get(country,'#000000')})
    last_points.sort(key=lambda x:x['val'])
    min_gap=.1
    for i in range(1, len(last_points)):
        if  last_points[i]['val']-last_points[i-1]['val']< min_gap:
            last_points[i]['val']=last_points[i-1]['val']+ min_gap
    for p in last_points:
        annotations.append(dict(x=p['year'], y=p['val'], xref='x', yref='y', text=f'<b> {p['name']}</b>', showarrow=False, xanchor='left', xshift=5, font=dict( color=p['color'], size=13)))
    fig.update_layout (title={'x':.05,'font':{'size':20}}, xaxis_title='', yaxis_title='', showlegend=False, hovermode='x unified', height=500, margin={'t':80,'b':40,'l':40,'r':80},
                       annotations=annotations, hoverlabel=dict(bgcolor='rgba(255,255,255,.9)', bordercolor='rgba(0,0,0,0)'), uirevision='constant')
    fig.update_yaxes  (type='log', showgrid=False, showticklabels=False, zeroline=False)
    fig.update_xaxes  (dtick= 2  , showgrid=False, tickfont={'size':15}, tickformat='d', showspikes=True, spikecolor='#C0C0C0', spikesnap='cursor', spikemode='across', spikethickness=1, spikedash=dash)
    st .plotly_chart  (fig, width='stretch')
top10  =filter.groupby('country')['arrivals'].sum( ).nlargest(10).index.tolist( )
names  ={'Argentina':'Argentina',   'Chile':'Chile'   ,'Estados Unidos':'United States','Paraguai':'Paraguay',    'Uruguai':'Uruguay'       ,
            'França':'France'   ,'Portugal':'Portugal',      'Alemanha':'Germany'      ,  'Itália':'Italy'   ,'Reino Unido':'United Kingdom'}
palette=[  '#0065FF','#4CAF50'  , '#FF4500','#00BFFF' ,       '#F030E0','#7B70EE'      , '#800000','#BCBD11' ,    '#FF7F0E','#808080'       ]
PlotlyArrivals(filter,    top10 ,'Top 10 InterNational Tourist Arrivals in Brazil'                , palette, labels=None , dash='dot' )
st.divider(           )
# Selected Countries
st.subheader(f'Selected Countries ({filter['year'].min( )}–{filter['year'].max( )})')
selected=['Austrália'     ,'Canadá'     ,'China'      ,'Estados Unidos'     ,'Japão'    ]
flags   ={'Austrália':'🇦🇺','Canadá':'🇨🇦','China':'🇨🇳','Estados Unidos':'🇺🇸','Japão':'🇯🇵'}
names   ={'Austrália':'Australia','Canadá':'Canada'   ,'China':'China' ,'Estados Unidos':'United States','Japão':'Japan'}
custom  =[  '#F030E0'     ,'#FF4500'    ,'#4CAF50'    ,'#0065FF'       ,'#00BFFF'       ]
PlotlyArrivals(filter, selected,'InterNational Tourist Arrivals in Brazil for Selected Countries', custom , labels=names, dash='dash')
st.divider (          )
plt.close  (    'all' )
st.toast   ('Travel!', icon='😎')
