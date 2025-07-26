#!/usr/bin/env python3
"""
测试阿里云 SLS 连接和日志发送
"""

import os
import time
from loguru import logger

def test_sls_connection():
    """测试 SLS 连接"""
    try:
        # 加载环境变量
        from dotenv import load_dotenv
        load_dotenv('../.env')
        print("✅ 已加载 .env 文件")
    except ImportError:
        print("⚠️  python-dotenv 未安装")
        return False
    
    # 检查环境变量
    endpoint = os.getenv('SLS_ENDPOINT')
    project = os.getenv('SLS_PROJECT')
    logstore = os.getenv('SLS_LOGSTORE')
    access_key_id = os.getenv('SLS_ACCESS_KEY_ID')
    access_key_secret = os.getenv('SLS_ACCESS_KEY_SECRET')
    region = os.getenv('SLS_DEFAULT_REGION')
    
    print(f"📍 SLS 配置:")
    print(f"   Endpoint: {endpoint}")
    print(f"   Project: {project}")
    print(f"   Logstore: {logstore}")
    print(f"   Region: {region}")
    print(f"   Access Key ID: {access_key_id[:8] if access_key_id else 'None'}...")
    
    if not all([endpoint, project, logstore, access_key_id, access_key_secret]):
        print("❌ SLS 环境变量不完整")
        return False
    
    # 测试直接使用 SLS SDK
    try:
        from aliyun.log import LogClient  # type: ignore
        
        # 创建客户端
        client = LogClient(f"https://{endpoint}", access_key_id, access_key_secret)
        
        # 测试连接 - 获取项目信息
        print(f"\n🔍 测试连接到项目: {project}")
        try:
            project_info = client.get_project(project)
            print(f"✅ 项目连接成功")
        except Exception as e:
            print(f"❌ 项目连接失败: {e}")
            return False
        
        # 测试获取日志库信息
        print(f"🔍 测试连接到日志库: {logstore}")
        try:
            logstore_info = client.get_logstore(project, logstore)
            print(f"✅ 日志库连接成功")
        except Exception as e:
            print(f"❌ 日志库连接失败: {e}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ SLS 连接测试失败: {e}")
        return False

def test_with_yai_loguru_sinks():
    """使用 yai-loguru-sinks 测试"""
    try:
        from yai_loguru_sinks import register_protocol_parsers, create_config_from_file
        
        print("\n🚀 使用 yai-loguru-sinks 发送测试日志...")
        
        # 设置扩展配置
        register_protocol_parsers()
        
        # 加载配置文件
        config = create_config_from_file('configs/logging.yaml')
        print("✅ 配置文件加载成功")
        
        # 发送测试日志
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        
        logger.info(f"[测试] 信息日志 - {current_time}")
        logger.warning(f"[测试] 警告日志 - {current_time} - 这条应该发送到 SLS")
        logger.error(f"[测试] 错误日志 - {current_time} - 这条应该发送到 SLS")
        
        print("✅ 测试日志发送完成")
        print("⏳ 等待 3 秒让日志批量发送...")
        time.sleep(3)
        
        return True
        
    except Exception as e:
        print(f"❌ yai-loguru-sinks 测试失败: {e}")
        return False

def main():
    print("🔍 阿里云 SLS 连接测试")
    print("=" * 50)
    
    # 测试 1: 直接 SLS 连接
    print("\n📡 测试 1: 直接 SLS SDK 连接")
    sls_ok = test_sls_connection()
    
    if sls_ok:
        # 测试 2: yai-loguru-sinks
        print("\n📡 测试 2: yai-loguru-sinks 日志发送")
        yai_ok = test_with_yai_loguru_sinks()
        
        if yai_ok:
            print("\n🎉 所有测试通过！")
            print("\n📋 查看 SLS 日志的步骤:")
            print("1. 访问阿里云控制台: https://sls.console.aliyun.com/")
            print("2. 选择地域: cn-beijing")
            print("3. 进入项目: yai-log-test")
            print("4. 进入日志库: app-log")
            print("5. 点击 '查询分析' 或 '消费预览'")
            print("6. 查看最近的日志记录")
        else:
            print("\n❌ yai-loguru-sinks 测试失败")
    else:
        print("\n❌ SLS 连接测试失败，请检查配置")

if __name__ == "__main__":
    main()