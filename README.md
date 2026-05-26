# 🏙️ **Document Analyzer Tool**

We are going to build a user-friendly document research tool designed for effortless information retrieval. Users can input article URLs and ask questions to receive relevant insights. (It's features can be extended to any domain.)
![product screenshot](resources/image.png)

<img width="1617" height="706" alt="image" src="https://github.com/user-attachments/assets/fbcea389-172c-417a-b6d9-80e3a43a1262" />

### Features

- Load URLs to fetch article content.
- Process article content through LangChain's SeleniumURLLoader Loader
- Construct an embedding vector using HuggingFace embeddings and leverage ChromaDB as the vectorstore, to enable swift and effective retrieval of relevant information.
- Interact with the LLM's (Llama3 via Groq) by inputting queries and receiving answers along with source URLs.


### Set-up

1. Run the following command to install all dependencies. 

    ```bash
    pip install -r requirements.txt
    ```

2. Create a .env file with your GROQ credentials as follows:
    ```text
    GROQ_MODEL=MODEL_NAME_HERE
    GROQ_API_KEY=GROQ_API_KEY_HERE
    ```

3. Run the streamlit app by running the following command.

    ```bash
    streamlit run main.py
    ```


### Usage/Examples

The web app will open in your browser after the set-up is complete.

- On the sidebar, you can input URLs directly.

- Initiate the data loading and processing by clicking "Process URLs."

- Observe the system as it performs text splitting, generates embedding vectors using HuggingFace's Embedding Model.

- The embeddings will be stored in ChromaDB.

- One can now ask a question and get the answer based on those articles

- In the tutorial, we will use the following articles
  - https://www.ign.com/articles/forza-horizon-6-review
  - https://www.ign.com/wikis/forza-horizon-6/Tips_and_Tricks_-_Everything_to_Know_Before_Playing
  - https://www.ign.com/wikis/forza-horizon-6/Best_Starter_Car


</br>

---<img width="1617" height="706" alt="image" src="https://github.com/user-attachments/assets/e4baa12a-55ac-41fa-8639-19a2fd5eb59b" />
