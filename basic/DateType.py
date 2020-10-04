# 整数
int_a = 10000000
int_b = 10_000_000
print(int_a == int_b) #True
# 十六进程
int_c = 0x1234
int_d = 0x1234_567a
print(int_c, int_d) #4660 305419898

# 浮点数
float_a = 1.23
float_b = 1.23e10
float_c = 1.23e-3
print(float_a, float_b, float_c) #1.23 12300000000.0 0.00123

# 字符串 '' 或者 "" 括起来的文本， \ 可以转义字符 \n 代表换行
str_a = 'abc124'
str_b = ".or3e_="
str_c = 'I\'m "OK"!'
print(str_a, str_b, str_c) #abc124 .or3e_= I'm "OK"!
# r'' 表示 '' 内部字符默认不转义，repr() 同理，用于变量
print(r'haha\nlala',repr(str_c)) #haha\nlala 'I\'m "OK"!'


# 布尔型
bool_a = True
bool_b = False
print(bool_a, bool_b)
print(bool_a and bool_b, bool_a or bool_b, not bool_a, bool_a ^ bool_b) #False True False True

# 空值
print(None) #None

# 字符串编码
'''
ASCII：一个字节（8bit）只支持英文字符和一些标点符号，不支持中文
Unicode：两个字节表示一个字符，非常偏僻的字符需要4字节，支持中英文，一个中文(中)或者英文字符(A)算一个字符
UTF-8：1-6个字节，英文字母1个字节，一个汉字通常3个字节，生僻字4-6个字节

计算机内存中统一使用Unicode编码，存储到硬盘或者传输时，使用UTF-8
记事本（Unicode）<---> 文件abc.txt（UTF-8）
'''
# ord()：将字符转为整数  chr()：将整数转为字符
print(ord('A'), ord('中')) #65 20013
print(chr(66), chr(20014)) #B 丮
print('\u4e2d\u6587') #中文 0xu4e2d == 20013
print(b'abc', 'abc') #b'abc' abc 前者是字节，后者是字符
print(b'abc'.decode('ascii'), b'\xe4\xb8\xad\xe6\x96\x87'.decode('utf-8')) #abc 中文
print(len(b'abc'), len('abc'), len('中文'), len(b'\xe4\xb8\xad\xe6\x96\x87')) #3 3 2 6
# 格式化输出，与上面一样，只不多写法不同
'''
占位符	替换内容
%d	     整数
%f	     浮点数
%s	     字符串
%x	     十六进制整数
'''
print('%6d--%6.3f--%6s--%x' %(123, 3.1415926, 'haha', 0x12ba)) #   123-- 3.142--  haha--12ba
