# Libraries:
import numpy               as np
import pandas              as pd
import matplotlib.pyplot   as plt
import matplotlib.ticker   as ticker
import seaborn             as sns
import streamlit           as st
st.set_page_config(page_title='TourismBR', page_icon='🇧🇷', layout='wide', initial_sidebar_state='collapsed')
# DATA:
DATA     =     'https://github.com/kauefs/DS/raw/refs/heads/@/datasets/tourismBR.csv'
@st.cache_data
def LoadData():
    DD   = pd.read_csv(DATA)
    return DD
DD       = LoadData(       )
# SIDE:
st.sidebar.title(    'ƊⱭȾɅViƧi🧿Ƞ' )
st.sidebar.divider(                 )
st.sidebar.header(   'Brazil 🇧🇷 International Tourist Arrivals')
st.sidebar.subheader('Time Series Data Analysis')
st.sidebar.divider(                 )
st.sidebar.markdown('''Source: [Ministry of Tourism](https://dados.turismo.gov.br/dataset/chegada-de-turistas-internacionais)''')
st.sidebar.write(    'Annual Reports from {} to {}'.format(DD['year'].min(), DD['year'].max()))
st.sidebar.write(    'Total Visitors: {}'.format(f"{DD['arrivals'].sum():,.0f}"))
st.sidebar.divider(                 )
st.sidebar.markdown('''
![2024.10.17](  https://img.shields.io/badge/2024.10.17-000000)

[![GitHub](     https://img.shields.io/badge/-000000?logo=github&logoColor=FFFFFF)](https://github.com/kauefs/)
[![Medium](     https://img.shields.io/badge/-000000?logo=medium&logoColor=FFFFFF)](https://medium.com/@kauefs)
[![LinkedIn](   https://img.shields.io/badge/-0077B5?logo=linkedin&logoColor=FFFFFF)](https://www.linkedin.com/in/kauefs/)
[![Python](     https://img.shields.io/badge/-3-4584B6?logo=python&logoColor=FFDE57&labelColor=4584B6&color=646464)](https://www.python.org/)

[![License](    https://img.shields.io/badge/Apache--2.0-D22128?style=flat&logo=apache&logoColor=CB2138&label=License&labelColor=6D6E71&color=D22128)](https://www.apache.org/licenses/LICENSE-2.0)

[![ƊⱭȾɅViƧi🧿Ƞ](https://img.shields.io/badge/ƊⱭȾɅViƧi🧿Ƞ&trade;-0065FF?style=plastic&logo=&logoColor=0065FF&label=&copy;2024&labelColor=0065FF&color=0065FF)](https://datavision.one/)
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
# By Year:
st.subheader('Annual Time Series')
DF=DD['arrivals'].groupby(DD['year']).sum()
df=pd.DataFrame(DF)
values=df['arrivals'].groupby(df.index).sum().values
fig=plt.figure(figsize=(15,15), frameon=True)
ax =plt.subplot(111)
ax =sns.barplot(     y='arrivals',    x=df.index,          data=df, hue=values, palette='viridis'      ,      saturation=.75,     legend=False )
plt.title('Annual International Tourist Arrivals in Brazil ({}–{})'.format(DD['year'].min(), DD['year'].max()), fontsize= 20, fontweight='bold')
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
# By Month:
st.subheader('By Month')
DF=DD['arrivals'].groupby(DD['month']).sum()
df=pd.DataFrame(DF)
df.index=pd.Categorical(df.index, categories=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'], ordered=True)
values=df['arrivals'].groupby(df.index, observed= True).sum().values
sort=df.sort_values(by='arrivals'     ,ascending=False)
fig=plt.figure(frameon= True )
ax =plt.subplot(111)
ax =sns.barplot(     y='arrivals'     ,        x=df.index,  data=df, hue=values,   palette='brg_r'      ,        saturation=.75,     legend=False )
plt.title('Monthly International Tourist Arrivals in Brazil ({}–{})'.format(DD['year'].min(), DD['year'].max()),   fontsize= 15, fontweight='bold')
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
DF=DD['arrivals'].groupby(DD['via']).sum()
df=pd.DataFrame(DF)
values=df['arrivals'].groupby(df.index, observed= True).sum().values
sort=df.sort_values(by='arrivals'     ,ascending=False)
fig=plt.figure(frameon= True )
ax =plt.subplot(111)
ax =sns.barplot(     y=sort.index     ,        x='arrivals',   data=sort       ,         hue=sort.index, palette='Accent' ,saturation=.75,     legend=False )
plt.title('International Tourist Arrivals in Brazil ({}–{}) by Means of Travel'.format(DD['year'].min(), DD['year'].max()),  fontsize= 15, fontweight='bold')
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
DF=DD['arrivals'].groupby(DD['continent']).sum()
df=pd.DataFrame(DF)
values=df['arrivals'].groupby(df.index, observed= True).sum().values
sort=df.sort_values(by='arrivals'     ,ascending=False)
fig=plt.figure(frameon= True )
ax =plt.subplot(111)
ax =sns.barplot(     y=sort.index,             x='arrivals',   data=sort ,         hue=sort.index, palette='autumn' , saturation=.75,     legend=False )
plt.title('International Tourist Arrivals in Brazil ({}–{}) by Continent'.format(DD['year'].min(), DD['year'].max()),   fontsize= 20, fontweight='bold')
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
DF=DD['arrivals'].groupby(DD['country']).sum()
df=pd.DataFrame(DF)
values=df['arrivals'].groupby(df.index, observed= True).sum().values
sort=df.sort_values(by='arrivals'     ,ascending=False)[:12]
fig=plt.figure(frameon= True)
ax =plt.subplot(111)
ax =sns.barplot(     y=sort.index,             x='arrivals',  data=sort    ,         hue=sort.index, palette='Blues_r', saturation=.75,     legend=False )
plt.title('Top International Tourist Arrivals in Brazil ({}–{}) by Country'.format(DD['year'].min(), DD['year'].max()),   fontsize= 15, fontweight='bold')
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
DF=DD['arrivals'].groupby(DD['UF']).sum()
df=pd.DataFrame(DF)
values=df['arrivals'].groupby(df.index, observed= True).sum().values
sort=df.sort_values(by='arrivals'     ,ascending=False)
fig=plt.figure(figsize=(15,12)        ,  frameon= True)
ax =plt.subplot(111)
ax =sns.barplot(     y=sort.index,             x='arrivals',      data=sort   ,         hue=sort.index, palette='tab20_r', saturation=.75,     legend=False )
plt.title('International Tourist Arrivals in Brazil ({}–{}) by Arrival Estate'.format(DD['year'].min(), DD['year'].max()),   fontsize= 20, fontweight='bold')
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
st.toast('Travel!', icon='😎')
