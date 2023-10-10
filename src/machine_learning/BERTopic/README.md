# BERTopic_Telegram_Analysis

Leverage the BERTopic framework to generate easily interpretable topics from vast datasets originating from 32 public Telegram channels used by Ukrainian refugees. This project aims to study the refugees' needs within Switzerland.

## Installation
To utilize this model, install BERTopic via pip:
```bash
pip install -U bertopic
```
```python
topic_model = BERTopic.load("kdot/BERTopicTelegramAnalysis")
topic_info = topic_model.get_topic_info()
```
## Topic Overview

| Attribute          | Value   |
|--------------------|---------|
| Total topics       | 30      |
| Training documents | 339,650 |

### Training Hyperparameters

| Parameter              | Value   |
|------------------------|---------|
| calculate_probabilities| False   |
| language               | multilingual |
| low_memory             | False   |
| min_topic_size         | 10      |
| n_gram_range           | (1, 1)  |
| nr_topics              | 30      |
| seed_topic_list        | None    |
| top_n_words            | 10      |
| verbose                | True    |

### Framework Versions

| Library               | Version |
|-----------------------|---------|
| Numpy                 | 1.24.4  |
| HDBSCAN               | 0.8.33  |
| UMAP                  | 0.5.4   |
| Pandas                | 2.0.3   |
| Scikit-Learn          | 1.0.2   |
| Sentence-transformers | 2.2.2   |
| Transformers          | 4.33.2  |
| Numba                 | 0.58.0  |
| Plotly                | 5.17.0  |
| Python                | 3.8.10  |
| bertopic              | 0.15.0  |


Note:When saving the model, make sure to also keep track of the versions of dependencies and Python used. Loading and saving the model should be done using the same dependencies and Python. Moreover, models saved in one version of BERTopic are not guaranteed to load in other versions.

## Data Preprocessing
Initially, data preprocessing involved removing stopwords, hyperlinks, and emojis. However, we discovered that certain preprocessing steps, like emoji removal, could potentially impair the transformer models' training environment. Emojis, for instance, can be crucial for identifying advertisements. Thus, we keep the emoji, delaying the stopwords application until post-embedding to preserve the text's full contextual information, essential for accurate embedding generation.
The dataset was also cleansed of noisy elements like HTML tags, following Maarten's suggestion. From the unlabeled dataset of over 2 million records, data pertinent to Switzerland was extracted and merged with the supervised dataset, retaining only the text and cluster_id columns.

## Semi-Supervised Strategy
To execute our semi-supervised strategy, pre-defined topics were supplied as input to the y parameter when fitting the BERTopic model. This approach allows BERTopic to fine-tune the topic creation based on these specified labels.
```python
class_name_dict = {-1:"no_class",
    0:"S Status Information",
    1:"Medical Information",
    2:"Consulate Services",
    **dict.fromkeys([3, 14]:'Education'),
    4:'no_class', #don't know
    5:"Accomodation",
    6:'Public Transportation',
    7:'Consumer Products Needed',
    8: 'Refugee Camp Information',
    9: 'Pets',
    10:"no_class", #Ads
    11:"Social Security",
    12:'no_class', #Ads beauty
    **dict.fromkeys([13,15,16,21]:'Social Activities'),
    17:"Psychological Support",
    18:"no_class", #Ads for Phones
    19:"Employment",
    20:"Divorce", #probably not relevant
    22:'Legal Information',
    23:"S Status Extension",
    24:"no_class", #mushroom
    25:"Nursing for Special Care", #Ads
    26:"State Secretariat for Migration Information",
    27:"Religious Information",
    28:'no_class', #@ mentions
} 
```
A semi-supervised UMAP instance was utilized to reduce the embeddings' dimensionality before clustering documents with HDBSCAN. Our BERTopic configuration is detailed below:

```python
self.model = BERTopic(
    embedding_model="paraphrase-multilingual-MiniLM-L12-v2",
    language="multilingual",
    verbose=True,
    nr_topics='30',
    umap_model=umap_model,
    hdbscan_model=hdbscan_model,
    vectorizer_model=vectorizer_model,
    calculate_probabilities=False
)
```
Performance enhancements were achieved by setting low_memory=true and calculate_probabilities=False. During the UMAP step, n_neighbours was truncated to 10 for smoother operations to combat the dominance of non-essential data like timestamps or ads in leading clusters. Relevant Russian keywords were appended to our stopwords_ua.txt list, applied post-embedding and clustering.

## Transformer Selection
Our transformer selection was influenced by a comparison between paraphrase-multilingual-mpnet-base-v2 and paraphrase-multilingual-MiniLM-L12-v2. Despite the former's slightly superior performance, its processing speed was thrice as slow, making paraphrase-multilingual-MiniLM-L12-v2 a more efficient choice.

The trained model was stored using safertensors due to its lightweight format, suitable for production use, and shared on the HuggingFace Hub.  https://huggingface.co/kdot/BERTopicTelegramAnalysis
