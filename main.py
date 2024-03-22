from intc_page import *
from amd_page import *
from tsla_page import *
from mara_page import *
from amzn_page import *
from predict_module import *
from home import *

# Define the list for the sidebar selection
sidebar_list = ['Home', 'INTC', 'AMD', 'TSLA', 'MARA', 'AMZN', 'Make Prediction 💹']

# Sidebar for stock selection
selected_page = st.sidebar.selectbox('Select a page:', sidebar_list)



# Function calls to render the selected stock's page
if selected_page == 'Home':
    home_page()
elif selected_page == 'INTC':
    intc_page(data)
elif selected_page == 'AMD':
    amd_page(data)
elif selected_page == 'TSLA':
    tsla_page(data)
elif selected_page == 'MARA':
    mara_page(data)
elif selected_page == 'AMZN':
    amzn_page(data)
else:
    input_page()