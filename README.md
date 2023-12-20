## Alphatube

- A python package that extracts S&P 500 companies from Youtube video transcrpit. Utilizing Youtube API and Huggingface pipeline to run named entity recognition. 

- To install the package:
```commandline
!pip install -q git+https://github.com/hellozeyu/alphatube
```
- Example use case:
```python
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
from alphatube import download_channel_transcript, extract_named_entity
from googleapiclient.discovery import build
from tqdm import tqdm
import pandas as pd
import os

API_Key = "Your youtube API key"
service = build("youtube", "v3", developerKey=API_Key)

# Download all the videos of the channel as a list of dictionaries
# For multiple channels, you can use a for loop and append the result
# Use the commentted line below if you are just testing because there is a quota on the youtube API

# videos = download_channel_transcript(service, "UCCmJVw9xQfYuuAAwZGedKRg", testing=True)
videos = download_channel_transcript(service, "UCCmJVw9xQfYuuAAwZGedKRg")

# Set up the tokenizer
ner_tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER")
ner_model = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER")
ner_pipeline = pipeline('ner', model=ner_model, tokenizer=ner_tokenizer, aggregation_strategy="simple", device=0)

# Saving ner result along with the videos as a list of dictionaries
final_result = []
for video in tqdm(videos):
    ner_result = extract_named_entity(video["transcript"], ner_pipeline)
    if ner_result:
        for result in ner_result:
            video_new = {"source_ts": video["source_ts"],
                            "source_url": video["source_url"],
                            "source_entity": result["source_entity"],
                            "text": result["text"]}
            final_result.append(video_new)
```