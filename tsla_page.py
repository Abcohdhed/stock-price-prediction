import pandas as pd
import numpy as np
import streamlit as st
import joblib
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import yfinance as yf
import datetime
import os 


#import general stock data
# Get the absolute path to the current script's directory
script_directory = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_directory, 'stock_data.csv')
data = pd.read_csv(file_path)   # Load the CSV file using the absolute path


#Load current data from yfinance
def load_data():
    ticker = 'TSLA'
    start_date = "2014-01-01"
    end_date = datetime.datetime.now().strftime('%Y-%m-%d')  # Format the current date as a string
    data = yf.download(ticker, start=start_date, end=end_date)
    data.reset_index(inplace=True)
    return data



def tsla_page(data):
    st.markdown(
        """
        <div style='color: #D22B2B;'>
        <p style='font-size: 23px;  font-weight: bold;'>Welcome to the TSLA Insights Page!</p>
        </div>
        
        Embark on an analytical exploration of Tesla, Inc. (TSLA), an innovative force in the electric vehicle and clean energy sector. This page presents a curated selection of visualizations and metrics illuminating TSLA's stock movements, from volatility patterns to growth trajectories. Dive into the data that mirrors Tesla's disruptive impact on the automotive industry and its implications for investors.
        
        """,
        unsafe_allow_html=True)
    

    # Load data
    tsla_data = load_data()

    # Displaying the dataset for AMD
    st.markdown("#### TSLA Stock Data")
    display_data = tsla_data.copy()
    display_data.sort_values(by='Date', ascending=False, inplace=True)
    display_data['Date'] = pd.to_datetime(display_data['Date'])
    display_data['Trade Volume'] = display_data['Volume']
    display_data['DayOfWeek'] = display_data['Date'].dt.day_name()   #DayOfWeek
    display_data['  Month  '] = display_data['Date'].dt.strftime('%B')    #Month
    display_data['Date'] = display_data['Date'].dt.date
    
    #drop redundant columns
    display_data.drop(['Adj Close', 'Volume'], axis=1, inplace=True)

    #display_data.set_index('Date', inplace=True)
    st.dataframe(display_data, hide_index=True)

    

    # Filter data for TSLA
    tsla_data = display_data.copy()
    tsla_data['O-C'] = tsla_data['Close'] - tsla_data['Open']  #O-C

    ## Plotting Closing Prices for TSLA

    # Using st.markdown() to customize font size
    st.markdown("""
    <style>
    .font {
        font-size:20px !important;
    }
    </style>
    """, unsafe_allow_html=True)
    st.markdown('<p class="font">TSLA Closing Prices Over The Last Decade</p>', unsafe_allow_html=True) 

    # Define radio button with options
    plot_option = st.radio("Choose a plot type:", ('Line Plot', 'Candlestick Plot'))

    if plot_option == 'Line Plot':
        # Line plot for INTC Closing Prices
        fig = px.line(tsla_data, 
                    x='Date', 
                    y='Close',
                    color_discrete_sequence=['#D22B2B'])
        fig.update_layout(height=480, width=700,xaxis_title='Date',
                        yaxis_title='Closing Price')
        st.plotly_chart(fig)

    elif plot_option == 'Candlestick Plot':
        # Candlestick plot
        figure = go.Figure(data=[go.Candlestick(x=tsla_data["Date"],
                                            open=tsla_data["Open"], 
                                            high=tsla_data["High"],
                                            low=tsla_data["Low"], 
                                            close=tsla_data["Close"],
                                            increasing_line_color='green', increasing_fillcolor='green',
                                            decreasing_line_color='red', decreasing_fillcolor='red')])
        figure.update_layout(height=480, width=700,xaxis_rangeslider_visible=False)
                            
        st.plotly_chart(figure)

    
    # Inference
    st.markdown("""

    - **Rapid Ascent in Market Valuation:** The trajectory of Tesla's closing prices over the last decade encapsulates a remarkable journey of growth and market disruption. This trend not only reflects Tesla's success in popularizing electric vehicles (EVs) but also its expanding ecosystem encompassing energy storage and autonomous driving technologies.

    - **Innovations and Milestones:** Key inflection points in the plot often coincide with Tesla's groundbreaking product launches, ambitious production targets, and significant technological breakthroughs. These milestones have continually fueled investor optimism and reinforced Tesla's position as a leader in the EV revolution.

    - **Elon Musk's Influence:** The influence of Elon Musk, Tesla's CEO, is unmistakably imprinted on the stock's performance. His visionary leadership, combined with his ability to engage with the public and investors through social media, has significantly impacted Tesla's market perception and, subsequently, its stock volatility.

    - **Volatility Amid Growth:** Despite the overall upward trend, the plot reveals periods of volatility, underscoring the speculative nature of Tesla's stock amidst varying investor sentiment, regulatory challenges, and competitive pressures. This volatility serves as a reminder of the high-risk, high-reward nature of investing in companies at the forefront of technological innovation.

    - **Future Outlook:** As Tesla continues to navigate the complexities of scaling its operations globally, advancing its technological edge, and entering new markets, its closing price plot will remain a focal point for investors. The ongoing evolution in the automotive and energy sectors, coupled with regulatory changes and economic factors, will play critical roles in shaping Tesla's future trajectory.

    This visualization not only charts the history of one of the most closely watched stocks in recent years but also invites investors to contemplate the interplay between innovation, leadership, market dynamics, and the broader shift towards sustainable energy. As we look forward, the plot of Tesla's closing prices will undoubtedly continue to serve as a barometer for both the company's performance and the market's belief in its vision for the future.
    """, unsafe_allow_html=True)



    ## Create the line plot for TSLA's daily volatility
    fig = px.line(tsla_data, x='Date', y='O-C', title=f'TSLA Daily Volatility (Open - Close)',
                hover_data={'DayOfWeek': True}, 
                text='DayOfWeek')

    # Update traces to display the custom hover text
    fig.update_traces(mode='lines', hoverinfo='text', line=dict(width=2, color='#FA5F55'))  # Here you can specify the color

    # Unified hover mode for a cleaner interface
    fig.update_layout(hovermode='x unified')

    fig.update_layout(
        xaxis_title='Date',
        yaxis_title='Daily Volatility (O-C)',
        height=480, width=700,
        hoverlabel=dict(
            bgcolor='rgba(255,255,255,0.9)',
            font_size=10,  
            font_color="black"  
        )
    )
    # Display the plot in Streamlit
    st.plotly_chart(fig)

    #Inference
    st.markdown(
    """
    **Observation:** TSLA's volatility has escalated over recent years, highlighting its growing impact on the market, driven by significant milestones, advancements in electric vehicle technology, and Elon Musk's market influence. The recent spikes underscore heightened investor attention and speculative trading.

    **Recommendation:** Given TSLA's increased volatility and market impact, investors might consider a long-term hold strategy to ride out the volatility for potential gains, especially if they believe in the future of electric vehicles and renewable energy. However, the high volatility also suggests the potential for significant short-term gains (or losses), making it suitable for more risk-tolerant traders who can closely monitor market signals and news.

    """,
    unsafe_allow_html=True
    )

    
    ##TSLA Trading Volume vs Closing Price Over Time

    # Create subplots with 1 row and 1 column, setting up a secondary y-axis
    fig = make_subplots(rows=1, cols=1, shared_xaxes=True, 
                        vertical_spacing=0.04, 
                        specs=[[{"secondary_y": True}]])

    # Add volume bar chart with solid color for better visibility
    fig.add_trace(
        go.Bar(x=tsla_data['Date'], y=tsla_data['Trade Volume'], name="Trade Volume", marker=dict(color='rgb(50, 171, 96)')),
        row=1, col=1, secondary_y=False
    )

    # Add closing price line chart
    fig.add_trace(
        go.Scatter(x=tsla_data['Date'], y=tsla_data['Close'], name="Closing Price", line=dict(color='#FA5F55')),
        row=1, col=1, secondary_y=True
    )

    # Update layout with a suitable title
    fig.update_layout(height=480, width=700, title_text="TSLA Trading Volume vs Closing Price Over Time",
                    showlegend=False, template="plotly_white")

    # Set x-axis and y-axes titles
    fig.update_xaxes(title_text="Date")
    fig.update_yaxes(title_text="<b>Trade Volume</b>", secondary_y=False)
    fig.update_yaxes(title_text="<b>Closing Price</b>", secondary_y=True)

    # Display Plotly chart in Streamlit
    st.plotly_chart(fig)

    #Inference for Tesla
    st.markdown(
    """
    Over the span of the last decade, Tesla has cemented its position as a vanguard of the electric vehicle revolution, enticing investors with its vision and execution. A closer look at its trading volumes juxtaposed with price movements offers valuable perspectives for potential investors.

    In the early years of the last decade, Tesla's trading volumes were considerably high, mirroring the period of Amazon's, albeit for different reasons. This phase was marked by Tesla's aggressive expansion, groundbreaking product launches, and Elon Musk's growing influence. High trading volumes during this period reflected the market's keen interest and the speculative nature of investments in Tesla, amidst its promise to redefine automotive and energy industries.

    However, a notable shift in trading volumes is observed in recent years, despite Tesla's continued prominence and stock appreciation. This trend, similar to Amazon's, could indicate a transition towards more stable, long-term investment strategies among Tesla's shareholder base, and a potential reduction in speculative trading.

    Distinct from Amazon, Tesla exhibits a specific pattern where trading volumes tend to decrease during bull runs, contrasting with spikes in volumes during price reversals, especially during downturns. This suggests that investor enthusiasm and confidence in Tesla's long-term potential might lead to a hold strategy during upward trends, while significant sell-offs during downturns - possibly triggered by profit-taking or market corrections - increase trading volumes.

    For investors, understanding these patterns is crucial. The decreased volumes during bull runs could suggest a collective confidence in Tesla's long-term value, implying that dips might offer buying opportunities for those who share this outlook. Conversely, the spikes in volume during downturns highlight moments of heightened market activity that might warrant caution or present opportunities, depending on one's investment strategy and perception of Tesla's future.

    Navigating Tesla's investment landscape requires a nuanced approach, balancing the excitement around its potential with careful consideration of market trends and volume indicators. Investors are advised to integrate these insights with a broader investment strategy that includes technical analysis and a firm grasp of Tesla's fundamentals and industry position.
    """,
    unsafe_allow_html=True
    )


    # Pivot the DataFrame
    pivot_df = data.pivot(index='Date', columns='Symbol', values='Close')

    #Calculate the Correlation Matrix
    correlation_matrix = pivot_df.corr()

    # Create the heatmap
    fig = go.Figure(data=go.Heatmap(
        z=correlation_matrix,
        x=correlation_matrix.columns,
        y=correlation_matrix.columns,
        colorscale='Viridis', 
        colorbar_title='Correlation'
    ))

    # Update the layout
    fig.update_layout(
        title='Correlation Heatmap of Stocks',
        xaxis_title='Stock Symbol',
        yaxis_title='Stock Symbol',
        #title_x=0.5, # Center the title
    )

    # Display Plotly chart in Streamlit
    st.plotly_chart(fig)

    #Infrence
    st.markdown(
        """
        - **Symbiotic Relationship with High-Growth Tech Stocks:** TSLA's very strong positive correlations with AMD (0.92) and AMZN (0.81) underscore its alignment with broader tech sector movements, reflecting investor sentiment and market trends that favor innovation and growth.
            - *Risk and Reward:* This alignment with the fortunes of the tech sector means TSLA investors are positioned to benefit from the sector's growth but also face heightened risk during tech downturns. Diversifying with stocks outside this high-correlation group can help manage this risk.
            - *Market Influence and Volatility:* TSLA's market performance is often seen as a barometer for investor appetite in technology and sustainable energy. Its strong correlation with other tech stocks may amplify its influence on portfolio performance, warranting careful monitoring and potentially strategic rebalancing to manage exposure.
            - *Sector Analysis for Portfolio Adjustment:* Investors might consider TSLA's performance in the context of broader economic and sector-specific trends, including shifts in consumer behavior, regulatory changes, and technological breakthroughs. Aligning TSLA holdings with these trends can optimize portfolio performance in alignment with long-term market developments.

        TSLA's integration with the tech sector's pulse not only positions it at the forefront of growth opportunities but also calls for strategic portfolio management to navigate the interconnected risks and rewards.
        """,
        unsafe_allow_html=True
    )







