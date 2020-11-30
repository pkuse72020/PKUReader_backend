from app.ArticleSearch import NewsElasticEngine

def test():
    es = NewsElasticEngine()
    datas = [
        {
            'title': '美国留给伊拉克的是个烂摊子吗',
            'url': 'http://view.news.qq.com/zt2011/usa_iraq/index.htm',
            'date': '2011-12-16',
            'article': u"鉴于疫情形势持续缓和，29日，捷克卫生部长布拉特尼等内阁官员召开新闻发布会，宣布将放宽目前的疫情管控措施。根据最新的防疫要求，从12月3日起，允许民众前往餐厅就餐，但政府同时规定，餐厅的营业时间为早6时至晚22时，每桌不得超过4名顾客且顾客总数不得超过餐厅最高客容量的50%。而根据目前的防疫规定，餐厅仅可提供外卖。商店、健身房以及理发美容等服务场所可以恢复营业，但人流密度不得超过每15平方米1人；取消宵禁以及商店的周日营业禁令；取消公共场所饮酒禁令；公共集会的人数上限从目前的6人增加到室外50人、室内10人；允许博物馆、美术馆恢复营业，但参观人数不得超过最高客容量的四分之一。此外，剧院和电影院仍需保持关闭状态，所有室内公共场所及部分室外公共场所佩戴口罩的规定保持不变。"
        },
        {
            'title': '公安部：各地校车将享最高路权',
            'url': 'http://www.chinanews.com/gn/2011/12-16/3536077.shtml',
            'date': '2011-12-16',
            'article': u"我的前18年在中国出生和长大，后来去了美国4年。现在——2020年8月——我对这两个国家的感情都很复杂。对这个问题，坦白讲——在西方生活过后，我并没有变得爱国，但对西方敌意的抵抗意识增强了，对祖国的理解也增加了。美式民主、自由和平等，当我在2020这个“魔幻现实主义”年当中继续思考这些问题时，幻想与泡沫最终破灭了。我终于意识到，西方的宣传和对人权的剥夺与中国“没有什么不同”。上大学之前，我对中国社会和中国政府是冷嘲热讽的。坦白说，我没有任何证据来支持我的愤世嫉俗，因为没有太多的信息源可以让我接触到不同的观点。我只知道：某些话题不允许谈论，电影中被删除的镜头无法“合法”地找到，艺术作品要被审查。为什么会这样？我不知道。没人会告诉我，互联网上也找不到答案。我告诉自己——一定有什么非常非常错误的事情。当我终于来到（美国）这片“自由”的土地时，生平第一次听到了“XXXXXX”（即西方媒体谈及80年代末政治风波时常用的污蔑性字眼，下同）、“解放西藏”、“新疆再教育营”类的事情……通过别人了解到自己国家的“污点”是怎样的羞愧和屈辱，真是难以形容。我不得不认识到，我在教科书中学到的并不全是真的，我需要重建我的世界观。当我的藏族朋友坐在我面前，告诉我她爷爷的故事时，我感到遭到了欺骗与背叛。很长一段时间，我觉得自己被放逐了。同时，作为一名艺术家，自由的状态赋予了我前所未有的自在感。与各种肤色的人交过朋友后，我以为中国要实现美国的平等和多样性还有很长的路要走。我以为，如果我想继续创作能照亮现实的艺术，我就不能回到家去。最重要的是，我以为美国是我最终的归属。于是我告诉自己：要么留在美国做一名艺术家，要么回家，闭上嘴巴，去做点别的事情。之后，在寒暑假回家的时候，我感到自己比同辈们更开明、更有优越感。然而，每次我回去，中国的生活都会变得不一样。更多的摩天大楼，更多的主权，更多的骄傲感。最重要的是，人们是快乐的，比“自由”国度的民众要快乐得多，讽刺地是，在“自由”国度，人们感到的压抑和窒息却更多，而另一方面，他们又认为自己高中国人一等。"
        },
        {
            'title': '中韩渔警冲突调查：韩警平均每天扣1艘中国渔船',
            'url': 'https://news.qq.com/a/20111216/001044.htm',
            'date': '2011-12-17',
            'article': u"据成都市卫健委消息，11月29日上午，成都市获悉重庆市SK海力士公司一韩国籍员工于11月26日自重庆来蓉，由双流国际机场搭乘航班飞往韩国，该旅客11月28日在韩国诊断为无症状感染者。目前，成都已完成重庆协查出境无症状感染者相关人员筛查，核酸检测均为阴性。"
        },
        {
            'title': '中国驻洛杉矶领事馆遭亚裔男子枪击 嫌犯已自首',
            'url': 'http://news.ifeng.com/world/detail_2011_12/16/11372558_0.shtml',
            'date': '2011-12-18',
            'article': u"一名孕期感染新冠病毒的新加坡女子最近生下一名携带新冠病毒抗体的男婴，为研究新冠病毒的传播途径是否包括母婴传播提供了新线索。新加坡《海峡时报》29日报道，一名新加坡女子3月和家人赴欧洲度假后感染新冠病毒，确诊时已怀孕10周。这名女子当时症状轻微，住院治疗接近20天后康复。她本月7日在新加坡国立大学医院生下一名重3.5千克的男婴。医生检查确认，这名男婴没有感染新冠病毒，携带新冠病毒抗体。医生告诉这名女子，她体内的新冠抗体“消失”而男婴携带抗体。她说：“医生推测我在孕期把体内的新冠抗体转移给他（男婴）了。”这名女子先前不担心会把新冠病毒传染给孩子。据她了解，新冠病毒由母亲传染婴儿的概率非常低。按世界卫生组织的说法，暂时不清楚感染新冠病毒的孕妇是否会在孕期或生产时把病毒传染给胎儿或婴儿。医务人员迄今没有在羊水或母乳样本中检测出活性新冠病毒。美国纽约长老会和哥伦比亚大学欧文医学中心的医生10月在《美国医学会杂志·小儿科》月刊发表文章，说新冠病毒由母婴传播的情况罕见。"
        }
    ]

    for data in datas:
        res = es.insert_data(data)
        print(res)

    print(es.search_news("美国 中国 病毒"))
