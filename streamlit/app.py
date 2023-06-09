import streamlit as st
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import nltk
import math
import torch

model_name = "afnanmmir/t5-base-abstract-to-plain-language-1"
# model_name = "afnanmmir/t5-base-axriv-to-abstract-3"
max_input_length = 1024
max_output_length = 256

st.header("Generate summaries")

st_model_load = st.text('Loading summary generator model...')

# @st.cache(allow_output_mutation=True)
@st.cache_data
def load_model():
    print("Loading model...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    nltk.download('punkt')
    print("Model loaded!")
    return tokenizer, model

tokenizer, model = load_model()
st.success('Model loaded!')
st_model_load.text("")

# with st.sidebar:
#     st.header("Model parameters")
#     if 'num_titles' not in st.session_state:
#         st.session_state.num_titles = 5
#     def on_change_num_titles():
#         st.session_state.num_titles = num_titles
#     num_titles = st.slider("Number of titles to generate", min_value=1, max_value=10, value=1, step=1, on_change=on_change_num_titles)
#     if 'temperature' not in st.session_state:
#         st.session_state.temperature = 0.7
#     def on_change_temperatures():
#         st.session_state.temperature = temperature
#     temperature = st.slider("Temperature", min_value=0.1, max_value=1.5, value=0.6, step=0.05, on_change=on_change_temperatures)
#     st.markdown("_High temperature means that results are more random_")

if 'text' not in st.session_state:
    st.session_state.text = ""
st_text_area = st.text_area('Text to generate the summary for', value=st.session_state.text, height=500)

def generate_summary():
    st.session_state.text = st_text_area

    # tokenize text
    inputs = ["summarize: " + st_text_area]
    # print(inputs)
    inputs = tokenizer(inputs, return_tensors="pt", max_length=max_input_length, truncation=True)
    print("Tokenized inputs: ")
    # print(inputs)
    # inputs = tokenizer(inputs, return_tensors="pt")

    # # compute span boundaries
    # num_tokens = len(inputs["input_ids"][0])
    # print(f"Input has {num_tokens} tokens")
    # max_input_length = 500
    # num_spans = math.ceil(num_tokens / max_input_length)
    # print(f"Input has {num_spans} spans")
    # overlap = math.ceil((num_spans * max_input_length - num_tokens) / max(num_spans - 1, 1))
    # spans_boundaries = []
    # start = 0
    # for i in range(num_spans):
    #     spans_boundaries.append([start + max_input_length * i, start + max_input_length * (i + 1)])
    #     start -= overlap
    # print(f"Span boundaries are {spans_boundaries}")
    # spans_boundaries_selected = []
    # j = 0
    # for _ in range(num_titles):
    #     spans_boundaries_selected.append(spans_boundaries[j])
    #     j += 1
    #     if j == len(spans_boundaries):
    #         j = 0
    # print(f"Selected span boundaries are {spans_boundaries_selected}")

    # # transform input with spans
    # tensor_ids = [inputs["input_ids"][0][boundary[0]:boundary[1]] for boundary in spans_boundaries_selected]
    # tensor_masks = [inputs["attention_mask"][0][boundary[0]:boundary[1]] for boundary in spans_boundaries_selected]

    # inputs = {
    #     "input_ids": torch.stack(tensor_ids),
    #     "attention_mask": torch.stack(tensor_masks)
    # }

    # compute predictions
    # outputs = model.generate(**inputs, do_sample=True, temperature=temperature, max_length=max_output_length)
    outputs = model.generate(**inputs, do_sample=True, max_length=max_output_length, early_stopping=True, num_beams=8, length_penalty=2.0, no_repeat_ngram_size=2, min_length=64)
    # print("outputs", outputs)
    decoded_outputs = tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]
    # print("Decoded_outputs", decoded_outputs)
    predicted_summaries = nltk.sent_tokenize(decoded_outputs.strip())
    # print("Predicted summaries", predicted_summaries)
    # decoded_outputs = tokenizer.batch_decode(outputs, skip_special_tokens=True)
    # predicted_summaries = [nltk.sent_tokenize(decoded_output.strip())[0] for decoded_output in decoded_outputs]

    st.session_state.summaries = predicted_summaries

# generate title button
st_generate_button = st.button('Generate summary', on_click=generate_summary)

# title generation labels
if 'summaries' not in st.session_state:
    st.session_state.summaries = []

if len(st.session_state.summaries) > 0:
    # print("In summaries if")
    with st.container():
        st.subheader("Generated summaries")
        st.markdown(f"{' '.join(st.session_state.summaries)}")
