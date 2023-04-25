import streamlit as st
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import nltk
import math
import torch
import random
from datasets import load_dataset

st.session_state.indices_already_seen = set()


st.session_state.window_to_summary = {"left": "", "right": ""}

@st.cache_data
def load_model(model_name):
    print("Loading model...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    nltk.download('punkt')
    print("Model loaded!")
    return tokenizer, model

tokenizer, model = load_model("afnanmmir/t5-base-abstract-to-plain-language-1")

@st.cache_data
def get_datasets():
    print("Loading datasets...")
    predicted_set = load_dataset("json", data_files="../plos_readability_ctrl_sum_corpus_output_update/test_plos_output.jsonl")
    actual_set = load_dataset("json", data_files="../plos_readability_ctrl_sum_corpus/test_plos.jsonl")

    predicted_summaries = predicted_set["train"]["predicted summary"]
    actual_summaries = actual_set["train"]["abstract"]
    return predicted_summaries, actual_summaries

predicted_summaries, actual_summaries = get_datasets()

def get_random_summaries(generated_summaries, actual_summaries):
    n = len(generated_summaries)
    index = random.randint(0, n-1)
    while index in st.session_state.indices_already_seen:
        index = random.randint(0, n-1)
    st.session_state.indices_already_seen.add(index)
    return generated_summaries[index], actual_summaries[index]

def display_summaries(generated_summary, actual_summary):
    # pick a number uniformly random from 0 to 1
    rand_num = random.random()
    if(rand_num < 0.5):
        st.session_state.left_summary = generated_summary
        st.session_state.right_summary = actual_summary
        with col1.container():
            st.markdown(st.session_state.left_summary)
            st.button("Left", on_click=record_left_button)
        with col2.container():
            st.write(st.session_state.right_summary)
            st.button("Right", on_click=record_right_button)
        st.session_state.window_to_summary["left"] = "generated"
        st.session_state.window_to_summary["right"] = "actual"
    else:
        st.session_state.left_summary = actual_summary
        st.session_state.right_summary = generated_summary
        with col1.container():
            st.markdown(st.session_state.left_summary)
            st.button("Left", on_click=record_left_button)
        with col2.container():
            st.markdown(st.session_state.right_summary)
            st.button("Right", on_click=record_right_button)
        st.session_state.window_to_summary["left"] = "actual"
        st.session_state.window_to_summary["right"] = "generated"

def generate_summaries(generated_summaries, actual_summaries):
    generated_summary, actual_summary = get_random_summaries(generated_summaries, actual_summaries)
    display_summaries(generated_summary, actual_summary)

def update_screen():
    generate_summaries(predicted_summaries, actual_summaries)


def record_left_button():
    if(st.session_state.window_to_summary["left"] == "generated"):
        st.session_state.file.write("1\n")
    else:
        st.session_state.file.write("0\n")

def record_right_button():
    if(st.session_state.window_to_summary["right"] == "generated"):
        st.session_state.file.write("1\n")
    else:
        st.session_state.file.write("0\n")
    
def open_file():
    st.session_state.file = open('results.txt', 'a')
    # Do something with the file, e.g. read its contents

# Call the open_file function when the app starts
open_file()

# st.session_state.file.write("Hello\n")
# Define a function to close the file when the app stops
def close_file():
    if st.session_state.file is not None:
        st.session_state.file.close()

col1, col2 = st.columns(2)

# title generation labels
if 'left_summaries' not in st.session_state:
    st.session_state.left_summaries = ""
if 'right_summaries' not in st.session_state:
    st.session_state.right_summaries = ""

update_screen()


st.button("Close file", on_click=close_file)

