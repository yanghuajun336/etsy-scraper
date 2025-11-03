from enum import Enum
from typing import Any, List
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

class SelectorType(Enum):
    CSS = 'css'
    XPATH = 'xpath'
    CLASS_NAME = 'class_name'
    ID = 'id'
    NAME = 'name'
    TAG_NAME = 'tag_name'
    LINK_TEXT = 'link_text'
    PARTIAL_LINK_TEXT = 'partial_link_text'
    ACCESSIBILITY_ID = 'accessibility_id'

class Selector:
    def __init__(self, driver: WebDriver, selector_type: SelectorType, selector_value: str):
        self.driver = driver
        self.selector_type = selector_type
        self.selector_value = selector_value

    def find(self) -> List[Any]:
        if self.selector_type == SelectorType.CSS:
            return self.driver.find_elements(By.CSS_SELECTOR, self.selector_value)
        elif self.selector_type == SelectorType.XPATH:
            return self.driver.find_elements(By.XPATH, self.selector_value)
        elif self.selector_type == SelectorType.CLASS_NAME:
            return self.driver.find_elements(By.CLASS_NAME, self.selector_value)
        elif self.selector_type == SelectorType.ID:
            return self.driver.find_elements(By.ID, self.selector_value)
        elif self.selector_type == SelectorType.NAME:
            return self.driver.find_elements(By.NAME, self.selector_value)
        elif self.selector_type == SelectorType.TAG_NAME:
            return self.driver.find_elements(By.TAG_NAME, self.selector_value)
        elif self.selector_type == SelectorType.LINK_TEXT:
            return self.driver.find_elements(By.LINK_TEXT, self.selector_value)
        elif self.selector_type == SelectorType.PARTIAL_LINK_TEXT:
            return self.driver.find_elements(By.PARTIAL_LINK_TEXT, self.selector_value)
        elif self.selector_type == SelectorType.ACCESSIBILITY_ID:
            return self.driver.find_elements(By.ACCESSIBILITY_ID, self.selector_value)
        else:
            raise ValueError("Invalid selector type")

    def get_text(self) -> List[str]:
        elements = self.find()
        return [element.text for element in elements]

    def get_attribute(self, attribute: str) -> List[str]:
        elements = self.find()
        return [element.get_attribute(attribute) for element in elements]

class SelectorLibrary:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.selectors = {
            "product_title": Selector(driver, SelectorType.CSS, ".product-title"),
            "product_price": Selector(driver, SelectorType.CSS, ".product-price"),
            "product_image": Selector(driver, SelectorType.CSS, ".product-image"),
            "shop_name": Selector(driver, SelectorType.CSS, ".shop-name"),
            "shop_rating": Selector(driver, SelectorType.CSS, ".shop-rating"),
            "product_description": Selector(driver, SelectorType.CSS, ".product-description"),
            "shop_link": Selector(driver, SelectorType.CSS, ".shop-link"),
            "cart_button": Selector(driver, SelectorType.CSS, ".cart-button"),
            "checkout_button": Selector(driver, SelectorType.CSS, ".checkout-button"),
            "wishlist_button": Selector(driver, SelectorType.CSS, ".wishlist-button"),
            "product_reviews": Selector(driver, SelectorType.CSS, ".product-reviews"),
        }
