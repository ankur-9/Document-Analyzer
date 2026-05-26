import streamlit as st
from rag import process_urls,generate_answers

st.title("Document Analyzer Tool")

with st.sidebar:
    st.markdown("Paste urls below")
    url1 = st.sidebar.text_input("URL1")
    url2 = st.sidebar.text_input("URL2")
    url3 = st.sidebar.text_input("URL3")
    process_url = st.sidebar.button("Process URLs")

placeholder = st.empty()

if process_url:
    urls = list(set([url for url in (url1,url2,url3) if url!='']))
    if len(urls)==0:
        placeholder.text("You must provide at least one valid url")
    else:
        process_urls(urls)

query = st.text_input("Question")
submit = st.button("Get Answer")
if submit:
    if query:
        try:
            answers,sources = generate_answers(query)
            st.header("Answers : ")
            st.write(answers)
            if sources:
                st.header("Source : ")
                for s in range(len(sources)):
                    st.write(sources[s])

        except RuntimeError as e:
            placeholder.text("You must provide at least one valid url")
