# U.S. Higher Educational Institutions Financial Data Visualization

This repository contains two versions of a web application that visualizes financial data for U.S. higher educational institutions. The data is sourced from the Integrated Postsecondary Education Data System (IPEDS) of the US Department of Education.

## Features

- Interactive plots of various financial metrics for educational institutions
- Filtering by state and institution size
- Visualization of trends over time with confidence intervals
- Available in both Streamlit and Flask versions

## Data Preprocessing

The application preprocesses the data to exclude certain institutions:

- Institutions with status ACT as ('D', 'I', 'O'):
  - D: Delete out of business
  - I: Inactive due to hurricane related problems
  - O: Out-of-scope of IPEDS - not postsecondary
- Public institutions (SECTOR values 1, 5, 7)
- Institutions offering degrees with HLOFFER values 1, 2, 3, 4, -2, -3

## Streamlit Version

### Requirements

- Python 3.7+
- Streamlit
- Pandas
- NumPy
- Plotly
- SciPy

### Installation

1. Clone this repository
2. Install the required packages:

```sh
pip install streamlit pandas numpy plotly scipy
```

### Running the Streamlit App

Navigate to the directory containing the Streamlit app and run:

```sh
streamlit run college-financial-vis-app.py
```

![streamlitprev](./assets/web_app_streamlit.gif)

## Flask Version

### Requirements

- Python 3.7+
- Flask
- Pandas
- NumPy
- Plotly
- SciPy

### Installation

1. Clone this repository
2. Install the required packages:
```sh
pip install flask pandas numpy plotly scipy
```

### Running the Flask App

1. Navigate to the directory containing the Flask app
2. Set the Flask environment variable (optional):
- On Windows: `set FLASK_ENV=development`
- On macOS/Linux: `export FLASK_ENV=development`
3. Run the Flask application:
```sh
python college-financials-vis-app_flask.py
```

4. Open a web browser and go to `http://127.0.0.1:5000/`

## Usage

1. Select a state from the dropdown menu
2. Choose an institution size category
3. Click the "Plot" button to generate the visualizations

## Data Visualized

The application generates plots for the following financial metrics:

1. Total Assets
2. Total Revenues
3. Student Grants
4. Total Expenses
5. Student Service
6. Total Liabilities
7. Tuition and Fees
8. Total Expenses - Salaries
9. Instructional Salaries

All financial data is presented in millions of USD.

## Contributing

Contributions to improve the application are welcome. Please feel free to submit a Pull Request.

## License

Copyright (c) 2024 Masoud Masoumi.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


## Acknowledgments

- Data provided by the Integrated Postsecondary Education Data System (IPEDS)
- Visualization powered by Plotly


