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


def intc_page(data):
    #st.title(f"{selected_stock} Insights and Visualizations")

    st.markdown(
        """
        <div style='color: #0096FF;'>
        <p style='font-size: 23px;  font-weight: bold;'>Welcome to the INTC Insights Page!</p>
        </div>
        
        On this page, we dive deep into the performance and market dynamics of Intel Corporation (INTC), a leader in the semiconductor industry. Explore comprehensive analyses, from closing prices and daily volatility to in-depth technical indicators. Understand INTC's market position, historical trends, and what these might mean for future performance. Whether you're considering investing in INTC or simply want to learn more about its stock behavior, you'll find valuable insights here.
        
        """,
        unsafe_allow_html=True)
    

    # Load data
    intc_data = load_data()

    # Displaying the dataset for AMD
    st.markdown("#### INTC Stock Data")
    display_data = intc_data.copy()
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

    
    
    # Filter data for INTC
    intc_data = display_data.copy()
    intc_data['O-C'] = intc_data['Close'] - intc_data['Open']  #O-C

    # Plotting Closing Prices for INTC
    # Using st.markdown() to customize font size
    st.markdown("""
    <style>
    .font {
        font-size:20px !important;
    }
    </style>
    """, unsafe_allow_html=True)
    st.markdown('<p class="font">INTC Closing Prices Over The Last Decade</p>', unsafe_allow_html=True) 

    # Define radio button with options
    plot_option = st.radio("Choose a plot type:", ('Line Plot', 'Candlestick Plot'))

    if plot_option == 'Line Plot':
        # Line plot for INTC Closing Prices
        fig = px.line(intc_data, 
                    x='Date', 
                    y='Close')
        fig.update_layout(height=480, width=700,xaxis_title='Date',
                        yaxis_title='Closing Price')
        st.plotly_chart(fig)

    elif plot_option == 'Candlestick Plot':
        # Candlestick plot
        figure = go.Figure(data=[go.Candlestick(x=intc_data["Date"],
                                            open=intc_data["Open"], 
                                            high=intc_data["High"],
                                            low=intc_data["Low"], 
                                            close=intc_data["Close"],
                                            increasing_line_color='green', increasing_fillcolor='green',
                                            decreasing_line_color='red', decreasing_fillcolor='red')])
        figure.update_layout(height=480, width=700,xaxis_rangeslider_visible=False)
                            
        st.plotly_chart(figure)



    
    # Inference
    st.markdown(
    """

    - **Decade of Resilience and Challenges:** INTC, a titan in the semiconductor industry, has navigated through a decade marked by technological revolutions, competitive pressures, and changing market demands. This plot of INTC's closing prices over the last decade encapsulates a story of resilience amidst the dynamic tech landscape.

    - **Stable Yet Cautious Growth:** Unlike the meteoric rise seen in some tech stocks, INTC has shown a pattern of steady growth punctuated by periods of stagnation and mild volatility. This trend suggests a company that is firmly rooted in its core business, yet facing the constant challenge of innovation and market expansion.

    - **Impact of Industry Dynamics:** The plot reveals moments of notable price movements, which often correlate with key industry events such as product launches, competitive advancements, and shifts in global supply chains. These fluctuations highlight INTC's sensitivity to both its internal strategic decisions and the broader industry environment.

    - **Investor Sentiment and Market Position:** The closing prices reflect investor sentiment towards INTC's ability to maintain its market position and capitalize on growth opportunities in the evolving semiconductor space. Periods of price stability suggest investor confidence, while downturns may reflect market uncertainties or concerns over future growth prospects.

    - **Looking Ahead:** As INTC continues to adapt to the fast-paced technological landscape, this decade-long view of its stock performance serves as a reminder of the importance of innovation, strategic foresight, and market responsiveness. Investors and analysts alike will be keenly watching how INTC positions itself in the face of emerging technologies and competitive pressures.
    """,
    unsafe_allow_html=True
    )

    # Create the line plot for INTC's daily volatility
    fig = px.line(intc_data, x='Date', y='O-C', title=f'INTC Daily Volatility (Open - Close)',
                hover_data={'DayOfWeek': True}, 
                text='DayOfWeek')

    # Update traces to display the custom hover text
    fig.update_traces(mode='lines', hoverinfo='text', line=dict(width=2, color='skyblue'))  # Here you can specify the color

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
    **Observation:** INTC exhibits minimal daily volatility, showcasing a mature and stable market position less affected by rapid industry shifts. This steadiness might appeal to investors seeking less risky assets.

    **Recommendation:** INTC's stability and strong market position make it a potentially safer bet for investors seeking steady returns and lower volatility. It could serve as a defensive stock in a diversified portfolio, offering protection against broader market volatility. However, investors should also monitor Intel's strategies for innovation and market competition to ensure it can maintain its position and continue to provide value.

    """,
    unsafe_allow_html=True
    )



    ##INTC Trading Volume vs Closing Price Over Time

    # Create subplots with 1 row and 1 column, setting up a secondary y-axis
    fig = make_subplots(rows=1, cols=1, shared_xaxes=True, 
                        vertical_spacing=0.04, 
                        specs=[[{"secondary_y": True}]])

    # Add volume bar chart with solid color for better visibility
    fig.add_trace(
        go.Bar(x=intc_data['Date'], y=intc_data['Trade Volume'], name="Trade Volume", marker=dict(color='rgb(50, 171, 96)')),
        row=1, col=1, secondary_y=False
    )

    # Add closing price line chart
    fig.add_trace(
        go.Scatter(x=intc_data['Date'], y=intc_data['Close'], name="Closing Price", line=dict(color='skyblue')),
        row=1, col=1, secondary_y=True
    )

    # Update layout with a suitable title
    fig.update_layout(height=480, width=700, title_text="INTC Trading Volume vs Closing Price Over Time",
                    showlegend=False, template="plotly_white")

    # Set x-axis and y-axes titles
    fig.update_xaxes(title_text="Date")
    fig.update_yaxes(title_text="<b>Trade Volume</b>", secondary_y=False)
    fig.update_yaxes(title_text="<b>Closing Price</b>", secondary_y=True)

    # Display Plotly chart in Streamlit
    st.plotly_chart(fig)

    #Inference for Intel
    st.markdown(
    """
    As a stalwart in the semiconductor industry, Intel's performance over the last decade reveals a narrative of stability and endurance amidst the rapidly evolving tech landscape. An analysis of its trading volumes and stock price movements provides a foundation for understanding Intel's position from an investor's perspective.

    Intel's trading volumes have been relatively moderate, a reflection not of investor apathy but of the stock's consistent, stable performance over the years. This stability is a testament to Intel's established position in the semiconductor industry, a sector known for its cyclical nature and fierce competition. Unlike the dramatic fluctuations observed in the trading volumes of newer, more speculative investments, Intel's steadiness is indicative of a mature company with a long-standing investor base.

    However, this very stability might also be interpreted as a sign of the challenges Intel faces in maintaining high growth rates. The semiconductor industry is marked by rapid technological advancements and shifting market dynamics, with new entrants and existing competitors alike vying for dominance. Intel's moderate trading volumes, in this light, could suggest investor caution, reflecting concerns about the company's ability to innovate and compete effectively in an industry where technological leadership is paramount.

    For investors, Intel's stock presents a dichotomy. On one hand, its stability offers a semblance of safety, appealing to those seeking less volatile investments within the tech sector. On the other hand, the moderate trading volumes and the underlying reasons for this stability warrant a closer examination of Intel's growth strategy, competitive positioning, and potential for market disruption.

    Investing in Intel, therefore, requires a balanced view that considers its established market presence against the backdrop of an industry in flux. Potential investors should weigh the company's efforts to innovate and capture new growth opportunities against the inherent challenges of competing in a sector that demands constant evolution. A well-informed investment strategy for Intel will embrace both its enduring strengths and the imperative for adaptability in the face of technological change.
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
        - **Unique Position in the Semiconductor Industry:** Despite being part of the tech sector, INTC's stock movements show a distinct pattern with moderate to low correlations with AMZN (0.63), AMD (0.34), and TSLA (0.21). This differentiation highlights INTC's unique market dynamics compared to other high-growth tech companies.
            - *Investment Implication:* INTC's diverse correlation profile can be an asset for investors seeking to mitigate risk within the tech sector. Its moderate correlation with AMZN and lower correlations with AMD and TSLA suggest that INTC may respond differently to market events, providing a stabilizing effect in a tech-heavy portfolio.
            - *Sector Diversification:* Given its established presence and focus on innovation within the semiconductor industry, INTC represents a potentially more stable investment option, offering a counterbalance to the volatility of newer tech market entrants.

        INTC's positioning as a cornerstone in the semiconductor industry, coupled with its unique correlation profile, underscores its value for investors aiming for diversified, stable exposure within the technology sector.
        """,
        unsafe_allow_html=True
    )











    
    