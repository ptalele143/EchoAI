import streamlit as st
import openai
from brain import get_index_for_pdf
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
import os
import io
from taskExt_CTO_A_B_C import cto_C

def main_job_description(conversation):
    
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

    conversation_filename = f"{conversation_folder}/conversation_CTO3.txt"
    final_CTO3_list = os.path.join(final_list_folder, "CTOC_Summary_Update.txt")
    getCTO3list = []
            
    if os.path.exists(final_CTO3_list) and os.path.getsize(final_CTO3_list) > 0:
        pass
    else: 
        getCTO3list = cto_C(conversation_filename)
        with open(final_CTO3_list, "w") as final_file:
            final_file.write("".join(getCTO3list))
            

    # Caching of vectordb for creating to a vectordb for the given PDF file
    @st.cache_data
    def create_vectordb(files, filenames):
        
        with st.spinner("Vector database"):
            vectordb = get_index_for_pdf(
                [file.getvalue() for file in files], filenames, openai.api_key
            )
        return vectordb

    #pdf_files = st.file_uploader("", type="pdf", accept_multiple_files=True)

    #if pdf_files:
    #    pdf_file_names = [file.name for file in pdf_files]
    #    st.session_state["vectordb"] = create_vectordb(pdf_files, pdf_file_names)

    #PDF file uploaded by admin would be used

    pdf_file_path = r"pdf_files\BACKGROUND INFO Worker-1.pdf"
    

    pdf_file_names = ["BACKGROUND INFO Worker-1.pdf"]

    with open(pdf_file_path, 'rb') as file:
        pdf_content = file.read()

    # Wrapping of content in a BytesIO object
    pdf_content_io = io.BytesIO(pdf_content)

    # Use of the PDF content in vectordb creation
    st.session_state["vectordb"] = create_vectordb([pdf_content_io], pdf_file_names)


    prompt_template = """

    ### Ask the user to provide their job title and enter or upload a job description.
    ### Based on the user input and the content of the Background Data (which lists tasks associated with different types of financial analysts and provide templates), organize the job description in up to 5 key WORKFLOWS, each workflow being described shortly and associated with a core list of tasks provided by the user or/and listed in the background information.
    ### Ask the user to comment or edit the list and descriptions of workflows. The goal being to get a comprehensive picture of the workflows associated with the job.
    Let’s work this out in a step-by-step way to be sure we have the right answer
        
        Background Data :
        {pdf_extract}
    """

    prompt = st.session_state.pop("prompt", [{"role": "system", "content": "none"}])

    if not conversation:
        for message in prompt:
            if message["role"] != "system" and not (message["role"] == "user" and message["content"].lower() == "hi"):
                with st.chat_message(message["role"]):
                    st.write(message["content"])


    question = st.chat_input("Your AI assistant here for Job Description Analysis! Ask me anything ...")
    user_interacted = st.session_state.get(f"user_interacted", False)

    if  user_interacted:
        question = "hi"
        st.session_state["user_interacted"] = False

    if question:
        vectordb = st.session_state.get("vectordb", None)
        if not vectordb:
            with st.message("assistant"):
                st.write("You need to provide a PDF")
                st.stop()     

        search_results = vectordb.similarity_search(question, k=3)
        
        pdf_extract = "/n ".join([result.page_content for result in search_results])

        # Updatation the prompt with the pdf extract
        prompt[0] = {
            "role": "system",
            "content": prompt_template.format(pdf_extract=pdf_extract),
        }

        prompt.append({"role": "user", "content": question})

        if question =="hi" :
            pass
        else: 
            with st.chat_message("user"):
                st.write(question)

        with st.chat_message("assistant"):
            botmsg = st.empty()

        response = []
        result = ""
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

        conversation_filename = f"{conversation_folder}/JobDescription.txt"
        with open(conversation_filename, "a") as file:
            file.write(f"user: {question}\n")
            file.write(f"assistant: {result}\n")

if __name__ == "__main__":
    st.session_state["conversation"] = [] 
    main_job_description(st.session_state["conversation"])