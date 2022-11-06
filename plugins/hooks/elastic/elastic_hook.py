from airflow.plugins_manager import AirflowPlugin
from airflow.hooks.base import BaseHook

from elasticsearch import Elasticsearch

# Custom Hook

# Create class inherit from BaseHook
class ElasticHook(BaseHook):
    def __init__(self, conn_id="elastic_default", *args, **kwargs):
        # get connection
        super().__init__(*args, **kwargs)
        # id that creat in connection tab
        conn = self.get_connection(conn_id)

        conn_config = {}
        # can has multiple host
        hosts = []

        # if have a host, port, login
        if conn.host:
            hosts = conn.host.split(",")
        if conn.port:
            conn_config["port"] = int(conn.port)
        if conn.login:
            conn_config["http_auth"] = (conn.login, conn.password)

        self.es = Elasticsearch(hosts, **conn_config)
        self.index = conn.schema

    def info(self):
        return self.es.info()

    def set_index(self, index):
        self.index = index

    def add_doc(self, index, doc_type, doc):
        self.set_index(index)
        res = self.es.index(index=index, doc_type=doc_type, doc=doc)
        return res


# Register plugin to airflow
class AirflowElasticPlugin(AirflowPlugin):
    name = "elastic"
    # add hooks
    hook = [ElasticHook]


# After add plugin -> restart docker
