# This is a sample Python script.
import textwrap
from typing import Optional

from dependencies import Dependencies
from services.vector_db.vector_db_protocol import VectorDbRecord


def create_chunks_from_md(text: str, subject: str) -> list[str]:
    """
    Create chunks for a given markdown text
    :param text:
    :param subject:
    :return:
    """
    return Dependencies.instance().chunker_service.create(text, subject)

def create_embedding(text: str) -> Optional[list[float]]:
    """
    Create demo embeddings for a given text
    :param text:
    :return:
    """
    return Dependencies.instance().embedding_service.create(text)

def fill_text_store(text: str, subject: str) -> int:
    """
    Fill the vector store with the chunks created with the create_chunks_from_md function
    :param text:
    :return:
    """
    text_chunks: list[str] = create_chunks_from_md(text, subject)
    for text_chunk in text_chunks:
        Dependencies.instance().vector_repository.add(text_chunk)

    return len(text_chunks)

def search_vector_repository(query: str) -> list[str]:
    return Dependencies.instance().vector_repository.search(query, 1)

if __name__ == '__main__':
    text = textwrap.dedent("""
# BrewMate Mini – Productinformatie

## Over het apparaat

De BrewMate Mini is een compacte espressomachine, ontworpen voor gebruik in kleine keukens en studentenkamers. 
Het apparaat weegt slechts 1,8 kilogram en heeft een waterreservoir van 0,6 liter, genoeg voor twee tot drie 
kopjes espresso zonder bijvullen.

## Werking

De machine werkt met een pompdruk van 15 bar en bereikt de ideale zettemperatuur binnen ongeveer 25 seconden na het 
inschakelen. Dankzij het compacte formaat past de BrewMate Mini eenvoudig op een smal aanrecht, en het lichtgewicht 
ontwerp maakt het apparaat ook geschikt om mee te nemen op reis of naar kantoor.

## Kleuren en prijs

BrewMate Home levert de Mini standaard in de kleur mat zwart, al is er ook een witte uitvoering verkrijgbaar tegen
een kleine meerprijs. De adviesprijs bedraagt 79,95 euro.

## Garantie

Op het apparaat zit een garantie van één jaar, geldig vanaf de aankoopdatum bij een erkende verkoper.
      """)
    print(create_chunks_from_md(text, "BrewMate"))
    print(create_embedding(text))
    print(f'Added {fill_text_store(text, "BrewMate")} items to vector repository')
    print('[Kleur]')
    print(search_vector_repository("In welke kleur is de brewmate mini te verkrijgen?"))
    print('[Pompdruk]')
    print(search_vector_repository("Wat is de pompdruk van de brewmate mini?"))


