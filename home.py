import streamlit as st

def home_page():

    # Welcome message with Markdown styling
    st.markdown(
        """
        <div style='color: #FF4B4B;'>
        <p style='font-size: 23px;  font-weight: bold;'>Welcome to QuantForecast!</p>
        </div>
        Welcome to QuantForecast, your go-to app for stock market insights and predictions, where we unravel the intricacies of the stock market through the lens of five pivotal stocks: INTC, AMD, TSLA, MARA, and AMZN. In a market rich with opportunities and risks, these stocks stand out for their impact and the unique investment prospects they offer.
                
        <p></p>
        <p>Our mission is to provide concise, data-driven insights that guide you to smarter investment decisions. Through targeted analysis, we'll explore trends, forecast potential shifts, and decode market signals, empowering you to navigate the market's ebbs and flows with confidence. Let's embark on this analytical journey together, leveraging insights to harness the potential of these key stocks.
        Dive into the analytics to explore trends, uncover patterns, and get predictions to navigate the complexities of the stock market with confidence.
        </p>
        """,
        unsafe_allow_html=True
    )

    # Introduction to other pages
    st.markdown(
        """
        #### What to Expect Across QuantForecast:

        - **INTC, AMD, TSLA, MARA, AMZN Pages**: Each stock has its dedicated page, offering a deep dive into its performance, market trends, and a unique set of insights derived from our analyses. Whether you're interested in the technological advancements of AMD and INTC, the innovative strides of TSLA, the cryptocurrency influence on MARA, or the e-commerce giant AMZN, you'll find tailored insights to guide your investment choices.

        - **Make Prediction 💹**: Our predictive analytics feature is a must-visit for those looking to stay ahead. Leveraging advanced algorithms, we offer predictions on stock movements, helping you make informed decisions based on future outlooks rather than just historical performance.

        **Explore, analyze, and strategize with QuantForecast.** Whether you're a seasoned investor or new to the stock market, our app aims to equip you with the insights needed to navigate the investment landscape with greater confidence and foresight.
        """
    )

