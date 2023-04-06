# Towards Mitigating Answer-Position Bias in Machine Reading Comprehension
## Introduction
> Machine Reading Comprehension (MRC) models have a tendency to take advantage of spurious correlations (also known as dataset bias or annotation artifacts in the research community). Consequently, these models may perform the MRC task without fully comprehending the given context and question, which is undesirable since it may result in low robustness against distribution shift. This paper delves into the concept of answer-position bias, where a significant percentage of training questions have answers located solely in the first sentence of the context. We hypothesize that the main reason causing the answer-position bias is that when model are trained with biased train set, which leads us to another hypothesis such that the MRC models can overcome the bias and achieve a good performance on the test set with anti-biased samples. We validate our hypothesis using model BERT and dataset SQuAD. We find the a large proportion of samples of development set SQuAD can be solved simply with answer-position bias, and this dataset is overestimate the true comprehension ability of MRC models. Besides, we also show that BERT trained with unanswerable questions can recognize that the first sentence in the context is not an appropriate source for the answer the question, but it fail to find out answer in other sentences of the context.
## Usage
### Requirements
```
pip install src/requirements.txt
```
### Survey
### Debias Answer-Position using Unanswerable Questions
