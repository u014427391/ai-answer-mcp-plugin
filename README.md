# 数学题图片识别与解答工具

一个基于SiliconFlow API的数学题图片识别与解答工具，支持上传包含数学题的图片，自动识别题目并给出答案和解题步骤。

## 功能特点

- 支持上传图片识别数学题
- 自动解答并返回详细解题步骤
- 简洁直观的用户界面
- 易于部署和扩展

## 技术架构

- 后端：Python + FastMCP框架
- 前端：HTML + CSS + JavaScript
- 核心API：SiliconFlow图像识别与数学解题API

## 快速开始

### 前置条件

- Python 3.8+
- 一个SiliconFlow API密钥（可在[SiliconFlow官网](https://siliconflow.cn/)申请）

### 安装步骤

1. 克隆仓库
```bash
git clone https://github.com/yourusername/math-problem-solver.git
cd math-problem-solver

### 依赖安装

Tesseract OCR引擎安装（必选）
本工具使用Tesseract进行图片文字识别，需先安装：

- **Ubuntu/Debian**:
  ```bash
  sudo apt update
  sudo apt install tesseract-ocr
  sudo apt install tesseract-ocr-chi-sim  # 简体中文语言包