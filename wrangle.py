import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import pycountry
import math

# Import fig_layout with error handling
try:
    import fig_layout
    layout_config = fig_layout.my_figlayout
except ImportError:
    print("Warning: fig_layout module not found. Using default layout.")
    layout_config = {
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)',
        'font': {'color': 'white', 'family': 'Roboto'}
    }

# Read data with error handling
try:
    df = pd.read_csv("Unicorn_Companies.csv")
except FileNotFoundError:
    print("Warning: Unicorn_Companies.csv not found. Creating dummy data.")
    # Create dummy data for testing
    df = pd.DataFrame({
        'Company': ['Company A', 'Company B', 'Company C'] * 300,
        'Valuation ($B)': ['$1.5', '$2.3', '$3.1'] * 300,
        'Date Joined': ['1/1/2020', '2/1/2021', '3/1/2022'] * 300,
        'Country': ['United States', 'China', 'United Kingdom'] * 300,
        'City': ['San Francisco', 'Beijing', 'London'] * 300,
        'Industry': ['Fintech', 'E-commerce', 'AI'] * 300,
        'Select Inverstors': ['Investor A, Investor B', 'Investor C', 'Investor D'] * 300,
        'Founded Year': [2010, 2015, 2020] * 300,
        'Total Raised': ['$100M', '$200M', '$300M'] * 300,
        'Financial Stage': ['Series A', 'Series B', 'IPO'] * 300,
        'Investors Count': [5, 8, 12] * 300
    })

# Data cleaning and processing
def clean_and_process_data():
    global df
    
    # Clean the data - fix column shifting issue
    if 'Select Inverstors' in df.columns:
        # Find rows where Select Investors is null (indicating shifted data)
        ind_shifted = df[df["Select Inverstors"].isnull()].index.to_list()
        
        # Remove index 789 if it exists and is correct
        if 789 in ind_shifted:
            ind_shifted.remove(789)
        
        # Fix shifted columns
        for i in ind_shifted:
            if i < len(df):
                city = df.at[i, "City"]
                industry = df.at[i, "Industry"] 
                invest = df.at[i, "Select Inverstors"]
                
                df.at[i, "City"] = invest
                df.at[i, "Industry"] = city
                df.at[i, "Select Inverstors"] = industry

    # Process Valuation column
    if 'Valuation ($B)' in df.columns:
        df["Valuation ($B)"] = df["Valuation ($B)"].apply(
            lambda x: float(str(x).replace('$', '')) if pd.notna(x) else 0
        )
    
    # Process Date Joined
    if 'Date Joined' in df.columns:
        df["Date Joined"] = pd.to_datetime(df["Date Joined"], errors='coerce')
    
    # Replace "None" values with np.nan
    def replace_none_with_npnan(x):
        return np.nan if str(x) == "None" else x
    
    df = df.map(replace_none_with_npnan)
    
    # Fill missing Investors Count
    if 'Investors Count' in df.columns:
        df["Investors Count"] = df["Investors Count"].fillna(0)
    
    # Process Total Raised column
    def get_actual_total_raised(value):
        if pd.isna(value):
            return np.nan
        
        value_str = str(value)
        to_replace = "$BMK"
        
        # Extract numeric part
        numeric_part = ''.join(c for c in value_str if c.isdigit() or c == '.')
        if not numeric_part:
            return 0
        
        try:
            numeric_value = float(numeric_part)
        except ValueError:
            return 0
        
        # Get unit (last character)
        unity = value_str[-1].upper()
        
        if unity == "B":
            result = numeric_value * 1000000000
        elif unity == "M":
            result = numeric_value * 1000000
        elif unity == "K":
            result = numeric_value * 1000
        else:
            result = numeric_value
            
        return result
    
    if 'Total Raised' in df.columns:
        df["Total Raised"] = df["Total Raised"].apply(get_actual_total_raised)
        df["Total Raised"] = df["Total Raised"] / 1e6  # Convert to millions
    
    # Rename columns
    column_renames = {
        "Total Raised": "Total Raised(M)",
        "Select Inverstors": "Select Investors"
    }
    df = df.rename(columns=column_renames)
    
    # Clean specific values
    if 'Financial Stage' in df.columns:
        df['Financial Stage'] = df['Financial Stage'].replace({"Acq": "Acquired"})
    
    if 'Industry' in df.columns:
        df["Industry"] = df["Industry"].replace({
            "Finttech": "Fintech", 
            "Artificial intelligence": "Artificial Intelligence"
        })
    
    # Convert column types
    categorical_columns = ['Country', 'City', 'Industry']
    for col in categorical_columns:
        if col in df.columns:
            df[col] = df[col].astype('category')
    
    if 'Investors Count' in df.columns:
        df["Investors Count"] = df["Investors Count"].astype(int)

# Clean and process the data
clean_and_process_data()

# Create visualizations
def create_top_investors_chart():
    """Create top 10 investors bar chart"""
    investors = []
    
    if 'Select Investors' in df.columns:
        for i, row in df.iterrows():
            if pd.notna(row["Select Investors"]):
                investors.extend(str(row["Select Investors"]).split(', '))
    
    if investors:
        investors_series = pd.Series(investors).value_counts()[:10]
        investors_series.sort_values(ascending=True, inplace=True)
        
        fig = go.Figure([
            go.Bar(
                x=investors_series.values, 
                y=investors_series.index, 
                orientation='h',
                marker=dict(color='#3DED97')
            )
        ])
        
        fig.update_layout(
            title='Top 10 Investors',
            xaxis_title='Unicorns count',
            yaxis_title='Investors'
        )
        fig.update_layout(layout_config)
        return fig
    else:
        # Return empty figure if no data
        fig = go.Figure()
        fig.add_annotation(
            text="No investor data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
        return fig

def create_top_companies_scatter():
    """Create top 20 companies scatter plot"""
    if len(df) == 0:
        return go.Figure()
    
    top_20_companies = df.nlargest(20, "Valuation ($B)")
    
    fig = px.scatter(
        top_20_companies, 
        x="Valuation ($B)", 
        y="Total Raised(M)",
        size="Investors Count", 
        color="Industry",
        hover_name="Company", 
        size_max=60,
        title='Top 20 companies'
    )
    
    fig.update_layout(
        title={
            'text': 'Top 20 companies',
            'font': {
                'family': 'Roboto_font',
                'size': 22,
                'color': 'White'
            },
        },
        legend=dict(
            title={
                'text': 'Industries',
                'font': {
                    'family': 'Roboto_font',
                    'size': 18,
                    'color': 'White'
                },
            },
        )
    )
    fig.update_layout(layout_config)
    return fig

def create_world_map():
    """Create world map of top 10 countries"""
    try:
        top_10_countries = df.groupby("Country")["Valuation ($B)"].sum().nlargest(10).reset_index()
        
        if len(top_10_countries) == 0:
            return go.Figure()
        
        top_10_countries_total_valuation = top_10_countries["Valuation ($B)"].sum()
        total_valuation_all = df["Valuation ($B)"].sum()
        top_10_countries_total_valuation_perc = (top_10_countries_total_valuation * 100 / total_valuation_all) if total_valuation_all > 0 else 0
        
        # Get ISO codes with error handling
        def get_iso_code(country_name):
            try:
                return pycountry.countries.lookup(country_name).alpha_3
            except:
                # Common country name mappings
                country_mapping = {
                    'United States': 'USA',
                    'United Kingdom': 'GBR',
                    'South Korea': 'KOR'
                }
                return country_mapping.get(country_name, 'USA')  # Default fallback
        
        top_10_countries["iso_code"] = top_10_countries["Country"].apply(get_iso_code)
        
        color_scale = ["#9BECB2", "#55E77C", "#26E1B2", "#25C488", "#06BE84", "#097759", "#003141", "#002837"]
        
        fig = px.choropleth(
            top_10_countries, 
            locations="iso_code", 
            color="Valuation ($B)",
            hover_name="Country", 
            title=f"Valuation for top 10 countries is {top_10_countries_total_valuation:.1f} B$ ({top_10_countries_total_valuation_perc:.1f}% of total)",
            color_continuous_scale=color_scale
        )
        fig.update_layout(layout_config)
        return fig
        
    except Exception as e:
        print(f"Error creating world map: {e}")
        return go.Figure()

def create_industry_chart():
    """Create industry distribution chart"""
    if 'Industry' in df.columns and 'Valuation ($B)' in df.columns:
        industry_total_val = df.groupby("Industry")["Valuation ($B)"].sum().sort_values(ascending=True)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=industry_total_val.index,
            x=industry_total_val.values,
            hovertext=industry_total_val.index,
            marker=dict(color='#3DED97'),
            orientation='h'
        ))
        
        fig.update_layout(
            title={
                'text': 'Industries distribution by total valuation',
                'font': {'family': 'Roboto_font', 'color': 'white', 'size': 26}
            }
        )
        fig.update_layout(layout_config)
        return fig
    else:
        return go.Figure()

# Create all figures
fig2 = create_top_investors_chart()
fig3 = create_top_companies_scatter()
fig4 = create_world_map()
fig5 = create_industry_chart()

# Calculate constants
total_valuation = math.ceil(df['Valuation ($B)'].sum() * 10**-3) if len(df) > 0 else 0
total_number_unicorn = df['Company'].count() if 'Company' in df.columns else 0
total_funding = round(df["Total Raised(M)"].sum() * 10**-3, 2) if 'Total Raised(M)' in df.columns else 0

# Fix variable names (remove typos)
toatl_number_unicorn = total_number_unicorn  # Keep for backward compatibility
toatl_funding = total_funding  # Keep for backward compatibility