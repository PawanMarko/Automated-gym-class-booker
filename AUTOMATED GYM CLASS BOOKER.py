# DAY 49!!

"""AUTOMATED GYM CLASS BOOKER"""

# Author: Marko 😎
# Description:
#   Automates login, finds the next Tuesday & Thursday,
#   books classes, verifies them, retries on failure, and prints summary.

#----------IMPORTS------------
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from time import sleep

#---------CONFIGURATION CLASS------------

class Config:
  """Handels enviroment variables and browser configurations."""
  def __init__(self):
    load_dotenv(dotenv_path=r"C:\Users\Pawan Marko\Documents\Coding\Python\.envgym.txt")
    
    self.GYM_URL = os.getenv("GYM_URL")
    self.GYM_USERNAME = os.getenv("GYM_USERNAME")
    self.GYM_PASSWORD = os.getenv("GYM_PASSWORD")
    
    if not all([self.GYM_URL, self.GYM_USERNAME, self.GYM_PASSWORD]):
      raise ValueError("⚠️ Missing credentials in .env ffile. Check your setup..") 
    
    
    
#---------------DATE CALCUULATION------------

def get_next_tuesday_thursday():
  """Calculate next Tuesday and Thursday from today.."""
  today = datetime.today()
  days = {"Tuesday": (1 - today.weekday()) % 7, "Thursday": (3 - today.weekday()) % 7}
  next_tuesday = today + timedelta(days=days["Tuesday"])
  next_thursday = today + timedelta(days=days["Thursday"])
  return [next_tuesday.strftime("%d/%m/%Y"), next_thursday.strftime("%d/%m/%Y")]


# GYM BOT CLASS...(The main class that controls the browser and booking logic.)

class GymBot:
  def __init__(self, config: Config):
    self.config = config
    self.driver = None
    self.wait = None
    self.booking_attempted = 0
    self.booking_successful = 0
    self.already_booked_count = 0
    self.errors = 0
  
  # BROWSER SETUP..
  def start_browser(self):
    """Initialize Chrome with custom settings.."""
    print("🚀 Launching Chrome Browser")
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True) # keep open after script
    chrome_options.add_argument("--start-maximized") 
    
    self.driver = webdriver.Chrome(options=chrome_options)
    self.wait = WebDriverWait(self.driver, 20)
    
    
  # RETRY Utility...
  
  def retry_action(self, func, retries=3, delay=2, description="Actions"):
    """Retries a given function if it fails (up to 3 times)."""
    for attempt in  range(1, retries + 1):
      try:
        return func()
      except (TimeoutException, NoSuchElementException, WebDriverException) as e:
        print(f"⚠️ {description} failed (attempt {attempt}/{retries}): {e}")
        sleep(delay)      
    print(f"❌ {description} ultimately failed after {retries} retries..")
    self.errors += 1
    return None
  
  # LOGIN.
  
  def login(self):
    """Logs into the gym system."""
    print("🔐 Logging into the gym system.")
    self.driver.get(self.config.GYM_URL)
    
    def perform_login():
      username_input = self.wait.until(EC.presence_of_element_located((By.ID, "email")))
      password_input = self.driver.find_element(By.ID, "password")
      login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
      username_input.send_keys(self.config.GYM_USERNAME)
      password_input.send_keys(self.config.GYM_PASSWORD)
      login_button.click()
      self.wait.until(EC.presence_of_element_located((By.XPATH, "/h2[contains(text(),'Welcome')]")))
      
    self.retry_action(perform_login, description="Login")
    print("✅ Loggrd in successfully.")
    
  # BOOK CLASS.
  
  def book_class(self, target_date):
    """Attempts to book a class for the given date."""
    self.booking_attempted += 1 
    print(f"\n📆 Attempting to book class for {target_date}...")
    
    def perform_booking():
      # Go to booking page.
      schedule_link = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Book Classes")))
      schedule_link.click()
      self.wait.until(EC.presence_of_element_located((By.ID, "class-schedule")))
      
      # Find the date cell
      date_element = self.driver.find_element(By.XPATH, f"//td[contains(text(), '{target_date}')]")
      date_element.click()
      sleep(2)
      
      # Click book now button if avaiable
      try:
        book_button = self.driver.find_element(By.XPATH, "//button[contains(text(),'Book Now')]")
        book_button.click()
        print(f"✅ Successfully booked class for {target_date}")
        self.booking_successful +=1 
        
      except NoSuchElementException:
        print(f"⚠️ Class on {target_date} already booked.")
        self.already_booked_count +=1 
    self.retry_action(perform_booking, description=f"Booking for {target_date}")

  # Verification.
  def verify_booking(self):
    """Verifies that booked classes apper on the 'My Booking' page."""
    print("\n📃 Verifying booked classes..")
    
    def perform_verification():
      my_booking_link = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "My Bookings")))
      my_booking_link.click()
      sleep(2)
      
      if "Booked" in self.driver.page_source:
        print("✅ Verification successful — classes found!")
      else:
        print("⚠️ No booking found in verification.")
    self.retry_action(perform_verification, description="Booking Verification")
    
  # Summary..
  def summary(self):
    print("\n=========📃 BOOKING SUMARY =========")
    print(f"📆 Bookings attempted: {self.booking_attempted}")
    print(f"✅ Successful bookings: {self.booking_successful}")
    print(f"⚠️ Already booked: {self.already_booked_count}")
    print(f"❌ Errors encountered: {self.errors}")
    print("=====================================")
    print("🏁 Automated completed! Brower will stay open for review.")
    
    
# MAIN EXEUCTION..

if __name__ == "__main__":
  print("🤖 Starting the BULLETPROOF Gym Class Booker...\n")
  
  config= Config()
  bot = GymBot(config)
  
  bot.start_browser()
  bot.login()
  
  target_dates = get_next_tuesday_thursday()
  print(f"🎯 Target dates for booking: {target_dates}")
  
  for date in target_dates:
    bot.book_class(date)
    
  bot.verify_booking()
  bot.summary()
  
#  COMPLETED!!