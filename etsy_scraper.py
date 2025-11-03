class EtsyScraper:
    def __init__(self):
        """Initialize the scraper and set up the driver."""
        self.driver = self._init_driver()

    def _init_driver(self):
        """Initialize the web driver."""
        # Here you would initialize your web driver (e.g., Selenium)
        pass

    def open_page(self, url):
        """Open a specified URL."""
        self.driver.get(url)

    def scrape_product_page(self, product_url):
        """Scrape the product page for data."""
        self.open_page(product_url)
        # Logic for scraping product data goes here
        pass

    def print_all_selectors(self):
        """Print all available CSS selectors for the page elements."""
        # Logic for printing selectors goes here
        pass

    def close(self):
        """Close the web driver."""
        self.driver.quit()

    def __enter__(self):
        """Enter the runtime context related to this object."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the runtime context and clean up."""
        self.close()