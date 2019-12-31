import requests
from urllib.parse import urljoin
from Cmdb.settings import server_url


class RequestTask:
    def __init__(self, url, params, server=None):
        """

        :param url: 请求路由
        :param params:  请求参数
        :param server:  请求主机服务
        """
        self.params = params
        if server:
            self.server = server
        else:
            self.server = server_url

        self.url = url
        ## 拼接请求的url
        self.path_url = urljoin(self.server, self.url)

    def runget(self):
        ## 发送get请求

        requests.get(self.path_url, self.params)


    def runpost(self):
        requests.post(self.path_url,data=self.params)
