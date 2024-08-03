
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats

st.set_page_config(layout="wide")
st.rerun(minutes=5)

st.title("Finances for the U.S. Educational Institutions")
st.write("""
This app allows you to plot some aggregate financial data of the educational institutions in the US for some given categories of students.
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
- Institutions that offer degrees with the following values, HLOFFER with following:
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
    df_orig = pd.read_csv(csv_url, dtype={'EIN': str})
    
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

        # Aggregate data
        def aggregate_data_with_ci(df, column, confidence=0.95):
            """
            Aggregate data and calculate confidence intervals.
            """
            # Group by year and calculate mean
            agg_df = df.groupby('YR')[column].agg(['mean', 'std', 'count']).reset_index()
            
            # Calculate confidence interval
            # For 95% CI
            z = stats.norm.ppf(0.975)
            agg_df['ci'] = z * (agg_df['std'] / np.sqrt(agg_df['count']))
        
            return agg_df
        
        # Create subplots
        fig = make_subplots(rows=3, cols=3, subplot_titles=[
            'Total Assets (in million USD)', 
            'Total Revenues (in million USD)', 
            'Student Grants (in million USD)', 
            'Total Expenses (in million USD)', 
            'Student Service (in million USD)', 
            'Total Liabilities (in million USD)', 
            'Tuition and Fees (in million USD)', 
            'Total Expenses - Salaries (in million USD)', 
            'Instructional Salaries (in million USD)'
        ])

        # Function to add line plots with confidence intervals
        def add_line_trace_with_ci(ax, df, column, row, col, title):
            aggregated_df = aggregate_data_with_ci(df, column)
            fig.add_trace(
                go.Scatter(
                    x=aggregated_df['YR'],
                    y=aggregated_df['mean'],
                    mode='lines',
                    name=title,
                    line=dict(width=2),
                    error_y=dict(
                        type='data',
                        array=aggregated_df['ci'],
                        visible=True,
                        #color='rgba(0,0,0,0.2)',  # Color of the error bars
                        thickness=0.5,  # Thickness of the error bars
                        width=1  # Width of the error bars (change this to adjust thickness)
                    )
                ),
                row=row, col=col
            )

        # Plot Total Assets with Confidence Interval
        add_line_trace_with_ci(fig, df, 'F2A02', row=1, col=1, title='Total Assets')

        # Plot Total Revenues with Confidence Interval
        add_line_trace_with_ci(fig, df, 'F2D16', row=1, col=2, title='Total Revenues')

        # Plot Student Grants with Confidence Interval
        add_line_trace_with_ci(fig, df, 'F2C07', row=1, col=3, title='Student Grants')

        # Plot Total Expenses with Confidence Interval
        add_line_trace_with_ci(fig, df, 'F2B02', row=2, col=1, title='Total Expenses')

        # Plot Student Service with Confidence Interval
        add_line_trace_with_ci(fig, df, 'F2E051', row=2, col=2, title='Student Service')

        # Plot Total Liabilities with Confidence Interval
        add_line_trace_with_ci(fig, df, 'F2A03', row=2, col=3, title='Total Liabilities')

        # Plot Tuition and Fees with Confidence Interval
        add_line_trace_with_ci(fig, df, 'F2D01', row=3, col=1, title='Tuition and Fees')

        # Plot Total Expenses - Salaries with Confidence Interval
        add_line_trace_with_ci(fig, df, 'F2E132', row=3, col=2, title='Total Expenses - Salaries')

        # Plot Instructional Salaries with Confidence Interval
        add_line_trace_with_ci(fig, df, 'F2E012', row=3, col=3, title='Instructional Salaries')


        # Update layout to add titles and adjust spacing
        fig.update_layout(
            height=1000, 
            width=1200, 
            title_text=f'Finances of the institutions in category "{subset} students" for {df.dropna().shape[0]} institutes in the state of {state_name}</b>',
            title_x=0.5,  # Center the title horizontally
            title_xanchor='center',  # Anchor the title in the center
            showlegend=False
        )

        return fig

    # Select columns to plot
    inst_sizes = ['Under 1,000', '1,000 - 4,999', '5,000 - 9,999', '10,000 - 19,999', '20,000 and above']
    st.write("Select the State and Institution Size:")
    state = st.selectbox("State:", options=sorted(df_sub['STABBR'].unique()))
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

        # Center the plot using Streamlit's layout features
        col1, col2, col3 = st.columns([1, 10, 1])  # Adjust the proportions as needed

        with col2:
            st.plotly_chart(fig, use_container_width=True)          
