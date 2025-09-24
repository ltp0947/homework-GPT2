# homework-GPT2
注：项目文件保存在master分支中
1.Description
利用开源的中文GPT2模型在自己的数据集上进行训练。GTP2来源：https://github.com/lvfinn/chinese-GPT2-start-from-zero； 数据集：《凡人修仙传》的.txt文本； 目标：对给定的一句开头，续写十句话以上的文本

2.Modification
（1）调整数据预处理的代码
在\data文件夹下的clr_ctrl.py将input.json文件里文本进行标准化处理，但是下载的文本使用编码方式为gb2312，因此在读取文件时选择encoding='gb2312'而不是utf-8。修改后的代码保存为clr_ctrl_2.py

(2)训练代码
Problem：训练过程中在第一个epoch的训练过程中程序自动终止，并且没有error报错
检查发现，在读取训练文件后提示sequence length大于specified maximum sequence length
对此想出了3个方案：
a. 增大num_pieces，100->1000，企图让每一段训练文本更短（无效）
b. 修改build_files函数，对每个样本单独处理，而不是链接成长序列（修改方案由Deepseek提供，运行过程中电脑蓝屏，还没找到原因）
c. 增大词汇表，这样减少原数据的token数，例如将vocab_size从13317增大到50257；但是这需要相应修改tokenization  （对此方面没有太清晰的理解，还没有尝试）
