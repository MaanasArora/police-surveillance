import argparse
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
import pymupdf
import spacy

from tqdm import tqdm

nlp = spacy.load("en_core_web_sm")


@dataclass
class Page:
    text: str


@dataclass
class Document:
    year: int
    name: str
    pages: list
    entities: list


@dataclass
class Entity:
    text: str
    sentence: str
    label: str


def read_document_from_filename(filename):
    doc_pdf = pymupdf.open(filename)

    name = filename.stem
    year = int(str(filename).replace("tpsb-", "").split("/")[-2])
    doc = Document(year=year, name=name, pages=[], entities=[])
    for page_pdf in doc_pdf:
        page = Page(text=page_pdf.get_text())
        doc.pages.append(page)
    return doc


def read_documents(path, limit=None):
    names = list(Path(path).glob("./*/*.pdf"))

    if limit:
        if len(names) > limit:
            names = names[:limit]

    docs = list(map(read_document_from_filename, names))
    return docs


def parse_entities(text):
    text_nlp = nlp(text)
    return [
        Entity(label=ent.label_, text=ent.text, sentence=ent.sent.text)
        for ent in text_nlp.ents
        if ent.label_ == "ORG"
    ]


def main():
    keys = pd.read_csv("./data/names.txt", header=None)[0].dropna().tolist()
    documents = read_documents("./data/tpsb")

    data = []
    for doc in tqdm(documents):
        for i, page in tqdm(enumerate(doc.pages, 1), leave=False):
            ents = parse_entities(page.text)
            data.extend(
                [
                    {
                        "document": doc.name,
                        "page": i,
                        "entity": ent.text,
                        "sentence": ent.sentence,
                    }
                    for ent in ents
                ]
            )

    df = pd.DataFrame(data)
    df.to_csv("result.csv")


if __name__ == "__main__":
    main()
