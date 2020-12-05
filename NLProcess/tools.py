import jieba
import jieba.analyse

from lxml import etree

# 词性标注用
# import jieba.posseg as pseg


REPLACE_DICT = {'\n':' ','\u3000':' '}
TRANSTABLE = str.maketrans(REPLACE_DICT)
ALLOWPOS = ('n','nr','nz','PER','f','ns','LOC','nt','s','ORG','nw','eng')
FUNCS = {'textrank':jieba.analyse.textrank,'tfidf':jieba.analyse.extract_tags}

def html2txt(html):
    response = etree.HTML(text=html)
    out_txt = response.xpath('string(.)')
    out_txt = out_txt.translate(TRANSTABLE)
    return out_txt

def tokenizer(cleaned_txt):
    jieba_out = jieba.lcut(cleaned_txt)
    jieba_out = [e for e in jieba_out if e not in [' ','']]
    return jieba_out

def getEachPOS(cleaned_txt):
    import jieba.posseg as pseg
    words = pseg.cut(cleaned_txt)
    words = list(words)
    words = [list(e) for e in words if list(e)[0] not in [' ',''] and list(e)[1] not in ['x']]
    return words

def getKeywords(cleaned_txt,method = 'textrank'):
    if method not in FUNCS:
        method = 'textrank'
    keywords = FUNCS[method](cleaned_txt, allowPOS = ALLOWPOS, withFlag=False)
    return keywords

if __name__ == "__main__":
    import feedparser
    url = 'https://myrsshub-git-master.zkcpku.vercel.app/cctv/tech'
    feed = feedparser.parse(url)
    html = feed.entries[0]['summary']
    # test html2txt
    cleaned_txt = html2txt(html)
    print(cleaned_txt)

    # test tokenizer
    print(tokenizer(cleaned_txt))

    # test keywords
    print(getKeywords(cleaned_txt))

    # test getPOS
    print(getEachPOS(cleaned_txt))
