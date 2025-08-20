import os
from app import app
from fastmcp import McpPlugin

# 初始化MCP插件
plugin = McpPlugin()


# 注册插件启动函数
@plugin.startup
def startup():
    """MCP插件启动入口"""
    # 从MCP环境变量获取配置
    if "SILICONFLOW_API_KEY" in os.environ:
        os.environ["SILICONFLOW_API_KEY"] = os.environ["SILICONFLOW_API_KEY"]

    # 启动Flask应用
    app.run(
        host=os.getenv("MCP_HOST", "0.0.0.0"),
        port=int(os.getenv("MCP_PORT", 8000)),
        debug=False
    )


# 注册插件健康检查
@plugin.health_check
def health_check():
    """健康检查接口"""
    return {"status": "healthy", "version": "1.0.0"}


if __name__ == "__main__":
    plugin.run()