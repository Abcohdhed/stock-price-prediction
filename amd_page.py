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


def load_data():
    ticker = 'AMD'
    start_date = "2014-01-01"
    end_date = datetime.datetime.now().strftime('%Y-%m-%d')  # Format the current date as a string
    data = yf.download(ticker, start=start_date, end=end_date)
    data.reset_index(inplace=True)
    return data


def amd_page(data):
    st.markdown(
        """
        <div style='color: #50C878;'>
        <p style='font-size: 23px;  font-weight: bold;'>Welcome to the AMD Insights Page!</p>
        </div>
        
        Discover the journey of Advanced Micro Devices (AMD), a key player in the semiconductor sector, through data-driven insights and visualizations. This page covers AMD's stock performance, highlighting growth trends, market volatility, and predictive analytics. Gain a deeper understanding of AMD's competitive edge and investment potential as we unpack the factors driving its market value.
        
        """,
        unsafe_allow_html=True)
    

    # Load data
    amd_data = load_data()

    # Displaying the dataset for AMD
    st.markdown("#### AMD Stock Data")
    display_data = amd_data.copy()
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


    # Filter data for AMD
    amd_data = display_data.copy()
    amd_data['O-C'] = amd_data['Close'] - amd_data['Open']  #O-C

    # Closing Prices for AMD
    # Using st.markdown() to customize font size
    st.markdown("""
    <style>
    .font {
        font-size:20px !important;
    }
    </style>
    """, unsafe_allow_html=True)
    st.markdown('<p class="font">AMD Closing Prices Over The Last Decade</p>', unsafe_allow_html=True) 

    # Define radio button with options
    plot_option = st.radio("Choose a plot type:", ('Line Plot', 'Candlestick Plot'))

    if plot_option == 'Line Plot':
        # Line plot for INTC Closing Prices
        fig = px.line(amd_data, 
                    x='Date', 
                    y='Close',
                    color_discrete_sequence=['#50C878'])
        fig.update_layout(height=480, width=700,xaxis_title='Date',
                        yaxis_title='Closing Price')
        st.plotly_chart(fig)

    elif plot_option == 'Candlestick Plot':
        # Candlestick plot
        figure = go.Figure(data=[go.Candlestick(x=amd_data["Date"],
                                            open=amd_data["Open"], 
                                            high=amd_data["High"],
                                            low=amd_data["Low"], 
                                            close=amd_data["Close"],
                                            increasing_line_color='green', increasing_fillcolor='green',
                                            decreasing_line_color='red', decreasing_fillcolor='red')])
        figure.update_layout(height=480, width=700,xaxis_rangeslider_visible=False)
                            
        st.plotly_chart(figure)


    
    # Inference
    st.markdown(
    """

    - **Remarkable Growth Trajectory:** AMD's journey over the last decade has been nothing short of spectacular, showcasing a remarkable growth trajectory that underscores its success in the highly competitive semiconductor industry. This plot captures the essence of AMD's transformation from an underdog to a key player in the tech space.

    - **Innovation and Market Expansion:** The significant uptrend in AMD's closing prices can largely be attributed to its relentless focus on innovation, strategic partnerships, and expansion into new market segments. Each spike and rally in the plot can often be linked to key product launches, technological breakthroughs, or strategic corporate moves.

    - **Volatility as a Growth Indicator:** While AMD's path has been marked by rapid growth, it has not been without its share of volatility. This volatility reflects the dynamic nature of the tech industry and investor sentiment towards AMD's aggressive growth strategies and market positioning. Such fluctuations offer insights into the challenges and opportunities faced by AMD in its quest for market dominance.

    - **Investor Confidence and Speculative Dynamics:** The overall upward trend in AMD's closing prices highlights growing investor confidence in the company's future prospects. Periods of accelerated growth may also reflect speculative dynamics, as investors bet on AMD's potential to capture market share from its competitors and lead innovation in the semiconductor space.

    - **Future Outlook:** As AMD continues to navigate the complexities of the semiconductor industry, this plot of its decade-long stock performance reflects not just past achievements but also the potential for future growth. Investors and market analysts will closely monitor AMD's strategic initiatives and market adaptation strategies, looking for signs of sustained growth and profitability in an ever-evolving tech landscape.

    """,
    unsafe_allow_html=True
    )


    # Create the line plot for AMD's daily volatility
    fig = px.line(amd_data, x='Date', y='O-C', title=f'AMD Daily Volatility (Open - Close)',
                hover_data={'DayOfWeek': True}, 
                text='DayOfWeek')

    # Update traces to display the custom hover text
    fig.update_traces(mode='lines', hoverinfo='text', line=dict(width=2, color='#AFE1AF'))  # Here you can specify the color

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
    **Observation:** Like AMZN, AMD experiences moderate volatility, punctuated by recent spikes, likely tied to its product launches, competitive positioning in the semiconductor industry, and sector-wide trends.

    **Recommendation:** AMD, being at the forefront of semiconductor technology, offers significant growth opportunities, particularly with increasing demands for computing power, gaming, and AI. Investors might focus on the long-term growth trajectory, considering AMD's innovation capabilities and market expansion. However, staying informed about industry competition and technological advancements is crucial to navigating its volatility.

    """,
    unsafe_allow_html=True
    )



    ##AMD Trading Volume vs Closing Price Over Time

    # Create subplots with 1 row and 1 column, setting up a secondary y-axis
    fig = make_subplots(rows=1, cols=1, shared_xaxes=True, 
                        vertical_spacing=0.04, 
                        specs=[[{"secondary_y": True}]])

    # Add volume bar chart with solid color for better visibility
    fig.add_trace(
        go.Bar(x=amd_data['Date'], y=amd_data['Trade Volume'], name="Trade Volume", marker=dict(color='rgb(50, 171, 96)')),
        row=1, col=1, secondary_y=False
    )

    # Add closing price line chart
    fig.add_trace(
        go.Scatter(x=amd_data['Date'], y=amd_data['Close'], name="Closing Price", line=dict(color='#AFE1AF')),
        row=1, col=1, secondary_y=True
    )

    # Update layout with a suitable title
    fig.update_layout(height=480, width=700, title_text="AMD Trading Volume vs Closing Price Over Time",
                    showlegend=False, template="plotly_white")

    # Set x-axis and y-axes titles
    fig.update_xaxes(title_text="Date")
    fig.update_yaxes(title_text="<b>Trade Volume</b>", secondary_y=False)
    fig.update_yaxes(title_text="<b>Closing Price</b>", secondary_y=True)

    # Display Plotly chart in Streamlit
    st.plotly_chart(fig)

    #Inference for AMD
    st.markdown(
    """
    AMD's journey through the last decade, marked by periods of intense trading activity, underscores a dynamic transformation that captured investor interest and redefined its market position. A close analysis of its trading volumes and price movements reveals pivotal moments in AMD's corporate narrative that have profound implications for investors.

    Between July 2016 and October 2019, AMD experienced exceptionally high trading volumes, a clear indicator of surging investor interest. This period coincides with AMD's strategic shift towards high-performance computing and graphics technologies, challenging established industry giants and positioning itself as a formidable contender in the semiconductor sector. The increased trading volumes during this phase can be attributed to growing investor confidence in AMD's turnaround strategy, product innovation, and market penetration efforts.

    This surge in trading activity suggests that AMD was successfully leveraging technological advancements and strategic partnerships to capture market share and enter new segments, including gaming, data centers, and AI. For investors, this period represented a golden opportunity to participate in AMD's growth story, with the company's stocks becoming a focal point for those seeking exposure to the booming tech sector.

    However, such high trading volumes also signal heightened market sensitivity, where stock prices can be more volatile, reacting swiftly to news, earnings reports, and industry trends. Investors in AMD, therefore, needed to navigate a landscape marked by potential rapid shifts in sentiment and market dynamics.

    For potential investors, understanding the context behind these periods of intense trading activity is crucial. While past performance is not indicative of future results, AMD's ability to innovate and adapt to market demands remains a key consideration. Investors should monitor AMD's ongoing efforts to maintain its competitive edge, invest in research and development, and explore new markets.

    In summary, AMD's historical trading volumes highlight a transformative period in the company's history, offering valuable lessons for investors about timing, risk assessment, and the importance of staying informed about technological and market trends. As AMD continues to evolve, so too should the strategies of those investing in its future.
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
    - **Tech Sector Synergy:** AMD's stock shows a strong positive correlation with both TSLA (0.92) and AMZN (0.89), indicating a close relationship with broader tech sector movements and investor sentiment towards technological innovation and growth.
        - *Portfolio Implications:* This synergy suggests that AMD is a key component of the tech growth narrative. Investors looking to capitalize on technological advancements should consider AMD's role in their portfolio, keeping in mind the correlated risks with other tech giants.
        - *Market Sentiment Indicator:* Given AMD's correlation with tech leaders like TSLA and AMZN, its stock performance can serve as a barometer for investor confidence in the tech sector. Sharp movements in AMD's stock may reflect broader sector shifts, offering strategic insights for timely investment decisions.
    
    - **Volatility and Growth Potential:** The high trading volumes observed, especially from mid-2016 to late 2019, highlight periods of significant investor interest and potential volatility. This period coincides with significant advancements in AMD's technology and market share gains in the semiconductor industry.
        - *Strategic Entry Points:* For investors, these periods of heightened trading activity and volatility could offer opportunities for strategic entry points, assuming a long-term positive outlook on AMD's market position and growth potential.
        - *Risk Management:* Given the potential for significant price swings, investors should consider risk management strategies when including AMD in their portfolios, such as diversification, setting stop-loss orders, or adopting a dollar-cost averaging approach to mitigate the impact of volatility.
    
    Understanding AMD's market dynamics and its correlation with other tech giants is crucial for investors aiming to navigate the tech sector's complexities and capitalize on growth opportunities while managing risk.
    """,
    unsafe_allow_html=True
    )







