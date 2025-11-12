"""
主程序模块：包含以下功能
- 使用 Firefox 配置文件启动 Selenium 浏览器（支持 geckodriver 自动/手动安装回退）
- 从 JSON 文件加载 cookies 并自动注入到浏览器
- visit_etsy_with_firefox() 用于访问 Etsy 并（可选）加载 cookie
备注：所有函数均包含中文注释，便于阅读与维护
"""
import json
import os
import time
import logging
import shutil
import tempfile
from typing import Optional
import logging
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from webdriver_manager.firefox import GeckoDriverManager


# FIREFOX_PROFILE_PATH = r"C:\Users\16957\AppData\Roaming\Mozilla\Firefox\Profiles\bnfugt8c.default-release-1"
FIREFOX_PROFILE_PATH = ""

class Config:
    FIREFOX_PROFILE_PATH = FIREFOX_PROFILE_PATH
    GECKODRIVER_PATH = "D:\\work\\etsy\\huakuai\\tools\\geckodriver.exe"
    PROXY = None
    PAGE_LOAD_TIMEOUT = 30


class LoggerSetup:
    @staticmethod
    def get_logger(name: str):
        logger = logging.getLogger(name)
        if not logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger

# 删除旧的 `class config`，使用统一的 Config 类

class FirefoxBrowserManager:
    """Firefox 浏览器管理器"""
    
    def __init__(self, instance_id=0, headless=False, profile_path: Optional[str] = None):
        self.instance_id = instance_id
        self.headless = headless
        self.profile_path = profile_path or Config.FIREFOX_PROFILE_PATH
        self.logger = logging.getLogger(__name__)
        self.driver = None
    
    def create_driver(self):
        """创建 Firefox WebDriver"""
        self.logger.info(f"Firefox 实例 {self.instance_id} 正在创建...")
        
        try:
            options = FirefoxOptions()
            
            # 无头模式
            if self.headless:
                options.add_argument('--headless')
            
            # 使用真实 Firefox Profile
            if self.profile_path:
                if os.path.exists(self.profile_path):
                    options.add_argument('-profile')
                    options.add_argument(self.profile_path)
                    self.logger.info(f"  ✓ 使用 Firefox Profile: {self.profile_path}")
                else:
                    self.logger.warning(f"  ✗ Firefox Profile 不存在: {Config.FIREFOX_PROFILE_PATH}")
            
            # 代理设置
            if hasattr(Config, 'PROXY') and Config.PROXY:
                proxy_parts = Config.PROXY.replace('http://', '').replace('https://', '')
                host, port = proxy_parts.split(':')
                options.set_preference('network.proxy.type', 1)
                options.set_preference('network.proxy.http', host)
                options.set_preference('network.proxy.http_port', int(port))
                options.set_preference('network.proxy.ssl', host)
                options.set_preference('network.proxy.ssl_port', int(port))
                self.logger.info(f"  使用代理: {Config.PROXY}")
            
            # 反检测设置
            options.set_preference('dom.webdriver.enabled', False)
            options.set_preference('useAutomationExtension', False)
            
            # 创建 Service（使用本地 geckodriver 或自动下载）
            if hasattr(Config, 'GECKODRIVER_PATH') and Config.GECKODRIVER_PATH and os.path.exists(Config.GECKODRIVER_PATH):
                service = FirefoxService(executable_path=Config.GECKODRIVER_PATH)
                self.logger.debug(f"  使用本地 geckodriver: {Config.GECKODRIVER_PATH}")
            else:
                service = FirefoxService(GeckoDriverManager().install())
                self.logger.debug("  使用 webdriver-manager 自动管理 geckodriver")
            # Set geckodriver log path for debugging
            log_dir = os.path.join(os.getcwd(), 'diagnose_logs')
            if not os.path.exists(log_dir):
                os.makedirs(log_dir, exist_ok=True)
            service.log_path = os.path.join(log_dir, f'geckodriver_{self.instance_id}.log')
            self.logger.debug(f"  geckodriver log: {service.log_path}")
            
            # 创建驱动
            self.driver = webdriver.Firefox(service=service, options=options)
            self.driver.set_page_load_timeout(Config.PAGE_LOAD_TIMEOUT)
            
            self.logger.info(f"Firefox 实例 {self.instance_id} ✓ 创建成功")
            return self.driver
            
        except Exception as e:
            self.logger.error(f"Firefox 实例 {self.instance_id} ✗ 创建失败: {e}")
            # 尝试读取 geckodriver 日志以帮助调试
            try:
                with open(service.log_path, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()[-100:]
                    self.logger.error('geckodriver log last lines:')
                    for line in lines:
                        self.logger.error(line.rstrip())
            except Exception:
                pass
            raise
    
    def close(self):
        """关闭浏览器"""
        if self.driver:
            try:
                self.driver.quit()
                self.logger.info(f"Firefox 实例 {self.instance_id} 已关闭")
            except Exception as e:
                self.logger.warning(f"Firefox 实例 {self.instance_id} 关闭时出错: {e}")
    
    def __enter__(self):
        self.create_driver()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()



if __name__ == '__main__':
    firefox = FirefoxBrowserManager(instance_id=1, headless=False)
    driver = firefox.create_driver()
    driver.get('https://www.etsy.com/sg-en/search?q=sofa&ref=pagination&page=3')
    time.sleep(500)
    firefox.close()




# import ddddocr

# det = ddddocr.DdddOcr(det=False, ocr=False)
# with open('D:\\work\\etsy\\huakuai\\image\\fp_46d6309a_block_1762681461.png', 'rb') as f:
#     target_bytes = f.read()

    
# with open('D:\\work\\etsy\\huakuai\\image\\fp_46d6309a_bg_1762681461.png', 'rb') as f:
#     background_bytes = f.read()

# res = det.slide_match(target_bytes, background_bytes)

# print(res)