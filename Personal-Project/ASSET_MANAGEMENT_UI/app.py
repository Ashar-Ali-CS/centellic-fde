


import streamlit as st
import requests

import uuid   #This is unique identifier to stop duplicate form submissisions 


st.set_page_config(page_title="ASSET MANAGE WEBAPP ", page_icon=":)", layout="centered")

st.title("ASSET MANAGEMENT WEBAPP ")



#This makes it horzizontally allignee
tab1, tab2,tab3,tab4,tab5= st.tabs([ "MANAGER PORTAL", "0 - GROUNDED ASK ","1 - SEARCH DOCS", "2 - ASK AGENT" , "3 -  FUNDS SUMMARY "] )

API_URL  = "http://127.0.0.1:8000"


#A separate text box and button for retrieval without generation.
#When clicked, it must call POST /knowledge/search, and:
#List every result returned, with its title and its score
#Handle the case where the index has not been built yet, this returns a specific status code, not a generic failure
#Handle a normal failure differently from the “index not built” case

with tab3: 
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




#Feature 2: Ask Agent 
#A text box where someone can type a question in plain English, and a button to send it.

#When clicked, it must call POST /agent/ask with the question, and:

#Show the answer text if the request completed successfully
#Show something sensible if it did not complete (the agent hit its iteration limit)
#Show the number of tool calls made and the token counts somewhere on screen
#Show a clear error message if the request fails, do not let it crash silently

with tab4: 
    Question = st.text_area("FEATURE 2 - ASK AGENT HERE (it will need client_id if using predict portfolio returns tool)")

    if st.button("Click me to ask agent something"):
        try:
            # Notice stream=True is removed because we want standard JSON back
            response = requests.post(f"{API_URL}/agent/ask", params={"question": Question}, timeout=60)
            
            if response.status_code == 200:
                data = response.json()
                
                st.markdown("### Agent Response")
                st.write(data.get("answer", "No answer provided."))
                
                if not data.get("completed", True):
                    st.warning("Note: The agent reached its iteration limit before fully completing.")
                
                st.divider()
                col1, col2, col3 = st.columns(3)
                col1.metric("Tool Calls", data.get("tool_calls_made", 0))
                col2.metric("Input Tokens", data.get("input_tokens", 0))
                col3.metric("Output Tokens", data.get("output_tokens", 0))
                
            else:
                st.error(f"ERROR OCCURRED ON API END - STATUS CODE: {response.status_code}")
                st.write(response.text)
                
        except requests.exceptions.Timeout:
            st.error("The request timed out. API took too long to respond.")
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the API server. Make sure Uvicorn is running at http://127.0.0.1:8000.")
        except Exception as e:
            st.error(f"An unexpected error occurred: {str(e)}")
     #       data =  response.json()
     #       st.write(f"Connection successfull heres info: {data}")
     #   except requests.exceptions.Timeout:
     #       st.error("The request timed out. The agent took too long to respond.")
     #   except requests.exceptions.ConnectionError:
     #       st.error("Could not connect to the API server. Make sure Uvicorn is running at http://127.0.0.1:8000.")
     #   except Exception as e:
     #       # Prevent silent crashing
     #       st.error(f"An unexpected error occurred: {str(e)}")


       


#Feature 3: STREAM SUMMARY FUND FACT SHEET 
#A text box where someone can type a question in plain English, and a button to send it.

#When clicked, it must call POST /llm/stream_summary/{fund_id}, and:

#Show the answer text if the request completed successfully
#Show something sensible if it did not complete (the agent hit its iteration limit)
#Show the number of tool calls made and the token counts somewhere on screen
#Show a clear error message if the request fails, do not let it crash silently


#reverse engnieered from firm intel UI

with tab5: 
    fund_id = st.text_area("FEATURE 3 - STREAM LLM SUMMARY- Write fund id number to summarise fund factsheet ")

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


with tab1: 
    st.subheader("Portfolio Manager Portal- View All,compare and add client portfolios ")

    if st.button("SEE YOUR CLIENT PORTFOLIOS"):
        try:
            # GET requests don't need a json payload for this
            response = requests.get(f"{API_URL}/portfolios/", timeout=60)
            
            if response.status_code != 200:
                st.error(f"ERROR HAS OCCURRED ON API END - STATUS CODE: {response.status_code} - {response.text}")
            else:
                data = response.json()
                st.success("Successfully fetched portfolios!")
                ## Display the data nicely as a JSON tree or dataframe
                #st.json(data)
                # Loop through and display each portfolio inside a clean card container
                for i, portfolio_text in enumerate(data):
                    with st.container(border=True):
                    
                        st.markdown(f"### 💼 Portfolio Record #{i + 1}")
                        st.write(portfolio_text)

        except requests.exceptions.Timeout:
            st.error("The request timed out. API took too long to respond.")
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the API server. Make sure Uvicorn is running at http://127.0.0.1:8000.")
        except Exception as e:
            st.error(f"An unexpected error occurred: {str(e)}")








    st.markdown("#####  Add New Client Portfolio")
    
    with st.form("create_portfolio_form", clear_on_submit=True):
        title = st.text_input("Portfolio Title", placeholder="e.g., Client Portfolio: Jane Turncoat")
        
        st.caption("USE THIS FORMAT COPY AND PASTE FOR RECORD CONSISTENCY : Client_Name: ... / Portfolio_Allocation: ... / Total_Assets: ... / Client_Mandate: ...")
        body = st.text_area(
            "Portfolio Details", 
            placeholder="Client_Name: Jane Doe / Portfolio_Allocation: 50% FastSaver / Total_Assets: £200,000 / Client_Mandate: Growth",
            height=100
        )

        submitted = st.form_submit_button("Submit New Portfolio")

        if submitted:
            if not title.strip() or not body.strip():
                st.warning("Please fill in both fields.")
            else:
                try:
                    payload = {"title": title.strip(), "body": body.strip()}
                    headers = {"idempotency-key": str(uuid.uuid4())}
                    
                    res = requests.post(f"{API_URL}/portfolios/add", json=payload, headers=headers, timeout=30)
                    
                    if res.status_code in (200, 201):
                        st.success("Portfolio added successfully!")
                        st.rerun()
                    else:
                        st.error(f"Error: {res.text}")
                except Exception as e:
                    st.error(f"An unexpected error occurred: {str(e)}")



    #NOT NEEDED DUE TO REGULATORY/COMPLIANCE - A PORTFOLIO MANAGER CANNOT JUST DELETE PORTFOLIOS 

    # delete client portfolio by client id 
        
   # st.markdown("###  Delete client portfolio by id ")
   # # 1. Input field for the manager to specify the ID
   # client_id_to_delete = st.number_input("Enter Client ID to Delete", min_value=1, step=1, value=1)
    
   # if st.button("Delete Portfolio"):
   #     try:
   #         # 2. Use requests.delete instead of post, hitting your exact backend route
   #         response = requests.delete(f"{API_URL}/portfolios/{client_id_to_delete}", timeout=60)
   #         
   #         # 3. Handle the 204 No Content success status (no json body is returned)
   #         if response.status_code == 204:
   #             st.success(f"Successfully deleted Client ID {client_id_to_delete}!")
   #             st.rerun()  # Refresh the UI to reflect the deletion
   #         elif response.status_code == 404:
   #             st.error(f"Client ID {client_id_to_delete} was not found.")
   #         else:
   #             st.error(f"ERROR HAS OCCURRED ON API END - STATUS CODE: {response.status_code}")
   #             
   #     except Exception as e:
   #         st.error(f"An unexpected error occurred: {str(e)}")




with tab2: 

    user_query = st.text_area("FEATURE 0 -Stream a Grounded Answer")

    if st.button("Click me to ask LLM question"):
        if user_query:
            payload = {"question": user_query, "top_k": 3}
            
            response = requests.post(
                f"{API_URL}/knowledge/ask", 
                json=payload, 
                stream=True
            )
            
            if response.status_code == 200:
                # Check if response is streaming text or JSON refusal
                content_type = response.headers.get("content-type", "")
                if "application/json" in content_type:
                    data = response.json()
                    if data.get("refused"):
                        st.warning(f"Refused: {data.get('reason')}")
                else:
                    st.write_stream(response.iter_content(chunk_size=1024, decode_unicode=True))
            elif response.status_code == 429:
                st.error("Rate limit reached. Please wait a few seconds and try again.")
            else:
                st.error(f"Error {response.status_code}: {response.text}")



