import nmap
# from .requestFunc import RequestTask
from sdk.requestFunc import RequestTask


class NmapSdk:
    def __init__(self, params):
        self.nm = nmap.PortScanner()
        self.params = params

    def checkOneIP(self):
        """
        探测 主机是否存活
            :param params:
            params = {ip}
        """

        ip = self.params.get("ip")
        res = self.nm.scan(ip, arguments="-sP")
        print(res)
        flag = False
        if len(res["scan"]) != 0:
            for key, values in res["scan"].get(ip).items():
                if key == 'status' and values["state"] == "up":
                    ## 主机开启状态
                    flag = True

        if not flag:
            print(flag)
            ## 如果为关闭状态发送get请求
            url = "resources/task_update_host_status/"
            params = dict(ip=ip)
            rt = RequestTask(url, params)
            rt.runget()

    def checkPort(self):
        """
        探测单个主机开放哪些端口
        :return:
        response_data = {
            "ip":ip,
            "status":"",   ## 主机状态
            "ports":[
                {
                    "port":"3306",  ## 端口
                    "state":"",   ## 状态
                    "reason":"",  ##  原因
                    "extrainfo":"",  ##  额外信息
                    "name":"",  ##  名字
                    "version":"",  ##  版本
                    "product":"",  ## 产品
                    "cpe":"",  ##  CPE
                }
            ]
        }
        """

        response_data = {
            "ip": self.params.get("ip"),
            "order_no": self.params.get("order_no"),
            "status": "",
            "ports": [
            ]
        }
        ip = self.params.get("ip")
        res = self.nm.scan(ip, arguments='-v -n -A')

        for host, result in res['scan'].items():
            if result['status']['state'] == "up":
                ## 主机开启状态
                response_data["status"] = "up"
                for port in result["tcp"]:
                    if result.get("tcp", None):
                        if result.get('tcp').get(port):
                            # print(result.get('tcp').get(port))
                            ports = {

                                "port": str(port),  ## 端口
                                "state": result['tcp'][port].get('state', ''),  ## 状态
                                "reason": result['tcp'][port].get('reason', ''),  ##  原因
                                "extrainfo": result['tcp'][port].get('extrainfo', ''),  ##  额外信息
                                "name": result['tcp'][port].get('name', ''),  ##  名字
                                "version": result['tcp'][port].get('version', ''),  ##  版本
                                "product": result['tcp'][port].get('product', ''),  ## 产品
                                "cpe": result['tcp'][port].get('cpe', ''),  ##  CPE
                                "script": result['tcp'][port].get('script', ''),  ##  脚本

                            }
                            response_data["ports"].append(ports)
            else:
                ## 主机关闭
                response_data["status"] = "down"

        url = "resources/task_scan_ports_result/"
        import json
        response_data = json.dumps(response_data)
        rt = RequestTask(url, response_data)
        rt.runpost()
        return response_data


if __name__ == '__main__':
    params = {
        "ip": "172.16.221.134",
        "order_no": "11111"
    }
    task = NmapSdk(params)
    res = task.checkPort()
    print(res)
