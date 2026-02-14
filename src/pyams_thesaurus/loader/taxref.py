# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

import codecs
import csv
import io

import chardet

from pyams_thesaurus.interfaces.loader import IThesaurusLoader
from pyams_thesaurus.loader import BaseThesaurusLoader, BaseThesaurusLoaderHandler, ThesaurusLoaderDescription, \
    ThesaurusLoaderTerm
from pyams_utils.registry import utility_config

__docformat__ = 'restructuredtext'


class TaxrefThesaurusLoaderHandler(BaseThesaurusLoaderHandler):
    """TaxRef thesaurus loader handler"""

    def read(self, data, configuration=None):
        """TaxRef file loader reader"""
        terms = {}
        if configuration is None:
            configuration = self.configuration
        encoding = None
        if configuration and configuration.encoding:
            encoding = configuration.encoding
        if (not encoding) and isinstance(data, str):
            encoding = chardet.detect(data[:1000]).get('encoding', 'utf-8')
        # define description
        description = ThesaurusLoaderDescription()
        if configuration and configuration.language:
            description.language = configuration.language
        # load terms
        if encoding !=  'utf-8':
            data = io.StringIO(codecs.getreader(encoding).decodeLocation(data.read())[0].encode('utf-8'))
        alias = {}
        utf_reader = codecs.getreader('utf-8')
        csv_reader = csv.DictReader(utf_reader(data), delimiter=';', quotechar='"')
        for term in csv_reader:
            key = term.get('CD_NOM')
            if not key:
                continue
            label = term.get('LB_NOM')
            note = term.get('LB_AUTEUR')
            generic = term.get('CD_SUP')
            ref = term.get('CD_REF')
            definition = term.get('URL')
            terms[key] = ThesaurusLoaderTerm(label,
                                             note=note,
                                             definition=definition,
                                             generic=generic,
                                             usage=ref if ref != key else None)
            names = term.get('NOM_VERN')
            if names:
                for name in map(str.strip, names.split(',')):
                    alias[name] = key
        if configuration.import_synonyms:
            for key, value in alias.items():
                terms[key] = ThesaurusLoaderTerm(key, usage=value)
                terms[value].used_for.append(key)
        return description, terms


@utility_config(name='TaxRef',
                provides=IThesaurusLoader)
class TaxrefThesaurusLoader(BaseThesaurusLoader):
    """TaxRef format thesaurus loader"""

    handler = TaxrefThesaurusLoaderHandler
