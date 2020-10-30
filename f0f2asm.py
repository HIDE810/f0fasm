import requests, json, sys ,os

def call_hextoarm_api(code):
    url = "https://armconverter.com/api/convert"
    request_body = {
        "hex" : code,
        "offset" : '',
        "arch" : ["armbe"]
    }
    request_head = {
        "Host" : "armconverter.com",
        "Content-Length": str(len(json.dumps(request_body))),
        "Content-Type" : "application/json",
        "Accept" : "*/*",
        "Accept-Encofing" : "gzip, deflate, br",
        "Connection" : "keep-alive"
    }
    session = requests.Session()
    r = session.post(url=url, headers=request_head, json=request_body)
    return json.loads(r.text)["asm"]["armbe"]

if __name__ == "__main__":
    path= os.path.dirname(os.path.abspath(sys.argv[1]))
    file = path + "/" + os.path.basename(sys.argv[1])
    with open(file) as f:
        code = ''
        for line in f:
            if f"{line}".split()[0] != "F0F00000":
                code += f"{line}"
        res = call_hextoarm_api(code.replace(' ', '\n'))
        if res[0] != True: # IF HEX CODE IS WRONG
            print("ARM CODE ERROR!")
            exit(1)
        else:
            with open(path + "/" + os.path.splitext(os.path.basename(file))[0] + "_asm.txt", mode='w') as fw:
                codes = res[1].split("\n")
                for code in codes:
                    fw.write(code + "\n")