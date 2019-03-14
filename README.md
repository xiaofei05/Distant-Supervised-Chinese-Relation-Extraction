# Distant-Supervised-Chinese-Relation-Extraction
## 基于远监督的中文关系抽取

### 数据集构建

* 中文通用知识库CN-DBpedia
* 远监督假设

处理流程可在 kg_data/README.md 中查看。点击[此处(谷歌云盘)](https://drive.google.com/file/d/1eBrXikY0pxO9dbipwB9et2U-OtPcxEGr/view?usp=sharing)下载处理后的数据子集。

### 模型选择

使用 thunlp/OpenNRE 的模型, 具体信息参考其说明。

**源链接:** https://github.com/thunlp/OpenNRE

### 运行代码

数据集文件目录代码默认为 data/chinese，在命令中运行：
```
python train_demo.py chinese pcnn att
```

### 模型改进

未完待续