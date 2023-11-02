import pysbd
import os
import pandas as pd

dirname = os.path.dirname(__file__)

company_df = pd.read_csv(dirname + "/data/company.csv")
companies = list(company_df['Name'].str.lower())


def extract_named_entity(transcript, ner_pipeline):
    seg = pysbd.Segmenter(language="en", clean=False)
    result = []

    text = seg.segment(transcript)
    # Iterate through the chunks
    for index, txt in enumerate(text):
        # Pass the transcript to the NER pipeline
        ner_result = ner_pipeline(txt)
        # Only continue if there is NER result
        if ner_result:
            entity_set = set()
            for entity in ner_result:
                if entity['entity_group'] == 'ORG':
                    # Only continue if the entity is org and in our companies list
                    if entity['word'].lower() in companies and entity['word'] not in entity_set:
                        entity_set.add(entity['word'])
                        prev_sent = text[index - 1] if index > 0 else ""
                        next_sent = text[index + 1] if index < len(text) - 1 else ""
                        txt = prev_sent + txt + next_sent
                        # Save everything is a Python dict and append it to the result list
                        item = {'source_entity': entity['word'], 'text': txt}
                        result.append(item)
    return result
