
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout="wide")

st.title("Finances for private, not-for-profit institutions in the US")
st.write("""
This app allows you to plot some aggregate financial data of the institutions in the US for some given categories of students.
The data is taken from the Integrated Postsecondary Education Data System (IPEDS) of the US Department of Education.
         
The data is preprocessed to EXCLUDE some institutions detailed as below:
- Institutions with status ACT as ('D', 'I', 'O'):
    - D	-	Delete out of business
    - I	-	Inactive due to hurricane related problems
    - O	-	Out-of-scope of IPEDS - not postsecondary
- Public institutions, if there are any, so NO SECTOR with value
    - 1 - Public, 4-year or above,
    - 5 - Public, 2-year,
    - 7 - Public, less-than 2-year
- institutions that offer degrees with the following values, HLOFFER with following:
    - 1	- Award of less than one academic year
    - 2	- At least 1, but less than 2 academic yrs
    - 3	- Associate's degree
    - 4	- At least 2, but less than 4 academic yrs
    - -2	- Not applicable, first-professional only
    - -3	- {Not available}
""")

# Load CSV file
csv_url = st.text_input("URL of the CSV file", "https://raw.githubusercontent.com/MasoudMiM/college-data-vis/main/finance_private_not_for_profite_inst.csv")
if csv_url is not None:
    df_orig = pd.read_csv(csv_url)
    
    df_sub = df_orig[~df_orig['ACT'].isin(['D', 'I', 'O'])]
    df_sub = df_sub[~df_sub['SECTOR'].isin([1, 5, 7])]
    df_sub = df_sub[df_sub['CONTROL'] == 2]

    df_sub = df_sub[~df_sub['HLOFFER'].isin([1, 2, 3, 4, -2, -3])]
    df_sub = df_sub[df_sub['ICLEVEL'] == 1]


    columns = ['UNITID', 'YR', 'SECTOR', 'INSTNM', 'ADDR', 'ZIP', 'EIN', 'WEBADDR', 'STABBR',\
            'COUNTYCD', 'COUNTYNM', 'LONGITUD', 'LATITUDE', 'DFRCGID', 'INSTSIZE', 'F2A02', 'F2A03', \
                'F2A06', 'F2B01', 'F2B02', 'F2B07', 'F2C07', 'F2D01', 'F2D16', 'F2E121', 'F2E122', \
                    'F2E131', 'F2E132', 'F2E133', 'F2E134', 'F2E135', 'F2E136', 'F2E137', 'F2E011', \
                        'F2E012', 'F2E021', 'F2E022', 'F2E031', 'F2E032', 'F2E041', 'F2E042', \
                            'F2E051', 'F2E052', 'F2E061', 'F2E062']

    # cols_mean = {"year" : 'YR', 'STABBR':' ', 
    # 'F2A02': 'Total assets',
    # 'F2A03' : 'Total liabilities',
    # 'F2B01': 'Total revenues and investment return',
    # 'F2B02': 'Total expenses', 
    # 'F2B07': 'Net assets, end of the year',
    # 'F2C07': 'Total student grants',
    # 'F2D01': 'Tuition and fees - Total',
    # 'F2D16': 'Total revenues and investment return - Total',
    # 'F2E131': 'Total expenses-Total amount',
    # 'F2E132': 'Total expenses-Salaries and wages',
    # 'F2E133': 'Total expenses-Benefits',
    # 'F2E134': 'Total expenses-Operation and maintenance of plant',
    # 'F2E135': 'Total expenses-Depreciation',
    # 'F2E011': 'Instruction-Total amount',
    # 'F2E012': 'Instruction-Salaries and wages',
    # 'F2E021': 'Research-Total amount',
    # 'F2E022': 'Research-Salaries and wages',
    # 'F2E041': 'Academic support-Total amount',
    # 'F2E042': 'Academic support-Salaries and wages',
    # 'F2E051': 'Student service-Total amount',
    # 'F2E052': 'Student service-Salaries and wages',
    # 'F2E061': 'Institutional support-Total amount',
    # 'F2E062': 'Institutional support-Salaries and wages'}

    df_sub = df_sub[columns]


    df_sub = df_sub[~df_sub['INSTSIZE'].isin([-1, -2])]
    df_sub_1 = df_sub[df_sub['INSTSIZE'] == 1]
    df_sub_2 = df_sub[df_sub['INSTSIZE'] == 2]
    df_sub_3 = df_sub[df_sub['INSTSIZE'] == 3]
    df_sub_4 = df_sub[df_sub['INSTSIZE'] == 4]
    df_sub_5 = df_sub[df_sub['INSTSIZE'] == 5]

    def plot_finances(df: pd.DataFrame, subset: str, state_name: str):

        # let's divide y values by 1e6 to make the numbers more readable
        df = df.copy()

        df.loc[:, 'F2A02'] = df['F2A02'] / 1e6
        df.loc[:, 'F2D16'] = df['F2D16'] / 1e6
        df.loc[:, 'F2C07'] = df['F2C07'] / 1e6
        df.loc[:, 'F2B02'] = df['F2B02'] / 1e6
        df.loc[:, 'F2E051'] = df['F2E051'] / 1e6
        df.loc[:, 'F2A03'] = df['F2A03'] / 1e6
        df.loc[:, 'F2E132'] = df['F2E132'] / 1e6
        df.loc[:, 'F2E012'] = df['F2E012'] / 1e6
        df.loc[:, 'F2D01'] = df['F2D01'] / 1e6


        # put all the plots as subplots in a single figure. i also ignore NaN values
        sns.set(font_scale=0.75)
        fig, axs = plt.subplots(3, 3, figsize=(15, 10))
        # increase the vertical space between the subplots
        fig.subplots_adjust(hspace=0.25)
        fig.suptitle(f'Finances of the institutions [{subset} students] for {df.shape[0]} institutes in the state of {state_name}', y=0.93)

        sns.lineplot(data=df.dropna(), x='YR', y='F2A02', ax=axs[0, 0])
        axs[0, 0].set_ylabel('Total Assets (in million USD)')
        axs[0, 0].set_xlabel('Year')
        sns.lineplot(data=df.dropna(), x='YR', y='F2D16', ax=axs[0, 1])
        axs[0, 1].set_ylabel('Total Revenues (in million USD)') 
        axs[0, 1].set_xlabel('Year')
        sns.lineplot(data=df.dropna(), x='YR', y='F2C07', ax=axs[0, 2])
        axs[0, 2].set_ylabel('Student Grants (in million USD)') 
        axs[0, 2].set_xlabel('Year')


        sns.lineplot(data=df.dropna(), x='YR', y='F2B02', ax=axs[1, 0])
        axs[1, 0].set_ylabel('Total Expenses (in million USD)') 
        axs[1, 0].set_xlabel('Year')
        sns.lineplot(data=df.dropna(), x='YR', y='F2E051', ax=axs[1, 1])
        axs[1, 1].set_ylabel('Student Service (in million USD)') 
        axs[1, 1].set_xlabel('Year')
        sns.lineplot(data=df.dropna(), x='YR', y='F2A03', ax=axs[1, 2])
        axs[1, 2].set_ylabel('Total Liabilities (in million USD)')
        axs[1, 2].set_xlabel('Year')


        sns.lineplot(data=df.dropna(), x='YR', y='F2D01', ax=axs[2, 0])
        axs[2, 0].set_ylabel('Tuition and Fees (in million USD)') 
        axs[2, 0].set_xlabel('Year')
        sns.lineplot(data=df.dropna(), x='YR', y='F2E132', ax=axs[2, 1])
        axs[2, 1].set_ylabel('Total Expenses - Salaries (in million USD)')
        axs[2, 1].set_xlabel('Year')
        sns.lineplot(data=df.dropna(), x='YR', y='F2E012', ax=axs[2, 2])
        axs[2, 2].set_ylabel('Instructional Salaries (in million USD)')
        axs[2, 2].set_xlabel('Year')

        return fig

    # Select columns to plot
    inst_sizes = ['Under 1,000', '1,000 - 4,999', '5,000 - 9,999', '10,000 - 19,999', '20,000 and above']
    st.write("Select the State and Institution Size:")
    state = st.selectbox("state:", options=df_sub['STABBR'].unique())
    st.write(f"Selected the category size:")
    instsz = st.selectbox("Inst. Size:", options=inst_sizes)

    # Plot the data
    if instsz and state:
        if instsz == 'Under 1,000':
            fig = plot_finances(df_sub_1[df_sub_1['STABBR'] == state], instsz, state)
        elif instsz == '1,000 - 4,999':
            fig = plot_finances(df_sub_2[df_sub_2['STABBR'] == state], instsz, state)
        elif instsz == '5,000 - 9,999':
            fig = plot_finances(df_sub_3[df_sub_3['STABBR'] == state], instsz, state)
        elif instsz == '10,000 - 19,999':
            fig = plot_finances(df_sub_4[df_sub_4['STABBR'] == state], instsz, state)
        elif instsz == '20,000 and above':
            fig = plot_finances(df_sub_5[df_sub_5['STABBR'] == state], instsz, state)             
        st.pyplot(fig)
