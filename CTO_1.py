import streamlit as st
import openai
from brain import get_index_for_pdf
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
import os
import io
from taskExt_CTO_A_B_C import cto_A
from taskExt_CTO_A_B_C import cto_B
from taskExt_CTO_A_B_C import cto_C
from taskExt_CTO_A_B_C import open_file

def main_job_description_CTO1(conversation):
    
    #use your openai key for setting up 

    #used in for sending to PDF extracts for RAG in chunks
    openai.api_key = open_file('key_openai.txt').strip()
    
    #used in env for backend extrraction bots    
    os.environ["OPENAI_API_KEY"] = open_file('key_openai.txt').strip()

    conversation_folder = "chat_logs"

    
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
    pdf_file_path = r"pdf_files/BACKGROUND INFO CTO-1.pdf"

    pdf_file_names = ["BACKGROUND INFO CTO-1.pdf"]

    with open(pdf_file_path, 'rb') as file:
        pdf_content = file.read()

    # Wrapping of content in a BytesIO object
    pdf_content_io = io.BytesIO(pdf_content)

    # Use of the PDF content in vectordb creation
    st.session_state["vectordb"] = create_vectordb([pdf_content_io], pdf_file_names)

    prompt_template = """
 
    Goal: Your goal is to help the user form their own view about what can and cannot be done by chatbots powered by LLMs (excluding tools, fine-tuning, etc), in their line of business. The user work in the field of financial analysis.
    Let’s work this out step by step to make sure we get the right approach.
    Step1: Output the following summary of the current abilities and limitations of chatbots powered by frontier LLMs. DO NOT CHANGE THE TEXT. Then Invite the user to ask questions or suggest modifications.
    SUMMARY:
    “SCOPE
    This summary focuses on the current abilities and limitations of frontier LLM models used in chatbots (excluding additional tools and systems), in the context of financial analysis related activities.
    INTRODUCTION
    Large language models (LLMs) like GPT-4 and Claude 2.1 represent revolutionary AI systems, trained on vast data, power chatbots to converse via text with humans. Frontier LLMs like GPT-4 and Claude 2.1 demonstrate advanced reasoning and language capabilities, but still have limitations compared to human cognition and abilities.
    RESULTS AT EXAMS
    In specialized exams, frontier LLMs reveal remarkable language understanding and reasoning that meets and sometimes exceeds human performance. GPT4 scored 90% on the Uniform Bar Exam, while Claude ranked in the 93rd percentile on the Graduate Record Examination test (Analytical Writing, Verbal Reasoning, Quantitative Reasoning). However, GPT$ failed the CFA exam so far: it showed potential in certain areas but struggled with complex finance topics, especially in the Level II exam. Its performance was close to the estimated passing threshold under certain conditions but was not consistently above the passing mark.
    FUNDAMENTAL LIMITATIONS
    However, frontier LLMs used via chatbots demonstrate clear constraints versus humans:
    •   No Real-Time Data: They cannot process or analyze live data, limiting usefulness in fast-changing finance settings.
    •   No Quantitative Analysis: They lack the mathematical capabilities for statistical analysis expected in finance.
    •   Context Size Constraints: even with ‘large’ context widows (128k tokens for GPT$, 200k tokens for Claude 2.1), performance drops when context exceeds 70k tokens (about 100 pages or 50k words), risking losing crucial details.
    •   Factual Inaccuracies: Reality gaps mean they generate plausible but incorrect information much more frequently than humans.
    •   Difficulty to follow complex multi-steps directions compared to humans.
    •   Overconfidence: They attempt to answer questions beyond their competencies, rather than admitting ignorance.
    •   Reading limitations: Interpreting complex tables and charts continues to challenge them.
    •   While chatbots can produce text, they cannot execute actions (e.g. trading, etc.) without additional tools.
    ABILITIES IN PRACTICE
    For finance-related use cases, they show strengths in:
    •   Reading text (from reports, news, research etc) almost immediately, in multiple languages, and a low cost ($0.1 to $1 per 150 pages).
    •   Analysis: Assessing sentiment, pros & cos, applying scoring systems, extracting information, calculating basic ratios, comparing, summarizing key takeaways, etc.
    •   Generating text: Processing volumes of text in multiple languages quickly and with no spelling mistakes, at low cost ($0.2 to $3 per 150 pages).
    CONCLUSION
    These abilities can be mobilized to augment (speed, scope) or replace tasks in several workflows related to financial analysis, such as consuming research to spotlight connections or drafting summaries, analyzing large volume of documents to identify relevant insights, generating first draft of reports, supporting research, etc.”
    Step 2: Answer the user’s question based on your background data (context provided in PDF content). ALWAYS invite them to ask more questions or comments OR suggest modifications.
         
    The PDF content is:
        {pdf_extract}
    """
    #prompt_template = """
    #    Greet Financial analyst in 5 weords  
    #"""

    prompt = st.session_state.pop("prompt", [{"role": "system", "content": "none"}])

    if not conversation:
        for message in prompt:
            if message["role"] != "system" and not (message["role"] == "user" and message["content"].lower() == "perform your work"):
                    with st.chat_message(message["role"]):
                        st.write(message["content"])


    question = st.chat_input("Your AI assistant here for AI LLM! Ask me anything ...")
    user_interacted = st.session_state.get(f"user_interacted", False)

    if not user_interacted:
        question = "perform your work"
        st.session_state["user_interacted"] = True

    if question:
        vectordb = st.session_state.get("vectordb", None)
        if not vectordb:
            with st.message("assistant"):
                st.write("You need to provide a PDF")
                st.stop()     

        search_results = vectordb.similarity_search(question, k=3)
        
        pdf_extract = "/n ".join([result.page_content for result in search_results])

        # Updating the the prompt with the pdf extract content with similarity search
        prompt[0] = {
            "role": "system",
            "content": prompt_template.format(pdf_extract=pdf_extract),
        }

        prompt.append({"role": "user", "content": question})

        if question =="perform your work" :
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

        conversation_filename = f"{conversation_folder}/conversation_CTO1.txt"
        with open(conversation_filename, "a") as file:
            file.write(f"user: {question}\n")
            file.write(f"assistant: {result}\n")

if __name__ == "__main__":
    st.session_state["conversation"] = [] 
    main_job_description_CTO1(st.session_state["conversation"])
