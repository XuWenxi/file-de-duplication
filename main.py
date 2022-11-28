import os
import hashlib

class files:
    hash_value = 0
    def __init__(self, path, hashsum):
        self.FilePath = path
        if os.path.isdir(path) == False and hashsum == 0:
            # 计算哈希值
            self.CalcFileSha256()
            print(os.path.basename(path), "\t\t", self.hash_value)
            print(path, " ", self.hash_value, file=fp)
        else:
            self.hash_value = hashsum
            print(os.path.basename(path), "\t\t", self.hash_value)
        
    def CalcFileSha256(self):
        with open(self.FilePath, "rb") as file:
            sha256obj = hashlib.sha256()
            sha256obj.update(file.read())
            self.hash_value = sha256obj.hexdigest()
            return 0

def GetFilesList(MotherDirPath):
    FilesList = []
    for dirpath, dirnames, filenames in os.walk(MotherDirPath):
        for filename in filenames:
            FilesList.append(os.path.join(dirpath, filename))
    return FilesList


Files = []
sha256sums = []
Method = input("工作模式：")
if Method == "1":
    TablePath = input("索引表地址")
    fs = open(TablePath, 'r', encoding="utf-8")
    lines = fs.readlines()
    for line in lines:
        a = files(line[:-66], line[-65:-2])
        Files.append(a)
        sha256sums.append(a.hash_value)

elif Method == "2":
    Dir = input("文件目目录：")
    print("将生成索引表至", Dir, ".txt")
    fp = open(Dir+".txt", "a", encoding="utf-8")
    List = GetFilesList(Dir)
    for file in List:
        a = files(file, 0)
        Files.append(a)
        sha256sums.append(a.hash_value)
else:
    print("输入错误")

if Method == "2":
    fp.close()
setList = set(sha256sums)
if len(sha256sums) != len(setList):
    for EachItem in setList:
        # 统计出现次数
        ReCount = 0
        for EachItem_L in sha256sums:
            if EachItem == EachItem_L:
                ReCount += 1
            if ReCount >= 2:
                # 重复的删掉
                print(sha256sums.index(EachItem), Files[sha256sums.index(EachItem)].FilePath, ": ", ReCount, EachItem)
                
                try:
                    sha256sums.remove(EachItem)
                    os.remove(Files[sha256sums.index(EachItem)].FilePath)
                except IOError:
                    pass
else:
    print("无重复")

print("结束")