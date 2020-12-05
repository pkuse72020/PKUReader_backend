from app.NLP import NLP

from flask import request, session, jsonify

from NLProcess.tools import html2txt, tokenizer, getEachPOS, getKeywords

@NLP.route('/')
def hello_world():
    return "hello nlp!"

# 注册
# 传入参数格式{"username":...,"password":...}
# 成功时返回参数格式{"state":"success","UserId":...}
# 失败时返回参数格式{"state":"failed","description":...}
@NLP.route('/tokenizer', methods=["POST", "GET"])
def tokenizer_func():
    if request.method == "GET":
        cleaned_txt = request.args.get("txt")
    else:
        cleaned_txt = request.form.get("txt")
    try:
        cleaned_txt = html2txt(cleaned_txt)
        words_list = tokenizer(cleaned_txt)

        return {"state":"success", "rst":words_list}
    except Exception as e:
        return {"state":"failed", "rst":str(e)}


@NLP.route('/getKeywords', methods=["POST", "GET"])
def getKeywords_func():
    if request.method == "GET":
        cleaned_txt = request.args.get("txt")
    else:
        cleaned_txt = request.form.get("txt")
    try:
        cleaned_txt = html2txt(cleaned_txt)
        words_list = getKeywords(cleaned_txt)

        return {"state":"success", "rst":words_list}
    except Exception as e:
        return {"state":"failed", "rst":str(e)}


