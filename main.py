import streamlit as st

# CSS styles
css = '''
<style>
.reportview-container {
        background: url("image/bg.png");
    }
}

/* Center the main content */
.main-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin: 0 auto;
    width: 100%;
    max-width: 800px;
}

.button {
    width: 100%;
    font-size: 1.2em;
}
</style>
'''

# Apply CSS to Streamlit
st.markdown(css, unsafe_allow_html=True)

# Main content
st.markdown('<div class="main-content">', unsafe_allow_html=True)

st.header('簡易アプリ')
st.write('このアプリが正常に動作している場合、以下のテキストが表示されます。')

if st.button('次へ進む', use_container_width=True):
    st.write('ボタンがクリックされました！')

st.markdown('</div>', unsafe_allow_html=True)
