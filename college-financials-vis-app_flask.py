from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats
import json

app = Flask(__name__)

# Load CSV file
def load_data(csv_url):
    df_orig = pd.read_csv(csv_url, dtype={'EIN': str})
    
    df_sub = df_orig[~df_orig['ACT'].isin(['D', 'I', 'O'])]
    df_sub = df_sub[~df_sub['SECTOR'].isin([1, 5, 7])]
    df_sub = df_sub[df_sub['CONTROL'] == 2]
    df_sub = df_sub[~df_sub['HLOFFER'].isin([1, 2, 3, 4, -2, -3])]
    df_sub = df_sub[df_sub['ICLEVEL'] == 1]

    columns = ['UNITID', 'YR', 'SECTOR', 'INSTNM', 'ADDR', 'ZIP', 'EIN', 'WEBADDR', 'STABBR',
               'COUNTYCD', 'COUNTYNM', 'LONGITUD', 'LATITUDE', 'DFRCGID', 'INSTSIZE', 'F2A02', 'F2A03',
               'F2A06', 'F2B01', 'F2B02', 'F2B07', 'F2C07', 'F2D01', 'F2D16', 'F2E121', 'F2E122',
               'F2E131', 'F2E132', 'F2E133', 'F2E134', 'F2E135', 'F2E136', 'F2E137', 'F2E011',
               'F2E012', 'F2E021', 'F2E022', 'F2E031', 'F2E032', 'F2E041', 'F2E042',
               'F2E051', 'F2E052', 'F2E061', 'F2E062']

    df_sub = df_sub[columns]
    df_sub = df_sub[~df_sub['INSTSIZE'].isin([-1, -2])]

    return df_sub

def aggregate_data_with_ci(df, column, confidence=0.95):
    agg_df = df.groupby('YR')[column].agg(['mean', 'std', 'count']).reset_index()
    z = stats.norm.ppf(0.975)
    agg_df['ci'] = z * (agg_df['std'] / np.sqrt(agg_df['count']))
    return agg_df

def plot_finances(df, subset, state_name):
    df = df.copy()
    columns_to_scale = ['F2A02', 'F2D16', 'F2C07', 'F2B02', 'F2E051', 'F2A03', 'F2E132', 'F2E012', 'F2D01']
    for col in columns_to_scale:
        df[col] = df[col] / 1e6

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

    def add_line_trace_with_ci(fig, df, column, row, col, title):
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
                    thickness=0.5,
                    width=1
                )
            ),
            row=row, col=col
        )

    columns_to_plot = ['F2A02', 'F2D16', 'F2C07', 'F2B02', 'F2E051', 'F2A03', 'F2D01', 'F2E132', 'F2E012']
    titles = ['Total Assets', 'Total Revenues', 'Student Grants', 'Total Expenses', 'Student Service',
              'Total Liabilities', 'Tuition and Fees', 'Total Expenses - Salaries', 'Instructional Salaries']

    for i, (col, title) in enumerate(zip(columns_to_plot, titles)):
        add_line_trace_with_ci(fig, df, col, (i // 3) + 1, (i % 3) + 1, title)

    fig.update_layout(
        height=1000, 
        width=1200, 
        title_text=f'Finances of the institutions in category "{subset} students" for {df.dropna().shape[0]} institutes in the state of {state_name}</b>',
        title_x=0.5,
        title_xanchor='center',
        showlegend=False
    )

    return fig.to_dict()

@app.route('/')
def index():
    csv_url = "https://raw.githubusercontent.com/MasoudMiM/college-data-vis/main/finance_private_not_for_profite_inst.csv"
    df_sub = load_data(csv_url)
    states = sorted(df_sub['STABBR'].unique())
    inst_sizes = ['Under 1,000', '1,000 - 4,999', '5,000 - 9,999', '10,000 - 19,999', '20,000 and above']
    return render_template('index.html', states=states, inst_sizes=inst_sizes)

@app.route('/plot', methods=['POST'])
def plot():
    csv_url = "https://raw.githubusercontent.com/MasoudMiM/college-data-vis/main/finance_private_not_for_profite_inst.csv"
    df_sub = load_data(csv_url)
    
    state = request.form['state']
    instsz = request.form['instsz']
    
    print(f"Received request for state: {state}, instsz: {instsz}")  # Debug print
    
    df_sub_filtered = df_sub[df_sub['STABBR'] == state]
    
    if instsz == 'Under 1,000':
        df_plot = df_sub_filtered[df_sub_filtered['INSTSIZE'] == 1]
    elif instsz == '1,000 - 4,999':
        df_plot = df_sub_filtered[df_sub_filtered['INSTSIZE'] == 2]
    elif instsz == '5,000 - 9,999':
        df_plot = df_sub_filtered[df_sub_filtered['INSTSIZE'] == 3]
    elif instsz == '10,000 - 19,999':
        df_plot = df_sub_filtered[df_sub_filtered['INSTSIZE'] == 4]
    elif instsz == '20,000 and above':
        df_plot = df_sub_filtered[df_sub_filtered['INSTSIZE'] == 5]
    
    print(f"Filtered data shape: {df_plot.shape}")  # Debug print
    
    fig = plot_finances(df_plot, instsz, state)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    print("Graph JSON created")  # Debug print
    
    return jsonify(graphJSON=graphJSON)

if __name__ == '__main__':
    app.run(debug=True)