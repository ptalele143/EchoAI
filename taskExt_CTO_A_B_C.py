from langchain.chat_models import ChatOpenAI
from langchain.schema.document import Document
from langchain.document_loaders import PyPDFLoader, TextLoader
from langchain.document_loaders.merge import MergedDataLoader
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.prompts import PromptTemplate
from langchain.chains.llm import LLMChain
import openai
import os


def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as infile:
        return infile.read()

def cto_A(input_txt):
    # input_text should be chat conversation with CTO-1
    loader_text = TextLoader(input_txt) 
    loader_pdf = PyPDFLoader("pdf_files/BACKGROUND INFO CTO-1.pdf")
    #loader_all = MergedDataLoader(loaders=[loader_text, loader_pdf])
    loader_all = MergedDataLoader(loaders=[loader_pdf,loader_text])
    doc = loader_all.load()

    prompt_template = """
    Your GOAL is to update the SUMMARY provided in your background knowledge, to reflect the feedback and address the questions provided in the TRANSCRIPT of the chat (provided in background knowledge).
    Your output MUST ABSOLUTLY maintain the size, structure, format and tone as the original SUMMARY. Only change what is necessary to incorporate the insights and questions of the user. Nothing more. It is important to me, please.
    Let’s work this out in a step-by-step way to be sure we have the right answer.

    Background Knlowledge:
    "{text}"

    """
    prompt = PromptTemplate.from_template(prompt_template)

    # Define LLM chain
    llm = ChatOpenAI(temperature=0, model_name="gpt-4-1106-preview")
    llm_chain = LLMChain(llm=llm, prompt=prompt)

    # Define StuffDocumentsChain
    stuff_chain = StuffDocumentsChain(llm_chain=llm_chain, document_variable_name="text")
    ctoA_op = stuff_chain.run(doc)
    return ctoA_op

def cto_B(input_txt):
    # input_text should be chat conversation with CTO-2
    loader_text = TextLoader(input_txt)  # , encoding = 'UTF-8'
    loader_pdf = PyPDFLoader("pdf_files/BACKGROUND INFO CTO-B.pdf")
    #loader_all = MergedDataLoader(loaders=[loader_text, loader_pdf])
    loader_all = MergedDataLoader(loaders=[loader_pdf,loader_text])
    doc = loader_all.load()

    prompt_template = """
    Your GOAL is to update the EXECUTIVE SUMMARY OF ENHANCEMENTS OPTIONS provided in your background knowledge, to reflect the feedback and address the questions provided in the TRANSCRIPT of the chat (provided in background knowledge). 
    Your output MUST ABSOLUTLY maintain the size, structure, format and tone as the original EXECUTIVE SUMMARY OF ENHANCEMENTS OPTIONS. Only change what is necessary to incorporate the insights and questions of the user. Nothing more. It is important to me, please. 
    Let’s work this out in a step-by-step way to be sure we have the right answer.

    Background Knlowledge:
    "{text}"

    """
    prompt = PromptTemplate.from_template(prompt_template)

    # Define LLM chain
    llm = ChatOpenAI(temperature=0, model_name="gpt-4-1106-preview")
    llm_chain = LLMChain(llm=llm, prompt=prompt)

    # Define StuffDocumentsChain
    stuff_chain = StuffDocumentsChain(llm_chain=llm_chain, document_variable_name="text")
    ctoB_op = stuff_chain.run(doc)
    return ctoB_op


def cto_C(input_txt):
    # input_text should be chat conversation with CTO-3
    loader_text = TextLoader(input_txt)  # , encoding = 'UTF-8'
    loader_pdf = PyPDFLoader("pdf_files/BACKGROUND INFO CTO-C.pdf")
    #loader_all = MergedDataLoader(loaders=[loader_text, loader_pdf])
    loader_all = MergedDataLoader(loaders=[loader_pdf,loader_text])
    doc = loader_all.load()

    prompt_template = """
    Your GOAL is to update the OUTLOOK provided in your background knowledge, to reflect the feedback and address the questions provided in the TRANSCRIPT of the chat (provided in background knowledge) about this outlook.
    Your output MUST ABSOLUTLY maintain the size, structure, format and tone as the original OUTLOOK. Only change what is necessary to incorporate the insights and questions of the user. Nothing more. It is important to me, please.
    Let’s work this out in a step-by-step way to be sure we have the right answer.

    Background Knlowledge:
    "{text}"

    """
    prompt = PromptTemplate.from_template(prompt_template)

    # Define LLM chain
    llm = ChatOpenAI(temperature=0, model_name="gpt-4-1106-preview")
    llm_chain = LLMChain(llm=llm, prompt=prompt)

    # Define StuffDocumentsChain
    stuff_chain = StuffDocumentsChain(llm_chain=llm_chain, document_variable_name="text")
    ctoC_op = stuff_chain.run(doc)
    return ctoC_op