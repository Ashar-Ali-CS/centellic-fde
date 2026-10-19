


import streamlit as st
import requests



st.set_page_config(page_title="ASSET MANAGE WEBAPP   ", page_icon=":)", layout="centered")

st.title("ASSET MANAGEMENT WEBAPP ")



#This makes it horzizontally allignee
tab1, tab2,tab3,tab4= st.tabs(["1 - SEARCH DOCS", "2 - ASK AGENT" , "3 -  FUNDS SUMMARY ", "VIEW CLIENT PORTFOLIOS"] )

API_URL  = "http://127.0.0.1:8000"


#A separate text box and button for retrieval without generation.
#When clicked, it must call POST /knowledge/search, and:
#List every result returned, with its title and its score
#Handle the case where the index has not been built yet, this returns a specific status code, not a generic failure
#Handle a normal failure differently from the “index not built” case

with tab1: 
    Query = st.text_area("FEATURE 1-  SEMANTIC SEARCH (knowledge/search )  ")
    Top_K = 3

    if st.button("Click me to search"):

        try:
            #Knowledge/search 
            payload = {"question": Query, "top_k": Top_K}
            response = requests.post(f"{API_URL}/knowledge/search", json=payload, timeout=60)
            if response.status_code !=200:
                st.write(f"ERROR HAS OCCURED ON API END - HERE IS STATUS CODE:  {response.status_code}  ")
            data =  response.json()
            st.write(f"Connection successfull heres the  info: {data}")
        except requests.exceptions.Timeout:
            st.error("The request timed out. API took too long to respond.")
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the API server. Make sure Uvicorn is running at http://127.0.0.1:8000.")
        except Exception as e:
            # Prevent silent crashing
            st.error(f"An unexpected error occurred: {str(e)}")




#Feature 2: Ask
#A text box where someone can type a question in plain English, and a button to send it.

#When clicked, it must call POST /agent/ask with the question, and:

#Show the answer text if the request completed successfully
#Show something sensible if it did not complete (the agent hit its iteration limit)
#Show the number of tool calls made and the token counts somewhere on screen
#Show a clear error message if the request fails, do not let it crash silently

with tab2: 
    Question = st.text_area("FEATURE 2 - ASK AGENT HERE ( it will need client_Id if using  predict portfolio returns tool) ")

    if st.button("Click me to ask agent something"):

        try:
            # Call POST /agent/ask with the question as a query parameter
            response = requests.post(f"{API_URL}/agent/ask", params={"question": Question}, timeout=60)
            if response.status_code !=200:
                st.write(f"ERROR HAS OCCURED ON API END - HERE IS STATUS CODE: {response.status_code}  ")
            data =  response.json()
            st.write(f"Connection successfull heres info: {data}")
        except requests.exceptions.Timeout:
            st.error("The request timed out. The agent took too long to respond.")
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the API server. Make sure Uvicorn is running at http://127.0.0.1:8000.")
        except Exception as e:
            # Prevent silent crashing
            st.error(f"An unexpected error occurred: {str(e)}")






#Feature 3: STREAM SUMMARY FUND FACT SHEET 
#A text box where someone can type a question in plain English, and a button to send it.

#When clicked, it must call POST /llm/stream_summary/{fund_id}, and:

#Show the answer text if the request completed successfully
#Show something sensible if it did not complete (the agent hit its iteration limit)
#Show the number of tool calls made and the token counts somewhere on screen
#Show a clear error message if the request fails, do not let it crash silently


#reverse engnieered from firm intel UI

with tab3: 
    fund_id = st.text_area("FEATURE 3 - STREAM LLM SUMMARY- WRITE FUND IDNUMBER TO SUMMMARISE FACTSHEET ")

    if st.button("Click me to stream an LLM summary of Fund Factsheets"):

        try:
            #Knowledge/search 
            response = requests.post(
                f"http://127.0.0.1:8000/llm/stream_summary/{fund_id}",
                stream=True
            )
            
            # Simplest way to loop through incoming text chunks:
            if response.status_code == 200:
                            # Generator function yields decoded text chunks to st.write_stream
                            def generate_chunks():
                                for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
                                    if chunk:
                                        yield chunk

                            # Streams text progressively in real time into a single paragraph
                            st.write_stream(generate_chunks)
            else:
                st.write(f"ERROR HAS OCCURED ON API END - HERE IS STATUS CODE:  {response.status_code}  ")
        except requests.exceptions.Timeout:
            st.error("The request timed out. API took too long to respond.")
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the API server. Make sure Uvicorn is running at http://127.0.0.1:8000.")
        except Exception as e:
            # Prevent silent crashing
            st.error(f"An unexpected error occurred: {str(e)}")



# EXTRA FEATURES - VIEW ALL CLIENT PORTFOLIOS 




#Endpoint 0 - Get all client portfolios to see. 

#@router.get("")
#def get_all_portfolios():
#    return ( document for document in DOCUMENTS if document["type"]== "client_portfolio")


#URL/portfolios

with tab4: 
    Query = st.text_area("EXTRA FEATURE - VIEW ALL CLIENT PORTFOLIOS )  ")
    Top_K = 3

    if st.button("Click me to search"):

        try:
            #Knowledge/search 
            payload = {"question": Query, "top_k": Top_K}
            response = requests.post(f"{API_URL}/knowledge/search", json=payload, timeout=60)
            if response.status_code !=200:
                st.write(f"ERROR HAS OCCURED ON API END - HERE IS STATUS CODE:  {response.status_code}  ")
            data =  response.json()
            st.write(f"Connection successfull heres the  info: {data}")
        except requests.exceptions.Timeout:
            st.error("The request timed out. API took too long to respond.")
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the API server. Make sure Uvicorn is running at http://127.0.0.1:8000.")
        except Exception as e:
            # Prevent silent crashing
            st.error(f"An unexpected error occurred: {str(e)}")

