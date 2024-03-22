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
    ticker = 'AMZN'
    start_date = "2014-01-01"
    end_date = datetime.datetime.now().strftime('%Y-%m-%d')  # Format the current date as a string
    data = yf.download(ticker, start=start_date, end=end_date)
    data.reset_index(inplace=True)
    return data



def amzn_page(data):
    st.markdown(
        """
        <div style='color: #FF5733;'>
        <p style='font-size: 23px;  font-weight: bold;'>Welcome to the AMZN Insights Page!</p>
        </div>
        
        Delve into the world of Amazon.com, Inc. (AMZN), a global powerhouse in e-commerce and cloud computing. Here, you'll find detailed visualizations and analyses of AMZN's stock performance, showcasing its growth dynamics, market influence, and what these mean for future prospects. Explore the data behind Amazon's expansive reach and its strategic moves in the market.
        
        """,
        unsafe_allow_html=True)
    

    # Load data
    amzn_data = load_data()

    # Displaying the dataset for AMD
    st.markdown("#### AMZN Stock Data")
    display_data = amzn_data.copy()
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
    amzn_data = display_data.copy()
    amzn_data['O-C'] = amzn_data['Close'] - amzn_data['Open']  #O-C
    
    # Plotting Closing Prices for AMZN
    # Using st.markdown() to customize font size
    st.markdown("""
    <style>
    .font {
        font-size:20px !important;
    }
    </style>
    """, unsafe_allow_html=True)
    st.markdown('<p class="font">AMZN Closing Prices Over The Last Decade</p>', unsafe_allow_html=True) 

    # Define radio button with options
    plot_option = st.radio("Choose a plot type:", ('Line Plot', 'Candlestick Plot'))

    if plot_option == 'Line Plot':
        # Line plot for INTC Closing Prices
        fig = px.line(amzn_data, 
                    x='Date', 
                    y='Close',
                    color_discrete_sequence=['#FF5733'])
        fig.update_layout(height=480, width=700,xaxis_title='Date',
                        yaxis_title='Closing Price')
        st.plotly_chart(fig)

    elif plot_option == 'Candlestick Plot':
        # Candlestick plot
        figure = go.Figure(data=[go.Candlestick(x=amzn_data["Date"],
                                            open=amzn_data["Open"], 
                                            high=amzn_data["High"],
                                            low=amzn_data["Low"], 
                                            close=amzn_data["Close"],
                                            increasing_line_color='green', increasing_fillcolor='green',
                                            decreasing_line_color='red', decreasing_fillcolor='red')])
        figure.update_layout(height=480, width=700,xaxis_rangeslider_visible=False)
                            
        st.plotly_chart(figure)

    # Inference
    st.markdown("""

    - **Robust Growth Trajectory:** Amazon's stock has displayed a remarkable upward trajectory over the past decade, highlighting the company's dominant position in the e-commerce sector and its successful expansion into cloud computing, digital streaming, and artificial intelligence. This growth reflects investors' confidence in Amazon's business model, innovation, and market expansion strategies.

    - **E-Commerce and Cloud Computing Synergies:** The consistent rise in AMZN's stock price underscores the synergy between its e-commerce platform and AWS (Amazon Web Services), its cloud computing division. AWS's profitability has significantly contributed to Amazon's overall financial health, making it a key driver of stock performance.

    - **Resilience in Market Fluctuations:** Despite experiencing volatility during market downturns and global economic uncertainties, AMZN has shown resilience and a strong capacity for recovery. Its ability to adapt to changing consumer behaviors, especially during times of increased online shopping, has reinforced its market leadership.

    - **Investor Sentiment and Future Prospects:** The sustained increase in Amazon's stock price over the years indicates positive investor sentiment and confidence in the company's long-term growth potential. Future prospects, including ventures into new markets and technologies, are likely to further influence its stock performance.

    - **Strategic Implications for Investors:** The historical performance of AMZN's stock serves as a testament to the company's robust business model and its ability to innovate and capture market share. Investors considering AMZN should weigh its growth potential against market expectations and valuation metrics. The company's continued investment in innovation and expansion into new markets presents both opportunities and challenges for future growth.

    This analysis provides a snapshot of Amazon's impressive growth and the factors contributing to its stock performance, offering valuable insights for investors looking to understand the dynamics behind one of the most influential companies in the global market.

    """, unsafe_allow_html=True)


    # Create the line plot for TSLA's daily volatility
    fig = px.line(amzn_data, x='Date', y='O-C', title=f'AMZN Daily Volatility (Open - Close)',
                hover_data={'DayOfWeek': True}, 
                text='DayOfWeek')

    # Update traces to display the custom hover text
    fig.update_traces(mode='lines', hoverinfo='text', line=dict(width=2, color='#FFAC1C'))  # Here you can specify the color

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
    **Observation:** AMZN shows moderate volatility with spikes in recent years, reflective of ongoing innovations, market expansions, and the tech sector's overall dynamics. The movements indicate investor reactions to company developments and broader tech trends.

    **Recommendation:** Investors in AMZN should consider a balanced approach, recognizing Amazon's solid market position and growth prospects in e-commerce, cloud computing, and other ventures. While there are opportunities for growth, the stock's volatility requires a cautious strategy, potentially focusing on long-term growth while being mindful of market corrections and tech sector fluctuations.

    """,
    unsafe_allow_html=True
    )



    ##AMZN Trading Volume vs Closing Price Over Time

    # Create subplots with 1 row and 1 column, setting up a secondary y-axis
    fig = make_subplots(rows=1, cols=1, shared_xaxes=True, 
                        vertical_spacing=0.04, 
                        specs=[[{"secondary_y": True}]])

    # Add volume bar chart with solid color for better visibility
    fig.add_trace(
        go.Bar(x=amzn_data['Date'], y=amzn_data['Trade Volume'], name="Trade Volume", marker=dict(color='rgb(50, 171, 96)')),
        row=1, col=1, secondary_y=False
    )

    # Add closing price line chart
    fig.add_trace(
        go.Scatter(x=amzn_data['Date'], y=amzn_data['Close'], name="Closing Price", line=dict(color='#FFAC1C')),
        row=1, col=1, secondary_y=True
    )

    # Update layout with a suitable title
    fig.update_layout(height=480, width=700, title_text="AMZN Trading Volume vs Closing Price Over Time",
                    showlegend=False, template="plotly_white")

    # Set x-axis and y-axes titles
    fig.update_xaxes(title_text="Date")
    fig.update_yaxes(title_text="<b>Trade Volume</b>", secondary_y=False)
    fig.update_yaxes(title_text="<b>Closing Price</b>", secondary_y=True)

    # Display Plotly chart in Streamlit
    st.plotly_chart(fig)

    #Inference
    st.markdown(
    """
    Over the years, Amazon has demonstrated an impressive trajectory of stock price growth, becoming a centerpiece of investment strategies across the globe. A detailed examination of its trading volume and price movements reveals a nuanced narrative for potential investors.

    In the initial half of the last decade (2014-2019), Amazon's trading volumes were notably higher, reflecting a period of heightened market activity and investor interest. This era can be associated with Amazon's rapid expansion into new markets, its dominance in e-commerce, and significant investments in cloud computing and artificial intelligence, sparking investor enthusiasm and speculative trading.

    However, in recent years, despite the continued upward trajectory in its stock price, there has been a discernible decrease in daily trading volumes. This shift could suggest a maturation phase for Amazon, where wild speculative trading gives way to more stable, long-term holding by investors confident in the company's growth story and less reactive to short-term market dynamics.

    An interesting observation is the correlation between trading volume spikes and price reversals, particularly during downward movements. This pattern suggests that significant sell-offs, potentially driven by profit-taking or reactions to broader market trends, prompt increased trading activity. For investors, these moments can represent strategic entry or re-entry points, assuming a long-term belief in Amazon's market position and growth potential.

    Investors should consider these insights in the context of their portfolios. While the decrease in volume might imply a stabilization, the correlation between volume spikes and price reversals highlights the importance of staying informed about market trends and Amazon's fundamental strengths. As always, a balanced approach, considering both technical signals and fundamental analysis, is advisable when navigating the complexities of investing in dynamic tech giants like Amazon.
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
    - **Tech Sector Growth Engine:** AMZN's significant positive correlations with AMD (0.89) and TSLA (0.81) highlight its role as a central player in the tech growth narrative. These correlations reflect shared market sensitivities and the impact of technological innovations on stock performance.
        - *Diversification Considerations:* While the strong correlation with other tech giants suggests potential for shared growth, it also indicates shared risk. Investors might consider diversification strategies that include sectors or assets with lower correlation to tech to balance portfolio risk.
        - *Long-Term Growth vs. Short-Term Volatility:* The correlation data underscores the importance of differentiating between AMZN's long-term growth potential and short-term market volatility. Investors should weigh these aspects when making investment decisions, particularly in response to market dips or rallies that might affect tech stocks uniformly.
        - *Strategic Portfolio Positioning:* Given AMZN's central role in e-commerce and cloud computing, investors could view its stock as a barometer for tech sector health. Aligning investment strategies with AMZN's performance trends might involve adjusting exposure based on broader tech sector indicators and economic signals.

    AMZN's pivotal position within the tech ecosystem, underscored by its correlations with other leading tech stocks, offers both opportunities and challenges for investors. Navigating this landscape requires a nuanced approach that balances sector enthusiasm with prudent risk management and diversification strategies.
    """,
    unsafe_allow_html=True
    )


