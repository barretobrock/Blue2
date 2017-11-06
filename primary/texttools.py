#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import re


class MarkovText:
    def __init__(self, bulk_text):
        self.mkov = __import__('markovify')
        if isinstance(bulk_text, list):
            # Multiple models
            models = []
            for i in bulk_text:
                m = self.mkov.Text(i)
                models.append(m)
            self.model = self.mkov.combine(models)
        if isinstance(bulk_text, dict):
            models = []
            for i in list(bulk_text.values()):
                m = self.mkov.Text(i)
                models.append(m)
            self.model = self.mkov.combine(models)
        else:
            self.model = self.mkov.Text(bulk_text)

    def generate_n_sentences(self, n, char_limit=0):
        sentences = []
        for i in range(n):
            sentences.append(self.generate_sentence(char_limit))
        return sentences

    def generate_sentence(self, char_limit=0):
        if char_limit > 0:
            return self.model.make_short_sentence(char_limit)
        else:
            return self.model.make_sentence()


class WebExtractor:
    def __init__(self):
        self.bs4 = __import__('bs4')
        self.bs = self.bs4.BeautifulSoup

    def get_text(self, url, element='p'):
        respond = requests.get(url)
        soup = self.bs(respond.text, 'lxml')
        return soup.find_all(element)

    def get_links(self, url, url_match=''):
        items = self.get_text(url, 'a')
        url_list = []
        for item in items:
            # Determine if element has href attribute
            attr = None
            try:
                attr = item._attr_value_as_string('href')
            except:
                pass
            if attr is not None:
                if url_match == '':
                    url_list.append(attr)
                elif url_match in attr:
                    url_list.append(attr)
        return url_list


class TextCleaner:
    def __init__(self):
        pass

    def process_text(self, text):
        regex_pattern = '[\(\[].*?[\)\]]'  # pattern to remove brackets and their info
        rem_chars = "()[]{}«»"  # characters to explicitly remove from the string
        # eliminate brackets and text with brackets
        text = re.sub(regex_pattern, '', text)
        # eliminate any special characters
        for ch in list(rem_chars):
            if ch in text:
                text = text.replace(ch, '')
        # fix any issues with strings having no space after periods
        space_fixes_find = [r'\.(?! )', r'\?(?! )', r'\!(?! )']
        space_fixes_rep = ['. ', '? ', '! ']
        for s in range(0, len(space_fixes_find)):
            text = re.sub(space_fixes_find[s], space_fixes_rep[s], re.sub(r' +', ' ', text))
        return text
