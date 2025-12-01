"""
Browser Manager for Ticket Monitoring Bot
Handles Chrome browser initialization, configuration, and basic operations

Developer: Prasob G Nath
GitHub: github.com/Prasobgnath
"""

import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    NoSuchElementException, TimeoutException, JavascriptException,
    ElementClickInterceptedException
)
import config


class BrowserManager:
    """Manages Chrome browser instance and operations"""
    
    def __init__(self):
        self.driver = None
        self.wait = None
        
    def setup_chrome_options(self):
        """
        Configure Chrome options based on config settings
        
        Returns:
            Options - configured Chrome options
        """
        opt = Options()
        
        # Apply options from config
        if config.CHROME_OPTIONS["headless"]:
            opt.add_argument("--headless")
        
        opt.add_argument(f"window-size={config.CHROME_OPTIONS['window_size']}")
        
        if config.CHROME_OPTIONS["incognito"]:
            opt.add_argument("--incognito")
        
        if config.CHROME_OPTIONS["ignore_certificate_errors"]:
            opt.add_argument('--ignore-certificate-errors')
        
        if config.CHROME_OPTIONS["ignore_ssl_errors"]:
            opt.add_argument('--ignore-ssl-errors')
        
        if config.CHROME_OPTIONS["disable_images"]:
            opt.add_argument('blink-settings=imagesEnabled=false')
        
        if config.CHROME_OPTIONS["disable_gpu"]:
            opt.add_argument("--disable-gpu")
        
        if config.CHROME_OPTIONS["no_sandbox"]:
            opt.add_argument("--no-sandbox")
        
        # User data directory - dedicated Selenium profile with copied Chrome profile
        opt.add_argument(f'--user-data-dir={config.CHROME_USER_DATA}')
        opt.add_argument('--profile-directory=Default')  # Use the copied Default profile
        
        # Fix for Chrome connection issues
        opt.add_argument("--remote-debugging-port=9222")
        opt.add_argument("--disable-dev-shm-usage")
        opt.add_argument("--disable-blink-features=AutomationControlled")
        # Extensions enabled to keep SSO extension
        opt.add_argument("--start-maximized")
        
        # Automation flags
        opt.add_experimental_option("excludeSwitches", ["enable-automation"])
        opt.add_experimental_option('useAutomationExtension', False)
        
        return opt
    
    def initialize_browser(self):
        """
        Initialize Chrome browser with configured options
        
        Returns:
            bool - True if successful, False otherwise
        """
        try:
            # Kill existing Chrome processes
            os.system("taskkill /f /im chrome.exe")
            time.sleep(2)
            
            # Setup Chrome options
            opt = self.setup_chrome_options()
            service = Service(config.CHROME_DRIVER_PATH)
            
            # Create driver instance
            self.driver = webdriver.Chrome(service=service, options=opt)
            self.driver.maximize_window()
            
            # Setup WebDriverWait
            self.wait = WebDriverWait(self.driver, config.TIMEOUTS["element_wait"])
            
            print("Browser initialized successfully")
            return True
            
        except Exception as e:
            print(f"Error initializing browser: {e}")
            return False
    
    def navigate_to_url(self, url, retry_count=3):
        """
        Navigate to URL with retry logic
        
        Args:
            url: str - URL to navigate to
            retry_count: int - number of retries on failure
            
        Returns:
            bool - True if successful, False otherwise
        """
        for attempt in range(retry_count):
            try:
                self.driver.get(url)
                time.sleep(config.TIMEOUTS["page_load"])
                return True
            except Exception as e:
                print(f"Navigation attempt {attempt + 1} failed: {e}")
                if attempt < retry_count - 1:
                    time.sleep(2)
                else:
                    return False
        return False
    
    def switch_to_snow_iframe(self):
        """
        Switch to ServiceNow main iframe using shadow DOM
        
        Returns:
            bool - True if successful, False otherwise
        """
        try:
            # Wait for shadow root to load
            time.sleep(3)
            
            # Get iframe from shadow DOM
            iframe = self.driver.execute_script(config.SNOW_XPATHS["iframe"])
            self.driver.switch_to.frame(iframe)
            return True
            
        except JavascriptException as e:
            print(f"Error switching to iframe: {e}")
            return False
    
    def refresh_page(self):
        """Refresh the current page"""
        try:
            self.driver.refresh()
            time.sleep(config.TIMEOUTS["page_load"])
        except Exception as e:
            print(f"Error refreshing page: {e}")
    
    def close_browser(self):
        """Close the browser and clean up"""
        try:
            if self.driver:
                self.driver.quit()
                print("Browser closed successfully")
        except Exception as e:
            print(f"Error closing browser: {e}")
    
    def get_driver(self):
        """
        Get the WebDriver instance
        
        Returns:
            WebDriver - Selenium WebDriver instance
        """
        return self.driver
    
    def get_wait(self):
        """
        Get the WebDriverWait instance
        
        Returns:
            WebDriverWait - Selenium WebDriverWait instance
        """
        return self.wait
    
    def is_session_valid(self):
        """
        Check if the current browser session is still valid
        
        Returns:
            bool - True if session is valid, False otherwise
        """
        if not self.driver:
            return False
        
        try:
            # Try to get current URL to verify session is alive
            _ = self.driver.current_url
            return True
        except Exception as e:
            print(f"Session validation failed: {e}")
            return False
    
    def recover_session(self):
        """
        Attempt to recover browser session if it's invalid
        
        Returns:
            bool - True if recovery successful, False otherwise
        """
        print("Attempting to recover browser session...")
        
        try:
            # Close any existing broken session
            if self.driver:
                try:
                    self.driver.quit()
                except Exception:
                    pass
            
            # Reinitialize browser
            return self.initialize_browser()
            
        except Exception as e:
            print(f"Error recovering session: {e}")
            return False


