import spacy

nlp = spacy.load('en_core_web_sm')

def named_entities_searcher(text:str) -> list[tuple[str, str]]:
    """
    Calculates the Named Entities

    Args:
      text (str):the text to process

    Returns:
       list[tuple[str,str]]:A list of tuples with the pairs word,entity_type

    Example:
        >>> text ="Once upon a time, in a land filled with vibrant flowers and sparkling streams, lived a herd of unicorns. These weren't ordinary unicorns; they were as colorful as the flowers that carpeted the meadows. Among them was a young unicorn named Lily. Lily was unique, with a coat as white as snow and a mane that shimmered like a rainbow. Her horn was a spiral of iridescent light, casting a soft glow wherever she went. Lily loved flowers more than anything else. She would spend her days frolicking among the tulips, roses, and daisies, her laughter echoing through the valley. The flowers seemed to dance with her, swaying in the breeze as if sharing her joy. One day, Lily discovered a flower she had never seen before. It was a delicate bloom, with petals as transparent as crystal, shimmering in the sunlight. It was the rare Crystal Blossom, a flower said to bloom once every thousand years. Seeing the Crystal Blossom, Lily realized that like the flowers, each unicorn was unique and beautiful in their own way. She understood that their differences made them special, just like the myriad of flowers that adorned their home. From that day forward, Lily shared her wisdom with her fellow unicorns. The unicorns, in turn, learned to appreciate each other's uniqueness, living harmoniously amidst the flowers, under the watchful eye of the Crystal Blossom. And so, the land of unicorns and flowers thrived, filled with love, respect, and the laughter of unicorns playing among the flowers."
        >>> named_entities_searcher(text)
        [('Lily', 'PERSON'), ('her days', 'DATE'), ('One day', 'DATE'), ('Lily', 'PERSON'), ('Crystal Blossom', 'LOC'), ('every thousand years', 'DATE'), ('the Crystal Blossom', 'PRODUCT'), ('Lily', 'PERSON'), ('that day', 'DATE'), ('Lily', 'PERSON'), ('the Crystal Blossom', 'LOC')] 
    """
    doc = nlp(text)

    return [(ent.text,ent.label_) for ent in doc.ents ]

