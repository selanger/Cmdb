from selenium import webdriver
import os
from Cmdb.settings import BASE_DIR
from sdk.requestFunc import RequestTask


class JieTu:
    def __init__(self, params):
        """

            params = {
                "ip_list": [
                    {"ip":ip,"ports":ports},
                    {}
                ],
                "order_no": order_no
            }

        :param params:
        """
        self.params = params
        self.ip_list = params.get("ip_list")
        self.order_no = params.get("order_no")
        print(params)
        # 创建chrome参数对象
        opt = webdriver.ChromeOptions()

        # 把chrome设置成无界面模式，不论windows还是linux都可以，自动适配对应参数
        opt.set_headless()

        # 创建chrome无界面对象，并指定 chrome 驱动地址
        self.driver = webdriver.Chrome(executable_path="./chromedriver", options=opt)

        # 设置窗口大小
        self.driver.set_window_size(1920, 1080)

        # # 最大化窗口
        # driver.maximize_window()

    def run(self):
        ## 创建目录
        result = {
            "order_no":self.order_no,
            "info":[
                # {
                #     "ip":"",
                #     "port":"",
                #     "imagename":""
                # }
            ]
        }


        path = os.path.join(BASE_DIR, 'static', self.order_no)
        os.mkdir(path)
        data = self.params.get("ip_list")
        for one in data:
            for port in one["ports"]:
                url = "http://" + data.get("ip") + ":" + port
                # 发送请求
                self.driver.get(url)

                # 进行页面截屏
                image_name = os.path.join(path, "%s_%s.png" % (data.get("ip"), port))
                self.driver.save_screenshot(image_name)
                result["info"].append(dict(ip=data.get("ip"),port=port,imagename=image_name))
        url = "resources/task_jietu_result/"
        import json
        response_data = json.dumps(result)
        rt = RequestTask(url, response_data)
        rt.runpost()

        return response_data