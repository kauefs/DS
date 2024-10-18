# Libraries:
import numpy               as np
import pandas              as pd
import matplotlib.pyplot   as plt
import matplotlib.ticker   as ticker
import seaborn             as sns
import streamlit           as st
st.set_page_config(page_title='TourismBR', page_icon='🇧🇷', layout='wide', initial_sidebar_state='collapsed')
# DATA:
DATA  ='https://github.com/kauefs/DS/raw/refs/heads/@/datasets/tourismBR.csv'
@st.cache_data
def LoadData():
    df = pd.read_csv('https://github.com/kauefs/DS/raw/refs/heads/@/datasets/tourismBR.csv', index_col=0)
    return df
df     = LoadData()
# SIDE:
st.sidebar.title(    'ƊⱭȾɅViƧi🧿Ƞ'       )
st.sidebar.divider(                      )
st.sidebar.header(   'Annual International Tourists Arrival in Brazil')
st.sidebar.subheader('Data Analysis'     )
st.sidebar.divider(                      )
st.sidebar.markdown('''Source:    [Ministry of Tourism](https://dados.turismo.gov.br/dataset/chegada-de-turistas-internacionais)''')
st.sidebar.write(    'Yearly reports from {} to {}'.format(df.index.min(), df.index.max()))
st.sidebar.divider(                      )
st.sidebar.markdown('''
![2024.10.17](  https://img.shields.io/badge/2024.10.17-000000)

[![GitHub](     https://img.shields.io/badge/-000000?logo=github&logoColor=FFFFFF)](https://github.com/kauefs/)
[![Medium](     https://img.shields.io/badge/-000000?logo=medium&logoColor=FFFFFF)](https://medium.com/@kauefs)
[![LinkedIn](   https://img.shields.io/badge/-0077B5?logo=linkedin&logoColor=FFFFFF)](https://www.linkedin.com/in/kauefs/)
[![Python](     https://img.shields.io/badge/-3-4584B6?logo=python&logoColor=FFDE57&labelColor=4584B6&color=646464)](https://www.python.org/)

[![License](    https://img.shields.io/badge/Apache--2.0-D22128?style=flat&logo=apache&logoColor=CB2138&label=License&labelColor=6D6E71&color=D22128)](https://www.apache.org/licenses/LICENSE-2.0)

[![ƊⱭȾɅViƧi🧿Ƞ](https://img.shields.io/badge/ƊⱭȾɅViƧi🧿Ƞ&trade;-0065FF?style=plastic&logo=&logoColor=0065FF&label=&copy;2023&labelColor=0065FF&color=0065FF)](https://datavision.one/)
                    ''')
# MAIN:
st.divider(            )
st.title(    'International Tourists Arrival in Brazil')
st.divider(            )
st.markdown('''
International tourist arrivals in Brazil have seen dynamic fluctuations, reflecting the country's rich cultural diversity, stunning landscapes, and vibrant cities.
Known for its iconic attractions like the Amazon rainforest, Christ the Redeemer, and the lively beaches of Rio de Janeiro, Brazil draws millions of visitors each year.
Recent trends indicate a gradual recovery in tourism following global disruptions, with travelers increasingly seeking authentic experiences that highlight Brazil's unique heritage, gastronomy, and natural wonders.
As the country continues to invest in its tourism infrastructure and promote sustainable travel, Brazil remains a captivating destination for international visitors.
            ''')
# st.subheader('Annual Time Series')
values=df['chegadas'].groupby(df.index).sum().values
fig=plt.figure(figsize = (15, 15), frameon=True)
ax =plt.subplot(111)
ax =sns.barplot(      x=df.index,        y='chegadas',           data=df, hue=values, palette='viridis', saturation=.75)
plt.title('Annual International Tourists Arrival in Brazil', fontsize=20,          fontweight='bold')
plt.yticks(ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}')))
plt.xticks(fontsize=15, fontweight='semibold', rotation='vertical')
plt.ylabel(None)
plt.xlabel(None)
plt.legend([], frameon=False)
plt.grid(visible=True, which='major', axis='y' ,linestyle=':', linewidth=.75, color='#DCDCDC')
for spine in ['top', 'right', 'left', 'bottom']:ax.spines[spine].set_visible(False)
plt.gca().axes.get_yaxis().set_visible(False)
plt.tick_params(axis  = 'both',
                which = 'both',
                left  =  False,
                bottom=  False)
# for p in ax.patches:ax.annotate(format(p.get_height(), ',.0f'), (p.get_x() + p.get_width()/2., p.get_height()), 
#             ha='center', va='center', xytext=(0,-40), textcoords='offset points', rotation='vertical', fontweight='semibold')
for c in ax.containers:
    values = df.value_counts(ascending=False).iloc[0:0].values
    ax.bar_label(container=c, labels=values, fmt='{:,.0f}', fontsize=13, padding=-80, fontweight='bold', rotation='vertical', color='#FFFFFF')
st.pyplot(fig)
st.markdown('''
            ''')
st.divider(    )
st.toast('Travel!', icon='😎')
