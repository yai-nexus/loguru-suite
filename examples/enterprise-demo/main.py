#!/usr/bin/env python3
"""
Enterprise Demo - 企业级日志示例
展示 yai-loguru-sinks 的 SLS 集成功能
"""

import os
import sys
import time
import subprocess
from pathlib import Path

# 首先加载环境变量
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ 已加载 .env 文件")
except ImportError:
    print("⚠️ 未安装 python-dotenv，跳过 .env 文件加载")
except Exception as e:
    print(f"⚠️ 加载 .env 文件失败: {e}")

# 然后导入其他模块
from loguru import logger
import yai_loguru_sinks
from loguru_config import LoguruConfig  # type: ignore

def setup_logging():
    """设置日志配置"""
    import re
    import tempfile
    
    # 移除默认处理器
    logger.remove()
    
    # 注册协议解析器
    yai_loguru_sinks.register_protocol_parsers()
    
    # 读取原始配置文件
    config_path = Path(__file__).parent / "logging.yaml"
    with open(config_path, 'r', encoding='utf-8') as f:
        config_content = f.read()
    
    # 手动替换环境变量
    def expand_env_vars(text):
        def replace_var(match):
            var_name = match.group(1)
            return os.environ.get(var_name, match.group(0))
        return re.sub(r'\$\{([^}]+)\}', replace_var, text)
    
    expanded_content = expand_env_vars(config_content)
    
    # 如果有环境变量被替换，显示信息
    if expanded_content != config_content:
        print("🔧 已替换配置中的环境变量")
    
    # 创建临时配置文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write(expanded_content)
        temp_config_path = f.name
    
    try:
        # 加载处理后的配置文件
        config = LoguruConfig()
        config.load(temp_config_path)
        logger.info("日志系统初始化完成")
    finally:
        # 清理临时文件
        os.unlink(temp_config_path)

def check_sls_config():
    """检查 SLS 配置"""
    print("🔍 检查 SLS 环境变量:")
    
    # 只检查敏感信息的环境变量
    sls_vars = {
        'SLS_ACCESS_KEY_ID': os.getenv('SLS_ACCESS_KEY_ID'),
        'SLS_ACCESS_KEY_SECRET': os.getenv('SLS_ACCESS_KEY_SECRET'),
    }
    
    for var_name, var_value in sls_vars.items():
        if var_value:
            # 对敏感信息进行部分隐藏
            if 'SECRET' in var_name or 'KEY' in var_name:
                display_value = f"{var_value[:8]}..." if len(var_value) > 8 else "***"
            else:
                display_value = var_value
            print(f"  ✅ {var_name}: {display_value}")
        else:
            print(f"  ❌ {var_name}: 未设置")
    
    print(f"📝 项目配置: yai-log-test/app-log (cn-beijing)")
    print(f"☁️ SLS 日志将发送到阿里云")
    
    logger.info("SLS 配置检查通过")
    return all(sls_vars.values())

def demo_basic_logging():
    """基础日志示例"""
    logger.info("=== 基础日志示例 ===")
    
    logger.debug("这是调试信息")
    logger.info("这是普通信息")
    logger.warning("这是警告信息")
    logger.error("这是错误信息")

def demo_structured_logging():
    """结构化日志示例"""
    logger.info("=== 结构化日志示例 ===")
    
    # 用户操作日志
    logger.info("用户登录", extra={
        "user_id": "12345",
        "username": "admin",
        "ip_address": "192.168.1.100",
        "user_agent": "Mozilla/5.0...",
        "action": "login",
        "status": "success"
    })
    
    # API 调用日志
    logger.info("API 调用", extra={
        "api_path": "/api/v1/users",
        "method": "GET",
        "status_code": 200,
        "response_time": 150,
        "request_id": "req-abc123"
    })
    
    # 业务指标日志
    logger.info("业务指标", extra={
        "metric_name": "order_created",
        "metric_value": 1,
        "order_id": "order-789",
        "amount": 99.99,
        "currency": "CNY"
    })

def demo_error_logging():
    """错误日志示例"""
    logger.info("=== 错误日志示例 ===")
    
    try:
        # 模拟一个错误
        result = 10 / 0
    except ZeroDivisionError as e:
        logger.exception("计算错误", extra={
            "error_type": "ZeroDivisionError",
            "operation": "division",
            "operands": [10, 0]
        })

def demo_sls_logging():
    """SLS 专用日志示例"""
    logger.info("=== SLS 日志示例 ===")
    
    # 这些日志会同时输出到控制台、文件和 SLS
    logger.info("企业级日志记录", extra={
        "environment": "production",
        "service": "enterprise-demo",
        "version": "1.0.0",
        "deployment": "k8s-cluster-1"
    })
    
    # 安全审计日志
    logger.warning("安全事件", extra={
        "event_type": "failed_login_attempt",
        "user_id": "unknown",
        "ip_address": "192.168.1.200",
        "attempts": 3,
        "severity": "medium"
    })
    
    # 添加一些特殊的测试日志，便于后续检查
    logger.info("Enterprise Demo 测试日志", extra={
        "test_marker": "enterprise_demo_test",
        "timestamp": time.time(),
        "demo_type": "sls_integration_test"
    })

def check_sls_logs():
    """检查 SLS 日志是否成功写入"""
    print("\n" + "=" * 50)
    print("🔍 开始检查 SLS 日志写入情况...")
    print("⏳ 等待 5 秒让日志完全写入 SLS...")
    time.sleep(5)  # 等待日志写入
    
    try:
        # 获取当前脚本目录
        current_dir = Path(__file__).parent
        check_script = current_dir / "check_sls_logs.py"
        
        if not check_script.exists():
            print(f"❌ 检查脚本不存在: {check_script}")
            return False
        
        print(f"📋 运行日志检查脚本: {check_script}")
        
        # 运行检查脚本
        result = subprocess.run(
            [sys.executable, str(check_script)],
            cwd=str(current_dir),
            capture_output=True,
            text=True,
            timeout=30  # 30秒超时
        )
        
        # 输出检查结果
        if result.stdout:
            print(result.stdout)
        
        if result.stderr:
            print("错误输出:")
            print(result.stderr)
        
        if result.returncode == 0:
            print("✅ SLS 日志检查完成！")
            return True
        else:
            print(f"❌ SLS 日志检查失败，退出码: {result.returncode}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ SLS 日志检查超时")
        return False
    except Exception as e:
        print(f"❌ 运行 SLS 日志检查时出错: {e}")
        return False

def main():
    """主函数"""
    print("🏢 Enterprise Demo - 企业级日志示例")
    print("=" * 50)
    
    # 设置日志
    setup_logging()
    
    # 检查 SLS 配置
    sls_available = check_sls_config()
    if sls_available:
        logger.info("SLS 功能已启用")
    else:
        logger.info("SLS 功能未启用，仅使用本地日志")
    
    # 运行示例
    demo_basic_logging()
    demo_structured_logging()
    demo_error_logging()
    
    if sls_available:
        demo_sls_logging()
    
    logger.info("Enterprise Demo 运行完成")
    print("\n✅ 示例运行完成！")
    print("📁 本地日志文件：logs/enterprise-demo.log")
    if sls_available:
        print("☁️ SLS 日志已发送到阿里云")
        
        # 自动检查 SLS 日志
        check_success = check_sls_logs()
        if check_success:
            print("\n🎉 完整闭环测试成功！日志已成功写入并验证！")
        else:
            print("\n⚠️ 闭环测试部分失败，请手动检查 SLS 日志")

if __name__ == "__main__":
    main()