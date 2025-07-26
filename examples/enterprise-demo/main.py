#!/usr/bin/env python3
"""
Enterprise Demo - 企业级日志示例
展示 yai-loguru-sinks 的 SLS 集成功能
"""

from loguru import logger
from src.config import load_environment, setup_logging, check_sls_config
from src.demos import (
    demo_basic_logging,
    demo_structured_logging, 
    demo_error_logging,
    demo_sls_logging,
    check_sls_logs
)

def main():
    """主函数"""
    print("🏢 Enterprise Demo - 企业级日志示例")
    print("=" * 50)
    
    # 加载环境变量
    load_environment()
    
    # 设置日志
    setup_logging()
    
    # 检查 SLS 配置
    sls_available = check_sls_config()
    if sls_available:
        logger.info("SLS 功能已启用")
        logger.info("PackId 功能已启用 - 相关日志将自动分组")
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
        print("🏷️ PackId 功能已启用 - 业务流程日志将自动分组")
        
        # 自动检查 SLS 日志
        check_success = check_sls_logs()
        if check_success:
            print("\n🎉 完整闭环测试成功！日志已成功写入并验证！")
        else:
            print("\n⚠️ 闭环测试部分失败，请手动检查 SLS 日志")


if __name__ == "__main__":
    main()