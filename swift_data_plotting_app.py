import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from io import StringIO

st.set_page_config(page_title='Swift - Data Plotting App')

st.title(':chart_with_upwards_trend: Swift - Data Plotting App')
st.subheader('Quick, Easy & Interactive Plots')
st.text('')
st.markdown('**Just copy/paste any data to generate plots that you can :orange[pan], :green[zoom], and :blue[download]**')
st.markdown('***')

with st.sidebar:
    profile_url = "https://www.linkedin.com/in/gauravchachra"
    st.markdown("**Developer: [Gaurav Chachra](%s)**" % profile_url)
    st.markdown(f'''<a href="{profile_url}">
    <img src="https://content.linkedin.com/content/dam/me/business/en-us/amp/brand-site/v2/bg/LI-Bug.svg.original.svg" width="30" height="30"></a>
    ''', unsafe_allow_html=True)
    st.markdown('***')

if 'app_initialized' not in st.session_state:
    st.session_state['chart_type_dict'] = {'Lines + Scatter':'lines+markers', 'Lines':'lines', 'Scatter':'markers'}
    st.session_state['data_ready_for_plot'] = False
    st.session_state['x_y_submitted'] = False
    st.session_state['y1'] = 'y1'
    st.session_state['y2'] = 'y2'
    st.session_state['y3'] = 'y3'
    st.session_state['y4'] = 'y4'
    st.session_state['y5'] = 'y5'
    st.session_state['x_axis'] = 'x'
    st.session_state['n_unique_vars'] = 6
    st.session_state['message'] = ''

    col_list = [st.session_state['y1'], st.session_state['y2'], st.session_state['y3'], st.session_state['y4'], st.session_state['y5']]
    st.session_state['df'] = pd.DataFrame(columns=col_list, index=pd.Index([], name=st.session_state['x_axis']))

    st.session_state['app_initialized'] = True

def col_name_submit():
    st.session_state['x_y_submitted'] = True

def data_ready():
    st.session_state['data_ready_for_plot'] = True

def update_x_y():
    if st.session_state['x_input'] != '':
        st.session_state['x_axis'] = st.session_state['x_input']
    else:
        st.session_state['x_axis'] = 'x'


    if st.session_state['y1_input'] != '':
        st.session_state['y1'] = st.session_state['y1_input']
    else:
        st.session_state['y1'] = 'y1'

    if st.session_state['y2_input'] != '':
        st.session_state['y2'] = st.session_state['y2_input']
    else:
        st.session_state['y2'] = 'y2'

    if st.session_state['y3_input'] != '':
        st.session_state['y3'] = st.session_state['y3_input']
    else:
        st.session_state['y3'] = 'y3'

    if st.session_state['y4_input'] != '':
        st.session_state['y4'] = st.session_state['y4_input']
    else:
        st.session_state['y4'] = 'y4'

    if st.session_state['y5_input'] != '':
        st.session_state['y5'] = st.session_state['y5_input']
    else:
        st.session_state['y5'] = 'y5'

    col_list = [st.session_state['y1'], st.session_state['y2'], st.session_state['y3'], st.session_state['y4'], st.session_state['y5']]
    var_list = col_list.copy()
    var_list.append(st.session_state['x_axis'])
    unique_vars = set(var_list)
    n_unique_vars = len(unique_vars)
    st.session_state['n_unique_vars'] = n_unique_vars

    if st.session_state['n_unique_vars'] == 6:
        st.session_state['message'] = ''
        modified_df = st.session_state['df_edited_as_object']
        modified_df.columns = col_list
        modified_df.index.name = st.session_state['x_axis']
        st.session_state['df'] = modified_df
    else:
        st.session_state['message'] = 'sorry, variable names must be unique :warning:'

if st.session_state['app_initialized']:
    st.subheader('Add data to the table')
    st.markdown('<p style="color:#4E4E4E; font-size: 20px;">You may type or just copy/paste from another table</p>', unsafe_allow_html=True)
    df_edited = st.data_editor(st.session_state['df'], num_rows='dynamic', key='df_edited', width=700, height=400)
    st.session_state['df_edited_as_object'] = df_edited
    plot_type_selector = st.selectbox(label='**Select Plot Type**', options=['Lines + Scatter', 'Lines', 'Scatter'], key='plot_type_selector')
    chart_title = st.text_input('**Enter chart title (... or leave blank)**', key='chart_title')
    generate_plot_button = st.button('Generate Plot', on_click=data_ready)

if st.session_state['data_ready_for_plot']:

    fig = make_subplots()
    chart_mode_selected = st.session_state['plot_type_selector']
    chart_mode = st.session_state['chart_type_dict'][chart_mode_selected]
    title = st.session_state['chart_title']

    st.session_state['active_cols'] = []

    for index, column in enumerate(df_edited.columns):
        if df_edited[column].notnull().any():
            st.session_state['active_cols'].append(index)
            fig.add_trace(
                go.Scatter(x=df_edited.index, y=df_edited[column], mode=chart_mode, name=column, line_color=px.colors.qualitative.Plotly[index]))
    fig.update_layout(
        title_text=title,
    )

    fig.update_xaxes(title_text=st.session_state['x_axis'])

    if len(st.session_state['active_cols']) == 1:
        index_active_col = st.session_state['active_cols'][0]
        fig.update_yaxes(title_text=st.session_state[f'y{index_active_col+1}'])

    st.plotly_chart(fig)

    image = fig.to_image(format='png', scale=3)
    st.download_button(label='Download as png image', data=image, file_name='plot.png'
    , mime='image/png'
    )

    buffer = StringIO()
    fig.write_html(buffer, include_plotlyjs='cdn')
    html_bytes = buffer.getvalue().encode()

    st.download_button(
        label='Download as interactive plot',
        data=html_bytes,
        file_name='plot.html',
        mime='text/html'
    )

    with st.sidebar:
        st.write('**You may specify custom x and y-variable names**')
        st.session_state['message']
        x_input = st.text_input('**x**', key='x_input', on_change=update_x_y)
        y1_input = st.text_input('**y1**', key='y1_input', on_change=update_x_y)
        y2_input = st.text_input('**y2**', key='y2_input', on_change=update_x_y)
        y3_input = st.text_input('**y3**', key='y3_input', on_change=update_x_y)
        y4_input = st.text_input('**y4**', key='y4_input', on_change=update_x_y)
        y5_input = st.text_input('**y5**', key='y5_input', on_change=update_x_y)
