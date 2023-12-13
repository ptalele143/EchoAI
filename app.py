import streamlit as st
from streamlit_option_menu import option_menu
from TaskAnalyser import main_task_analyser
from JobDescription import main_job_description
from AdminConsole import get_admin_console
from CTO_1 import main_job_description_CTO1
from CTO_2 import main_job_description_CTO2
from CTO_3 import main_job_description_CTO3
import textwrap

def main():

    st.set_page_config(page_title="AI Transition", layout="wide")

    st.markdown("""
        <style>
            .title-style {
                font-size: 40px;
                font-weight: bold;
                text-align: left;
                color: red; 
            }
            .menu-style {
                display: flex;
                justify-content: center;
                gap: 10px;
            }
        </style>
        """, unsafe_allow_html=True)

    st.markdown('<p class="title-style">CRISIL&rsquo;s Engage and Echo (CEE)</p>', unsafe_allow_html=True)

    selected_page = option_menu(None, 
    ["Home","AI LLMs" ,"AI Enhancements","AI Future","Job Assessor", "Abilities Comparison", 
    'Impact Analysis',"Suggestion", "Report","Admin Console"], 
    icons=[], 
    menu_icon=["cast"], default_index=0, orientation="horizontal")

    if st.session_state.get("selected_page", None) is None or selected_page != st.session_state["selected_page"]:
        st.session_state["selected_page"] = selected_page

    #initializing the session state
    if "conversation" not in st.session_state:
        st.session_state["conversation"] = []  

    st.write("\n\n")

    # Displaying selected page content based on the user selection page
    if selected_page == "Home":
        st.sidebar.markdown("## Homepage")
        homepagetext = """

        Welcome to CRISIL's Engage and Echo (CEE) Platform - AI-Driven Job Analysis Portal

        At CEE, we specialize in harnessing the power of Artificial Intelligence to transform the workplace. Our state-of-the-art AI-driven system is designed to analyze, assess, and optimize job functions, aligning them with the capabilities of AI for enhanced efficiency and innovation.

        Innovative Assessment Process

        Our three-phase process begins with a comprehensive validation of AI capabilities by our Chief Technology Officer and seasoned research team. We delve into the intricacies of existing and emerging AI technologies to prepare your organization for the future.

        Interactive User Engagement

        Through our interactive platform, users engage with our intelligent bots to dissect their daily tasks. Our system is not just a passive analyzer; it's an engaging conversational agent designed to understand and evaluate the core aspects of each role within your company.

        Data-Driven Insights

        The heart of our platform lies in its analytical prowess. By collating and summarizing user interactions, our Analyzer Bot provides a deep dive into the number of tasks impacted by AI, the ranking of these tasks, and their categorization across roles and divisions.

        Strategic Implementation

        The Summarizer Bot then takes the reins, using advanced AI to draft comprehensive reports that guide management and HR in making informed decisions for talent strategy and AI adoption.

        Seamless Integration

        Our portal is your gateway to a seamless integration of AI into your daily operations. It is designed to be intuitive, user-friendly, and a constant source of strategic insights for your organization.

        Join us in redefining the future of work, where AI and human expertise converge to create a more efficient, innovative, and fulfilling workplace."""
        dedented_text = textwrap.dedent(homepagetext).strip()
        
        col1, col2 = st.columns([2, 1])

        col1.markdown("## Overview")
        st.sidebar.markdown("""Welcome to CRISILs Engage and Echo (CEE) Platform - AI-Driven Job Analysis Portal
        At CEE, we specialize in harnessing the power of Artificial Intelligence to transform the workplace. Our state-of-the-art AI-driven system is designed to analyze, assess, and optimize job functions, aligning them with the capabilities of AI for enhanced efficiency and innovation.
        """)
        col1.markdown(f"<div style='white-space: pre:; font-family: Arial;'>{dedented_text}</div>", unsafe_allow_html=True)

        # Adding an image to the right column
        col2.image("abc.png", use_column_width=True)
    

    elif selected_page == "AI LLMs":
            
        st.sidebar.markdown("## AI LLMs")
        st.sidebar.markdown("### Abilities of Frontier Large Language Models:")
        st.sidebar.markdown("The framework we use for assessing the abilities of AI systems assumes that frontier Large Language Models (LLM) such as GPT4 or Claude constitute the fundamental building block. We therefore start by assessing the abilities of such models as a standalone tool provided via a chatbot such as ChatGPT")
        
        main_job_description_CTO1(st.session_state["conversation"])

    elif selected_page == "AI Enhancements":
        
        st.sidebar.markdown("## AI Enhancements")
        st.sidebar.markdown("### Enhancement of LLMs Capabilities Today:")
        st.sidebar.markdown("The bot focuses on how the use of tools/agents, fine-tuning, multi-agent systems, robotic and VR extensions can enhance the abilities of frontier LLMs today.")
        main_job_description_CTO2(st.session_state["conversation"])
        
    
    elif selected_page == "AI Future":
        
        st.sidebar.markdown("## AI Future")
        st.sidebar.markdown("Outlook for LLM-based Systems:")
        st.sidebar.markdown("Experts and forecasters expect tremendous progress in the next few years. Many estimate that Artificial General Intelligence (human level across abilities) will be reached between 2 and 10 years. In the third step, the bot provides insights from research to help you build your own vision of the future for your activity")  
        main_job_description_CTO3(st.session_state["conversation"])

    elif selected_page == "Job Assessor":

        st.sidebar.markdown("## Job Description Analysis Tool")
        st.sidebar.markdown("### Step 1: Identify the Critical Tasks in your Job")
        st.sidebar.markdown("The chatbot below assists you in listing and describing the critical tasks associated with your job, using a standard taxonomy of occupational tasks (O*Net). Start chatting: the bot will suggest tasks and descriptions and ask you a series of questions to fine-tune the list.")
        main_job_description(st.session_state["conversation"])  

    elif selected_page == "Abilities Comparison":
        st.sidebar.markdown("## Abilities Comparision Analysis Tool")
        st.sidebar.markdown("### Step 2: Identify the Critical Tasks in your Job")
        st.sidebar.markdown("The chatbot below assists you in listing and describing the critical tasks associated with your job, using a standard taxonomy of occupational tasks (O*Net). Start chatting: the bot will suggest tasks and descriptions and ask you a series of questions to fine-tune the list.") 
        main_task_analyser(st.session_state["conversation"])   

    elif selected_page == "Impact Analysis":
        st.sidebar.markdown("## Abilities Comparision Analysis Tool")
        st.sidebar.markdown("### Step 2: Identify the Critical Tasks in your Job")
        st.sidebar.markdown("The chatbot below assists you in listing and describing the critical tasks associated with your job, using a standard taxonomy of occupational tasks (O*Net). Start chatting: the bot will suggest tasks and descriptions and ask you a series of questions to fine-tune the list.")
        #main_job_description(st.session_state["conversation"])
    
    elif selected_page == "Suggestion":
        st.sidebar.markdown("## Abilities Comparision Analysis Tool")
        st.sidebar.markdown("### Step 2: Identify the Critical Tasks in your Job")
        st.sidebar.markdown("The chatbot below assists you in listing and describing the critical tasks associated with your job, using a standard taxonomy of occupational tasks (O*Net). Start chatting: the bot will suggest tasks and descriptions and ask you a series of questions to fine-tune the list.")
        #main_job_description(st.session_state["conversation"])
    
    elif selected_page == "Report":
        st.sidebar.markdown("## Abilities Comparision Analysis Tool")
        st.sidebar.markdown("### Step 2: Identify the Critical Tasks in your Job")
        st.sidebar.markdown("The chatbot below assists you in listing and describing the critical tasks associated with your job, using a standard taxonomy of occupational tasks (O*Net). Start chatting: the bot will suggest tasks and descriptions and ask you a series of questions to fine-tune the list.")
        #main_job_description(st.session_state["conversation"])

    elif selected_page == "Admin Console":
        get_admin_console(st.session_state["conversation"])

if __name__ == "__main__":
    main()
