#!/usr/bin/env python3
"""
演示模块 - 所有日志演示函数
"""

import time
import sys
from pathlib import Path
from loguru import logger


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
    import uuid
    
    # 生成唯一的 nonce 用于验证
    nonce = str(uuid.uuid4())[:8]  # 使用前8位作为简短的nonce
    
    logger.info("=== SLS 日志示例 ===")
    
    # 这些日志会同时输出到控制台、文件和 SLS
    logger.info("企业级日志记录", extra={
        "environment": "production",
        "service": "enterprise-demo",
        "version": "1.0.0",
        "deployment": "k8s-cluster-1",
        "test_nonce": nonce
    })
    
    # 安全审计日志
    logger.warning("安全事件", extra={
        "event_type": "failed_login_attempt",
        "user_id": "unknown",
        "ip_address": "192.168.1.200",
        "attempts": 3,
        "severity": "medium",
        "test_nonce": nonce
    })
    
    # PackId 功能演示 - 模拟一个业务流程的多个步骤
    logger.info("=== PackId 功能演示 ===")
    logger.info("开始处理订单", extra={
        "business_flow": "order_processing",
        "step": "start",
        "order_id": "order-12345",
        "test_nonce": nonce
    })
    
    logger.info("验证用户信息", extra={
        "business_flow": "order_processing", 
        "step": "user_validation",
        "user_id": "user-67890",
        "test_nonce": nonce
    })
    
    logger.info("计算订单金额", extra={
        "business_flow": "order_processing",
        "step": "amount_calculation", 
        "amount": 299.99,
        "currency": "CNY",
        "test_nonce": nonce
    })
    
    logger.info("完成订单处理", extra={
        "business_flow": "order_processing",
        "step": "complete",
        "status": "success",
        "test_nonce": nonce
    })
    
    # 添加一些特殊的测试日志，便于后续检查
    logger.info("Enterprise Demo 测试日志", extra={
        "test_marker": "enterprise_demo_test",
        "timestamp": time.time(),
        "demo_type": "sls_integration_test",
        "packid_test": "enabled",
        "test_nonce": nonce
    })
    
    print(f"🔑 本次测试 nonce: {nonce}")
    return nonce


def check_sls_logs(expected_nonce: str | None = None) -> bool:
    """检查 SLS 日志写入情况"""
    from .validates import validate_sls_integration
    return validate_sls_integration(expected_nonce)