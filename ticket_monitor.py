"""
Ticket Monitor for Ticket Monitoring Bot
Handles monitoring of incidents, changes, and change tasks in ServiceNow

Developer: Prasob G Nath
GitHub: github.com/Prasobgnath
"""

import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    NoSuchElementException, TimeoutException, StaleElementReferenceException,
    ElementClickInterceptedException, JavascriptException, WebDriverException
)
import config
from utils import (
    LogManager, ScopeDetector, get_instance_name, 
    format_ticket_display, format_ticket_for_teams, get_greeting_message
)


class TicketMonitor:
    """Monitors ServiceNow tickets and manages data collection"""
    
    def __init__(self, browser_manager, log_manager, scope_detector, teams_messenger):
        self.browser = browser_manager
        self.driver = browser_manager.get_driver()
        self.wait = browser_manager.get_wait()
        self.log_manager = log_manager
        self.scope_detector = scope_detector
        self.teams_messenger = teams_messenger
        self.scraped_tickets = []
    
    def check_if_empty(self):
        """
        Check if ticket list is empty
        
        Returns:
            bool - True if empty, False if tickets exist
        """
        try:
            empty_element = self.driver.execute_script(
                f"return document.querySelector('{config.SNOW_XPATHS['empty_list']}')"
            )
            return empty_element.text == "No records to display"
        except (NoSuchElementException, AttributeError):
            return False
    
    def get_total_count(self):
        """
        Get total count of tickets in queue
        
        Returns:
            str - total ticket count
        """
        try:
            total_element = self.wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, config.CSS_SELECTORS["total_rows"])))
            return self.driver.execute_script("return arguments[0].textContent;", total_element)
        except Exception as e:
            print(f"Error getting total count: {e}")
            return "0"
    
    def navigate_to_first_page(self):
        """Navigate to first page of results"""
        try:
            first_page = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, config.SNOW_XPATHS["first_page"])))
            first_page.click()
            time.sleep(5)
        except ElementClickInterceptedException:
            pass
        except Exception as e:
            print(f"Error navigating to first page: {e}")
    
    def read_table_rows(self, url, column_config):
        """
        Read all rows from current page
        
        Args:
            url: str - current URL for instance detection
            column_config: dict - column mappings for data extraction
            
        Returns:
            tuple - (ticket_data_list, important_list, normal_list)
        """
        ticket_data = []
        important_list = []
        normal_list = []
        
        try:
            tbody = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, config.SNOW_XPATHS["tbody"])))
            rows = tbody.find_elements(By.TAG_NAME, "tr")
            time.sleep(3)
            
            instance = get_instance_name(url)
            log_unique_ids = self.log_manager.get_unique_ids()
            
            for row in rows:
                try:
                    cells = row.find_elements(By.TAG_NAME, "td")
                    
                    # Extract ticket data based on column configuration
                    ticket = {
                        'number': cells[column_config['chg_number'] if 'chg_number' in column_config 
                                       else column_config['inc_number']].text.strip(),
                        'short_description': cells[column_config['short_description']].text.strip(),
                        'affected_user': cells[column_config['affected_user']].text.strip(),
                        'priority': cells[column_config['priority']].text.strip(),
                        'state': cells[column_config['state']].text.strip(),
                        'assignment_group': cells[column_config['assignment_group']].text.strip(),
                        'assigned_to': cells[column_config['assigned_to']].text.strip(),
                        'type': cells[column_config['type']].text.strip(),
                        'updated': cells[column_config['updated']].text.strip(),
                    }
                    
                    # Detect scope for this ticket
                    scope = self.scope_detector.detect_scope(ticket['short_description'])
                    
                    # Log ticket if not already logged
                    if ticket['number'] not in log_unique_ids:
                        self.log_manager.log_ticket(ticket, instance)
                    
                    # Format display string with scope
                    display_string = format_ticket_display(ticket, scope)
                    
                    # Skip if already in data
                    if display_string in ticket_data:
                        continue
                    
                    ticket_data.append(display_string)
                    
                    # Process unassigned tickets (check assignment_group)
                    if "(empty)" in ticket['assigned_to']:
                        formatted = format_ticket_for_teams(ticket, scope)
                        
                        # Categorize by priority
                        if "1 - Critical" in ticket['priority'] and ticket['number'] not in log_unique_ids:
                            if formatted not in important_list:
                                important_list.append(formatted)
                        elif "2 - High" in ticket['priority'] and ticket['number'] not in log_unique_ids:
                            if formatted not in important_list:
                                important_list.append(formatted)
                        else:
                            if ticket['number'] not in log_unique_ids and formatted not in normal_list:
                                if formatted not in important_list:
                                    normal_list.append(formatted)
                
                except IndexError:
                    # Skip rows with insufficient columns
                    continue
                except Exception as e:
                    print(f"Error processing row: {e}")
                    continue
            
        except Exception as e:
            print(f"Error reading table rows: {e}")
        
        return ticket_data, important_list, normal_list
    
    def paginate_and_collect(self, url, column_config):
        """
        Paginate through all pages and collect data
        
        Args:
            url: str - current URL
            column_config: dict - column mappings
            
        Returns:
            tuple - (all_ticket_data, all_important, all_normal)
        """
        all_ticket_data = []
        all_important = []
        all_normal = []
        
        try:
            # Get pagination elements
            next_button = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, config.SNOW_XPATHS["next_page"])))
            
            while True:
                try:
                    time.sleep(5)
                    
                    # Read current page
                    tickets, important, normal = self.read_table_rows(url, column_config)
                    
                    # Merge results
                    for t in tickets:
                        if t not in all_ticket_data:
                            all_ticket_data.append(t)
                    
                    for i in important:
                        if i not in all_important:
                            all_important.append(i)
                    
                    for n in normal:
                        if n not in all_normal:
                            all_normal.append(n)
                    
                    # Check if next button is enabled
                    if not next_button.is_enabled():
                        break
                    
                    next_button.click()
                    time.sleep(5)
                    
                    # Re-find next button after page change
                    next_button = self.wait.until(EC.presence_of_element_located(
                        (By.XPATH, config.SNOW_XPATHS["next_page"])))
                    
                except StaleElementReferenceException:
                    print("Stale element exception - refreshing page")
                    self.driver.refresh()
                    time.sleep(10)
                    break
                except Exception as e:
                    print(f"Error during pagination: {e}")
                    break
        
        except Exception as e:
            print(f"Error in pagination setup: {e}")
        
        return all_ticket_data, all_important, all_normal
    
    def monitor_tickets(self, url, column_config):
        """
        Main monitoring function for tickets
        
        Args:
            url: str - ServiceNow URL to monitor
            column_config: dict - column mappings (INCIDENT_COLUMNS or CHANGE_COLUMNS)
        """
        try:
            # Navigate to URL with retry
            retry_count = 0
            while retry_count < 3:
                try:
                    self.driver.get(url)
                    time.sleep(config.TIMEOUTS["page_load"])
                    
                    # Verify shadow root is accessible
                    self.driver.execute_script(config.SNOW_XPATHS["shadow_root"])
                    break
                except JavascriptException:
                    print("Network error - refreshing window")
                    self.driver.refresh()
                    retry_count += 1
                    time.sleep(5)
            
            # Switch to iframe
            if not self.browser.switch_to_snow_iframe():
                print("Failed to switch to iframe")
                return
            
            # Check if queue is empty
            if self.check_if_empty():
                print("No tickets in queue")
                self.teams_messenger.navigate_to_teams()
                return
            
            # Get total count
            total_count = self.get_total_count()
            print(f"Total Tickets Open: {total_count}\n")
            
            # Print header
            print("{:<11} : {:<15} : {:<15} : {:<20} : {:<20} : {:<15} : {} ".format(
                "Number", "Priority", "State", "Assignment Group", "Assigned_to", "Scope", "Short Description"))
            
            # Navigate to first page
            self.navigate_to_first_page()
            
            # Collect all ticket data
            all_tickets, important_list, normal_list = self.paginate_and_collect(url, column_config)
            
            # Navigate back to first page
            self.navigate_to_first_page()
            
            # Print collected tickets
            hold_count = 0
            assigned_count = 0
            
            for ticket in all_tickets:
                print(ticket)
                if "On Hold" in ticket:
                    hold_count += 1
                if "Assigned" in ticket:
                    assigned_count += 1
            
            not_assigned_count = len(important_list) + len(normal_list)
            print(f"Total INC Captured = {len(all_tickets)}, On Hold = {hold_count}, "
                  f"Assigned = {assigned_count}, Not Assigned = {not_assigned_count}")
            print(" ")
            
            # Add to scraped list
            for ticket in important_list + normal_list:
                if ticket not in self.scraped_tickets:
                    self.scraped_tickets.append(ticket)
            
            # Send message if there are unassigned tickets
            if important_list or normal_list:
                action = self.teams_messenger.should_send_message(self.scraped_tickets)
                greeting = get_greeting_message(url)
                
                if config.ENABLE_TEAMS_MESSAGING:
                    if action == "new":
                        self.teams_messenger.send_ticket_alert(
                            greeting, important_list, normal_list, total_count)
                    elif action == "reminder":
                        is_final = (self.teams_messenger.reminder_count == config.MAX_REMINDER_COUNT)
                        self.teams_messenger.send_reminder(is_final)
                    else:
                        print("Reminder limit reached - no message sent")
                else:
                    print("Teams messaging disabled - alerts logged but not sent to Teams")
                    self.teams_messenger.navigate_to_teams()
            else:
                self.teams_messenger.navigate_to_teams()
        
        except (JavascriptException, TimeoutException, NameError, 
                WebDriverException, UnicodeDecodeError, UnicodeEncodeError) as e:
            print(f"Error in ticket monitoring: {e}")
            time.sleep(3)


def monitor_incident(browser_manager, log_manager, scope_detector, teams_messenger, url):
    """
    Monitor incidents using INCIDENT_COLUMNS configuration
    
    Args:
        browser_manager: BrowserManager instance
        log_manager: LogManager instance
        scope_detector: ScopeDetector instance
        teams_messenger: TeamsMessenger instance
        url: str - incident URL to monitor
    """
    monitor = TicketMonitor(browser_manager, log_manager, scope_detector, teams_messenger)
    monitor.monitor_tickets(url, config.INCIDENT_COLUMNS)


def monitor_change(browser_manager, log_manager, scope_detector, teams_messenger, url):
    """
    Monitor changes/change tasks using CHANGE_COLUMNS configuration
    
    Args:
        browser_manager: BrowserManager instance
        log_manager: LogManager instance
        scope_detector: ScopeDetector instance
        teams_messenger: TeamsMessenger instance
        url: str - change URL to monitor
    """
    monitor = TicketMonitor(browser_manager, log_manager, scope_detector, teams_messenger)
    monitor.monitor_tickets(url, config.CHANGE_COLUMNS)
