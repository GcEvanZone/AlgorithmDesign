# 导入regex模块
import re

# 打开文件路径
filepath = "ClangAnalysis.cpp"
# filepath = "Prime.c"
# filepath = "Test.c"
file = open(filepath, "r+")
# 按行读取内容
contents = file.readlines()
# 去除每行左右两边多余的空格和tab
contents = [i.strip() for i in contents]
# 收集空行和注释行以外的行
misc = []
# 记录总行数
totalline = len(contents)
# macro记录”#“开头的语句
macro = 0
# function_name记录所有函数名称
function_name = []
# funcs_lines记录所有函数的行数
funcs_lines = []
# blankline记录空行数量
blankline = 0
# commentsline记录注释行数量
commentsline = 0

i = 0
while i < len(contents):
    # 记录空行
    if contents[i] == '':
        blankline += 1
        i += 1
        continue
    # 记录macro
    elif contents[i][0] == '#':
        macro += 1
        i += 1
        continue
    # 记录多行注释
    elif contents[i][:2] == "/*":
        if "*/" in contents[i]:
            commentsline += 1
            i += 1
            continue
        else:
            commentsline += 1
            i += 1
            while "*/" not in contents[i]:
                commentsline += 1
                i += 1
            commentsline += 1
            i += 1
            continue
    # 记录单行注释
    elif contents[i][:2] == "//":
        commentsline += 1
        i += 1
        continue
    # 收集杂项
    else:
        if contents[i].find("//") > -1:
            idx = contents[i].find("//")
            contents[i] = contents[i].replace(contents[i][idx:], '')
        misc.append(contents[i]) 
        i += 1
        continue

# 用list类型充当栈数据结构，新建一个栈
stack = []

# 复制一份字符串类型的杂项，以便使用正则表达式
misc_str = "".join(misc)

# 正则表达式找出所有函数声明和函数实现
functions = re.findall(r"\w+\**\s+\w+\s*\(.*?\)", misc_str)
for i in functions:
    # 区分主函数
    if "main" in i:
        pass
    # 区分“else if()”形式
    elif "else" in i and "if" in i:
        continue
    # 区分'ifstream in(name)'形式
    elif "ifstream" in i or "ofstream" in i:
        continue
    # 区分函数声明
    elif "string" in i and '("' in i and '")' in i:
        continue
    elif re.match(r"\w+\**\s+\w+\s*\(\)", i):
        continue
    function_name.append(i)

print(function_name)

# 记录所有函数名称和其返回值类型
for i in range(len(function_name)):
    function_name[i] = function_name[i].replace('(',' ').replace(')',' ').replace(',',' ').split(' ')[:2]

funcline = 0

# 按行遍历C代码内容
while i < len(contents):
    print("正在扫描第{}项".format(i))
    # 对找到的所有函数名称进行遍历
    for j in range(len(function_name)):
        # 如果这个C代码的当前行中包含了函数名称和函数返回值类型，则可以定位为函数声明或者实现
        if function_name[j][0] in contents[i] and function_name[j][1] in contents[i]:
            print("匹配到函数名了！")
            # 如果函数没有“{}”，只有“;”，则判定为函数声明
            if ";" in contents[i]:
                print("很不幸，这只是个声明=。=")
                continue
            # 否则即为函数实现
            else:
                print("匹配到函数本体啦！")
                # 找到函数体最外层的“{”，将其入栈
                # 每入栈一次即意味着函数行数增加一行
                while "{" not in contents[i]:
                    i += 1
                    funcline += 1
                    continue
                funcline += 1
                stack.append(contents[i])
                i += 1
                # 循环至栈的长度为0，就意味着最外层的"{}"匹配完成
                while len(stack) != 0:
                    # 遇到"{"就入栈，遇到"}就出栈"
                    if "{" in contents[i]:
                        stack.append(contents[i])
                    if "}" in contents[i]:
                        stack.pop()
                    funcline += 1
                    i += 1
                print("名称：{}函数\t行数：{}行".format(function_name[j][1], funcline))
                # 记录当前函数的行数
                funcs_lines.append(funcline)
                # 为下一次记录而清零
                funcline = 0
    i += 1
# 分割线
print("="*60) 

print("宏和预处理的行数：{}".format(macro))
print("空行的行数：{}".format(blankline))
print("注释的行数：{}".format(commentsline))


for i in range(len(function_name)):
    print("名称：{} {}函数\t行数：{}行".format(function_name[i][0], function_name[i][1], funcs_lines[i]))
# print(funcline_average)

# 计算各项指标
funcline_average = sum(funcs_lines) / len(funcs_lines)
comments_rate = commentsline / totalline * 100
blanklines_rate = blankline /totalline * 100

judge = [funcline_average, comments_rate, blanklines_rate]

judge_name = ["函数代码平均行数", "注释行占总行数的比率", "空行占总行数的比率"]

style = [
    [(10, 15), (8, 9, 15, 20), (5, 7, 21, 24), (5, 24)],
    [(15, 25), (10, 14, 26, 30), (5, 9, 31, 35), (5, 35)],
    [(15, 25), (10, 14, 26, 30), (5, 9, 31, 35), (5, 35)]
]

print("="*60)

print("测评指标\t数值(后两项为%)\t等级")
for i in range(len(style)):
    print("{}\t{}".format(judge_name[i], judge[i]), end="\t")
    # for j in range(len(style[i])):
    if  style[i][0][0] <= judge[i] <= style[i][0][1]:
        print("A")
    elif style[i][1][0] <= judge[i] <= style[i][1][1] or style[i][1][2] <= judge[i] <= style[i][1][3]:
        print("B")
    elif style[i][2][0] <= judge[i] <= style[i][2][1] or style[i][2][2] <= judge[i] <= style[i][2][3]:
        print("C")
    else:
        print("D")

file.close()