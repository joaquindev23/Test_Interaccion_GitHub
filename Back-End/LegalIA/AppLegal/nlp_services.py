# Este archivo contiene las funciones que se encargan de interactuar con los modelos de transformers para generar texto, resumir texto y clasificar texto.
from transformers import AutoModelForTokenClassification, AutoTokenizer,pipeline
import torch
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForTokenClassification

# Inicializamos las pipelines de transformers aquí para reutilización
generator = pipeline('text-generation', model='sshleifer/distilbart-cnn-12-6', revision='a4f8f3e')
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
qa_pipeline = pipeline("question-answering", model="deepset/roberta-base-squad2", tokenizer="deepset/roberta-base-squad2")

def generate_text(prompt):
    return generator(prompt, max_length=100, num_return_sequences=1)[0]['generated_text']

#def summarize_text(document_text):
#    return summarizer(document_text, max_length=150, min_length=30, do_sample=False)[0]['summary_text']
def summarize_text(text, max_length=130, min_length=30):
    #summarizer = get_summarizer()
    summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)[0]['summary_text']
    return summary


def classify_text(text, labels):
    return classifier(text, candidate_labels=labels)

def answer_question(question, context_text):
    result = qa_pipeline(question=question, context=context_text)
    return result['answer']

def get_ner_pipeline():
    model_name = "dccuchile/bert-base-spanish-wwm-cased"  # Modelo específico para español
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForTokenClassification.from_pretrained(model_name)
    
    # Configura la pipeline de NER
    ner_pipeline = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple")
    return ner_pipeline

def extract_entities(text):
    ner_pipeline = get_ner_pipeline()
    entities = ner_pipeline(text)
    return entities

def get_translation_pipeline():
    model_name = "Helsinki-NLP/opus-mt-es-en"  # Modelo para traducción de español a inglés
    translation_pipeline = pipeline("translation_es_to_en", model=model_name)
    return translation_pipeline

def translate_text(text, target_language='en'):
    translation_pipeline = get_translation_pipeline()
    translation = translation_pipeline(text, max_length=512)[0]['translation_text']
    return translation
