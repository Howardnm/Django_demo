import threading
import subprocess
import time
import requests


# 运行前，需安装python的组件
# pip install requests[socks]
# pip install shadowsocks

def run_sslocal():
    global process
    # 启动 Shadowsocks 客户端而不是服务器端
    command = ['sslocal', '-c', r'config.json']
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # 输出运行日志
    for line in process.stdout:
        print(line.decode(), end='')


# 创建并启动线程（启动ssr客户端，）
thread = threading.Thread(target=run_sslocal)
thread.start()

# 等待代理服务启动
# time.sleep(1)

# 配置 SOCKS5 代理
proxies = {
    'http': 'socks5h://127.0.0.1:1080',
    'https': 'socks5h://127.0.0.1:1080'
}

# 发送请求
url = 'https://www.google.com/'

# 配置请求头，防人机检测导致403
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Connection': 'keep-alive'
}

try:
    response = requests.get(url, headers=headers, proxies=proxies, timeout=5)  # proxies=proxies，把requests请求挂上代理
    print(response.status_code)
    content_type = response.headers.get('Content-Type')
    print(f"Content-Type: {content_type}")
    # 尝试自动检测编码
    response.encoding = response.apparent_encoding

    # 保存响应内容为 HTML 文件
    with open('output.html', 'w', encoding=response.encoding) as f:
        f.write(response.text)

except requests.exceptions.RequestException as e:
    print(f"Error: {e}")  # 请求web失败，显示错误

finally:
    # 程序结束时关闭 Shadowsocks 客户端进程
    if process:
        process.terminate()
        process.wait()  # 确保进程完全退出
        print("Shadowsocks 客户端已关闭。")

    # 等待线程结束
    thread.join()
