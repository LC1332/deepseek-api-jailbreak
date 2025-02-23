# 对各个云服务商DeepSeek模型的测试和越狱测试

<details>
    <summary> 王子谦, 李鲁鲁</summary>
    项目由李鲁鲁发起，代码部分主要由王子谦完成。

    这个项目主要是给目前在上海交大的王子谦同学练手
</details>

# 动机

在2025年2月，XX平台介入Deepseek的新闻不断在各大社媒刷屏,各家云服务商纷纷开始提供DeepSeek，包括R1和V3模型的API。我们了解到其中一些服务使用了蒸馏后的千问小模型。我们想在DeepSeek的原本报告中，抽样一个快速子集，来估计各家DeepSeek API和report的差异。

同时，qualys的报告指出，DeepSeek模型对于越狱的防御还不够完整。项目希望对此也进行探究

# 项目目标

- 根据DeepSeek-V3和R1的报告，抽样建立一个subset快速测集，初步估计各家API的反应速度和在几个benchmark上的抽样准确率
- 根据qualys的报告，抽样建立一个越狱测试集，测试各家API的越狱概率
- 编写一个后端，支持使用任意一家的API，将用户的query套用某个越狱模板进行测试。

# jailbreak通过率测试

## 测试方法
选取M个攻击目标query prompt和N个transfer的meta-prompt。

从MN组合中，抽样出KN个(prompt, meta-prompt) , ( K << M, K = 2 )

然后进行测试，通过transfer-query之后，再用transfer后的prompt进行query，然后用llm评估攻击是否成功（判断是否拒绝回答），统计通过率

## jailbreak测试结果
### 实验1
测试数据集：请查看./input/

恶意prompt数量：10

测试详细信息（模型给出的回答&越狱过程）：请查看./jailbreak_result/

| Model                         | Jailbreak Rate |
|-------------------------------|---------------|
| GLM-4-AIR                     | 90%           |
| 火山方舟DeepSeek-R1            | 90%           |
| 火山方舟DeepSeek-V3            | 50%           |
| 硅基流动DeepSeek-V3            | 80%           |

### 实验2

测试数据集：请查看./input/

恶意prompt数量：30

测试详细信息（模型给出的回答&越狱过程）：请查看./jailbreak_result/

（由于硅基流动响应过慢没有测试）

| Model                         | Jailbreak Rate |
|-------------------------------|---------------|
| GLM-4-AIR                     | 70%           |
| 火山方舟DeepSeek-R1            | 73.33%           |
| 火山方舟DeepSeek-V3            | 53.33%           |

### 实验3
测试数据集：请查看./input/

恶意prompt数量：30

测试详细信息（模型给出的回答&越狱过程）：请查看./jailbreak_result/

（由于硅基流动响应过慢没有测试）

| Model                         | Jailbreak Rate |
|-------------------------------|---------------|
| GLM-4-AIR                     | 70%           |
| 火山方舟DeepSeek-R1            | 73.33%           |
| 火山方舟DeepSeek-V3            | 53.33%           |

### 实验4

测试数据集：请查看./input/

恶意prompt数量：60

| Model                         | Jailbreak Rate |
|-------------------------------|---------------|
| GLM-4-AIR                     | 68.33%           |
| 火山方舟DeepSeek-R1            | 76.67%           |
| 火山方舟DeepSeek-V3            | 56.67%           |
| 阿里云DeepSeek-R1             | 78.83%         |
| 阿里云DeepSeek-V3            | 58.33%   |

# Benchmark subset测试

从deepseek原本报告中，找一些确定性评价的题目子集，抽样一个较小的subset，对各家的api进行评估。


# 参考资料

DeepSeek的攻击报告
https://blog.qualys.com/vulnerabilities-threat-research/2025/01/31/deepseek-failed-over-half-of-the-jailbreak-tests-by-qualys-totalai

---

## Paper Reading TODO

- 查阅lulu/0214_jailbreak_paper_reading.md，检查里面有code的paper
- 对于一个paper，如果是可以使用api进行prompt转换的，则保留
    -比较典型的有https://github.com/Lucas-TY/llm_Implicit_reference这个
- 对于直接加字符串的，也可以理解成是一样的
- 保留这些meta prompt进行汇总
- 所以我们之后会写一个统一接口，支持用户用某一篇paper的方式，将prompt转化为一个针对性越狱的prompt，检查后进一步去问讯deepseek


## 不要浪费key

有query就存下来，记得query的messages是啥 response是啥， 用了啥source的啥模型

## 恶意字符保存

用base64加密保存

