"""
Main Entry Point for Ticket Monitoring Bot
Orchestrates all modules and manages the monitoring workflow

Developer: Prasob G Nath
GitHub: github.com/Prasobgnath
"""


import time
import config
from browser_manager import BrowserManager
from utils import LogManager, ScopeDetector, SoundNotifier, load_inventory_data
from teams_messenger import TeamsMessenger
from ticket_monitor import monitor_incident, monitor_change


def main():
    """Main function to run the monitoring bot"""
    
    print("=" * 70)
    print("TICKET MONITORING BOT - Starting Up")
    print("=" * 70)
    
    # Initialize components
    print("\n[1/6] Initializing Browser Manager...")
    browser_manager = BrowserManager()
    if not browser_manager.initialize_browser():
        print("Failed to initialize browser. Exiting.")
        return
    
    print("[2/6] Loading Inventory Data...")
    scope_data = load_inventory_data(config.INVENTORY_EXCEL)
    
    print("[3/6] Initializing Log Manager...")
    log_manager = LogManager(config.LOG_EXCEL)
    
    print("[4/6] Initializing Scope Detector...")
    scope_detector = ScopeDetector(scope_data)
    
    print("[5/6] Initializing Sound Notifier...")
    sound_notifier = SoundNotifier(config.SOUND_FILE)
    sound_notifier.play()
    
    print("[6/6] Initializing Teams Messenger...")
    teams_messenger = TeamsMessenger(browser_manager, sound_notifier)
    
    print("\n" + "=" * 70)
    print("Initialization Complete - Starting Monitoring Loop")
    print(f"Teams Messaging: {'ENABLED' if config.ENABLE_TEAMS_MESSAGING else 'DISABLED'}")
    print(f"SNOW Instance 1 Monitoring: {'ENABLED' if config.ENABLE_SNOW_INSTANCE_1_MONITORING else 'DISABLED'}")
    print(f"SNOW Instance 2 Monitoring: {'ENABLED' if config.ENABLE_SNOW_INSTANCE_2_MONITORING else 'DISABLED'}")
    print(f"Incident Monitoring: {'ENABLED' if config.ENABLE_INCIDENT_MONITORING else 'DISABLED'}")
    print(f"Change Monitoring: {'ENABLED' if config.ENABLE_CHANGE_MONITORING else 'DISABLED'}")
    print(f"CTASK Monitoring: {'ENABLED' if config.ENABLE_CTASK_MONITORING else 'DISABLED'}")
    print("=" * 70 + "\n")
    
    url_counter = 1
    
    try:
        while True:
            print(f"\n{'='*70}")
            print(f"MONITORING CYCLE #{url_counter}")
            print(f"{'='*70}\n")
            
            # ========== INCIDENT MONITORING ==========
            if config.ENABLE_INCIDENT_MONITORING:
                print(">>> Scanning for Incidents...")
                print("-" * 70)
                
                # Determine which incident URLs to use
                if url_counter == 1:
                    incident_urls = config.INCIDENT_URLS_FIRST_SCAN
                    print("First scan - checking today's resolved incidents and active tickets")
                else:
                    incident_urls = config.INCIDENT_URLS_SUBSEQUENT
                    print("Subsequent scan - checking assigned tickets")
                
                # Filter URLs based on instance monitoring settings
                filtered_incident_urls = [
                    url for url in incident_urls
                    if (config.ENABLE_SNOW_INSTANCE_1_MONITORING and "instance1" in url) or
                       (config.ENABLE_SNOW_INSTANCE_2_MONITORING and "instance2" in url)
                ]
                
                for idx, url in enumerate(filtered_incident_urls, 1):
                    instance = "SNOW Instance 1" if "instance1" in url else "SNOW Instance 2"
                    print(f"\n[Incident {idx}/{len(filtered_incident_urls)}] Monitoring {instance}...")
                    monitor_incident(browser_manager, log_manager, scope_detector, 
                                   teams_messenger, url)
            else:
                print(">>> Incident monitoring disabled - skipping")
            
            time.sleep(5)
            
            # ========== CHANGE REQUEST MONITORING ==========
            if config.ENABLE_CHANGE_MONITORING:
                print("\n>>> Scanning for Change Requests...")
                print("-" * 70)
                
                # Filter URLs based on instance monitoring settings
                filtered_change_urls = [
                    url for url in config.CHANGE_URLS
                    if (config.ENABLE_SNOW_INSTANCE_1_MONITORING and "instance1" in url) or
                       (config.ENABLE_SNOW_INSTANCE_2_MONITORING and "instance2" in url)
                ]
                
                for idx, url in enumerate(filtered_change_urls, 1):
                    instance = "SNOW Instance 1" if "instance1" in url else "SNOW Instance 2"
                    print(f"\n[Change {idx}/{len(filtered_change_urls)}] Monitoring {instance}...")
                    monitor_change(browser_manager, log_manager, scope_detector, 
                                 teams_messenger, url)
            else:
                print("\n>>> Change Request monitoring disabled - skipping")
            
            time.sleep(5)
            
            # ========== CHANGE TASK MONITORING ==========
            if config.ENABLE_CTASK_MONITORING:
                print("\n>>> Scanning for Change Tasks (CTASKs)...")
                print("-" * 70)
                
                # Filter URLs based on instance monitoring settings
                filtered_ctask_urls = [
                    url for url in config.CTASK_URLS
                    if (config.ENABLE_SNOW_INSTANCE_1_MONITORING and "instance1" in url) or
                       (config.ENABLE_SNOW_INSTANCE_2_MONITORING and "instance2" in url)
                ]
                
                for idx, url in enumerate(filtered_ctask_urls, 1):
                    instance = "SNOW Instance 1" if "instance1" in url else "SNOW Instance 2"
                    print(f"\n[CTASK {idx}/{len(filtered_ctask_urls)}] Monitoring {instance}...")
                    monitor_change(browser_manager, log_manager, scope_detector, 
                                 teams_messenger, url)
            else:
                print("\n>>> Change Task monitoring disabled - skipping")
            
            # ========== TEAMS AUTH HANDLING ==========
            if config.ENABLE_TEAMS_MESSAGING:
                print("\n>>> Returning to Teams...")
                teams_messenger.navigate_to_teams()
                teams_messenger.handle_auth_banner()
            else:
                print("\n>>> Teams messaging disabled - skipping Teams navigation")
            
            # ========== SLEEP BETWEEN CYCLES ==========
            print(f"\n{'='*70}")
            print(f"Monitoring cycle #{url_counter} completed")
            print(f"Waiting {config.TIMEOUTS['sleep_between_scans']} seconds before next cycle...")
            print(f"{'='*70}\n")
            
            url_counter += 1
            time.sleep(config.TIMEOUTS['sleep_between_scans'])
    
    except KeyboardInterrupt:
        print("\n\nKeyboard interrupt received - shutting down...")
    
    except Exception as e:
        print(f"\n\nUnexpected error occurred: {e}")
    
    finally:
        print("\nCleaning up...")
        browser_manager.close_browser()
        print("Bot shutdown complete")


if __name__ == "__main__":
    main()

