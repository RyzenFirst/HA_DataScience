import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.figure import Figure
import time
import plotly as pl
import plotly.express as px
import altair as alt
"""
Погружение в мир оценок))))
"""
my_bar = st.progress(0)

for percent_complete in range(100):
    time.sleep(0.01)
    my_bar.progress(percent_complete + 1)

with st.echo(code_location='below'):
    """
    Анализ датасета про успеваемость студентов на экзамене
    
    """
    st.title('Visualization')
    @st.cache(allow_output_mutation=True)   #etting data
    def get_data():
        return pd.read_csv(r"C:\Users\dimab\Desktop\StudentsPerformance.csv")
    df = get_data()
    st.write(df.head())
    st.write(df.describe())
    """
    Let's find distribution of the scores for each exam
    """
    col = (st.selectbox('Select an exam which scores you would like to know',
                        ['math score', 'reading score', 'writing score']))
    st.header(col.capitalize() + ' distribution')
    fig = sns.histplot(df[col])
    plt.xlabel('Scores')
    plt.ylabel('Number of students')
    st.pyplot(fig.figure)

#   from the video of one indus
    """
    (Great! Now we can move further and find more interesting information and take a look at the correlation 
    between different factors)
    """
    col = (st.selectbox('Select the object of correlation', ['race/ethnicity',
                                                             'test preparation course', 'lunch', 'gender']))
    corr_df = df.pivot_table(columns=col) #чтобы посмотреть на корреляцию
    corr_df = corr_df.corr()
    st.write(corr_df)
    """
    Посмотрим на визуализации, которые нам может предложить библиотека altair и
    используем ее для построения heatmap корреляции
    """
    fig = alt.Chart(corr_df).mark_rect().encode(x=alt.X('source.x:O'), y=alt.Y('source.y:O'),color=alt.Color('source.score:Q')).interactive()
    st.altair_chart(fig)
    """
    How many students passed the minimum for exams
    """
    number = st.slider('Выберите проходной балл', min_value=0, max_value=100, step=5)
    df['Pass Math'] = np.where(df['math score'] >= number, 'Passed', 'Not Passed')
    x1 = df['Pass Math'].value_counts()
    df['Pass Reading'] = np.where(df['reading score'] >= number, 'Passed', 'Not Passed')
    x2 = df['Pass Reading'].value_counts()
    df['Pass Writing'] = np.where(df['writing score'] >= number, 'Passed', 'Not Passed')
    x3 = df['Pass Writing'].value_counts()
    df['Passed All'] = (np.where(np.logical_and(df['writing score'] > number,
                                                df['reading score'] > number,
                                                df['math score'] > number), 'Passed', 'Not Passed'))
    x4 = df['Passed All'].value_counts()
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('Math')
        st.bar_chart(x1)
    with col2:
        st.header('Reading')
        st.bar_chart(x2)
    with col3:
        st.header('Writing')
        st.bar_chart(x3)
    st.header('All exams')
    st.bar_chart(x4)
    # from the gallery streamlit
    """
    Красивое распределение солнцем
    """
    options = (st.multiselect(
        "Выберите структуру данных, которую вы хотите получить(в каком порядке выбираете, в таком вам и покажет",
               ['race/ethnicity', 'parental level of education', 'lunch', 'test preparation course']))
    st.write(options)
    fig = px.sunburst(df, path=options)
    st.plotly_chart(fig)
    """plotly.express is used"""
    """
    Средний балл по различным категориям
    """
    choice = (st.selectbox('Выберите критерий для анализа', ['race/ethnicity', 'parental level of education',
                                                             'lunch', 'test preparation course']))
    x = df.groupby(by=choice).mean().reset_index()
    st.write(x)

    """
    Зависимости 
    """
    choice_1 = (st.selectbox('Select first exam which scores you would like to compare',
                        ['math score', 'reading score', 'writing score']))
    choice_2 = (st.selectbox('Select second exam which scores you would like to compare',
                        ['math score', 'reading score', 'writing score']))
    fig = sns.lmplot(x=choice_1, y=choice_2, data=df)
    plt.xlabel(choice_1)
    plt.ylabel(choice_2)
    plt.title(f'{choice_1} and {choice_2}')
    st.pyplot(fig)

    choice_3 = (st.selectbox('Выберите экзамен',
                             ['math score', 'reading score', 'writing score']))
    choice_4 = (st.selectbox('Выберите параметр сравнения', ['race/ethnicity', 'parental level of education',
                                                             'lunch', 'test preparation course']))
    fig = sns.violinplot(x=df[choice_4], y=df[choice_3])
    plt.xlabel(choice_3)
    plt.ylabel(choice_4)
    plt.rcParams.update({'font.size': 5})
    plt.title(f'{choice_3} and {choice_4}')
    st.pyplot(fig.figure)
    """
    Посмотрим на визуализации, которые нам может предложить библиотека altair
    """
    fig = alt.Chart(df).mark_point().encode(x='math score', y = 'reading score').interactive()
    st.altair_chart(fig)
