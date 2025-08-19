from flask import Flask, jsonify, redirect, url_for, request
import requests
from PIL import Image, ImageEnhance, ImageFilter
import io
import base64
import os
import re
import time
from dotenv import load_dotenv
from flask_cors import CORS
# 导入PaddleOCR
from paddleocr import PaddleOCR

# 加载环境变量
load_dotenv()

# 初始化Flask应用
app = Flask(__name__, static_folder='../frontend', static_url_path='/')

# 允许跨域请求
CORS(app, resources={r"/*": {"origins": "*"}})

# 初始化PaddleOCR，支持中英文和数学公式
# use_angle_cls=True 启用方向检测，lang='ch' 支持中英文
ocr = PaddleOCR(use_angle_cls=True, lang='ch', show_log=False)

# SiliconFlow API配置
SILICONFLOW_API_KEY = os.getenv("SILICONFLOW_API_KEY")
SILICONFLOW_API_URL = "https://api.siliconflow.cn/v1/chat/completions"

# 服务配置
HOST = "0.0.0.0"
PORT = 8000
DEBUG = True


def preprocess_image(image: Image.Image) -> Image.Image:
    """图片预处理以提高OCR识别率"""
    # 转为灰度图
    img = image.convert("L")

    # 增强对比度
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.5)

    # 轻微锐化
    img = img.filter(ImageFilter.SHARPEN)

    # 二值化处理
    threshold = 150
    img = img.point(lambda p: p > threshold and 255)

    return img


def image_to_base64(image: Image.Image) -> str:
    """将图片转换为带格式前缀的base64编码字符串"""
    try:
        buffer = io.BytesIO()
        image_format = image.format if image.format in ["JPEG", "PNG", "GIF"] else "PNG"
        image.save(buffer, format=image_format)

        base64_str = base64.b64encode(buffer.getvalue()).decode("utf-8")
        return f"data:image/{image_format.lower()};base64,{base64_str}"
    except Exception as e:
        raise Exception(f"图片转换失败: {str(e)}")


def ocr_image(image: Image.Image) -> str:
    """使用PaddleOCR识别图片中的文本，特别优化中文和数学公式"""
    try:
        # 预处理图片
        processed_img = preprocess_image(image)

        # 保存预处理后的图片到内存
        img_byte_arr = io.BytesIO()
        processed_img.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()

        # 使用PaddleOCR识别
        # PaddleOCR接受文件路径或numpy数组，这里我们将图片转换为numpy数组
        import numpy as np
        img_np = np.array(processed_img)

        # 进行OCR识别
        result = ocr.ocr(img_np, cls=True)

        # 提取识别结果并按顺序拼接
        text = ""
        if result and len(result) > 0:
            # 按行排序
            lines = sorted(result[0], key=lambda x: x[0][0][1])
            for line in lines:
                # 每行的文本内容
                line_text = line[1][0]
                text += line_text + " "

        # 文本清理
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    except Exception as e:
        raise Exception(f"OCR识别失败: {str(e)}")


def call_siliconflow_api(problem_text: str) -> dict:
    """调用SiliconFlow对话API解答数学题"""
    if not SILICONFLOW_API_KEY:
        raise Exception("未配置SiliconFlow API密钥，请检查环境变量")

    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {SILICONFLOW_API_KEY}"
        }

        # 确认使用的模型是否有效，这可能是400错误的主要原因
        # 这里改用一个更通用的模型名称作为示例
        payload = {
            "model": "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B",  # 更改模型名称为有效选项
            "messages": [
                {
                    "role": "system",
                    "content": """你是一名数学老师，需要清晰解答用户提供的数学题。
                    请按照以下格式回答：
                    1. 先给出解题步骤，分点说明
                    2. 最后用"答案："开头给出最终答案
                    确保解答准确，步骤清晰易懂。"""
                },
                {
                    "role": "user",
                    "content": f"请解答以下数学题，并给出详细步骤：{problem_text}"
                }
            ],
            "temperature": 0.2,
            "max_tokens": 1000
        }

        start_time = time.time()
        response = requests.post(
            url=SILICONFLOW_API_URL,
            json=payload,
            headers=headers,
            timeout=60
        )

        # 打印响应内容以便调试
        print(f"API响应状态码: {response.status_code}")
        print(f"API响应内容: {response.text}")

        response.raise_for_status()
        result = response.json()

        # 添加响应时间信息
        result['response_time'] = time.time() - start_time
        return result
    except requests.exceptions.RequestException as e:
        # 更详细的错误信息
        raise Exception(f"API调用失败: {str(e)}. 响应内容: {getattr(response, 'text', '无响应内容')}")
    except Exception as e:
        raise Exception(f"处理API响应失败: {str(e)}")


@app.route("/", methods=["GET"])
def index():
    """服务首页"""
    return jsonify({
        "message": "数学题图片识别与解答服务",
        "endpoints": {
            "/solve_math_problem": "POST - 上传图片并解答数学题",
            "/frontend": "GET - 访问前端页面"
        }
    })


@app.route("/solve_math_problem", methods=["POST"])
def solve_math_problem():
    """处理数学题图片识别与解答请求"""
    try:
        # 检查是否有图片上传
        if "image" not in request.files:
            return jsonify({"error": "请上传图片文件"}), 400

        # 读取并处理图片
        image_file = request.files["image"]
        try:
            image = Image.open(image_file.stream)
        except Exception as e:
            return jsonify({"error": f"无效的图片文件: {str(e)}"}), 400

        # OCR识别题目文本
        try:
            problem_text = ocr_image(image)
            if not problem_text:
                return jsonify({"error": "未识别到题目文本，请上传清晰的图片"}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500

        # 调用API解答
        try:
            result = call_siliconflow_api(problem_text)
            answer_content = result["choices"][0]["message"]["content"]
        except Exception as e:
            return jsonify({"error": str(e)}), 500

        # 解析答案和步骤
        answer = "未找到答案"
        steps = []

        if "答案：" in answer_content:
            parts = answer_content.split("答案：")
            steps_content = parts[0].strip()
            answer = parts[1].strip()

            # 分割步骤
            steps = [step.strip() for step in re.split(r'\n\d+\.', steps_content) if step.strip()]
            # 恢复编号
            for i in range(len(steps)):
                steps[i] = f"{i+1}. {steps[i]}"
        else:
            steps = answer_content.split("\n")
            steps = [step.strip() for step in steps if step.strip()]

        # 返回结果
        return jsonify({
            "success": True,
            "problem": problem_text,
            "answer": answer,
            "steps": steps,
            "processing_time": f"{result.get('response_time', 0):.2f} 秒",
            "tokens_used": result.get('usage', {}).get('total_tokens', 0)
        })

    except Exception as e:
        return jsonify({"error": f"服务内部错误: {str(e)}"}), 500


@app.route("/frontend")
def frontend():
    """访问前端页面"""
    return redirect(url_for('static', filename='index.html'))


if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=DEBUG)
