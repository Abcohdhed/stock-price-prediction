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
    ticker = 'INTC'
    start_date = "2014-01-01"
    end_date = datetime.datetime.now().strftime('%Y-%m-%d')  # Format the current date as a string
    data = yf.download(ticker, start=start_date, end=end_date)
    data.reset_index(inplace=True)
    return data


def mara_page(data):
    st.markdown(
        """
        <div style='color: #6082B6;'>
        <p style='font-size: 23px;  font-weight: bold;'>Welcome to the MARA Insights Page!</p>
        </div>
        
        Welcome to your destination for insights on Marathon Digital Holdings (MARA), a trailblazer in the cryptocurrency mining industry. This page offers a lens into MARA's stock performance, encapsulating its volatility, market trends, and the broader implications of blockchain technology on its valuation. Navigate through our analyses to gauge MARA's investment prospects in the evolving digital currency landscape.
        
        """,
        unsafe_allow_html=True)
    

    # Load data
    mara_data = load_data()

    # Displaying the dataset for AMD
    st.markdown("#### MARA Stock Data")
    display_data = mara_data.copy()
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

    
    
    # Filter data for MARA
    mara_data = display_data.copy()
    mara_data['O-C'] = mara_data['Close'] - mara_data['Open']  #O-C
    
    # Plotting Closing Prices for MARA
    # Using st.markdown() to customize font size
    st.markdown("""
    <style>
    .font {
        font-size:20px !important;
    }
    </style>
    """, unsafe_allow_html=True)
    st.markdown('<p class="font">MARA Closing Prices Over The Last Decade</p>', unsafe_allow_html=True) 

    # Define radio button with options
    plot_option = st.radio("Choose a plot type:", ('Line Plot', 'Candlestick Plot'))

    if plot_option == 'Line Plot':
        # Line plot for INTC Closing Prices
        fig = px.line(mara_data, 
                    x='Date', 
                    y='Close',
                    color_discrete_sequence=['#6082B6'])
        fig.update_layout(height=480, width=700, xaxis_title='Date',
                        yaxis_title='Closing Price')
        st.plotly_chart(fig)

    elif plot_option == 'Candlestick Plot':
        # Candlestick plot
        figure = go.Figure(data=[go.Candlestick(x=mara_data["Date"],
                                            open=mara_data["Open"], 
                                            high=mara_data["High"],
                                            low=mara_data["Low"], 
                                            close=mara_data["Close"],
                                            increasing_line_color='green', increasing_fillcolor='green',
                                            decreasing_line_color='red', decreasing_fillcolor='red')])
        figure.update_layout(height=480, width=700, xaxis_rangeslider_visible=False)
                            
        st.plotly_chart(figure)

    
    # Inference
    st.markdown("""

    - **Downward Trend Amidst Cryptocurrency Volatility:** The closing prices for MARA have demonstrated a pronounced downward trend over the last decade, reflecting the challenges and volatility inherent in the cryptocurrency market. This trend suggests that despite the potential for high returns, investing in cryptocurrency-related stocks like MARA involves significant risks.

    - **Market Sensitivity and Investor Caution:** The decline in MARA's stock price underscores the sensitivity of cryptocurrency mining companies to market fluctuations, regulatory changes, and shifts in investor sentiment. The downward trajectory may indicate periods of reduced investor confidence or concerns over the sustainability of mining operations amid fluctuating cryptocurrency prices.

    - **Impact of Operational and External Factors:** MARA's performance is likely influenced by a range of operational factors, including mining efficiency, energy costs, and technological advancements, as well as external factors such as regulatory developments and competition within the cryptocurrency mining industry. The stock's decline may reflect broader challenges faced by the company in navigating these complex dynamics.

    - **Long-Term Investor Considerations:** For investors, the historical performance of MARA's stock serves as a cautionary tale on the importance of due diligence and risk assessment when investing in the volatile cryptocurrency sector. It highlights the need for a strategic approach, considering both the potential rewards and the risks associated with fluctuations in the digital asset market.

    - **Looking Ahead:** The future trajectory of MARA's stock will likely continue to be closely tied to the fortunes of the cryptocurrency market, regulatory landscapes, and the company's ability to adapt to changing market conditions. Investors should closely monitor these factors and be prepared for continued volatility in the stock's price.

    This analysis offers a comprehensive view of the factors contributing to MARA's downward trend and emphasizes the importance of informed investment decisions in the high-risk environment of cryptocurrency-related stocks.

    """, unsafe_allow_html=True)


    # Create the line plot for TSLA's daily volatility
    fig = px.line(mara_data, x='Date', y='O-C', title=f'MARA Daily Volatility (Open - Close)',
                hover_data={'DayOfWeek': True}, 
                text='DayOfWeek')

    # Update traces to display the custom hover text
    fig.update_traces(mode='lines', hoverinfo='text', line=dict(width=2, color='#6082B6'))  # Here you can specify the color

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
    **Observation:** MARA displayed pronounced volatility in its early years (2014-2018), indicative of its high sensitivity to market trends, regulatory news, and technological advancements. The recent years have seen a reduction in volatility, pointing towards a potential stabilization in the company's market position or investor perceptions.

    **Recommendation:** Investors interested in MARA should remain vigilant of the cryptocurrency market trends and regulatory environments, given MARA's close ties to blockchain and digital assets. While the recent stabilization suggests a maturing market position, the inherent volatility of the sector means investors should be prepared for sudden market movements. Diversification and a keen eye on industry developments are advised.

    """,
    unsafe_allow_html=True
    )



    ##MARA Trading Volume vs Closing Price Over Time

    # Create subplots with 1 row and 1 column, setting up a secondary y-axis
    fig = make_subplots(rows=1, cols=1, shared_xaxes=True, 
                        vertical_spacing=0.04, 
                        specs=[[{"secondary_y": True}]])

    # Add volume bar chart with solid color for better visibility
    fig.add_trace(
        go.Bar(x=mara_data['Date'], y=mara_data['Trade Volume'], name="Trade Volume", marker=dict(color='rgb(50, 171, 96)')),
        row=1, col=1, secondary_y=False
    )

    # Add closing price line chart
    fig.add_trace(
        go.Scatter(x=mara_data['Date'], y=mara_data['Close'], name="Closing Price", line=dict(color='#6082B6')),
        row=1, col=1, secondary_y=True
    )

    # Update layout with a suitable title
    fig.update_layout(height=480, width=700, title_text="MARA Trading Volume vs Closing Price Over Time",
                    showlegend=False, template="plotly_white")

    # Set x-axis and y-axes titles
    fig.update_xaxes(title_text="Date")
    fig.update_yaxes(title_text="<b>Trade Volume</b>", secondary_y=False)
    fig.update_yaxes(title_text="<b>Closing Price</b>", secondary_y=True)

    # Display Plotly chart in Streamlit
    st.plotly_chart(fig)

    #Inference for MARA
    st.markdown(
    """
    MARA's trading history, particularly when comparing the early years of the last decade to the present, offers a fascinating study in contrast and adaptation. The evolution of trading volumes against the backdrop of MARA's stock performance reveals underlying trends and shifts in investor sentiment and market dynamics that are critical for potential investors.

    In the initial years of the last decade, MARA's trading volumes were remarkably low, almost to the point of invisibility on some charts. This period, characterized by lesser investor engagement, might reflect the early stages of MARA's market development or a lack of broader market recognition. The low trading volumes could also suggest that MARA was, at the time, considered a more speculative or niche investment, not yet capturing the wider interest of the investment community.

    However, a dramatic shift occurred starting from 2020, with trading volumes surging significantly. This increase aligns with a growing interest in blockchain technology and digital currencies, sectors in which MARA has vested interests. The rise in trading volumes during this period likely reflects a heightened awareness of MARA's potential role and stake in these burgeoning markets, fueled by speculative trading and investors seeking to capitalize on the explosive growth of digital assets.

    This shift in trading dynamics, from near invisibility to significant market presence, underscores the importance of understanding market trends, technological advancements, and their implications for investment strategies. For investors, the increase in trading volumes coupled with MARA's performance trajectory suggests a growing market consensus around the value and potential of MARA's business model and its alignment with future technological trends.

    Investors considering MARA should be mindful of the volatility associated with high trading volumes, especially in sectors as unpredictable and rapidly evolving as blockchain and digital currencies. The recent history of trading volumes indicates not only growing interest but also increased market speculation, which can lead to price volatility.

    In conclusion, MARA's trading volume history offers a narrative of transformation and emerging market relevance. Investors interested in MARA need to balance the potential for high returns with the risks inherent in investing in highly volatile and speculative markets. Monitoring MARA's strategic direction, market adoption, and technological advancements will be key to navigating the investment opportunities and challenges it presents.
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

    #Inference
    st.markdown(
        """
        - **Contrarian Movement with Tech Giants:** MARA's stock exhibits negative correlations with tech giants like AMZN (-0.48) and AMD (-0.3), setting it apart in terms of price movement dynamics. This inverse relationship underlines MARA's distinct market drivers and its potential role as a hedge within a tech-focused portfolio.
            - *Strategic Hedging:* For investors predominantly exposed to the tech sector, incorporating MARA could serve as a strategic hedge, potentially offsetting losses in tech stocks during downturns. This approach leverages MARA's negative correlation to enhance portfolio resilience against tech sector volatility.
            - *Market Sensitivity Analysis:* Investors should carefully analyze the factors driving MARA's inverse correlation with other tech stocks, including market sentiment, regulatory impacts, and technological advancements. Understanding these dynamics can help investors make informed decisions about timing entries and exits in MARA as part of a broader investment strategy.

        MARA offers a unique investment angle within the tech landscape, presenting opportunities for strategic hedging and diversification. Its contrarian movement relative to other tech giants could be a key asset for investors looking to build a balanced and resilient portfolio.
        """,
        unsafe_allow_html=True
    )
