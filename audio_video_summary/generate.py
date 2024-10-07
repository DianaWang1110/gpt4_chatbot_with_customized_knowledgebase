"""Module to generate takeaways and summaries from the provided transcription"""
import openai
from langchain.docstore.document import Document
from langchain.llms.openai import OpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from audio_video_summary.constants import *


# Combine methods: How to combine chunks of text, eg map reduce, stuff, or refine
# Take in text and return text of bulleted key takeaways
# May move to main_functions file
def generate_takeaways(text, combine_method="map_reduce"):
    docs = split_text(text)
    llm = OpenAI(temperature=0, openai_api_key=openai.api_key)
    if combine_method.lower() == "map_reduce":
        return generate_takeaways_map_reduce(docs, llm)
    elif combine_method.lower() == "refine":
        return generate_takeaways_refine(docs, llm)
    else:
        print("Incorrect combine method or not implemented")
        return None


def generate_takeaways_map_reduce(docs, llm):
    prompt_template = """Generate some key takeways in bullet point format based on the provided webinar transcription:


    {text}


    TAKEAWAYS:"""

    prompt = PromptTemplate(template=prompt_template, input_variables=["text"])
    chain = load_summarize_chain(llm, chain_type="map_reduce", map_prompt=prompt, combine_prompt=prompt)
    output = chain.run(docs)
    return output


def generate_takeaways_refine(text, docs, llm):
    prompt_template = """Generate 5 key takeways in bullet point format based on the provided webinar transcription:


    {text}


    TAKEAWAYS:"""
    prompt = PromptTemplate(template=prompt_template, input_variables=["text"])
    refine_template = (
        "Your job is to produce a list of 5 key takeaways in bullet point format\n"
        "We have provided an existing list up to a certain point: {existing_answer}\n"
        "We have the opportunity to refine the existing list"
        "(only if needed) with some more context below.\n"
        "------------\n"
        "{text}\n"
        "------------\n"
        "Given the new context, refine the original list"
        "If the context isn't useful, return the original list."
    )
    refine_prompt = PromptTemplate(
        input_variables=["existing_answer", "text"],
        template=refine_template,
    )
    chain = load_summarize_chain(OpenAI(temperature=0, openai_api_key=openai.api_key), chain_type="refine",
                                 question_prompt=prompt, refine_prompt=refine_prompt)
    output = chain({"input_documents": docs}, return_only_outputs=True)
    # TODO: Cut out at least the last bullet point since it often has an unfinished one at the end
    return output['output_text']


# Take in text and return text of summary
def generate_summary(text, combine_method):
    print("not yet implemented")
    pass


# Splits the text into document pages
def split_text(text):
    text_splitter = RecursiveCharacterTextSplitter()
    texts = text_splitter.split_text(text)
    docs = [Document(page_content=t) for t in texts]
    return docs
