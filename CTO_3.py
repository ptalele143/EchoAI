import streamlit as st
import openai
from brain import get_index_for_pdf
from taskExtractor import cto1_extract
from taskExtractor import cto2_extract
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
import os
import io
import time
from taskExt_CTO_A_B_C import cto_A
from taskExt_CTO_A_B_C import cto_B
from taskExt_CTO_A_B_C import cto_C
from taskExt_CTO_A_B_C import open_file

def main_job_description_CTO3(conversation):
    
    #use your openai key for setting up 

    #used in for sending to PDF extracts for RAG in chunks
    openai.api_key = open_file('key_openai.txt').strip()

    #used in env for backend extrraction bots
    os.environ["OPENAI_API_KEY"] = open_file('key_openai.txt').strip()
    
    conversation_folder = "chat_logs"
    final_list_folder = "chat_logs/final_list"

    # Create a folder to store conversations if it doesn't exist
    if not os.path.exists(conversation_folder):
        os.makedirs(conversation_folder)

    # Caching of vectordb for creating to a vectordb for the given PDF file
    @st.cache_data
    def create_vectordb(files, filenames):
        
        with st.spinner("Vector database"):
            vectordb = get_index_for_pdf(
                [file.getvalue() for file in files], filenames, openai.api_key
            )
        return vectordb

    #PDF file uploaded by admin would be used
    pdf_file_path = r"pdf_files\BACKGROUND INFO CTO-3.pdf"

    pdf_file_names = ["BACKGROUND INFO CTO-3.pdf"]

    with open(pdf_file_path, 'rb') as file:
        pdf_content = file.read()

    # Wrapping of content in a BytesIO object
    pdf_content_io = io.BytesIO(pdf_content)

    # Use of the PDF content in vectordb creation
    st.session_state["vectordb"] = create_vectordb([pdf_content_io], pdf_file_names)
    
    prompt_template = """

    Goal: Your goal is to help the user form their own view about the outlook of the abilities of AI systems based on LLMs in their line of business in the next 6 month, 2 years and 5 years. The user work in the field of financial analysis. 
    Let’s work this out step by step to make sure we get the right approach. 
    ## Step1: Output the OUTLOOK included in your background data in full length. DO NOT CHANGE THE TEXT. It is important to me, please. Then Invite the user to ask questions or suggest modifications.
    ## Step 2: Answer the user’s question based on your background data. ALWAYS invite them to ask more questions or comments OR suggest modifications. 
    ##Rule: In your responses, always consider the abilities of LLMs used with chatbots, and how these abilities can be enhanced with fine-tuning, tools/agents, multi-agent systems, as well as robotic and VR extensions. Assume that these additional layers will become common practice.

    Background Data:   
        
        {pdf_extract}

    """
    #prompt_template = """
    #    Greet Prathamesh in 10 words
    #
    #    
    #"""
    
    prompt = st.session_state.pop("prompt", [{"role": "system", "content": "none"}])
    
    if not conversation:
        for message in prompt:
            if message["role"] != "system" and not (message["role"] == "user" and message["content"].lower() == "OUTLOOK"):
                with st.chat_message(message["role"]):
                    st.write(message["content"])


    question = st.chat_input("Your AI assistant here for AI Enhancement! Ask me anything ...")
    user_interacted = st.session_state.get(f"user_interacted", False)

    conversation_filename = f"{conversation_folder}/conversation_CTO2.txt"
    final_CTO1_list = os.path.join(final_list_folder, "CTOA_Summary_Update.txt")
    final_CTO2_list = os.path.join(final_list_folder, "CTOB_Summary_Update.txt")
    ct01_content = ""
    ct02_content = ""
    if not user_interacted:
        getCTO2list = cto_B(conversation_filename)
        with open(final_CTO2_list, "w") as final_file:
            final_file.write("".join(getCTO2list))
        question = "OUTLOOK" 

        with open(final_CTO2_list, "r") as file:
                ct02_content = file.read()  
        st.session_state["user_interacted"] = True

    result = ""
    if question:
        vectordb = st.session_state.get("vectordb", None)
        if not vectordb:
            with st.message("assistant"):
                st.write("You need to provide a PDF")
                st.stop()     

        search_results = vectordb.similarity_search(question, k=3)
        
        pdf_extract = "/n ".join([result.page_content for result in search_results])

        # Update the prompt with the pdf extracted data 
        prompt[0] = {
            "role": "system",
            "content": prompt_template.format(pdf_extract=pdf_extract)
        }

        prompt.append({"role": "user", "content": question})

        if question =="OUTLOOK" :
            pass
        else: 
            with st.chat_message("user"):
                st.write(question)

        with st.chat_message("assistant"):
            botmsg = st.empty()

        response = []
        
        for chunk in openai.ChatCompletion.create(
            model="gpt-4-1106-preview", messages=prompt, stream=True
        ):
            text = chunk.choices[0].get("delta", {}).get("content")
            if text is not None:
                response.append(text)
                result = "".join(response).strip()
                botmsg.write(result)

        prompt.append({"role": "assistant", "content": result})

        st.session_state["prompt"] = prompt

    conversation_filename = f"{conversation_folder}/conversation_CTO3.txt"
    with open(conversation_filename, "a") as file:
        file.write(f"user: {question}\n")
        file.write(f"assistant: {result}\n")

if __name__ == "__main__":
    st.session_state["conversation"] = [] 
    main_job_description_CTO3(st.session_state["conversation"])