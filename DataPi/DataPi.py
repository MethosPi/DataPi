import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pandasai import PandasAI
from pandasai.llm.openai import OpenAI
import openai
import csv
import io


delta = '\u0394'
pi = '\u03A0'


st.header('ΔΠ')
st.subheader('Prompt your data')
prompt = st.text_input('Type "Plot" to plot')

# Create a sidebar menu
sidebar = st.sidebar
sidebar.header(f'{delta}ata{pi}')
sidebar.header('Menu')
sidebar.text(' ')
sidebar.text('Supported file types:')
sidebar.text('CSV | EXCEL')
uploaded_files = sidebar.file_uploader("Upload files", accept_multiple_files=True)
sidebar.text(' ')
apikey = sidebar.text_input("Insert your OpenAI API key")
sidebar.text(' ')
sidebar.text(' ')
delimiter_input = sidebar.text_input("CSV delimiter", max_chars=1)
delimiter = delimiter_input
dataframes = []

OPENAI_API_KEY = apikey
openai.api_key = apikey

llm = OpenAI(api_token=apikey)
pandas_ai = PandasAI(llm)

if uploaded_files:  # Controlla se ci sono file caricati
    columns = st.columns(len(uploaded_files))
    if len(uploaded_files) > 1:
        # Controlla se ci sono più di un file caricato
                if st.button('PROMPT ALL', key='promptall_button'):
                            for uploaded_file in uploaded_files:
                                if uploaded_file.size > 0:  # Verifica se il file non è vuoto
                                    if uploaded_file.name.endswith('.csv'):
                                        def detect_delimiter(uploaded_file):
                                            with io.StringIO(uploaded_file.getvalue().decode('utf-8')) as file:
                                                content = '\n'.join(file.readlines()[:5])  # Ottieni solo le prime 5 righe del contenuto
                                                dialect = csv.Sniffer().sniff(content)
                                                return dialect.delimiter

                                        delimiter = detect_delimiter(uploaded_file)
                                        df = pd.read_csv(uploaded_file, delimiter=delimiter)

                                        if df.shape[1] == 1:
                                            st.write('Wrong delimiter, please insert it manually')                          
                                    if not df.empty:  # Verifica se il DataFrame non è vuoto dopo la lettura del file
                                        dataframes.append(df)
                                else:
                                    st.write(f'File {uploaded_file.name} is empty.')

                        for i, df in enumerate(dataframes):
                            st.write(f'File {i+1}:')
                            response = pandas_ai.run(df, prompt=prompt)
                            if 'Plot' in prompt or 'chart' in prompt:
                                plt.title('Plot')
                                st.pyplot(plt)
                            else:
                                st.write(response)
                                st.write('---')   # Separatore tra i risultati dei prompt  # Separatore tra i risultati dei prompt
    for i, uploaded_file in enumerate(uploaded_files):       
        with columns[i]:
            if uploaded_file.name.endswith('.csv'):
                def detect_delimiter(uploaded_file):
                    with io.StringIO(uploaded_file.getvalue().decode('utf-8')) as file:
                        content = '\n'.join(file.readlines()[:5])  # Ottieni solo le prime 5 righe del contenuto
                        dialect = csv.Sniffer().sniff(content)
                        return dialect.delimiter
                
                delimiter = detect_delimiter(uploaded_file)
                df = pd.read_csv(uploaded_file, delimiter=delimiter)
                
                if df.shape[1] == 1:
                    st.write('Wrong delimiter, please insert it manually')

                if df.empty:  # Verifica se il DataFrame è vuoto dopo la lettura del file
                    st.write(f'File {i+1} ({uploaded_file.name}) is empty.')
                else:
                    dataframes.append(df)
                    if st.button('Prompt CSV', key=f'promptcsv_button_{i}'):
                        response = pandas_ai.run(dataframes[-1], prompt=prompt)
                        if 'Plot' in prompt:
                            # Plot the data
                            plt.title('Chart')     
                            # Display the plot
                            st.pyplot(plt)
                        elif 'chart' in prompt:
                            # Plot the data
                            plt.title('Plot')     
                            # Display the plot
                            st.pyplot(plt)
                        else:
                            st.write(response)
                        # Buttons

                    if st.button('Show first 10 rows', key=f'10rcsv_button_{i}'):
                        st.write('First 10 rows:')
                        st.write(df.head(10))

                    if st.button('Describe', key=f'describecsv_button_{i}'):
                        st.write('Description:')
                        st.write(df.describe())

                    if st.button('Show number of rows and columns', key=f'numbercsv_button_{i}'):
                        st.write(f'Rows: {df.shape[0]}')
                        st.write(f'Columns: {df.shape[1]}')

                    if st.button('Duplicates rows', key=f'duplicatescsv_button_{i}'):
                        duplicates = df.duplicated().sum()
                        st.write(f'Duplicate rows: {duplicates}')

                    if st.button('Show CSV delimiter', key=f'delimiter_button_{i}'):
                        if df.shape[1] == 1 and delimiter == ',':
                            st.write(f'Possible incorrect delimiter, please verify the delimiter in the "Show first 10 rows" section or insert either ";" or "|".')
                        else:
                            st.write(delimiter)
            
            #excel
            elif uploaded_file.name.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file)
                dataframes.append(df)
                if st.button('Prompt EXCEL', key='promptxlsx_button_(2)'):
                    response = pandas_ai.run(dataframes[-1], prompt=prompt)
                    if 'Plot' in prompt:
                        # Plot the data
                        plt.title('Chart')     
                        # Display the plot
                        st.pyplot(plt)
                    elif 'chart' in prompt:
                        # Plot the data
                        plt.title('Plot')     
                        # Display the plot
                        st.pyplot(plt)
                    else:
                        st.write(response) 
                #Buttons
                if st.button('Show first 10 rows', key='10rxlsx_button'):
                    st.write('First 10 rows:')
                    st.write(df.head(10))
                
                if st.button('Describe', key='describexlsx_button'):
                    st.write('Description:')
                    st.write(df.describe())

                if st.button('Show number of rows and columns', key='numberxlsx_button'):
                    st.write(f'Rows: {df.shape[0]}')
                    st.write(f'Columns: {df.shape[1]}')

                if st.button('Duplicates rows', key='duplicatesxlsx_button'):
                    duplicates = df.duplicated().sum()
                    st.write(f'Duplicate rows: {duplicates}')
    

