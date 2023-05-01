# Research-Paper-Summarizer
Finetuning Large Language Models to perform summarization on research papers.

A base T5 auto-regressive model was finetuned on [this](https://www.dropbox.com/s/huwm01glsk9fou0/plos_readability_ctrl_sum_corpus.rar?dl=0) dataset of research papers paired with plain language summaries to generate readable summaries from technical abstracts.

The model achieved the following evaluation metrics:
- ROUGE-1: 0.403590
- ROUGE-2: 0.124948
- ROUGE-L: 0.214003



