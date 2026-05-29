# Supermarket Commodity System-超市商品识别与自助结算系统

基于 PyQt5 和 YOLOv5 的超市商品识别与自助结算系统。程序通过摄像头实时识别商品，自动统计商品数量与金额，并支持管理员修改价格、调整检测参数、查看销量统计。

## Description

PyQt5+YOLOv5 supermarket self-checkout system. It detects products via camera, counts items, calculates totals, records sales, and provides admin tools for price edits, confidence/IOU settings, camera control, and sales statistics. Main entry: `main.py`; model weights go in `weight_file/`.

## 项目功能

- 实时商品识别：调用本地 YOLOv5 模型识别摄像头画面中的商品。
- 自动结算：统计当前识别到的商品数量、单项金额和总价。
- 销量记录：结算后将商品销量累计写入 `xiaoshou.csv`。
- 管理员功能：可关闭摄像头、修改商品价格、调整置信度和 IOU 参数。
- 销量统计：按销量从高到低展示商品销售数量。

## 项目结构

```text
Supermarket_commodity_sys/
├── main.py                                  # 程序主入口
├── requirements.txt                         # Python 依赖
├── xiaoshou.csv                             # 商品销量数据
├── anniu.py / anniu.qrc                     # Qt 资源文件生成代码
├── images/                                  # Qt Designer UI 文件
├── icons/                                   # 界面图标
├── models/                                  # YOLOv5 模型结构
├── utils/                                   # YOLOv5 工具代码
├── data/                                    # 训练/测试图片与标签数据
└── weight_file/
    ├── weight_x.pt                          # 主程序默认加载的权重
    └── best.pt                              # 备用模型权重
```

## 环境要求

- Windows 系统
- Conda / Anaconda / Miniconda
- Python 3.8 或 3.9 推荐
- 摄像头设备
- NVIDIA GPU + CUDA 推荐

程序中模型加载代码为：

```python
torch.hub.load(".", "custom", path=".//weight_file//weight_x.pt", device="0", source="local")
```

其中 `device="0"` 表示默认使用第 1 块 CUDA 显卡。如果电脑没有 NVIDIA 显卡或 CUDA 环境，可将 `main.py` 中的 `device='0'` 改为 `device='cpu'` 后运行。

## 创建 Conda 环境

建议使用 Conda 创建独立运行环境：

```bash
conda create -n supermarket_sys python=3.9
conda activate supermarket_sys
```

安装依赖：

```bash
pip install -r requirements.txt
```

如果安装 PyTorch 失败，建议根据本机 CUDA 版本到 PyTorch 官网选择对应安装命令。

## 模型权重

模型文件可从以下 Google Drive 链接下载：

[https://drive.google.com/drive/folders/13bxQKh5SydovNluaRGkfowugwAVvZDio?usp=sharing](https://drive.google.com/drive/folders/13bxQKh5SydovNluaRGkfowugwAVvZDio?usp=sharing)

下载后将模型权重放到项目的 `weight_file/` 目录下。主程序默认加载：

```text
weight_file/weight_x.pt
```

如果下载得到的文件名不同，请重命名为 `weight_x.pt`，或修改 `main.py` 中的模型路径。

## 运行方式

项目主函数是 `main.py`，在项目根目录执行：

```bash
python main.py
```

启动后程序会全屏显示主界面，并自动准备本地模型。点击结算界面的开始按钮后，程序会打开默认摄像头并开始识别商品。

## 使用说明

1. 运行 `python main.py` 启动系统。
2. 在主界面点击开始结算按钮，开启摄像头识别。
3. 将商品放在摄像头画面中，系统会自动识别并更新结算表格。
4. 点击结算按钮后，系统会提示购买成功，并把商品销量累计保存到 `xiaoshou.csv`。
5. 点击管理员入口可打开管理界面，进行价格修改、检测参数调整、摄像头关闭和销量统计查看。

## 关键代码说明

- `MainWindow`：主结算窗口，负责加载主界面、模型、摄像头和结算逻辑。
- `Thread`：视频检测线程，读取摄像头画面并调用 YOLOv5 模型推理。
- `Thread_1`：表格刷新线程，实时更新商品名称、数量、金额和总价。
- `guanli_Window`：管理员窗口，支持价格表修改、置信度和 IOU 调整。
- `tonji_Window`：销量统计窗口，从 `xiaoshou.csv` 读取销量并排序展示。

## 数据与模型

- 默认模型权重：`weight_file/weight_x.pt`
- 备用权重：`weight_file/best.pt`
- 模型下载地址：[Google Drive](https://drive.google.com/drive/folders/13bxQKh5SydovNluaRGkfowugwAVvZDio?usp=sharing)
- 销量数据：`xiaoshou.csv`
- 商品类别数量：`models/yolov5s-Supermarket_commodity_testing.yaml` 中配置为 `nc: 50`

注意：`main.py` 中内置了商品类别、商品显示名称和商品价格映射。当前部分中文字符串存在编码显示异常，但不影响识别类别映射、价格计算和 CSV 统计逻辑。若需要修复界面中文显示，需要统一源文件编码并重新保存相关中文文本。

## 常见问题

### 1. 摄像头无法打开

程序默认使用 `cv2.VideoCapture(0)` 打开第一个摄像头。如果电脑有多个摄像头，可在 `main.py` 中将 `window.video.open(0)` 改为其他编号，如 `1` 或 `2`。

### 2. 没有 GPU 无法运行

将 `main.py` 中模型加载参数 `device='0'` 改为 `device='cpu'`。

### 3. 找不到权重文件

确认以下文件存在：

```text
weight_file/weight_x.pt
```

如果想使用备用模型，可将 `main.py` 中的权重路径改为：

```python
path=".//weight_file//best.pt"
```

### 4. 修改价格后重启失效

当前价格表主要保存在 `main.py` 的内存字典中，管理员界面修改价格只在当前运行期间生效。如果需要永久保存价格，需要增加价格文件，例如 CSV 或 JSON，并在程序启动时读取。

## 开发说明

UI 界面文件位于 `images/` 目录，可使用 Qt Designer 打开 `.ui` 文件进行修改。修改资源文件后，如涉及 `.qrc` 资源更新，需要重新生成对应的 Python 资源文件。

模型相关代码来自 YOLOv5 风格结构，主要目录为 `models/` 和 `utils/`。主程序通过 `torch.hub.load(..., source="local")` 从当前项目目录加载本地模型代码。
