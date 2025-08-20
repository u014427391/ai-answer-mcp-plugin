# 数学题图片识别与解答工具

一个基于PaddleOCR和SiliconFlow API的数学题图片识别与解答工具，支持上传包含数学题的图片，自动识别题目并给出答案和解题步骤。

## 功能特点

- 支持上传图片识别数学题（优化数学公式和中文识别）
- 自动解答并返回详细解题步骤
- 简洁直观的用户界面
- 基于Flask的轻量后端服务
- 图片预处理优化，提升识别准确率

## 技术架构

- 后端：Python + Flask框架
- 前端：HTML + CSS + JavaScript
- 图像识别：PaddleOCR（支持中英文和数学公式）
- 解题核心：SiliconFlow API

## 快速开始

### 前置条件

- Python 3.8.3（推荐版本，已验证兼容性）
- 一个SiliconFlow API密钥（可在[SiliconFlow官网](https://siliconflow.cn/)申请）

在项目根目录创建.env文件，添加以下内容：
```env
SILICONFLOW_API_KEY=你的API密钥
```

### 安装步骤

1. 克隆仓库
```bash
git clone https://github.com/yourusername/ai-answer-mcp-plugin.git
cd ai-answer-mcp-plugin
```

2. 进入后端目录
cd backend

3. 安装Python依赖
pip install -r requirements.txt

### 启动项目
启动服务
```bash
# 在backend目录下
python app.py
```

访问工具
打开浏览器，访问 http://localhost:8000/frontend 即可使用