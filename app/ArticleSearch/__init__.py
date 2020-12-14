from elasticsearch import Elasticsearch
import json

class NewsElasticEngine():
    def __init__(self, hosts=["49.234.217.176:9200"], index_name="news", doc_type="news"):
        self.es = Elasticsearch(hosts)
        self.hosts = hosts
        self.index_name = index_name
        self.doc_type = doc_type
        self.mapping = {
            'properties': {
                'title': {
                    'type': 'text',
                    'analyzer': 'ik_max_word',
                    'search_analyzer': 'ik_smart'
                },
                'article': {
                    'type': 'text',
                    'analyzer': 'ik_max_word',
                    'search_analyzer': 'ik_smart'
                }
            }
        }

    def rebuild_database(self, index_name, doc_type):
        self.es.indices.delete(index=index_name, ignore=[400, 404])
        self.es.indices.create(index=index_name, ignore=400)
        result = self.es.indices.put_mapping(
            index=index_name, doc_type=doc_type, body=self.mapping, include_type_name=True)
        return result

    def insert_data(self, input_data):
        res = self.es.index(index=self.index_name,
                            doc_type=self.doc_type, body=input_data)
        return res

    def search_news(self, keywords):
        dsl = {
            'query': {
                'multi_match': {
                    'query': keywords,
                    "fields": ["article", "title"]
                }
            }
        }
        result = self.es.search(index=self.index_name, doc_type=self.doc_type, body=dsl)
        return (json.dumps(result, indent=2, ensure_ascii=False))
