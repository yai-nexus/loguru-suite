#!/usr/bin/env python3
"""
Enterprise Demo - 企业级日志示例
展示 yai-loguru-sinks 的 SLS 集成功能
"""

import os
import sys
from pathlib import Path
from loguru import logger
import yai_loguru_sinks
from loguru_config import LoguruConfig

def setup_logging():
    """设置日志配置"""
    # 移除默认处理器
    logger.remove()
    
    # 注册协议解析器
    yai_loguru_sinks.register_protocol_parsers()
    
    # 加载配置文件
    config_path = Path(__file__).parent / "logging.yaml"
    config = LoguruConfig()
    config.load(str(config_path))
    
    logger.info("日志系统初始化完成")

def check_sls_config():
    """检查 SLS 配置"""
    required_vars = [
        "SLS_PROJECT",
        "SLS_LOGSTORE", 
        "SLS_REGION",
        "SLS_ACCESS_KEY_ID",
        "SLS_ACCESS_KEY_SECRET"
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        logger.warning(f"缺少 SLS 环境变量: {', '.join(missing_vars)}")
        logger.info("请参考 .env.example 文件配置 SLS 环境变量")
        return False
    
    logger.info("SLS 配置检查通过")
    return True

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

if __name__ == "__main__":
    main()