import streamlit as st
import openai
from brain import get_index_for_pdf
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
import os
import io
from taskExtractor import text_to_tasks
import pandas as pd

def main_task_analyser(conversation):
    
    #use your openai key for setting up 

    #used in for sending to PDF extracts for RAG in chunks
    openai.api_key = open_file('key_openai.txt').strip()
    
    #used in env for backend extrraction bots    
    os.environ["OPENAI_API_KEY"] = open_file('key_openai.txt').strip()

    conversation_folder = "chat_logs"
    final_list_folder = "chat_logs/final_list"

    if not os.path.exists(conversation_folder):
        os.makedirs(conversation_folder)

    if not os.path.exists(final_list_folder):
        os.makedirs(final_list_folder)

    tasks_file = "chat_logs/JobDescription.txt"

    tasks = text_to_tasks(tasks_file)

    final_list_file = os.path.join(final_list_folder, "final_extracted_list.txt")

    with open(final_list_file, "w") as txt_file:
        for task in tasks:
            txt_file.write(f"{task}\n")

    print("tasks === ",tasks)

    #table_data = {"Order No": [], "Task": [], "Status": []}

    #for i, task_description in enumerate(tasks, start=1):
    #    status_key = f"status_{i}"

        # Add data to the table
    #    table_data["Order No"].append(i)
    #    table_data["Task"].append(task_description)
    #    table_data["Status"].append(st.checkbox("", key=status_key))

    # Display the table in the sidebar
    #st.table(table_data)



    # Cached function for creating to a vectordb for the given PDF file
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

    pdf_file_path = r"pdf_files\BACKGROUND INFO Worker-Bot2_comparison.pdf"

    pdf_file_names = ["BACKGROUND INFO Worker-Bot2_comparison.pdf"]

    with open(pdf_file_path, 'rb') as file:
        pdf_content = file.read()

    pdf_content_io = io.BytesIO(pdf_content)

    st.session_state["vectordb"] = create_vectordb([pdf_content_io], pdf_file_names)

    prompt_template = """
    Your goal is to assess how a workflow described by the user is impacted by AI technologies. Let's work this out step by step to make sure we get the right answer. It is very important for me.
    Steps:
    1) Analyze the workflow description entered by the user to map the tasks, abilities, skills, knowledge, and technology skills required to execute the workflow (see your background information in below PDF content for list of items). The output of this step is a LONG DESCRIPTION of the WORKFLOW (see template in your background info in below PDF content). At the end of the first step, you ask the user for feedback, incorporate it, and seek final validation of the updated description before moving to the next task.
    2) CURRENT STATE: Now use the description of critical AI technologies included in your background data (below PDF content) to understand how the workflow described in step 1 can be augmented or replaced by an AI system instead of a human. To perform this analysis, you consider the following layers in the architecture of the AI system that is designed to perform the task:
    a. A frontier LLM (like GPT4) can be used as a standalone tool to try to perform the task using system prompts specific to the task.
    b. A more sophisticated approach involves fine-tuning the model to learn how to better perform the task.
    c. To further improve the ability to execute the task, the LLM can be combined with software tools and advanced capabilities such as vision and voice (see list of examples in background data of below PDF content).
    d. To improve the ability to execute the task even further, the LLMs and tools can be combined in a Muti-Agent System (MAS), which automate a series of sub-tasks.
    e. Robotic capabilities (e.g. sensors, actuators) can be added when it is necessary to interact with the physical environment.
    f. Using text-to-speech and text-to-video the AI system can also be ‘embodied’ and become an avatar in a virtual environment where it interacts with humans (e.g. video conference).
    It is to be noted that the addition of layer b to f involves designing a system to perform the task since such a system is not available on-shelf today.
    Based on the 2023 state of technologies described in your background data (below PDF content), output a discussion how the workflow can (or cannot) be executed by an AI system, with different layers incorporated (use the template from your background info i.e. below PDF content).

    3)PERPSECTIVES. The third step focuses on a forecast of how the limitations identified in step 2 are likely to be addressed in the near future, based on current R&D activities described in your background data ((below PDF content)). To perform this analysis, you consider the following time frames:
    a. Progress expected in the next 6 to 12 months.
    b. Progress expected in the next 36 months.
    c. Progress expected in the next 5 years.
    d. You output a description of your PERPSECTIVES based the template provided in your background data(below PDF content). At the end of the third step, you ask the user for feedback, incorporate it, and seek final validation of the updated forward-looking statement before moving to the next task.
	

    The PDF content is:
    {pdf_extract}
    """

    prompt = st.session_state.pop("prompt", [{"role": "system", "content": "none"}])

    current_task_index = st.session_state.get("current_task_index", 0)

    if not conversation:
        for message in prompt:
            if message["role"] != "system":
                with st.chat_message(message["role"]):
                    st.write(message["content"])

    if current_task_index < len(tasks):
        current_task = tasks[current_task_index].strip()
        user_interacted = st.session_state.get(f"user_interacted_task_{current_task_index}", False)

    question = st.chat_input("Your AI assistant here for One to one question discussion for job analysis final list ! Ask me anything ...")

    if st.button("Next Task") and user_interacted:
        current_task_index += 1
        if current_task_index < len(tasks):
            current_task = tasks[current_task_index].strip()
            st.session_state["current_task_index"] = current_task_index
            st.session_state["prompt"] = []
        else:
            st.write("No more tasks available.")
            st.stop()

    if question or (current_task and current_task != ""):
        vectordb = st.session_state.get("vectordb", None)
        if not vectordb:
                st.write("You need to provide a PDF")
                st.stop()

        if not question:
            question = current_task
            st.session_state[f"user_interacted_task_{current_task_index}"] = True

        search_results = vectordb.similarity_search(question, k=3)
        
        pdf_extract = "/n ".join([result.page_content for result in search_results])

        # Updating the prompt with the pdf extraction of content
        prompt[0] = {
            "role": "system",
            "content": prompt_template.format(pdf_extract=pdf_extract),
        }


        prompt.append({"role": "user", "content": question})
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
        conversation_filename = f"{conversation_folder}/comparison.txt"
        with open(conversation_filename, "a") as file:
            file.write(f"user: {question}\n")
            file.write(f"assistant: {result}\n")
        #download the conversation if required
        #st.download_button(label="Download the Conversation",data=open(conversation_filename, 'rb').read(),file_name=conversation_filename,key='download_button')
        #st.stop()

if __name__ == "__main__":
    st.session_state["conversation"] = [] 
    main_task_analyser(st.session_state["conversation"])