import clean_patterns as pt
from bs4 import BeautifulSoup
import nltk.corpus as corpus
import nltk.stem as stem
import nltk
import re


def _apply_cleaning(text, cleaning, cleaning_log, key):
    """Applies cleaning to text and stores cleaned test in cleaning_log[key]."""

    text = cleaning(text)
    cleaning_log[key] = text
    return text


def clean_text(text):
    """Clean raw text. Returns cleaned text and cleaning log."""

    cleaning_log = {}
    # Remove html.
    text = _apply_cleaning(text, _remove_html, cleaning_log, "remove_html")
    # Replace whitespaces.
    text = _apply_cleaning(text, _replace_whitespaces, cleaning_log, 'replace_whitespaces')
    # Replace multiple stopwords.
    text = _apply_cleaning(text, _replace_multiple_stop_characters, cleaning_log, 'replace_multiple_stop_characters')
    # Replace apostrophes.
    text = _apply_cleaning(text, _replace_apostrophes, cleaning_log, 'replace_apostrophes')
    # Expand contractions.
    text = _apply_cleaning(text, _expand_contractions, cleaning_log, 'expand_contractions')
    # Remove hyperlinks.
    text = _apply_cleaning(text, _remove_hyperlinks, cleaning_log, 'remove_hyperlinks')
    # Remove special characters.
    text = _apply_cleaning(text, _remove_special_characters, cleaning_log, 'remove_special_characters')
    # Remove numbers.
    text = _apply_cleaning(text, _remove_numbers, cleaning_log, 'remove_numbers')
    # Convert to lower case.
    text = _apply_cleaning(text, _convert_case, cleaning_log, 'convert_case')
    # Remove repeated characters.
    text = _apply_cleaning(text, _remove_repeated_characters, cleaning_log, 'remove_repeated_characters')
    #  Manually correct words.
    text = _apply_cleaning(text, _correct_manually, cleaning_log, 'correct_manually')
    # Sentence tokenize.
    text = _apply_cleaning(text, _sentence_tokenize, cleaning_log, 'sentence_tokenize')
    # Remove sentence ending characters.
    text = _apply_cleaning(text, _remove_end_characters, cleaning_log, 'remove_end_characters')
    # POS tag.
    text = _apply_cleaning(text, _pos_tag_text, cleaning_log, 'pos_tag')
    # Lemmatize.
    text = _apply_cleaning(text, _lemmatize_text, cleaning_log, 'lemmatize')
    # Remove stopwords.
    text = _apply_cleaning(text, _remove_stopwords, cleaning_log, 'remove_stopwords')
    # Merge.
    text = _apply_cleaning(text, _merge_sentences, cleaning_log, 'merge_sentences')
    # Merge tokens.
    text = _apply_cleaning(text, _merge_tokens, cleaning_log, '_merge_tokens')

    # Return cleaned text and cleaning log.
    return text



def _merge_tokens(tokens):
    return " ".join([t[0] for t in tokens]).strip()


# Removes htlm tags from a review
def _remove_html(text):
    return BeautifulSoup(text, 'lxml').get_text()


def _replace_whitespaces(text):
    """Replaces all whitespaces with one space."""

    # Replaces all whitespaces with ' '.
    text = re.sub(pt.get_whitespace_pattern(), ' ', text)
    # Strip leading whitespaces.
    text = text.strip()

    return text


def _replace_multiple_stop_characters(text):
    """Replaces multiple stopwords with single stopwords."""

    def get_single_match(match):
        """Returns single match of multiple match."""

        word = match.group()
        return word[0]

    text = re.sub('[.!?]+', get_single_match, text)

    return text


def _replace_apostrophes(text):
    """Replaces apostrophe pattern with '."""

    # Replaces apostrophe pattern with '.
    text = re.sub(pt.get_apostrophe_pattern(), "'", text)

    return text


def _expand_contractions(text):
    """Expands contractions in text."""

    # Creates contractions pattern.
    pattern = re.compile('({})'.format('|'.join(pt.get_contraction_dict().keys())), flags=re.IGNORECASE | re.DOTALL)

    def expand_match(contraction):
        """Expands matched contraction."""

        # Retrieves matched contraction from string.
        match = contraction.group(0)
        # Stores first character for case sensitivity.
        first_char = match[0]
        # Find expanded contraction in dictionary, based on contraction key.
        expanded_contraction = pt.get_contraction_dict().get(match)
        # If the contraction could not be found, try again with lower case.
        if not expanded_contraction:
            expanded_contraction = pt.get_contraction_dict().get(match.lower())
        # Add first character to expanded contraction.
        expanded_contraction = first_char + expanded_contraction[1:]
        return expanded_contraction

    # Replaces contractions with expanded contractions in text.
    text = pattern.sub(expand_match, text)

    # Strip text.
    text = text.strip()

    return text


def _remove_hyperlinks(text):
    """Remove hyperlinks from text."""

    # Replace hyperlinks with space.
    text = re.sub(pt.get_hyperlink_pattern(), r' ', text)

    # Then remove multiple adjacent spaces.
    text = re.sub(' +', ' ', text)

    # Strip text.
    text = text.strip()

    return text


def _remove_special_characters(text):
    """Removes special characters from text."""

    # Replace all special characters with spaces.
    text = re.sub(pt.get_special_characters_pattern(), r' ', text)
    # Then remove multiple adjacent spaces.
    text = re.sub(' +', ' ', text)
    # Strip text.
    text = text.strip()

    return text


def _remove_numbers(text):
    """Remove numbers from text."""

    text = re.sub(pt.get_number_pattern(), r' ', text)
    # Then remove multiple adjacent spaces.
    text = re.sub(' +', ' ', text)
    # Strip text.
    text = text.strip()

    return text


def _convert_case(text):
    """Converts case to lower."""

    return text.lower()


def _expand_abbreviations(text):
    """Expands contractions in text."""

    # Creates abbreviations pattern.
    pattern = re.compile('{}'.format(r'\.?\s|'.join(pt.get_abbreviation_dict().keys())),
                                       flags=re.IGNORECASE | re.DOTALL)

    print(1)

    def expand_match(match):
        """Expands matched contraction."""

        # Retrieves matched contraction from string.
        match = match.group(0)
        # If last character is space, remove space.
        if match[-1] == " ":
            match = match[:-1]
            remove_space = True
        else:
            remove_space = False
        # If last character is dot, remove dot.
        if match[-1] == r'.':
            match = match[:-1]
        # Find expanded contraction in dictionary, based on contraction key.
        expanded_contraction = pt.get_abbreviation_dict().get(match.lower())
        if not expanded_contraction:
            try:
                return match.group(0)
            except AttributeError:
                print(1)
        if remove_space:
            expanded_contraction += " "
        # Add first character to expanded contraction.
        return expanded_contraction

    # Replaces contractions with expanded contractions in text.
    text = text + ' '
    text = re.sub(pattern, expand_match, text)

    # Strip text.
    text = text.strip()

    return text


def _remove_stopwords(text):
    """Remove stopwords from word token list"""

    def remove_stopwords_sentence(sentence):
        """Removes stopwords from sentence."""

        # Create stopwords list.
        stop_set = set(corpus.stopwords.words('english'))
        stop_set.update(pt.get_stopwords())
        # Filter stopwords from text.
        sentence = [(word, tag) for (word, tag) in sentence if word not in stop_set]

        return sentence

    return [remove_stopwords_sentence(sentence) for sentence in text]


def _sentence_tokenize(text):
    "Sentence tokenizes text."

    text = nltk.sent_tokenize(text)

    return text


def _pos_tag_text(text):
    """Labels text with POS tags."""

    def pos_tag_sentence(sentence):
        """Labels sentence with POS tags."""

        def convert_tags(pos_tag):
            if pos_tag.startswith('J'):
                return corpus.wordnet.ADJ
            elif pos_tag.startswith('V'):
                return corpus.wordnet.VERB
            elif pos_tag.startswith('N'):
                return corpus.wordnet.NOUN
            elif pos_tag.startswith('R'):
                return corpus.wordnet.ADV
            else:
                return None

        sentence = sentence.split()
        sentence = nltk.pos_tag(sentence)
        sentence = [(word.lower(), convert_tags(pos_tag)) for word, pos_tag in sentence]
        return sentence

    return [pos_tag_sentence(sentence) for sentence in text]


def _lemmatize_text(text):
    """Applies lemmatization to text."""

    def lemmatize_sentence(sentence):
        """Applies lemmatization to sentence."""

        sentence = [(stem.WordNetLemmatizer().lemmatize(word, pos_tag), pos_tag) if pos_tag else (word, pos_tag)
                             for word, pos_tag in sentence]

        return sentence

    return [lemmatize_sentence(sentence) for sentence in text]


def _remove_end_characters(text):
    """Removes end characters from word token list."""

    def remove_characters(sentence):
        """Removes end characters from sentence."""

        sentence += ' '
        # Replace stopwords with spaces.
        sentence = re.sub(pt.get_end_characters_pattern(), r' ', sentence)
        # Then remove multiple adjacent spaces.
        sentence = re.sub(' +', ' ', sentence)
        # Then strip text.
        sentence = sentence.strip()

        return sentence

    return [remove_characters(sentence) for sentence in text]


def _remove_repeated_characters(text):

    text = text.split()

    repeat_pattern = re.compile(r'(\w*)(\w)\2(\w*)')
    match_substitution = r'\1\2\3'

    def replace(old_word):
        if corpus.wordnet.synsets(old_word):
            return old_word
        new_word = repeat_pattern.sub(match_substitution, old_word)
        return replace(new_word) if new_word != old_word else new_word

    text = [replace(word) for word in text]

    text = ' '.join([word for word in text])
    text = text.strip()

    return text


def _merge_sentences(text):
    """Merges sentences in one list."""

    return [word for sentence in text for word in sentence]


def _correct_manually(text):
    """Corrects texts manually."""

    # Creates pattern.
    pattern = re.compile('({})'.format('|'.join(pt.get_manual_corrections().keys())), flags=re.IGNORECASE | re.DOTALL)

    def correct_match(match):
        """Expands matched contraction."""

        # Retrieves matched string from string.
        match_string = match.group(0)
        # Stores first character for case sensitivity.
        first_char = match_string[0]
        # Find expanded contraction in dictionary, based on contraction key.
        corrected_match = pt.get_manual_corrections().get(match_string)
        # If the contraction could not be found, try again with lower case.
        if not corrected_match:
            corrected_match = pt.get_manual_corrections().get(match_string.lower())
        # Add first character to expanded contraction.
        corrected_match = first_char + corrected_match[1:]
        return corrected_match

    # Replaces contractions with expanded contractions in text.
    text = pattern.sub(correct_match, text)

    # Strip text.
    text = text.strip()

    return text
