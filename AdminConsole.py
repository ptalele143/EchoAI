import streamlit as st
import os
import yaml

#function to display the admin console
def get_admin_console(conversation):
    
    col1, col2 = st.columns(2)
    with col1:
        botName = st.text_input("Name of Chatbot")
    with col2:
        openai_key = st.text_input("OpenAI Key")

    # displaying sliders for Temperature Control, Maximum Tokens, and Number of Chunks
    col1, col2, col3 = st.columns(3)
    with col1:
        temperature = st.slider("Temperature Control", 0.0, 1.0, 0.7, step=0.01)
    with col2:
        max_tokens = st.slider("Maximum Tokens", 1, 5000, 250, step=1)
    with col3:
        num_chunks = st.slider("Number of Chunks", 1, 10, 5, step=1)

    #Model Selection based on LLM selection
    model = st.selectbox("Model Selection", ["GPT-4", "GPT-3.5"])

    #input for system prompt
    system_prompt = st.text_area("System Prompt")

    #backgorund knowledge Upload document option , mostly support for PDF
    uploaded_file = st.file_uploader("Upload Document", type=["txt", "pdf", "docx"])

    # Submit button for bot creation
    if st.button("Create Bot"):

        # Saving PDF file
        if uploaded_file and uploaded_file.type == "application/pdf":
            pdf_path = os.path.join("pdf_files", uploaded_file.name)
            with open(pdf_path, "wb") as pdf_file:
                pdf_file.write(uploaded_file.read())
            
            #data in YAML format for admin to create bot
            data = {
                "Name of Chatbot": botName,
                "OpenAI Key": openai_key,
                "Temperature Control": temperature,
                "Maximum Tokens": max_tokens,
                "Number of Chunks": num_chunks,
                "Model Selection": model,
                "System Prompt": system_prompt,
                "PDF Filename" : uploaded_file.name
            }

            # Saving in YAML file
            with open(os.path.join("bot_files", "bot_data.yaml"), "w") as yaml_file:
                yaml.dump(data, yaml_file, default_flow_style=False)


        st.write("Bot Created!")

if __name__ == "__main__":
    st.session_state["conversation"] = [] 
    get_admin_console(st.session_state["conversation"])
