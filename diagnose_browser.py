# diagnose_browser.py
# 用于诊断浏览器/Chromedriver/selenium 启动问题
# 输出包含 1) Chrome 可执行路径和版本 2) chromedriver 使用状态 3) selenium/uc 启动日志

import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

LOG_DIR = Path('diagnose_logs')
LOG_DIR.mkdir(exist_ok=True)


def log(msg):
    print(msg)
    with open(LOG_DIR / 'diagnose.log', 'a', encoding='utf-8') as f:
        f.write(msg + '\n')


# 1. 检查 Chrome 可执行路径和版本

def check_chrome():
    log('\n== Chrome Path and Version ==')
    candidates = [
        shutil.which('chrome'),
        shutil.which('chrome.exe'),
        os.path.expandvars(r'%ProgramFiles%\Google\Chrome\Application\chrome.exe'),
        os.path.expandvars(r'%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe'),
        r'C:\Program Files\Google\Chrome\Application\chrome.exe',
        r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
    ]
    paths = [p for p in candidates if p and os.path.exists(p)]
    if not paths:
        log('Chrome 未找到 (没有检测到 chrome 可执行文件)')
        return None

    chrome_path = paths[0]
    log(f'检测到 Chrome: {chrome_path}')
    try:
        proc = subprocess.run([chrome_path, '--version'], capture_output=True, text=True, timeout=10)
        out = proc.stdout.strip() or proc.stderr.strip()
        log(f'Chrome 版本输出: {out}')
    except subprocess.TimeoutExpired:
        # 某些环境 chrome --version 可能阻塞，用 PowerShell 查询文件版本作为备选
        try:
            ps_cmd = [
                'powershell', '-Command',
                f"(Get-Item '{chrome_path}').VersionInfo.FileVersion"
            ]
            proc2 = subprocess.run(ps_cmd, capture_output=True, text=True, timeout=10)
            out2 = proc2.stdout.strip() or proc2.stderr.strip()
            log(f'PowerShell 获取 Chrome 版本: {out2}')
        except Exception as e:
            log(f'无法通过 PowerShell 获取 Chrome 版本: {e}')
    except Exception as e:
        log(f'无法获取 Chrome 版本: {e}')
    return chrome_path


# 2. 检查 chromedriver/ webdriver-manager

def check_chromedriver():
    log('\n== chromedriver status ==')
    # 系统中 chromedriver
    try:
        proc = subprocess.run(['where', 'chromedriver'], capture_output=True, text=True, timeout=10, shell=True)
        out = proc.stdout.strip() or proc.stderr.strip()
        log('where chromedriver 输出:')
        log(out)
    except Exception as e:
        log(f'where chromedriver 失败: {e}')

    # 检查是否能直接执行 chromedriver --version
    try:
        proc = subprocess.run(['chromedriver', '--version'], capture_output=True, text=True, timeout=5, shell=True)
        out = proc.stdout.strip() or proc.stderr.strip()
        log(f'chromedriver --version: {out}')
    except Exception as e:
        log(f'chromedriver --version 调用失败: {e}')


# 3. 用 selenium + webdriver-manager 测试启动

def test_selenium():
    log('\n== selenium + webdriver-manager test ==')
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.chrome.options import Options
        from webdriver_manager.chrome import ChromeDriverManager
    except Exception as e:
        log('缺少 selenium 或 webdriver-manager: ' + str(e))
        return

    try:
        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-extensions')
        options.add_argument('--window-size=1200,800')
        # options.add_argument('--headless=new')

        log('开始安装chromedriver(如果未装)并尝试启动 chrome ...')
        try:
            driver_path = ChromeDriverManager().install()
        except Exception as e:
            # webdriver-manager 下载失败时，不要长时间卡住，打印提示并退出
            log('webdriver-manager 下载 chromedriver 失败: ' + str(e))
            log('建议：手动下载 chromedriver 或使用 undetected-chromedriver 作为 fallback')
            return
        log(f'webdriver-manager 下载/返回的 chromedriver: {driver_path}')

        service = Service(driver_path)
        service.log_path = str(LOG_DIR / 'chromedriver_selenium.log')
        driver = webdriver.Chrome(service=service, options=options)
        driver.set_page_load_timeout(15)
        driver.get('https://www.google.com')
        log('Selenium loaded title: ' + driver.title)
        driver.quit()
        log('Selenium 启动成功')
    except Exception as e:
        log('Selenium 测试失败: ' + str(e))


# 4. 测试 undetected-chromedriver（如果安装）

def test_uc():
    log('\n== undetected-chromedriver (uc) test ==')
    try:
        import undetected_chromedriver as uc
        from selenium.webdriver.chrome.options import Options
    except Exception as e:
        log('未安装 undetected_chromedriver: ' + str(e))
        return

    try:
        options = uc.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-extensions')
        options.add_argument('--window-size=1200,800')

        log('尝试使用 uc.Chrome() 启动 ...')
        driver = uc.Chrome(options=options)
        driver.set_page_load_timeout(15)
        driver.get('https://www.google.com')
        log('uc loaded title: ' + driver.title)
        driver.quit()
        log('uc 启动成功')
    except Exception as e:
        log('uc 测试失败: ' + str(e))


# 5. 检查 chrome 进程是否残留

def check_processes():
    log('\n== Running Chrome Processes ==')
    try:
        proc = subprocess.run(['tasklist', '/fi', 'imagename eq chrome.exe'], capture_output=True, text=True, timeout=10, shell=True)
        log(proc.stdout.strip())
    except Exception as e:
        log('tasklist 检查失败: ' + str(e))


if __name__ == '__main__':
    # 清空日志
    (LOG_DIR / 'diagnose.log').write_text('')
    log('诊断开始: ' + time.strftime('%Y-%m-%d %H:%M:%S'))

    chrome_path = check_chrome()
    check_chromedriver()
    check_processes()
    test_selenium()
    test_uc()

    log('诊断结束')

