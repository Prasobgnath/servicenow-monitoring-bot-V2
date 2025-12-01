"""
Utility functions for Ticket Monitoring Bot
Contains helper functions for logging, scope matching, and data handling

Developer: Prasob G Nath
GitHub: github.com/Prasobgnath
"""

import datetime
import winsound
import pandas as pd
from openpyxl import load_workbook
from fuzzywuzzy import process
import config


class LogManager:
    """Handles logging to Excel file"""
    
    def __init__(self, log_excel_path):
        self.log_excel_path = log_excel_path
        
    def get_unique_ids(self):
        """Get list of unique IDs from log file"""
        try:
            log_file = pd.read_excel(self.log_excel_path, sheet_name="log")
            return log_file['Unique ID'].values
        except Exception as e:
            print(f"Error reading log file: {e}")
            return []
    
    def log_ticket(self, ticket_data, instance):
        """
        Log ticket data to Excel file
        
        Args:
            ticket_data: dict containing ticket information
            instance: str - SNOW Instance 1, SNOW Instance 2, or other
        """
        try:
            wb = load_workbook(self.log_excel_path)
            log = wb.active
            
            # Prepare log data
            log_data = [
                ticket_data['number'],
                ticket_data['short_description'],
                ticket_data['affected_user'],
                ticket_data['priority'],
                datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S"),
                ticket_data['assignment_group'],
                ticket_data['type'],
                ticket_data['updated'],
                instance
            ]
            
            log.append(log_data)
            wb.save(self.log_excel_path)
            wb.close()
            print(f"Logged ticket: {ticket_data['number']}")
        except Exception as e:
            print(f"Error logging ticket: {e}")


class ScopeDetector:
    """Detects scope from ticket Short Description field using fuzzy matching with dynamic scopes"""
    
    def __init__(self, scope_data_dict, threshold=config.FUZZY_MATCH_THRESHOLD):
        """
        Initialize ScopeDetector with dynamic scope data
        
        Args:
            scope_data_dict: dict - Dictionary mapping scope names to node lists
                            Example: {'DNS': pd.Series([...]), 'PROXY': pd.Series([...])}
            threshold: int - Fuzzy matching threshold (default from config)
        """
        self.scope_data = scope_data_dict
        self.threshold = threshold
        self.scope_names = list(scope_data_dict.keys())
    
    def detect_scope(self, description):
        """
        Detect scope from Short Description field using fuzzy matching
        
        Args:
            description: str - ticket Short Description field content
            
        Returns:
            str - "<SCOPE_NAME> SCOPE" or "Unknown SCOPE"
        """
        best_match_score = 0
        best_scope = "Unknown SCOPE"
        
        # Try each scope and find the best match
        for scope_name, nodes in self.scope_data.items():
            if nodes.empty:
                continue
                
            match = process.extractOne(description, nodes)
            if match and match[1] > best_match_score and match[1] >= self.threshold:
                best_match_score = match[1]
                best_scope = f"{scope_name} SCOPE"
        
        return best_scope


class SoundNotifier:
    """Handles sound notifications"""
    
    def __init__(self, sound_file):
        self.sound_file = sound_file
    
    def play(self):
        """Play notification sound"""
        try:
            winsound.PlaySound(self.sound_file, 0)
        except Exception as e:
            print(f"Error playing sound: {e}")


def get_instance_name(url):
    """
    Determine instance name from URL
    
    Args:
        url: str - ServiceNow URL
        
    Returns:
        str - Instance name (SNOW Instance 1, SNOW Instance 2, or other)
    """
    if "instance1" in url.lower():
        return "SNOW Instance 1"
    elif "instance2" in url.lower():
        return "SNOW Instance 2"
    else:
        return "Unknown"


def get_ticket_type(url):
    """
    Determine ticket type from URL
    
    Args:
        url: str - ServiceNow URL
        
    Returns:
        str - Ticket type (incident, change_request, change_task)
    """
    if "incident" in url.lower():
        return "incident"
    elif "change_request" in url.lower():
        return "change_request"
    elif "change_task" in url.lower():
        return "change_task"
    else:
        return "unknown"


def format_ticket_display(ticket_data, scope=None):
    """
    Format ticket data for terminal display (includes assigned_to)
    
    Args:
        ticket_data: dict containing ticket information
        scope: str - optional scope information
        
    Returns:
        str - formatted ticket string
    """
    if scope:
        return "{:<11} : {:<15} : {:<15} : {:<20} : {:<20} : {:<15} : {} ".format(
            ticket_data['number'],
            ticket_data['priority'],
            ticket_data['state'],
            ticket_data['assignment_group'],
            ticket_data['assigned_to'],
            scope,
            ticket_data['short_description']
        )
    else:
        return "{:<11} : {:<15} : {:<15} : {:<20} : {:<20} : {:<15} : {} ".format(
            ticket_data['number'],
            ticket_data['priority'],
            ticket_data['state'],
            ticket_data['assignment_group'],
            ticket_data['assigned_to'],
            "Unknown SCOPE",
            ticket_data['short_description']
        )


def format_ticket_for_teams(ticket_data, scope=None):
    """
    Format ticket data for Teams message (excludes assigned_to)
    
    Args:
        ticket_data: dict containing ticket information
        scope: str - optional scope information
        
    Returns:
        str - formatted ticket string
    """
    if scope:
        return "{:<11} : {:<15} : {:<15} : {:<25} : {:<15} : {} ".format(
            ticket_data['number'],
            ticket_data['priority'],
            ticket_data['state'],
            ticket_data['assignment_group'],
            scope,
            ticket_data['short_description']
        )
    else:
        return "{:<11} : {:<15} : {:<15} : {:<25} : {:<15} : {} ".format(
            ticket_data['number'],
            ticket_data['priority'],
            ticket_data['state'],
            ticket_data['assignment_group'],
            "Unknown SCOPE",
            ticket_data['short_description']
        )


def load_inventory_data(inventory_excel_path, scope_columns=None):
    """
    Load scope node data from inventory Excel file dynamically
    
    Args:
        inventory_excel_path: str - path to inventory Excel file
        scope_columns: list - list of column names to load (default from config.SCOPE_COLUMNS)
        
    Returns:
        dict - Dictionary mapping scope names to pandas Series
               Example: {'DNS': pd.Series([...]), 'PROXY': pd.Series([...])}
    """
    if scope_columns is None:
        scope_columns = config.SCOPE_COLUMNS
    
    scope_data = {}
    
    try:
        data = pd.read_excel(inventory_excel_path)
        
        # Load each configured scope column
        for column in scope_columns:
            if column in data.columns:
                # Extract scope name from column name (e.g., 'DNS NODES' -> 'DNS')
                scope_name = column.replace(' NODES', '').strip()
                scope_data[scope_name] = data[column].dropna()  # Remove NaN values
                print(f"  [OK] Loaded {len(scope_data[scope_name])} nodes for {scope_name} scope")
            else:
                print(f"  [WARNING] Column '{column}' not found in inventory file")
        
        if not scope_data:
            print("  [WARNING] No scope columns were loaded from inventory")
            
    except Exception as e:
        print(f"  [ERROR] Error loading inventory data: {e}")
    
    return scope_data


def categorize_tickets(ticket_list):
    """
    Categorize tickets into high priority, critical, and normal
    
    Args:
        ticket_list: list of ticket strings
        
    Returns:
        dict - categorized tickets
    """
    categorized = {
        'critical': [],
        'high': [],
        'normal': [],
        'on_hold': [],
        'assigned': []
    }
    
    for ticket in ticket_list:
        if "1 - Critical" in ticket:
            categorized['critical'].append(ticket)
        elif "2 - High" in ticket:
            categorized['high'].append(ticket)
        elif "On Hold" in ticket:
            categorized['on_hold'].append(ticket)
        elif "Assigned" in ticket:
            categorized['assigned'].append(ticket)
        else:
            categorized['normal'].append(ticket)
    
    return categorized


def get_greeting_message(url):
    """
    Generate greeting message based on URL and ticket type
    
    Args:
        url: str - ServiceNow URL
        
    Returns:
        str - appropriate greeting message
    """
    instance = get_instance_name(url)
    ticket_type = get_ticket_type(url)
    
    key = f"{ticket_type}_{instance.lower()}"
    return config.MESSAGE_TEMPLATES.get(key, f"Hi Team, We Have Unassigned Tickets in {instance} Queue")


def print_ticket_summary(total_count, captured_count, hold_count, assigned_count, not_assigned_count):
    """
    Print summary of ticket counts
    
    Args:
        total_count: int - total tickets in queue
        captured_count: int - tickets captured by bot
        hold_count: int - tickets on hold
        assigned_count: int - assigned tickets
        not_assigned_count: int - unassigned tickets
    """
    print(f"Total Tickets Open: {total_count}")
    print(f"Total INC Captured = {captured_count}, On Hold = {hold_count}, "
          f"Assigned = {assigned_count}, Not Assigned = {not_assigned_count}")
    print(" ")
