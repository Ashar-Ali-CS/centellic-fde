

## ASSET_MANAGMENT_UI

# HOW TO RUN THE FRONT END 

This is how to run the streamlit front end 

git clone it 

IMPORTANT -    In seperate git bash remember to have the ASSET_MANGEMENT_API server running 
 $ uvicorn main:app --reload



1. CD to ASSET_MANAGEMENT_UI folder  in git bash


2. Create virtual enviroment in git bash 

 $ python -m venv venv


3. Activate virtual enviroment in git bash 

 $ source venv/Scripts/activate

 or 
 
 $ venv/Scripts/activate

4. Install requirements.text  in git bash 

 $ pip install -r requirements.txt



5. Run streamlit app with

$ streamlit run app.py        