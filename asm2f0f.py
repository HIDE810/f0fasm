import requests, json, sys ,os

def call_armtohex_api(code):
    url = "https://armconverter.com/api/convert"
    request_body = {
        "asm" : code,
        "offset" : '',
        "arch" : ["arm"]
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
    return json.loads(r.text)["hex"]["arm"]

if __name__ == "__main__":
    path= os.path.dirname(os.path.abspath(sys.argv[1]))
    file = path + "/" + os.path.basename(sys.argv[1])
    with open(file) as f:
        code = ''
        for line in f:
            code += f"{line}"
        res = call_armtohex_api(code)
        if res[0] != True: # IF ARM CODE IS WRONG
            print("ARM CODE ERROR!")
            exit(1)
        else:
            with open(path + "/" + os.path.splitext(os.path.basename(file))[0] + "_f0f.txt", mode='w') as fw:
                code = res[1].split("\n")
                fw.write("F0F00000 %08X\n" % (len(code) * 4))
                for i in range(len(code)):
                    fw.write(bytes.fromhex(code[i])[::-1].hex().upper() + (" " if (i & 1 == 0) else "\n"))
                if (i & 1 == 0):
                    fw.write("00000000\n")