## Written by Katara
from urllib.parse import urlparse
from math import log
import logging
import re
from multiprocessing.pool import ThreadPool


class InvalidURLError(Exception):
    print("URL String is Invalid")


class InvalidURLPATHError(Exception):
    print("Please Enter a Path to a Valid URL File")


class LexicalUtilities(object):
    def __init__(self, url: str):
        self.description = 'blah'
        self.url = url
        self.urlparse = urlparse(self.url)

    '''Log Errors'''
    def _error_logger(self, error):
        logging.exception(error)

    '''Check if URL is Valid'''
    def _is_valid_url(self):
        c1 = self.urlparse.netloc is not None
        c2 = len(self.urlparse.netloc) > 1
        check = c1 and c2
        while not check:
            return InvalidURLError()

    '''Get Vowels'''
    def _get_vows(self):
        return 'aeiouAEIOU'

    '''Estimate Shanon Entropy'''
    def _get_entropy(self, text):
        try:
            text = text.lower()
            probs = [text.count(c) / len(text) for c in set(text)]
            return -sum([p * log(p) / log(2.0) for p in probs])
        except Exception as e:
            print(e)
            return None

    '''Get English Language Punctuations'''
    def _get_punctuations(self):
        return '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'


class LexicalSynthaticFeature(LexicalUtilities):
    def __init__(self, url: str):
        super(LexicalSynthaticFeature, self).__init__(url)
        self._is_valid_url()

    ''' Get Character Length of URL String'''
    def url_length(self):
        try:
            return len(self.url)
        except Exception as e:
            self._error_logger(e)
            return None

    ''' Get Total number of 0-9 digits in URL string'''
    def num_digits(self):
        try:
            return len([i for i in self.url if i.isdigit()])
        except Exception as e:
            self._error_logger(e)
            return None

    ##############PUNCTUATION COUNT FEATURES##############
    ''' Get Total number of punctuations in URL string'''
    def num_puncs(self):
        try:
            return len([i for i in self.url if i in self._get_punctuations() and i != '/'])
        except Exception as e:
            self._error_logger(e)
            return None

    ''' Get Total number of encoded characters in URL string'''
    def num_encoded_char(self):
        try:
            return len([i for i in self.url if i == '%'])
        except Exception as e:
            self._error_logger(e)
            return None

    ''' Get Total number of underscores in URL string'''
    def num_underscore(self):
        try:
            return len([i for i in self.url if i == '_'])
        except Exception as e:
            self._error_logger(e)
            return None

    ''' Get Total number of hyphens in URL string'''
    def num_hyphens(self):
        try:
            return len([i for i in self.url if i == '-'])
        except Exception as e:
            self._error_logger(e)
            return None

    ''' Get Total number of periods in URL string'''
    def num_periods(self):
        try:
            return len([i for i in self.url if i == '.'])
        except Exception as e:
            self._error_logger(e)
            return None

    ''' Get Total number of uppercase characters in URL string'''
    def num_capitalizations(self):
        try:
            return len([i for i in self.url if i.isupper()])
        except Exception as e:
            self._error_logger(e)
            return None

    ''' Get ratio of punctuations to characters in URL string in URL string'''
    def punc_to_char_ratio(self):
        if self.url_length() and self.url_length() > 0:
            try:
                return self.num_puncs() / self.url_length()
            except Exception as e:
                self._error_logger(e)
                return None
        else:
            return 0

    ''' Get ratio of punctuations to digits in URL string in URL string'''
    def punc_to_digit_ratio(self):
        if self.num_digits() and self.num_digits() > 0:
            try:
                return self.num_puncs() / self.num_digits()
            except Exception as e:
                self._error_logger(e)
                return None
        else:
            return 0

    ''' Get ratio of punctuations to digits in URL string in URL string'''
    def digit_to_char_ratio(self):
        if self.url_length() and self.url_length() > 0:
            try:
                return self.num_digits() / self.url_length()
            except Exception as e:
                self._error_logger(e)
                return None
        else:
            return 0

    def cap_to_puncs_ratio(self):
        if self.num_puncs() and self.num_puncs() > 0:
            try:
                return self.num_capitalizations() / self.num_puncs()
            except Exception as e:
                self._error_logger(e)
                return None
        else:
            return 0

    def cap_to_digit_ratio(self):
        if self.num_digits() and self.num_digits() > 0:
            try:
                return self.num_capitalizations() / self.num_digits()
            except Exception as e:
                self._error_logger(e)
                return None
        else:
            return 0
    ##############PUNCTUATION COUNT FEATURES##############


    ###############VOWEL & CONSONANT FEATURES #####################
    ''' Get Total number of english vows in URL string'''
    def num_vows(self):
        try:
            return len([i for i in self.url.lower() if i in 'aeiou'])
        except Exception as e:
            self._error_logger(e)
            return None

    ''' Get Total number of english cons in URL string'''
    def num_cons(self):
        try:
            return len([i for i in self.url.lower() if i.isalpha() and i not in 'aeiou'])
        except Exception as e:
            self._error_logger(e)
            return None

    ''' Get ratio of vows to cons in URL string in URL string'''
    def vows_to_cons_ratio(self):
        if self.num_cons() and self.num_cons() > 0:
            try:
                return self.num_vows() / self.num_cons()
            except Exception as e:
                self._error_logger(e)
                return None
        else:
            return 0

    ''' Get ratio of vows to digits in URL string in URL string'''
    def vows_to_digit_ratio(self):
        if self.num_digits() and self.num_digits() > 0:
            try:
                return self.num_vows() / self.num_digits()
            except Exception as e:
                self._error_logger(e)
                return None
        else:
            return 0

    ''' Get ratio of vows to punctuations in URL string in URL string'''
    def vows_to_punc_ratio(self):
        if self.num_puncs() and self.num_puncs() > 0:
            try:
                return self.num_vows() / self.num_puncs()
            except Exception as e:
                self._error_logger(e)
                return None
        else:
            return 0

    ''' Get ratio of consonants to digits in URL string in URL string'''
    def cons_to_digit_ratio(self):
        if self.num_digits() and self.num_digits() > 0:
            try:
                return self.num_cons() / self.num_digits()
            except Exception as e:
                self._error_logger(e)
                return None
        else:
            return 0

    ''' Get ratio of vows to cons in URL string in URL string'''
    def cons_to_puncs_ratio(self):
        if self.num_cons() and self.num_cons() > 0:
            try:
                return self.num_vows() / self.num_cons()
            except Exception as e:
                self._error_logger(e)
                return None
        else:
            return
    ###############vows & cons FEATURES #####################


    '''Run Lexical Feature Extractor'''
    def run(self):
        pool = ThreadPool(processes=20)
        pas = [
            pool.apply_async(self.url_length),
            pool.apply_async(self.cap_to_digit_ratio),
            pool.apply_async(self.cap_to_puncs_ratio),
            pool.apply_async(self.cons_to_digit_ratio),
            pool.apply_async(self.cons_to_puncs_ratio),
            pool.apply_async(self.digit_to_char_ratio),
            pool.apply_async(self.num_cons),
            pool.apply_async(self.num_digits),
            pool.apply_async(self.num_encoded_char),
            pool.apply_async(self.num_hyphens),
            pool.apply_async(self.num_periods),
            pool.apply_async(self.num_puncs),
            pool.apply_async(self.num_underscore),
            pool.apply_async(self.num_vows),
            pool.apply_async(self.num_capitalizations),
            pool.apply_async(self.punc_to_char_ratio),
            pool.apply_async(self.punc_to_digit_ratio),
            pool.apply_async(self.vows_to_cons_ratio),
            pool.apply_async(self.vows_to_digit_ratio),
            pool.apply_async(self.vows_to_punc_ratio)
        ]
        results = [i.get() for i in pas]
        pool.terminate()
        return results


class LexicalSemanticFeature(LexicalUtilities):
    def __init__(self, url: str):
        super(LexicalSemanticFeature, self).__init__(url)
        self._is_valid_url()

    '''If Host is an IP address'''
    def url_host_is_ip(self):
        try:
            host = self.urlparse.netloc
            pattern = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
            match = pattern.match(host)
            return match is not None
        except Exception as e:
            self._error_logger(e)
            return None

    '''If a port number is visible in URL String'''
    def has_port_in_string(self):
        try:
            has_port = self.urlparse.netloc.split(':')
            return len(has_port) > 1 and has_port[-1].isdigit()
        except Exception as e:
            self._error_logger(e)
            return None

    '''Get the number of encoded characters in URL String'''
    def is_encoded(self):
        try:
            return '%' in self.url.lower()
        except Exception as e:
            self._error_logger(e)
            return None

    '''Check for the presence of CLIENT keyword in URL String'''
    def has_client_in_string(self):
        try:
            return 'client' in self.url.lower()
        except Exception as e:
            self._error_logger(e)
            return None

    '''Check for the presence of ADMIN keyword in URL String'''
    def has_admin_in_string(self):
        try:
            return 'admin' in self.url.lower()
        except Exception as e:
            self._error_logger(e)
            return None

    '''Check for the presence of SERVER keyword in URL String'''
    def has_server_in_string(self):
        try:
            return 'server' in self.url.lower()
        except Exception as e:
            self._error_logger(e)
            return None

    '''Check for the presence of LOGIN keyword in URL String'''
    def has_login_in_string(self):
        try:
            return 'login' in self.url.lower()
        except Exception as e:
            self._error_logger(e)
            return None

    '''Check is the URL string has WWW'''
    def has_www_in_string(self):
        try:
            return "www." in self.url.lower()
        except Exception as e:
            self._error_logger(e)
            return None

    '''Check is the URL string has mailto:'''

    def has_mailto_in_string(self):
        try:
            return "mailto:" in self.url.lower()
        except Exception as e:
            self._error_logger(e)
            return None

    '''Check is the URL string has WWW'''

    def has_javascript_in_string(self):
        try:
            return "javascript" in self.url.lower()
        except Exception as e:
            self._error_logger(e)
            return None

    '''Run Lexical Feature Extractor'''
    def run(self):
        pool = ThreadPool(processes=8)
        pas = [
            pool.apply_async(self.url_host_is_ip),
            pool.apply_async(self.has_port_in_string),
            pool.apply_async(self.is_encoded),
            pool.apply_async(self.has_client_in_string),
            pool.apply_async(self.has_admin_in_string),
            pool.apply_async(self.has_server_in_string),
            pool.apply_async(self.has_login_in_string),
            pool.apply_async(self.has_www_in_string),
            pool.apply_async(self.has_mailto_in_string),
            pool.apply_async(self.has_javascript_in_string)
        ]
        results = [i.get() for i in pas]
        pool.terminate()
        return results


class LexicalSchematicFeature(LexicalUtilities):
    def __init__(self, url: str):
        super(LexicalSchematicFeature, self).__init__(url)
        self._is_valid_url()

    '''Get Protocol of URL'''
    def url_scheme(self):
        try:
            return self.urlparse.scheme
        except Exception as e:
            self._error_logger(e)
            return None

    '''Get Domain Extension of URL String'''
    def tld(self):
        try:
            return self.url.split('.')[-1].split('/')[0]
        except Exception as e:
            self._error_logger(e)
            return None

    ''' Get Character Length of URL String Top Level Domain'''
    def len_tld(self):
        try:
            return len(self.urlparse.netloc.split('.')[-1].split(':')[0])
        except Exception as e:
            self._error_logger(e)
            return None

    ''' Get Character Length of URL String Path'''
    def url_path_length(self):
        try:
            return len(self.urlparse.path)
        except Exception as e:
            self._error_logger(e)
            return None

    '''Get Average Length of URL parameters'''
    def avg_param_len(self):
        try:
            params = self.urlparse.query.split("&")
            return sum([len(i) for i in params])/len(params)
        except Exception as e:
            self._error_logger(e)
            return None

    '''Get Average Length of URL paths'''
    def avg_path_len(self):
        try:
            paths = self.urlparse.path.split("/")
            return sum([len(i) for i in paths]) / len(paths)
        except Exception as e:
            self._error_logger(e)
            return None

    ''' Get Character Length of URL String Host'''
    def url_host_length(self):
        try:
            return len(self.urlparse.netloc)
        except Exception as e:
            self._error_logger(e)
            return None

    ''' Get Total number of subdirectories in URL string'''
    def num_subdirectories(self):
        try:
            return len(self.urlparse.path.replace("%", "").split('/'))
        except Exception as e:
            self._error_logger(e)
            return None

    ''' Get Total number of query string parameters in URL string'''
    def num_parameters(self):
        params = self.urlparse.query
        return 0 if params == '' else len(params.split('&'))

    ''' Get Total number of fragments in URL string'''
    def num_fragments(self):
        frags = self.urlparse.fragment
        return len(frags.split('#')) - 1 if frags == '' else 0

    '''Get Entropy of URL Host/Domain name'''
    def host_entropy(self):
        try:
            return self._get_entropy(self.urlparse.netloc)
        except Exception as e:
            self._error_logger(e)
            return None

    '''Get Entropy of URL subdirectory'''
    def path_entropy(self):
        try:
            return self._get_entropy(self.urlparse.path)
        except Exception as e:
            self._error_logger(e)
            return None

    '''Get Entropy of URL subdirectory'''
    def fragment_entropy(self):
        try:
            return self._get_entropy(self.urlparse.fragment)
        except Exception as e:
            self._error_logger(e)
            return None

    '''Get Entropy of URL subdirectory'''
    def parameter_entropy(self):
        try:
            return self._get_entropy(self.urlparse.params)
        except Exception as e:
            self._error_logger(e)
            return None

    '''If a port number is visible in URL String'''
    def has_port_in_string(self):
        try:
            has_port = self.urlparse.netloc.split(':')
            return int(len(has_port) > 1 and has_port[-1].isdigit())
        except Exception as e:
            self._error_logger(e)
            return None

    '''Get Port Number (Defaults to Port 80 for '''
    def port_number(self):
        try:
            return self.urlparse.netloc.split(":")[1]
        except Exception as e:
            self._error_logger(e)
            return 22 if 'https:' in self.url else 80

    '''Run Lexical Component Feature Extractor'''
    def run(self):
        pool = ThreadPool(processes=16)
        pas = [
            pool.apply_async(self.url_path_length),
            pool.apply_async(self.url_host_length),
            pool.apply_async(self.len_tld),
            pool.apply_async(self.num_parameters),
            pool.apply_async(self.num_fragments),
            pool.apply_async(self.num_subdirectories),
            pool.apply_async(self.has_port_in_string),
            pool.apply_async(self.url_scheme),
            pool.apply_async(self.tld),
            pool.apply_async(self.avg_path_len),
            pool.apply_async(self.avg_param_len),
            pool.apply_async(self.host_entropy),
            pool.apply_async(self.path_entropy),
            pool.apply_async(self.fragment_entropy),
            pool.apply_async(self.parameter_entropy),
            pool.apply_async(self.port_number)
        ]
        results = [i.get() for i in pas]
        pool.terminate()
        return results


class LexicalCharSequencialFeature(LexicalUtilities):
    def __init__(self, url: str):
        super(LexicalCharSequencialFeature, self).__init__(url)
        self._is_valid_url()

    '''Get the number of two vowels  (ae) following each other in the URL String (Number of Diphthongs)'''
    def vows_to_vows_seq(self):
        counter, vows = 0, self._get_vows()
        for i in range(1, len(self.url)):
            if self.url[i].isalpha():
                if self.url[i-1] in vows and self.url[i] in vows:
                    counter += 1
        return counter

    '''Get the number of times a consonant comes after a vowel (ad) in the URL String'''
    def vows_to_cons_seq(self):
        counter, vows = 0, self._get_vows()
        for i in range(1, len(self.url)):
            if self.url[i].isalpha():
                if self.url[i-1] in vows and self.url[i] not in vows:
                    counter += 1
        return counter

    '''Get the number of two consonants following each other'''
    def cons_to_cons_seq(self):
        counter, vows = 0, self._get_vows()
        for i in range(1, len(self.url)):
            if self.url[i].isalpha():
                if self.url[i-1] not in vows and self.url[i] not in vows:
                    counter += 1
        return counter

    '''Get the number of time a vowel comes after a consonant (da) in the URL String'''
    def cons_to_vows_seq(self):
        counter, vows = 0, self._get_vows()
        for i in range(1, len(self.url)):
            if self.url[i].isalpha():
                if self.url[i-1] not in vows and self.url[i] in vows:
                    counter += 1
        return counter

    '''Get the number of time a 0-9 digit comes after a consonant (d2) in the URL String'''
    def cons_to_digit_seq(self):
        counter, vows = 0, self._get_vows()
        for i in range(1, len(self.url)):
            if self.url[i].isalpha():
                if self.url[i-1] not in vows and self.url[i].isdigit():
                    counter += 1
        return counter

    '''Get the number of time a consonant comes after a 0-9 digit (2d) in the URL String'''
    def digit_to_cons_seq(self):
        counter, vows = 0, self._get_vows()
        for i in range(1, len(self.url)):
            if self.url[i].isalpha():
                if self.url[i-1].isdigit() and self.url[i] not in vows:
                    counter += 1
        return counter

    '''Get the number of time a 0-9 digit comes after a vowel (a2) in the URL String'''
    def vows_to_digit_seq(self):
        counter, vows = 0, self._get_vows()
        for i in range(1, len(self.url)):
            if self.url[i].isalpha():
                if self.url[i - 1] in vows and self.url[i].isdigit():
                    counter += 1
        return counter

    '''Get the number of time a vowel comes after a 0-9 digit(2a) in the URL String'''
    def digit_to_vows_seq(self):
        counter, vows = 0, self._get_vows()
        for i in range(1, len(self.url)):
            if self.url[i].isalpha():
                if self.url[i - 1].isdigit() and self.url[i] in vows:
                    counter += 1
        return counter

    '''Get the number of time a punctuation comes after a vowel (a-) in the URL String'''
    def vows_to_punc_seq(self):
        counter, vows = 0, self._get_vows()
        for i in range(1, len(self.url)):
            if self.url[i].isalpha():
                if self.url[i - 1] in vows and self.url[i] in self._get_punctuations():
                    counter += 1
        return counter

    '''Get the number of time a vowel comes after a punctuation (-a) in the URL String'''
    def punc_to_vows_seq(self):
        counter, vows = 0, self._get_vows()
        for i in range(1, len(self.url)):
            if self.url[i].isalpha():
                if self.url[i - 1] in self._get_punctuations() and self.url[i] in vows:
                    counter += 1
        return counter

    '''Get the number of time a punctuation comes after a consonant (d-) in the URL String'''
    def cons_to_punc_seq(self):
        counter, vows = 0, self._get_vows()
        for i in range(1, len(self.url)):
            if self.url[i].isalpha():
                if self.url[i - 1] not in vows and self.url[i] in self._get_punctuations():
                    counter += 1
        return counter

    '''Get the number of time a consonant comes after a punctuation (#d) in the URL String'''
    def punc_to_cons_seq(self):
        counter, vows = 0, self._get_vows()
        for i in range(1, len(self.url)):
            if self.url[i].isalpha():
                if self.url[i - 1] in self._get_punctuations() and self.url[i] not in vows:
                    counter += 1
        return counter
    ###############vows & cons FEATURES #####################


    '''Run Lexical Feature Extractor'''
    def run(self):
        pool = ThreadPool(processes=12)
        pas = [

            pool.apply_async(self.cons_to_cons_seq),
            pool.apply_async(self.cons_to_digit_seq),
            pool.apply_async(self.cons_to_punc_seq),
            pool.apply_async(self.cons_to_vows_seq),
            pool.apply_async(self.digit_to_cons_seq),
            pool.apply_async(self.digit_to_vows_seq),
            pool.apply_async(self.punc_to_cons_seq),
            pool.apply_async(self.punc_to_vows_seq),
            pool.apply_async(self.vows_to_cons_seq),
            pool.apply_async(self.vows_to_digit_seq),
            pool.apply_async(self.vows_to_punc_seq),
            pool.apply_async(self.vows_to_vows_seq)
        ]
        results = [i.get() for i in pas]
        pool.terminate()
        return results
