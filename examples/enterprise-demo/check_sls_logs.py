#!/usr/bin/env python3
"""
SLS 日志检查脚本
检查阿里云 SLS 中是否成功接收到日志
"""

import os
import sys
from datetime import datetime, timedelta
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def check_sls_logs():
    """检查 SLS 日志"""
    try:
        from aliyun.log import LogClient  # type: ignore
        from aliyun.log.logexception import LogException  # type: ignore
        
        # 获取配置
        project = "yai-log-test"
        logstore = "app-log"
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
        print("\n📋 查询最近 10 分钟的日志...")
        
        # 计算时间范围（最近10分钟）
        end_time = datetime.now()
        start_time = end_time - timedelta(minutes=10)
        
        from_time = int(start_time.timestamp())
        to_time = int(end_time.timestamp())
        
        try:
            # 查询日志 - 使用正确的 GetLogsRequest
            from aliyun.log import GetLogsRequest  # type: ignore
            
            request = GetLogsRequest(
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
            
            response = client.get_logs(request)
            
            logs = response.get_logs()
            
            if logs:
                print(f"✅ 找到 {len(logs)} 条日志记录")
                print("\n📝 最新日志内容:")
                print("-" * 50)
                
                for i, log in enumerate(logs[:3]):  # 只显示前3条
                    log_time = datetime.fromtimestamp(int(log.get_time()))
                    print(f"[{i+1}] 时间: {log_time.strftime('%Y-%m-%d %H:%M:%S')}")
                    
                    # 显示日志内容
                    for key, value in log.get_contents().items():
                        if key in ['message', 'level', 'function', 'line']:
                            print(f"    {key}: {value}")
                    print("-" * 30)
                    
                return True
            else:
                print("⚠️  未找到匹配的日志记录")
                print("💡 可能原因:")
                print("   1. 日志还未到达 SLS（有延迟）")
                print("   2. 日志级别过滤")
                print("   3. topic 或 source 不匹配")
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

def main():
    """主函数"""
    print("🔍 SLS 日志检查工具")
    print("=" * 50)
    
    success = check_sls_logs()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ SLS 日志检查成功！日志已正常写入阿里云")
    else:
        print("❌ SLS 日志检查失败，请检查配置或网络连接")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())