from main import FirefoxBrowserManager, FIREFOX_PROFILE_PATH
import os
import time
import sys
import math
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from tools.fingerprint_system.core.detector import FingerprintDetector
from PIL import Image

cookie_path = 'cookies.json'
with FirefoxBrowserManager(instance_id=0, headless=False, profile_path=FIREFOX_PROFILE_PATH) as mgr:
    driver = mgr.driver
    print('driver type:', type(driver))
    if driver:
        try:
            # 尝试加载页面（含重试逻辑）
            for attempt in range(3):
                try:
                    driver.get('https://www.etsy.com/sg-en/search?q=sofa&ref=pagination&page=3')
                    # driver.get('https://www.etsy.com')
                    break
                except Exception as e_inner:
                    print(f'第{attempt+1}次尝试加载页面失败: {e_inner}')
                    time.sleep(2)
            else:
                raise RuntimeError('多次尝试加载页面失败')
            print('title:', driver.title)
            time.sleep(2)

            # 尝试检测验证码并自动滑块
            detector = FingerprintDetector(headless=False)
            try:
                found = detector._wait_for_captcha(driver, timeout=5)
                if found:
                    print('captcha detected, saving canvas images...')
                    # detector switches to iframe; save canvases
                    bg_path, block_path = detector._save_canvas_images(driver, prefix='run_test')
                    print('bg:', bg_path, 'block:', block_path)

                    import ddddocr
                    det = ddddocr.DdddOcr(det=False, ocr=False)
                    with open('D:\\work\\etsy\\huakuai\\image\\fp_46d6309a_block_1762681461.png', 'rb') as f:
                        target_bytes = f.read()

                    with open('D:\\work\\etsy\\huakuai\\image\\fp_46d6309a_bg_1762681461.png', 'rb') as f:
                        background_bytes = f.read()

                    res = det.slide_match(target_bytes, background_bytes)

                    print(res)

                    # quit()

                    # 定位滑块并向右移动20像素（更健壮的实现，支持在iframe中查找）
                    def find_element_in_frames(driver, css_selectors=None, xpaths=None):
                        css_selectors = css_selectors or ['#captcha__frame__bottom .retryLink', 'button.retryLink', "[id*='captcha__frame__bottom'] button"]
                        xpaths = xpaths or ["//button[contains(@aria-label, 'Retry') or contains(normalize-space(.), 'Retry')]", "//button[contains(@class, 'retryLink')]"]
                        # 1. 在当前文档查找
                        for s in css_selectors:
                            try:
                                elems = driver.find_elements(By.CSS_SELECTOR, s)
                                if elems:
                                    return elems[0], None
                            except Exception:
                                pass
                        for xp in xpaths:
                            try:
                                elems = driver.find_elements(By.XPATH, xp)
                                if elems:
                                    return elems[0], None
                            except Exception:
                                pass

                        # 2. 遍历所有 iframe 并切换进去查找
                        frames_all = driver.find_elements(By.TAG_NAME, 'iframe')
                        for f in frames_all:
                            try:
                                driver.switch_to.frame(f)
                                for s in css_selectors:
                                    try:
                                        elems = driver.find_elements(By.CSS_SELECTOR, s)
                                        if elems:
                                            return elems[0], f
                                    except Exception:
                                        pass
                                for xp in xpaths:
                                    try:
                                        elems = driver.find_elements(By.XPATH, xp)
                                        if elems:
                                            return elems[0], f
                                    except Exception:
                                        pass
                            except Exception:
                                pass
                            finally:
                                try:
                                    driver.switch_to.default_content()
                                except Exception:
                                    pass
                        return None, None

                    def drag_element_right(driver, elem, frame, px=20):
                        try:
                            if frame is not None:
                                driver.switch_to.frame(frame)
                            # move to element and drag right by px
                            actions = ActionChains(driver)
                            # try to move to element center
                            actions.move_to_element(elem).click_and_hold().move_by_offset(int(px), 0).pause(0.05).release().perform()
                            print(f'向右拖动元素 {px} 像素完成')
                            return True
                        except Exception as e:
                            print('拖动元素失败:', e)
                            return False
                        finally:
                            try:
                                driver.switch_to.default_content()
                            except Exception:
                                pass


                    # 接着尝试定位滑块本体并向右移动 20px
                    slider_css = ['.sliderContainer .slider', '.sliderContainer .sliderIcon', '.slider', '.sliderTarget', '.sliderTargetIcon']
                    slider_xp = ["//div[contains(@class, 'slider')]//i", "//div[contains(@class,'sliderContainer')]//div[contains(@class,'slider')]"]
                    slider_elem, slider_frame = find_element_in_frames(driver, css_selectors=slider_css, xpaths=slider_xp)
                    if slider_elem:
                        print('找到滑块元素，执行向右 20px 移动')
                        moved_slider = drag_element_right(driver, slider_elem, slider_frame, px=res['target_x'])
                        print('滑块移动结果:', moved_slider)
                    else:
                        print('未找到滑块元素，跳过滑动')
                    if bg_path and block_path:
                        # 
                        pass
                    else:
                        print('✗ 未保存到验证码图片，无法匹配')
                    
                else:
                    print('no captcha found on page')
            except Exception as e:
                print('captcha automation failed:', e)
            finally:
                try:
                    driver.close()
                except Exception:
                    pass
        except Exception as e:
            print('load failed:', e)
