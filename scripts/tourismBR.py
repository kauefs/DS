# Libraries:
import      numpy          as   np
import     pandas          as   pd
import  streamlit          as   st
import    seaborn          as   sns
import matplotlib.pyplot   as   plt
import matplotlib.ticker   as   ticker
import matplotlib.cm       as   cm
from   matplotlib.colors import Normalize
from     datetime        import date
from   adjustText        import adjust_text
st.set_page_config(page_title='TourismBR', page_icon='🇧🇷', layout='wide', initial_sidebar_state='collapsed')
# DATA:
DATA     =     'https://github.com/kauefs/DS/raw/refs/heads/@/datasets/tourismBR.csv'
@st.cache_data
def LoadData():
    DF   = pd.read_csv(DATA)
    return DF
DF       = LoadData(       )
# SIDE:
st.sidebar.title(    'ƊⱭȾɅViƧi🧿Ƞ&trade;' )
st.sidebar.divider(                 )
st.sidebar.header(   'Brazil 🇧🇷 International Tourist Arrivals')
st.sidebar.subheader('Time Series Data Analysis')
st.sidebar.divider(                 )
st.sidebar.markdown('''Source: [Ministry of Tourism](https://dados.turismo.gov.br/dataset/chegada-de-turistas-internacionais)''')
st.sidebar.write(    'Annual Reports from {} to {}'.format(DF['year'].min(), DF['year'].max()                                ))
st.sidebar.write(      'Total Tourists ({}–{}): {}'.format(DF['year'].min(), DF['year'].max(), f"{DF['arrivals'].sum():,.0f}"))
st.sidebar.divider(                 )
st.sidebar.markdown('''
![2024.10.17](  https://img.shields.io/badge/2024.10.17-000000)

[![GitHub](     https://img.shields.io/badge/-000000?logo=github&logoColor=FFFFFF)](https://github.com/kauefs/)
[![Medium](     https://img.shields.io/badge/-000000?logo=medium&logoColor=FFFFFF)](https://medium.com/@kauefs)
[![LinkedIn](   https://img.shields.io/badge/-2867B2?logo=linkedin&logoColor=FFFFFF)](https://www.linkedin.com/in/kauefs/)
[![Python](     https://img.shields.io/badge/3-646464?logo=python&logoColor=FFDE57&labelColor=4584B6)](https://www.python.org/)

[![License](    https://img.shields.io/badge/Apache--2.0-D22128?style=flat&logo=apache&logoColor=CB2138&label=License&labelColor=6D6E71)](https://www.apache.org/licenses/LICENSE-2.0)

[![ƊⱭȾɅViƧi🧿Ƞ](https://img.shields.io/badge/ƊⱭȾɅViƧi🧿Ƞ&trade;-0065FF?style=plastic&label=&copy;2024&labelColor=0065FF&color=0065FF)](https://datavision.one/)
                    ''')
# MAIN:
st.title(            'Brazil 🇧🇷 International Tourist Arrivals')
st.divider(            )
st.markdown('''
Brazil's rich tapestry of cultures, breathtaking landscapes, and iconic landmarks, has long captivated a dynamic fluctuation of millions of visitors each year.
In recent times, Brazil has seen a resurgence in tourist arrivals, as travelers seek to explore its rich heritage, vibrant festivals, and culinary delights,
from the lush Amazon rainforest to the sun-kissed beaches of Rio de Janeiro, the country offers a diverse array of experiences.
As the country continues to enhance its tourism infrastructure and to promote sustainable travel initiatives,
it stands as an interesting destination for international visitors, showcasing the warmth and diversity of its people and landscapes.
            ''')
# Annual:
st.subheader('Annual Time Series')
DD=DF['arrivals'].groupby(DF['year']).sum()
df=pd.DataFrame(DD)
values=df['arrivals'].groupby(df.index).sum().values
fig=plt.figure(figsize=(15,15), frameon=True)
ax =plt.subplot(111)
ax =sns.barplot(     y='arrivals',    x=df.index,          data=df, hue=values, palette='viridis'      ,      saturation=.75,     legend=False )
plt.title('Annual International Tourist Arrivals in Brazil ({}–{})'.format(DF['year'].min(), DF['year'].max()), fontsize= 20, fontweight='bold')
plt.yticks(ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}')))
plt.xticks(fontsize=13 ,fontweight='semibold' ,          rotation='vertical'  )
plt.ylabel(None)
plt.xlabel(None)
plt.legend([], frameon= False)
plt.grid(      visible= False)
for spine in ['top'   ,'left','right','bottom']:ax.spines[spine].set_visible(False)
plt.gca().axes.get_yaxis().set_visible(False)
plt.tick_params(axis  ='both',
                which ='both',
                left  = False,
                bottom= False)
for c in ax.containers:
    values=df.value_counts(ascending=False).iloc[0:0].values
    ax.bar_label(container=c, labels=values, fmt='{:,.0f}', fontsize=11, padding=-80, fontweight='bold', rotation='vertical', color='#FFFFFF')
st.pyplot(fig   )
st.divider(     )
# Monthly:
st.subheader('Monthly')
DD=DF['arrivals'].groupby(DF['month']).sum()
df=pd.DataFrame(DD)
df.index=pd.Categorical(df.index, categories=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'], ordered=True)
values=df['arrivals'].groupby(df.index, observed= True).sum().values
sort=df.sort_values(by='arrivals'     ,ascending=False)
fig=plt.figure(frameon= True )
ax =plt.subplot(111)
ax =sns.barplot(     y='arrivals'     ,        x=df.index,  data=df, hue=values,   palette='brg_r'      ,        saturation=.75,     legend=False )
plt.title('Monthly International Tourist Arrivals in Brazil ({}–{})'.format(DF['year'].min(), DF['year'].max()),   fontsize= 15, fontweight='bold')
plt.yticks(ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}')))
plt.xticks(fontsize=13, fontweight='semibold', rotation='horizontal')
plt.ylabel(None)
plt.xlabel(None)
plt.legend([], frameon= False)
plt.grid(      visible= False)
for spine in ['top'   ,'left','right','bottom']:ax.spines[spine].set_visible(False)
plt.gca().axes.get_yaxis().set_visible(False)
plt.tick_params(axis  ='both',
                which ='both',
                left  = False,
                bottom= False)
for c in ax.containers:
    values=df.value_counts(ascending=False).iloc[0:0].values
    ax.bar_label(container=c, labels=values, fmt='{:,.0f}', fontsize=11, padding=-75, fontweight='bold', rotation='vertical', color='#FFFFFF')
plt.tight_layout(pad=1.15    )
st.pyplot(fig   )
st.divider(     )
# By Means of Travel:
st.subheader('By Means of Travel')
DD=DF['arrivals'].groupby(DF['via']).sum()
df=pd.DataFrame(DD)
values=df['arrivals'].groupby(df.index, observed= True).sum().values
sort=df.sort_values(by='arrivals'     ,ascending=False)
fig=plt.figure(frameon= True )
ax =plt.subplot(111)
ax =sns.barplot(     y=sort.index     ,        x='arrivals',   data=sort       ,         hue=sort.index, palette='GnBu_r' ,saturation=.75,     legend=False )
plt.title('International Tourist Arrivals in Brazil ({}–{}) by Means of Travel'.format(DF['year'].min(), DF['year'].max()),  fontsize= 15, fontweight='bold')
plt.yticks(fontsize=13, fontweight='semibold', rotation='horizontal')
plt.xticks([])
plt.ylabel(None)
plt.xlabel(None)
plt.legend([], frameon= False)
plt.grid(      visible= False)
for spine in ['top'   ,'left','right','bottom']:ax.spines[spine].set_visible(False)
plt.gca().axes.get_yaxis().set_visible(True)
plt.tick_params(axis  ='both',
                which ='both',
                left  = False,
                bottom= False)
for c in ax.containers:
    values=df.value_counts(ascending=False).iloc[0:0].values
    ax.bar_label(container=c, labels=values, fmt='{:,.0f}', fontsize=11, padding=10, fontweight='bold', rotation='horizontal', color='#000000')
st.pyplot(fig   )
st.divider(     )
# By Continent:
st.subheader('By Continent')
DD=DF['arrivals'].groupby(DF['continent']).sum()
df=pd.DataFrame(DD)
values=df['arrivals'].groupby(df.index, observed= True).sum().values
sort=df.sort_values(by='arrivals'     ,ascending=False)
fig=plt.figure(frameon= True )
ax =plt.subplot(111)
ax =sns.barplot(     y=sort.index,             x='arrivals',   data=sort ,         hue=sort.index, palette='autumn' , saturation=.75,     legend=False )
plt.title('International Tourist Arrivals in Brazil ({}–{}) by Continent'.format(DF['year'].min(), DF['year'].max()),   fontsize= 20, fontweight='bold')
plt.yticks(fontsize=13, fontweight='semibold', rotation='horizontal')
plt.xticks([])
plt.ylabel(None)
plt.xlabel(None)
plt.legend([], frameon= False)
plt.grid(      visible= False)
for spine in ['top'   ,'left','right','bottom']:ax.spines[spine].set_visible(False)
plt.gca().axes.get_yaxis().set_visible(True)
plt.tick_params(axis  ='both',
                which ='both',
                left  = False,
                bottom= False)
for c in ax.containers:
    values=df.value_counts(ascending=False).iloc[0:0].values
    ax.bar_label(container=c, labels=values, fmt='{:,.0f}', fontsize=11, padding=10, fontweight='bold', rotation='horizontal', color='#000000')
st.pyplot(fig   )
st.divider(     )
# By Country:
st.subheader('By Country')
DD=DF['arrivals'].groupby(DF['country']).sum()
df=pd.DataFrame(DD)
values=df['arrivals'].groupby(df.index, observed= True).sum().values
sort=df.sort_values(by='arrivals'     ,ascending=False)[:12]
fig=plt.figure(frameon= True)
ax =plt.subplot(111)
ax =sns.barplot(     y=sort.index,             x='arrivals',  data=sort    ,         hue=sort.index, palette='Blues_r', saturation=.75,     legend=False )
plt.title('Top International Tourist Arrivals in Brazil ({}–{}) by Country'.format(DF['year'].min(), DF['year'].max()),   fontsize= 15, fontweight='bold')
plt.yticks(fontsize=13, fontweight='semibold', rotation='horizontal')
plt.xticks([])
plt.ylabel(None)
plt.xlabel(None)
plt.legend([], frameon= False)
plt.grid(      visible= False)
for spine in ['top'   ,'left','right','bottom']:ax.spines[spine].set_visible(False)
plt.gca().axes.get_yaxis().set_visible(True)
plt.tick_params(axis  ='both',
                which ='both',
                left  = False,
                bottom= False)
for c in ax.containers:
    values=df.value_counts(ascending=False).iloc[0:0].values
    ax.bar_label(container=c, labels=values, fmt='{:,.0f}', fontsize=11, padding=10, fontweight='bold', rotation='horizontal', color='#000000')
st.pyplot(fig   )
st.divider(     )
# By Arrival Estate:
st.subheader('By Arrival Estate')
DD=DF['arrivals'].groupby(DF['UF']).sum()
df=pd.DataFrame(DD)
values=df['arrivals'].groupby(df.index, observed= True).sum().values
sort=df.sort_values(by='arrivals'     ,ascending=False)
fig=plt.figure(figsize=(15,12)        ,  frameon= True)
ax =plt.subplot(111)
ax =sns.barplot(     y=sort.index     ,    x='arrivals',       data=sort         ,         hue=sort.index, palette='Purples_r', saturation=.75,     legend=False )
plt.title('International Tourist Arrivals in Brazil ({}–{}) by Arrival Estate'.format(DF['year'].min(), DF['year'].max())  ,   fontsize= 20, fontweight='bold')
plt.yticks(fontsize=13, fontweight='semibold', rotation='horizontal')
plt.xticks([])
plt.ylabel(None)
plt.xlabel(None)
plt.legend([], frameon= False)
plt.grid(      visible= False)
for spine in ['top'   ,'left','right','bottom']:ax.spines[spine].set_visible(False)
plt.gca().axes.get_yaxis().set_visible(True)
plt.tick_params(axis  ='both',
                which ='both',
                left  = False,
                bottom= False)
for c in ax.containers:
    values=df.value_counts(ascending=False).iloc[0:0].values
    ax.bar_label(container=c, labels=values, fmt='{:,.0f}', fontsize=11, padding=10, fontweight='bold', rotation='horizontal', color='#000000')
st.pyplot(fig   )
st.divider(     )
# Monthly (2010–2019):
st.subheader('Monthly (2010–2019)')
years         = range( 2010,2020)
fig, axes     = plt.subplots(5, 2, figsize=(10, 25))
for i, year in enumerate(years):
    df_year   = DF[DF['year']==year]
    group= df_year.groupby('month')['arrivals'].sum().reset_index()
    group['month']=pd.Categorical(group['month'], categories=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], ordered=True)
    group= group.sort_values('month')
    norm=plt.Normalize(vmin=group['arrivals'].min(), vmax=group['arrivals'].max(), clip=False)
    cmap=cm.cividis_r
    data=norm(group['arrivals']).tolist()
    ax=axes[i // 2, i % 2]
    sns.barplot(x='month' , y='arrivals', hue='month', data=group, ax=ax, palette=cmap(data), legend=False)
    ax.set_title(f'{year}', fontweight='bold')
    labels = ax.get_xticklabels()
    plt.setp(labels, rotation=90, ha='center')
    ax.tick_params(axis='both', which='both', length=0)
    ax.set_xlabel('')
    ax.set_ylabel('')
    ax.set_yticks([])
    for spine in ['top','right','left','bottom']:ax.spines[spine].set_visible(False)
    for   c   in ax.containers:
        values=df_year.value_counts(ascending=False).iloc[0:0].values
        ax.bar_label(container=c, labels=values, fmt='{:,.0f}', fontsize=11, padding=-65, fontweight='bold', rotation='vertical', color='#F0F0F0')
plt.tight_layout(pad=1.15)
st.pyplot(fig)
st.divider(  )
# Top Countries (2010–2019):
filter=DF[(DF['year']>=2010)&(DF['year']<=2019)]
st.subheader('Top Countries ({}–{})'.format(filter['year'].min(), filter['year'].max()))
group =filter.groupby(   ['year','country'])['arrivals'].sum().reset_index()
group =group.sort_values(['year',            'arrivals'], ascending=[True, False])
fig   ,axes=plt.subplots(5,    2,                           figsize=(12.5,    20))
axes  =axes.flatten()
for i ,year in enumerate(range(2010, 2020)):
    df_year=group[group['year'] == year][:11]
    sns.barplot(x='arrivals', y='country', hue='country', data=df_year, ax=axes[i], orient='h', palette='Blues_r', legend=False)
    axes[i].set_title(f'Top Arrivals in {year}', fontweight='bold')
    axes[i].set_xlabel('')
    axes[i].set_ylabel('')
    axes[i].set_xticks([])
    axes[i].tick_params(axis='both', which='both', length=0)
    for spine in ['top','right','left','bottom']:axes[i].spines[spine].set_visible(False)
    for   c   in axes[i].containers:
        values=group.value_counts(ascending=False).iloc[0:0].values
        axes[i].bar_label(container=c, labels=values, fmt='{:,.0f}', fontsize=11, padding=10, fontweight='bold', rotation='horizontal', color='#000000')
plt.tight_layout(pad=1.15)
st.pyplot(fig)
st.divider(  )
# Top 10 Arrivals (2010–2019):
filter   =DF[(DF['year']>=2010)&(DF['year']<=2019)]
st.subheader('Top 10 Arrivals ({}–{})'.format(filter['year'].min(), filter['year'].max()))
group    =filter.groupby(['country','year'])['arrivals'].sum().reset_index()
countries= group.groupby( 'country')[        'arrivals'].sum().nlargest(10).index
top      = group[group[   'country'].isin(countries)]
piv      =   top.pivot_table(index ='year', columns='country', values='arrivals')
texts    =[]
fig      =plt.figure(figsize=(10, 5))
for i  ,country in enumerate(countries):
    plt.plot(piv.index, piv[country], label=country, color=plt.cm.tab10(i))
    x_end   =piv.index[-1]+    .05
    y_end   =piv[ country].iloc[-1]
    text=plt.annotate(f'{country} { y_end:,.0f}',
                      xy=(    x_end,y_end),
                      xytext=(x_end,y_end),
                      textcoords='data',
                      fontsize  =    8 ,
                      fontweight='semibold',
                      arrowprops=dict(arrowstyle='-', connectionstyle='arc3, rad=.15', color=plt.cm.tab10(i)))
    texts.append(text)
adjust_text(texts, avoid_self=False, pull_threshold=2.5, ensure_inside_axes=False, only_move={'explode':'x+,y+'})
plt.title('Top 10 Arrivals ({}–{})'.format(filter['year'].min(), filter['year'].max()), fontsize= 15, fontweight='bold')
plt.xlabel(''        )
plt.ylabel(''        )
plt.tick_params(axis='both', which='both', length=0, labelleft=False)
plt.yscale('log'     )
plt.grid(False       )
plt.box( False       )
plt.tight_layout(pad=1.15)
st.pyplot(fig)
st.divider(  )
# Selected Countries (2010–2019):
filter   =DF[(DF['year']>=2010)&(DF['year']<=2019)]
st.subheader('Selected Countries ({}–{})'.format(filter['year'].min(), filter['year'].max()))
group    =filter.groupby(['country','year'])['arrivals'].sum().reset_index()
countries=  ['Austrália', 'Canadá' ,'Estados Unidos','Japão']
top      = group[group[   'country'].isin(countries)]
piv      =   top.pivot_table(index ='year', columns='country', values='arrivals')
texts    =  []
colors   =  ['#00BFFF','#FF4500','#0065FF','#4CAF50']
fig      =plt.figure(figsize=(10, 5))
for i  ,country in enumerate(countries):
    plt.plot(piv.index, piv[country], label=country, color=colors[i])
    x_end   =piv.index[-1]+    .05
    y_end   =piv[ country].iloc[-1]
    text=plt.annotate(f'{country} { y_end:,.0f}',
                      xy=(    x_end,y_end),
                      xytext=(x_end,y_end),
                      textcoords='data',
                      fontsize  =    8 ,
                      fontweight='semibold',
                      arrowprops=dict(arrowstyle='-', connectionstyle='arc3, rad=.15', color=colors[i]))
    texts.append(text)
adjust_text(texts, avoid_self=False, pull_threshold=2.5, ensure_inside_axes=False, only_move={'explode':'x+,y+'})
plt.title('Selected Countries ({}–{})'.format(filter['year'].min(), filter['year'].max()), fontsize= 15, fontweight='bold')
plt.xlabel(''        )
plt.ylabel(''        )
plt.tick_params(axis='both', which='both', length=0, labelleft=False)
plt.yscale('log'     )
plt.grid(False       )
plt.box( False       )
plt.tight_layout(pad=1.15)
st.pyplot(fig)
st.divider(  )
st.toast('Travel!', icon='😎')
