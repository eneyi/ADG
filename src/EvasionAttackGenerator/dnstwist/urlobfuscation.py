# This is a sample Python script.
from random import choice, randrange, seed
from requests import head
import dns.resolver
from string import ascii_letters as letters
from string import digits
import wordninja
import faker.providers.internet.Provider as fake
from urllib.parse import urlparse
seed(100)


class ADGHelpers(object):
    def __init__(self):
        self.description = 'blah'

    '''Retruns a Random English Vowel'''
    def _get_random_vowel(self, text=None):
        vowels = 'aeiou'
        if text:
            text_vowels = [i for i in text if i in vowels]
            return choice(text_vowels)
        return choice(vowels)

    '''Return a Random English Consonant'''
    def _get_random_cons(self, text=None):
        consonants = "".join([i for i in letters if i not in 'aeiouAEIOU'])
        if text:
            text_cons = [i for i in text if i in consonants]
            return choice(text_cons)
        return consonants + consonants.upper()

    '''Return a Random English Punctuation'''
    def _get_random_punctuation(self):
        return choice('_,-')

    '''Return a random digit between 0 and 9'''
    def _get_random_digit(self):
        return choice(digits)

    '''Return a random index between 0 and the length of a given string'''
    def _get_random_index(self, string):
        start, end = 1, len(string)
        indexes = [i for i in range(start, end) if string[i].isalpha() or string[i].isdigit()]
        return choice(indexes)


'''ADGDNS Returns DNS Records of a given URL String'''
class ADGDNS(object):
    def __init__(self, url):
        self.description = 'blah'
        self.url = url

    def islive(self):
        r = head(self.url).status_code
        return r == 200

    def _get_A_records(self):
        arecords = dns.resolver.query(self.url, 'A')
        if len(arecords) > 0:
            return {"arecords": [arecord.to_text() for arecord in arecords]}
        else:
            return None

    def _get_CNAME_records(self):
        crecords = dns.resolver.query(self.url, 'CNAME')
        if len(crecords) > 0:
            return {"crecords": [crecord.target for crecord in crecords]}
        else:
            return 0

    def _get_MX_records(self):
        mxrecords = dns.resolver.query(self.url, 'MX')
        if len(mxrecords):
            return {"mxrecords": [mxrecord.exchange.text() for mxrecord in mxrecords]}
        else:
            return 0

    def _get_ip(self):
        return 0


class PathAdversary(ADGHelpers):
    def __init__(self, url):
        self.url = url
        self.component = urlparse(self.url).path
        super(PathAdversary, self).__init__()

    def pathdm(self):
        words = wordninja.split(self.component)
        return f"{self.component}/{words[0]}"

    def pathexe(self):
        words = wordninja.split(self.component)
        return f"{self.component}/{words[0]}.exe"

    def RunPathAdversary(self):
        call = choice((self.pathdm, self.pathexe))
        return call


class DomainAdversary(ADGHelpers):
    def __init__(self, url):
        self.url = url
        self.component = urlparse(self.url).netloc
        super(DomainAdversary, self).__init__()

    '''Insert "char" at position "index"'''
    def insertion(self):
        v, c = self._get_random_vowel(), self._get_random_cons()
        index = self._get_random_index(self.component)
        new = self.component[:index] + choice((v, c)) + self.component[index:]
        return new

    def bitsquatting(self):
        return 0

    def homoglyph(self):
        homoglyphs = {"o":"0", "l":"1", "vv":"ww", "rn":"m", "cl":"d", "1":"l", "w":"vv", "m":"rn", "d":"cl"}
        choice1 = choice(homoglyphs.keys())
        return self.component.replace(choice1, homoglyphs[choice1])

    def omissison(self):
        r = len(self.component)
        while r == len(self.component):
            r = randrange(self.component)
        return f"{self.component[:r]}{self.component[r+1:]}"

    def subdomian(self):
        random_index = self._get_random_index(self.component)
        k, j = self.component[:random_index], self.component[random_index:]
        return f"{k}.{j}"

    def hyphenation(self):
        random_index = self._get_random_index(self.component)
        k, j = self.component[:random_index], self.component[random_index:]
        return f"{k}-{j}"

    '''Replace a random character at position "index" with "char"'''
    def charswap(self):
        rep = choice(["v", "c"])
        if rep == "c":
            h = self.component.replace(rep, self._get_random_consonant(self.component))
        else:
            h = self.component.replace(rep, self._get_random_vowel(self.component))
        return h

    def repitition(self):
        random_index = self._get_random_index(self.component)
        k, j = self.component[:random_index], self.component[random_index:]
        return f"{k}{self.component[random_index]}{j}"

    def transpose(self):
        random_index = self._get_random_index(self.component)
        middle = self.component[random_index]
        swap = self.component[random_index-1]
        return f"{self.component[:random_index-2]}{middle}{swap}{self.component[random_index:]}"

    def wordhyphenation(self):
        words = wordninja.split(self.component)
        return "-".join(words)

    def wordrepition(self):
        words = wordninja.split(self.component)
        choice1 = f"{words[0]}-{self.component}"
        choice2 = f"{self.component}-{words[-1]}"
        return choice([choice1, choice2])

    def wordswap(self):
        words = wordninja.split(self.component)
        return f"{words[-1]}{words[0]}"

    def word_subdomain(self):
        fake_page = fake.uri_page()
        return f"{self.component}.{fake_page}"

    def tldreplace(self):
        fake_tld = fake.tld()
        tld = self.component.split(".")[-1]
        return self.component.replace(f".{tld}", f".{fake_tld}")

    def RunDomainAdversary(self):
        call = choice((self.addition, self.insertion, self.bitsquatting, self.homoglyph,
                       self.omissison, self.subdomian, self.hyphenation, self.charswap,
                       self.repitition, self.transpose, self.word_subdomain, self.wordswap,
                       self.wordrepition, self.wordhyphenation, self.tldreplace))()
        return call


class SimulatePhishingSites(PathAdversary, DomainAdversary):
    def __init__(self, url, iterations=10000):
        self.iterations = iterations
        self.url = url
        self.netloc = urlparse(self.url).netloc
        self.urlpath = urlparse(self.url).path
        super(SimulatePhishingSites, self).__init__(self.url)

    def get_new_url(self):
        c = choice(("path", "domain"))
        if c == "path":
            twist = self.RunPathAdversary()
            twist = self.url.replace(self.urlpath, twist)
        else:
            twist = self.RunDomainAdversary()
            twist = self.url.replace(self.netloc, twist)
        return twist

    def run_iterations(self):
        lives = []
        for i in range(0, self.iterations):
            this = self.get_new_url()
            DNSObject = ADGDNS(this)
            if DNSObject.islive():
                lives.append(this)

