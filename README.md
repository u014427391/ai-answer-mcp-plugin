# 数学题图片识别与解答工具

一个基于PaddleOCR和SiliconFlow API的数学题图片识别与解答工具，支持上传包含数学题的图片，自动识别题目并给出答案和解题步骤。

## 功能特点

- 支持上传图片识别数学题（优化数学公式和中文识别）
- 自动解答并返回详细解题步骤
- 简洁直观的用户界面
- 基于Flask的轻量后端服务
- 支持部署到蓝耕云MCP平台

## 技术架构

- 后端：Python + Flask框架
- 前端：HTML + CSS + JavaScript
- 图像识别：PaddleOCR（支持中英文和数学公式）
- 解题核心：SiliconFlow API
- 插件框架：FastMCP（支持MCP平台部署）

## 快速开始

### 本地运行

#### 前置条件
- Python 3.8.3
- SiliconFlow API密钥

#### 安装步骤
1. 克隆仓库并安装依赖（同上，略）

### 部署到蓝耕云MCP平台

#### 前置条件
- 蓝耕云平台账号
- 已创建MCP应用空间

#### 部署步骤
1. 确保项目根目录包含`mcp.json`配置文件
2. 打包项目为ZIP文件（不含虚拟环境）
3. 登录蓝耕云平台，进入MCP插件库
4. 点击"上传插件"，选择打包的ZIP文件
5. 配置插件参数（主要是SILICONFLOW_API_KEY）
6. 部署插件并启动服务

## 项目结构

```
ai-answer-mcp-plugin/
├── backend/ # 后端服务代码
│ ├── app.py # 主程序入口
│ ├── mcp_entry.py # MCP 插件入口
│ └── requirements.txt # 依赖清单
├── frontend/ # 前端页面
├── mcp.json # MCP 插件配置
├── .env # 本地环境变量
└── README.md # 项目说明
```