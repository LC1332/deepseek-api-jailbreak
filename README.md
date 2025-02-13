# 对各个云服务商DeepSeek模型的测试和越狱测试

<details>
    <summary> 王子谦, 李鲁鲁</summary>
    项目由李鲁鲁发起，代码部分主要由王子谦完成。
</details>

# 动机

在2025年2月，各家云服务商纷纷开始提供DeepSeek，包括R1和V3模型的API。我们了解到其中一些服务使用了蒸馏后的千问小模型。我们想在DeepSeek的原本报告中，抽样一个快速子集，来估计各家DeepSeek API和report的差异。

同时，qualys的报告指出，DeepSeek模型对于越狱的防御还不够完整。项目希望对此也进行探究

# 项目目标

- 根据DeepSeek-V3和R1的报告，抽样建立一个subset快速测集，初步估计各家API的反应速度和在几个benchmark上的抽样准确率
- 根据qualys的报告，抽样建立一个越狱测试集，测试各家API的越狱概率
- 编写一个后端，支持使用任意一家的API，将用户的query套用某个越狱模板进行测试。

# 参考资料

DeepSeek的攻击报告
https://blog.qualys.com/vulnerabilities-threat-research/2025/01/31/deepseek-failed-over-half-of-the-jailbreak-tests-by-qualys-totalai