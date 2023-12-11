from langchain.chat_models import ChatOpenAI
from langchain.schema.document import Document
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.prompts import PromptTemplate
from langchain.chains.llm import LLMChain
import ast
import os


def text_to_tasks(input_txt):
    with open(input_txt, 'r') as txt_file:
        data = txt_file.read().splitlines()
    doc = [Document(page_content=t, metadata={"source": input_txt}) for t in data]

    prompt_template = """Derive a final list of workflows along with description that the user does as part of thier job using following conversation between user and assistant:
    "{text}"

    Output ONLY the final list of workflows with description only, No tasks to be included in the form of python list and NOTHING ELSE like below:

    [workflow 1 with description, workflow 2 with description, workflow 3 with description, workflow 4 with description,workflow 5 with description]

    """
    prompt = PromptTemplate.from_template(prompt_template)

    # Define LLM chain
    llm = ChatOpenAI(temperature=0, model_name="gpt-4-1106-preview")
    llm_chain = LLMChain(llm=llm, prompt=prompt)

    # Define StuffDocumentsChain
    stuff_chain = StuffDocumentsChain(llm_chain=llm_chain, document_variable_name="text")
    tasks = stuff_chain.run(doc)
    return ast.literal_eval(tasks)
    

def cto1_extract(input_txt):
    with open(input_txt, 'r') as txt_file:
        data = txt_file.read().splitlines()
    doc = [Document(page_content=t, metadata={"source": input_txt}) for t in data]

    prompt_template = """Below is conversation between user and assistant on capabilities and limitations of frontier LLMs for use in financial analysis via chatbot interfaces, comparing them to human abilities.
    Derive a final detailed overview given by the assistant after confirming with user.
    "{text}"

    Output only the final response by the assistant as it is Final Overview (1,000 Words):and nothing else.

    """
    prompt = PromptTemplate.from_template(prompt_template)

    # Define LLM chain
    llm = ChatOpenAI(temperature=0, model_name="gpt-4-1106-preview")
    llm_chain = LLMChain(llm=llm, prompt=prompt)

    # Define StuffDocumentsChain
    stuff_chain = StuffDocumentsChain(llm_chain=llm_chain, document_variable_name="text")
    cto1_op = stuff_chain.run(doc)
    return cto1_op


def cto2_extract(input_txt):
    with open(input_txt, 'r') as txt_file:
        data = txt_file.read().splitlines()
    doc = [Document(page_content=t, metadata={"source": input_txt}) for t in data]

    prompt_template = """Below is conversation between user and assistant on LLM enhancements in financial analysis through multilayer approaches to help the user understand how the use of tools/agents, fine-tuning, multi-agent systems, robotic and VR extensions can enhance the abilities of frontier LLMs today.
    The purpose of this conversation is to generate 1,000-word description, including the dimensions explored in the discussion with the user
    Derive a final conclusive response given by the assistant after confirming/agreeing with user and integrating users's feedback.

    "{text}"

    Output only the final response by the assistant as it is and nothing else.

    """
    prompt = PromptTemplate.from_template(prompt_template)

    # Define LLM chain
    llm = ChatOpenAI(temperature=0, model_name="gpt-4-1106-preview")
    llm_chain = LLMChain(llm=llm, prompt=prompt)

    # Define StuffDocumentsChain
    stuff_chain = StuffDocumentsChain(llm_chain=llm_chain, document_variable_name="text")
    cto2_op = stuff_chain.run(doc)
    return cto2_op


def cto3_extract(input_txt):
    with open(input_txt, 'r') as txt_file:
        data = txt_file.read().splitlines()
    doc = [Document(page_content=t, metadata={"source": input_txt}) for t in data]

    prompt_template = """Below is conversation between user and assistant on how the use of tools/agents, fine-tuning, multi-agent systems, robotic and VR extensions can enhance the abilities of frontier LLMs today.
    The purpose of this conversation is to generate 1,000-word outlook of the expected improvement of these systems in the next 6 months, 2 years and 5 years including the dimensions explored in the discussion with the user.
    Derive a final conclusive response given by the assistant after validating with user.

    "{text}"

    Output only the final response by the assistant as it is and nothing else.

    """
    prompt = PromptTemplate.from_template(prompt_template)

    # Define LLM chain
    llm = ChatOpenAI(temperature=0, model_name="gpt-4-1106-preview")
    llm_chain = LLMChain(llm=llm, prompt=prompt)

    # Define StuffDocumentsChain
    stuff_chain = StuffDocumentsChain(llm_chain=llm_chain, document_variable_name="text")
    cto3_op = stuff_chain.run(doc)
    return cto3_op