#### 文件说明
1. ntru -> 实现代码:
    1. ntru/Poly.py -> 加解密用到的多项式
    2. ntru/KeyGen.py -> 密钥生成
    3. ntru/Manager.py -> 加解密
2. test -> 测试代码:
3. doc  -> 说明文档

#### 其他
1. 该实现不保证正确性，仅为了理解 ntru 算法，标准实现见 https://github.com/NTRUOpenSourceProject/NTRUEncrypt
2. 省略了对原始信息进行预处理的过程