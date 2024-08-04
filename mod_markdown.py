import streamlit as st

def display_safari_warning():
    st.warning("This application may not function optimally on Safari. For the best experience, please use Chrome or Firefox.")

# Load custom CSS
def load_css():
    st.markdown("""
    <style>
    /* Import fonts */
    @font-face {
      font-family: 'Lexend';
      font-display: block;
      src: url('https://example.com/fonts/Lexend-Regular.ttf') format('truetype'); /* Update with correct URL */
      font-weight: 400;
    }

    /* Define colors */
    :root {
      --background: #21232F;
      --main: #e7ebb2;
      --header: #d3738b;
      --element-background: #2d3143;
      --element-placeholder: #5D605E;
      --privacy-color: #848770;
      --element-main: white;
    }

    /* CSS reset */
    html {
      box-sizing: border-box;
      font-size: 16px;
    }

    *, *:before, *:after {
      box-sizing: inherit;
    }

    body, h1, h2, h3, h4, h5, h6, p, ol, ul {
      margin: 0;
      padding: 0;
      font-weight: normal;
    }

    ol, ul {
      list-style: none;
    }

    img {
      max-width: 100%;
      height: auto;
    }

    input, select {
      appearance: none;
      background-color: transparent;
      border: none;
      padding: 0 1em 0 0;
      margin: 0;
      width: 100%;
      font-family: inherit;
      font-size: inherit;
      cursor: inherit;
      line-height: inherit;
    }

    /* Begin styles */
    body {
      background-color: var(--background);
      background-attachment: fixed;
      background-repeat: no-repeat;
      background-position: bottom center;
      background-size: 100% 50%;
      position: absolute;
      top: 0;
      left: 0;
      margin: 0;
      padding: 0;
      width: 100vw;
      height: 100vh;
      overflow-x: hidden;
    }

    .sections {
      display: flex;
      margin-top: -3vh;
      height: 100vh;
      justify-content: center;
      align-items: center;
    }

    .section-prompt {
      font-family: Lexend;
      font-weight: 400;
      text-align: center;
      font-size: 3vh;
      color: var(--main);
    }

    input, select {
      border: 3px solid black;
      border-radius: 3vh;
      font-size: 4.2vh;
      height: 12.5vh;
      width: 68vh;
      background: transparent;
      padding: 4vh;
      font-family: Nunito;
      font-weight: 500;
      text-align: center;
    }

    textarea {
      width: 60vh;
      height: 35vh;
      font-family: Lexend;
      background: var(--element-background);
      border: none;
      border-radius: 3vh;
      padding: 5vh;
      font-size: 2.5vh;
      color: var(--main);
    }

    .button {
      width: 45vh;
      height: 8.75vh;
      background: linear-gradient(45deg, rgba(231, 235, 178, 0), rgba(231, 235, 178, 0), rgba(231, 235, 178, .3));
      border: 2px solid var(--main);
      border-radius: 100vh;
      color: var(--main);
      font-family: Lexend;
      font-weight: 500;
      font-size: 2.2vh;
      cursor: pointer;
      transition: transform 0.3s, opacity .8s;
    }

    @media (max-aspect-ratio: 3/5) {
      .section-prompt {
        width: 36vh;
        font-size: 2.5vh;
      }

      .button {
        width: 36vh;
      }

      textarea {
        width: 80vw;
      }
    }
    </style>
    """, unsafe_allow_html=True)

# Load custom CSS
load_css()

# Main app
st.title("Custom Streamlit Web App")

# Example form
st.header("User Input Form")
with st.form(key='my_form'):
    st.subheader("Enter Your Information")
    name = st.text_input("Name")
    email = st.text_input("Email")
    message = st.text_area("Message")
    submit_button = st.form_submit_button(label='Submit')

    if submit_button:
        st.success(f"Thank you {name}, your message has been received!")

# Example dynamic content
st.header("Dynamic Content Example")
st.write("This section can display dynamic content based on user interactions or data.")

# Example of conditional rendering
if name:
    st.write(f"Hello, {name}! Nice to meet you.")

# Example for data visualization
st.header("Data Visualization Example")
# Assuming we have some data
import pandas as pd
import numpy as np
data = pd.DataFrame({
    'X': np.random.randn(100),
    'Y': np.random.randn(100)
})
st.line_chart(data)

# Footer or additional info
st.markdown("### Footer")
st.markdown("This is an example footer where you can add additional information or links.")

