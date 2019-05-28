#!/usr/bin/python
#coding:utf-8

import os,sys,json,io

def main():
    path = sys.path[0]
    dsymPath = os.path.join(path,"Cyt-BabyHealth.app.dSYM")
    arr = os.popen("dwarfdump --uuid %s"%dsymPath).readlines()
    dsymuuid = arr[1]
    end = dsymuuid.find(" (arm64")
    dsymuuid = dsymuuid[6:end]
    print("DSYM_UUID=", dsymuuid)
    print("arr=", arr)

    crashPath = ""
    symbolicatecrash = ""
    for f in os.listdir(path):
        if f.find("symbolicatecrash")!=-1:
            symbolicatecrash = os.path.join(path,f)
        if f.find(".crash")!= -1:
            crashPath = os.path.join(path,f)
            with io.open(crashPath, "r", encoding="utf-8") as f_w:
                lines = f_w.read()
                start = lines.find('uuid":"')
                end = lines.find('","adam_id')
                uuid = lines[start+7:end]
                print("crash_UUID=",uuid)
            break
    if dsymuuid.lower()==uuid.lower():
        #export="export DEVELOPER_DIR=\"/Applications/Xcode.app/Contents/Developer\""
        #os.system("%s"%export)
        print("UUID匹配 开始解析：")
        logPath = os.path.join(path,"result.log")
        os.system("%s %s Cyt-BabyHealth.app.dSYM/ > %s"%(symbolicatecrash,crashPath,logPath))
        return True
    else:
        print("uuid不匹配")
        return False

main()

