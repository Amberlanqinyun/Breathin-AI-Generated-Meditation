import streamlit as st

def set_page_config():
    # Use st.secrets.get with a default value of True
    TESTING = st.secrets.get("TESTING", True)
    st.set_page_config(
        page_title="Meditator",
        page_icon=":sun:",
        layout="centered",
        initial_sidebar_state="expanded" if TESTING else "collapsed",
        menu_items={
            'Report a bug': 'https://github.com/theevann/meditator/issues',
            'About': "https://github.com/theevann/meditator/"
        }
    )

def apply_custom_css():
    st.markdown(
        f"""
        <style>
        @font-face {{
            font-family: 'Lexend';
            font-display: block;
            src: url('/fonts/Lexend-Regular.ttf') format('truetype');
            font-weight: 400;
        }}

        :root {{
            --background: #21232F;
            --main: #e7ebb2;
            --header: #d3738b;
            --element-background: #2d3143;
            --element-placeholder: #5D605E;
            --privacy-color: #848770;
            --element-main: white;
        }}

        body {{
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
        }}

        .sections {{
            display: flex;
            margin-top: -3vh;
            height: 100vh;
            justify-content: center;
            align-items: center;
        }}

        section {{
            opacity: 1;
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            animation: fadeIn 1.2s;
        }}

        section.section-form {{
            animation: fadeIn 1.2s, shiftUp 1.2s;
        }}

        @keyframes fadeIn {{
            0% {{ opacity: 0; }}
            20% {{ opacity: 0; }}
            100% {{ opacity: 1; }}
        }}

        @keyframes shiftUp {{
            0% {{ margin-top: 2vh; }}
            20% {{ margin-top: 2vh; }}
            100% {{ margin-top: 0vh; }}
        }}

        .section-prompt {{
            font-family: Lexend;
            font-weight: 400;
            text-align: center;
            font-size: 3vh;
            letter-spacing: 0.1vh;
            line-height: 6vh;
            width: 43vh;
            color: var(--main);
        }}

        input, select {{
            border: 3px solid black;
            border-radius: 3vh;
            font-size: 4.2vh;
            height: 12.5vh;
            margin-top: 6vh;
            width: 68vh;
            background: transparent;
            padding: 4vh;
            font-family: Nunito;
            font-weight: 500;
            text-align: center;
        }}

        textarea {{
            width: 60vh;
            height: 35vh;
            font-family: Lexend;
            min-height: 25vh;
            max-height: 42vh;
            background: var(--element-background);
            border: none;
            resize: vertical;
            border-radius: 3vh;
            padding: 5vh;
            line-height: 5vh;
            font-size: 2.5vh;
            margin: 5vh;
            transition: transform 1s;
            color: var(--main);
        }}

        .button {{
            display: flex;
            align-items: center;
            justify-content: center;
            width: 45vh;
            height: 8.75vh;
            background: linear-gradient(45deg, rgba(231, 235, 178, 0), rgba(231, 235, 178, 0), rgba(231, 235, 178, .3));
            border: 2px solid var(--main);
            border-radius: 100vh;
            color: var(--main);
            font-family: Lexend;
            font-weight: 500;
            font-size: 2.2vh;
            letter-spacing: 0.2vh;
            cursor: pointer;
            transition: transform 0.3s, opacity .8s;
            text-decoration: none;
            margin: 2vh 0 2vh 0;
        }}

        .button:hover {{
            transform: scale(1.05);
            transition: transform 0.3s;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )
