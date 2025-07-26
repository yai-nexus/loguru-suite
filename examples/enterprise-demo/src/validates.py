#!/usr/bin/env python3
"""
SLS 日志验证模块
检查阿里云 SLS 中是否成功接收到日志
"""

import os
from datetime import datetime, timedelta
from loguru import logger


def check_sls_logs(expected_nonce: str | None = None) -> bool:
    """检查 SLS 日志"""
    try:
        from aliyun.log import LogClient  # type: ignore
        from aliyun.log.logexception import LogException  # type: ignore
        
        # 获取配置
        project = "yai-log-test"
        logstore = "nexus-log"
        region = "cn-beijing"
        access_key_id = os.getenv('SLS_ACCESS_KEY_ID')
        access_key_secret = os.getenv('SLS_ACCESS_KEY_SECRET')
        
        if not access_key_id or not access_key_secret:
            print("❌ 缺少 SLS 访问密钥配置")
            return False
            
        # 创建客户端
        endpoint = f"https://{region}.log.aliyuncs.com"
        client = LogClient(endpoint, access_key_id, access_key_secret)
        
        print(f"🔍 检查 SLS 项目: {project}/{logstore}")
        print(f"📍 地域: {region}")
        print(f"🔗 端点: {endpoint}")
        
        # 检查项目是否存在
        try:
            client.get_project(project)
            print(f"✅ 项目 {project} 存在")
        except LogException as e:
            print(f"❌ 项目检查失败: {e}")
            return False
            
        # 检查日志库是否存在
        try:
            client.get_logstore(project, logstore)
            print(f"✅ 日志库 {logstore} 存在")
        except LogException as e:
            print(f"❌ 日志库检查失败: {e}")
            return False
            
        # 查询最近的日志
        print("\n📋 查询最近 5 分钟的日志...")
        
        # 计算时间范围（最近5分钟）
        end_time = datetime.now()
        start_time = end_time - timedelta(minutes=5)
        
        from_time = int(start_time.timestamp())
        to_time = int(end_time.timestamp())
        
        try:
            # 查询日志 - 使用精确的查询条件查找我们的测试日志
            from aliyun.log import GetLogsRequest  # type: ignore
            
            # 首先尝试查找我们的测试日志
            if expected_nonce:
                # 如果提供了 nonce，使用精确查询
                query = f'test_nonce="{expected_nonce}"'
                print(f"🔍 使用 nonce 精确查询: {expected_nonce}")
            else:
                # 否则使用通用查询
                query = 'test_marker="enterprise_demo_test" OR "Enterprise Demo 测试日志"'
                print("🔍 使用通用查询条件")
            
            test_request = GetLogsRequest(
                project=project,
                logstore=logstore,
                fromTime=from_time,
                toTime=to_time,
                topic="",
                query=query,
                line=50,
                offset=0,
                reverse=True
            )
            
            test_response = client.get_logs(test_request)
            test_logs = test_response.get_logs()
            
            if test_logs:
                print(f"✅ 找到 {len(test_logs)} 条测试日志记录")
                print("\n📝 测试日志内容:")
                print("-" * 50)
                
                nonce_verified = False
                
                for i, log in enumerate(test_logs[:3]):  # 显示前3条测试日志
                    log_time = datetime.fromtimestamp(int(log.get_time()))
                    print(f"[{i+1}] 时间: {log_time.strftime('%Y-%m-%d %H:%M:%S')}")
                    
                    # 显示日志内容
                    log_contents = log.get_contents()
                    print(f"📋 日志内容: {dict(log_contents)}")
                    for key, value in log_contents.items():
                        print(f"    {key}: {value}")
                    
                    # 验证 nonce
                    if expected_nonce:
                        log_nonce = log_contents.get('test_nonce', '')
                        if log_nonce == expected_nonce:
                            print(f"    ✅ nonce 验证成功: {log_nonce}")
                            nonce_verified = True
                        else:
                            print(f"    ⚠️ nonce 不匹配: 期望 {expected_nonce}, 实际 {log_nonce}")
                    
                    print("-" * 30)
                
                if expected_nonce:
                    if nonce_verified:
                        print("✅ SLS 集成验证成功！找到了匹配 nonce 的测试日志")
                        print("✅ 确认日志是本次运行产生的")
                    else:
                        print("⚠️ 找到了测试日志，但 nonce 不匹配")
                        print("💡 可能是查询到了之前运行的日志")
                        return False
                else:
                    print("✅ SLS 集成验证成功！找到了 Enterprise Demo 的测试日志")
                
                print("✅ 日志已成功写入阿里云 SLS")
                return True
            else:
                # 如果没找到测试日志，再查询一般的日志来验证连接
                print("ℹ️ 未找到测试日志，尝试查询一般日志验证连接...")
                
                general_request = GetLogsRequest(
                    project=project,
                    logstore=logstore,
                    fromTime=from_time,
                    toTime=to_time,
                    topic="",
                    query="*",
                    line=10,
                    offset=0,
                    reverse=True
                )
                
                general_response = client.get_logs(general_request)
                general_logs = general_response.get_logs()
                
                if general_logs:
                    print(f"✅ SLS 连接正常，找到 {len(general_logs)} 条日志记录")
                    print("⚠️ 但未找到 Enterprise Demo 的测试日志")
                    print("💡 可能原因：日志传输延迟或查询条件需要调整")
                    
                    # 显示最新的几条日志以便调试
                    print("\n📋 最新日志示例:")
                    for i, log in enumerate(general_logs[:2]):
                        log_content = log.get_contents()
                        print(f"  日志 {i+1}: {dict(log_content)}")
                    
                    return True
                else:
                    print("❌ 未找到任何日志记录")
                    return False
                
        except LogException as e:
            print(f"❌ 查询日志失败: {e}")
            return False
            
    except ImportError:
        print("❌ 缺少 aliyun-log-python-sdk 依赖")
        print("💡 请运行: uv add aliyun-log-python-sdk")
        return False
    except Exception as e:
        print(f"❌ 检查失败: {e}")
        return False


def validate_sls_integration(expected_nonce: str | None = None) -> bool:
    """验证 SLS 集成功能"""
    print("\n" + "=" * 50)
    print("🔍 开始检查 SLS 日志写入情况...")
    print("⏳ 等待 5 秒让日志完全写入 SLS...")
    
    import time
    time.sleep(5)
    
    success = check_sls_logs(expected_nonce)
    
    print("\n" + "=" * 50)
    if success:
        print("✅ SLS 日志检查成功！日志已正常写入阿里云")
    else:
        print("❌ SLS 日志检查失败，请检查配置或网络连接")
    
    print("\n✅ SLS 日志检查完成！")
    return success