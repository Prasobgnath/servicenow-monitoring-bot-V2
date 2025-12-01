"""
Teams Messenger for Ticket Monitoring Bot
Handles all Microsoft Teams messaging functionality

Developer: Prasob G Nath
GitHub: github.com/Prasobgnath
"""

import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (
    ElementClickInterceptedException, TimeoutException, NoSuchElementException
)
import config
from utils import SoundNotifier


class TeamsMessenger:
    """Handles Microsoft Teams messaging operations"""
    
    def __init__(self, browser_manager, sound_notifier):
        self.browser = browser_manager
        self.driver = browser_manager.get_driver()
        self.wait = browser_manager.get_wait()
        self.sound_notifier = sound_notifier
        self.sent_messages = []
        self.reminder_count = 1
    
    def navigate_to_teams(self):
        """
        Navigate to Microsoft Teams with session validation
        
        Returns:
            bool - True if successful, False otherwise
        """
        try:
            # Check if browser session is still valid
            if not self.browser.is_session_valid():
                print("Browser crashed - attempting recovery...")
                if self.browser.recover_session():
                    # Update driver and wait references after recovery
                    self.driver = self.browser.get_driver()
                    self.wait = self.browser.get_wait()
                    print("Browser session recovered successfully")
                else:
                    print("Failed to recover browser session")
                    return False
            
            self.driver.get(config.TEAMS_URL)
            time.sleep(config.TIMEOUTS["teams_load"])
            return True
        except Exception as e:
            print(f"Error navigating to Teams: {e}")
            
            # Check if it's a session error (browser crashed) vs page error
            if "invalid session id" in str(e).lower() or not self.browser.is_session_valid():
                print("Browser crashed - recovering session...")
                if self.browser.recover_session():
                    self.driver = self.browser.get_driver()
                    self.wait = self.browser.get_wait()
                    try:
                        self.driver.get(config.TEAMS_URL)
                        time.sleep(config.TIMEOUTS["teams_load"])
                        print("Successfully navigated to Teams after browser recovery")
                        return True
                    except Exception as e2:
                        print(f"Failed to navigate after recovery: {e2}")
                        return False
            else:
                # It's likely a page/network issue, just refresh
                print("Teams page issue - refreshing...")
                try:
                    self.driver.refresh()
                    time.sleep(config.TIMEOUTS["teams_load"])
                    self.driver.get(config.TEAMS_URL)
                    time.sleep(config.TIMEOUTS["teams_load"])
                    print("Successfully navigated to Teams after page refresh")
                    return True
                except Exception as e3:
                    print(f"Failed to navigate after refresh: {e3}")
                    return False
    
    def wait_for_teams_load(self):
        """
        Wait for Teams to fully load and verify send_id is available
        
        Returns:
            bool - True if loaded, False otherwise
        """
        try:
            send_id_xpath = config.TEAMS_XPATHS["send_id"].format(config.TEAMS_SENT_ID)
            send_id = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, send_id_xpath))).text
            return send_id is not None
        except Exception as e:
            print(f"Error waiting for Teams to load: {e}")
            return False
    
    def select_chat(self):
        """
        Select the configured Teams chat/channel
        
        Returns:
            bool - True if successful, False otherwise
        """
        try:
            send_id_xpath = config.TEAMS_XPATHS["send_id"].format(config.TEAMS_SENT_ID)
            self.wait.until(EC.presence_of_element_located(
                (By.XPATH, send_id_xpath))).click()
            time.sleep(2)
            return True
        except ElementClickInterceptedException:
            self.driver.refresh()
            return False
        except Exception as e:
            print(f"Error selecting chat: {e}")
            return False
    
    def clear_draft_message(self):
        """Clear any existing draft message"""
        try:
            delete_button = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, config.TEAMS_XPATHS["delete_button"])))
            delete_button.click()
            
            discard_button = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, config.TEAMS_XPATHS["discard_button"])))
            discard_button.click()
            time.sleep(1)
        except Exception:
            # No draft to clear
            pass
    
    def get_message_box(self):
        """
        Get the Teams message input box
        
        Returns:
            WebElement - message input box element
        """
        return self.wait.until(EC.presence_of_element_located(
            (By.XPATH, config.TEAMS_XPATHS["type_message"])))
    
    def send_simple_message(self, message):
        """
        Send a simple text message
        
        Args:
            message: str - message to send
        """
        try:
            msg_box = self.get_message_box()
            msg_box.send_keys(message)
            time.sleep(1)
            msg_box.send_keys(Keys.ENTER)
            time.sleep(2)
            print(f"Message sent: {message}")
        except Exception as e:
            print(f"Error sending message: {e}")
    
    def enable_formatting(self):
        """Enable formatting options in Teams message box"""
        try:
            expand_button = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, config.TEAMS_XPATHS["expand_compose"])))
            expand_button.click()
            time.sleep(1)
        except Exception as e:
            print(f"Error enabling formatting: {e}")
    
    def enable_bold(self):
        """
        Enable bold formatting
        
        Returns:
            bool - True if successful, False otherwise
        """
        try:
            # Try primary bold button
            bold_button = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, config.TEAMS_XPATHS["bold_button"])))
            bold_button.click()
            return True
        except Exception:
            try:
                # Try alternative bold button
                bold_button_alt = self.wait.until(EC.presence_of_element_located(
                    (By.XPATH, config.TEAMS_XPATHS["bold_button_alt"])))
                bold_button_alt.click()
                return True
            except Exception:
                # Use keyboard shortcut as fallback
                try:
                    msg_box = self.get_message_box()
                    msg_box.send_keys(Keys.CONTROL, Keys.SHIFT, Keys.x)
                    msg_box.send_keys(Keys.CONTROL, Keys.b)
                    print("Bold enabled by keyboard shortcut")
                    return True
                except Exception as e:
                    print(f"Error enabling bold: {e}")
                    return False
    
    def send_formatted_tickets(self, ticket_list, use_bold=True):
        """
        Send list of tickets with formatting
        
        Args:
            ticket_list: list - list of ticket strings to send
            use_bold: bool - whether to use bold formatting
        """
        try:
            msg_box = self.get_message_box()
            
            if use_bold:
                self.enable_formatting()
                self.enable_bold()
            
            time.sleep(1)
            
            for ticket in ticket_list:
                msg_box.send_keys(ticket)
                msg_box.send_keys(Keys.ENTER)
                self.sent_messages.append(ticket)
                time.sleep(2)
            
            msg_box.send_keys(Keys.ENTER)
            time.sleep(1)
            
            # Send message
            try:
                send_button = self.wait.until(EC.presence_of_element_located(
                    (By.XPATH, config.TEAMS_XPATHS["send_button"])))
                send_button.click()
                print("Formatted tickets sent")
            except Exception:
                # Use keyboard shortcut as fallback
                msg_box.send_keys(Keys.CONTROL, Keys.ENTER)
                print("Formatted tickets sent by keyboard shortcut")
                
        except Exception as e:
            print(f"Error sending formatted tickets: {e}")
    
    def send_ticket_alert(self, greeting, important_list, normal_list, total_count):
        """
        Send complete ticket alert message to Teams
        
        Args:
            greeting: str - greeting message
            important_list: list - list of high priority/critical tickets
            normal_list: list - list of normal priority tickets
            total_count: str - total ticket count
        """
        try:
            # Play notification sound
            self.sound_notifier.play()
            
            # Navigate to Teams and wait for load
            self.navigate_to_teams()
            while not self.wait_for_teams_load():
                time.sleep(5)
                self.navigate_to_teams()
            
            # Select chat
            if not self.select_chat():
                return False
            
            # Clear any draft messages
            self.clear_draft_message()
            
            # Send greeting
            self.send_simple_message(greeting)
            
            # Send important tickets with bold formatting
            if important_list:
                print("Sending important tickets...")
                self.send_formatted_tickets(important_list, use_bold=True)
            
            # Send normal tickets
            if normal_list:
                print("Sending normal priority tickets...")
                msg_box = self.get_message_box()
                for ticket in normal_list:
                    msg_box.send_keys(ticket)
                    msg_box.send_keys(Keys.ALT, Keys.ENTER)
                    self.sent_messages.append(ticket)
                    time.sleep(1)
                msg_box.send_keys(Keys.ENTER)
                time.sleep(1)
            
            # Send total count
            total_message = f"Total active Tickets in queue: {total_count}"
            self.send_simple_message(total_message)
            
            # Reset reminder count after new message
            self.reminder_count = 1
            print("New ticket message sent successfully")
            return True
            
        except Exception as e:
            print(f"Error sending ticket alert: {e}")
            self.driver.refresh()
            return False
    
    def send_reminder(self, is_final=False):
        """
        Send reminder message
        
        Args:
            is_final: bool - whether this is the final reminder
            
        Returns:
            bool - True if successful, False otherwise
        """
        try:
            self.sound_notifier.play()
            self.navigate_to_teams()
            time.sleep(15)
            
            if not self.select_chat():
                return False
            
            msg_box = self.get_message_box()
            
            if is_final:
                message = config.MESSAGE_TEMPLATES["final_reminder"]
                self.reminder_count += 1
            else:
                message = config.MESSAGE_TEMPLATES["reminder"].format(self.reminder_count)
                self.reminder_count += 1
            
            msg_box.send_keys(message)
            time.sleep(1)
            msg_box.send_keys(Keys.ENTER)
            time.sleep(2)
            
            print(f"Reminder message sent: {message}")
            return True
            
        except Exception as e:
            print(f"Error sending reminder: {e}")
            self.driver.refresh()
            return False
    
    def handle_auth_banner(self):
        """Handle Teams authentication banner if present"""
        try:
            time.sleep(40)
            auth_banner = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, config.TEAMS_XPATHS["auth_banner"])))
            auth_banner.click()
            print("Auth success")
        except (ElementClickInterceptedException, NoSuchElementException, TimeoutException):
            print("Skipped auth")
    
    def should_send_message(self, current_tickets):
        """
        Determine if a message should be sent based on ticket comparison
        
        Args:
            current_tickets: list - current list of unassigned tickets
            
        Returns:
            str - "new" for new message, "reminder" for reminder, "skip" to skip
        """
        if not current_tickets:
            return "skip"
        
        # Compare with previously sent messages
        if set(current_tickets) != set(self.sent_messages):
            return "new"
        
        # Send reminders up to max count
        if self.reminder_count <= config.MAX_REMINDER_COUNT:
            return "reminder"
        
        return "skip"
    
    def reset_reminder_count(self):
        """Reset the reminder counter"""
        self.reminder_count = 1
    
    def get_sent_messages(self):
        """
        Get list of sent messages
        
        Returns:
            list - list of sent ticket messages
        """
        return self.sent_messages
