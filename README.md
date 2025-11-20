# Automated-gym-class-booker

# 🏋️‍♂️ Automated Gym Class Booker (Python + Selenium)

This project  streamlines the process of **logging into an online gym booking system** and **reserving classes**  (like Tuesday and Thursday sessions)  utilizing **Selenium WebDriver**. It  retrieves login credentials and the booking portal URL from a `.env` file,  automatically calculates target booking dates, and interacts with the website to log in,  reserve confirm reservations.

---

## 🚀 Overview

 Booking gym classes manually tedious and require timely action. This Python bot automates the  entire Securely loads gym website credentials from an `.env` file.  
2.  Automatically calculates the **next Tuesday and  Thursday**. 3. Launches Chrome, logs into the booking portal, and navigates to the  class schedule.  
4. Attempts to  reserve available classes for both target dates.  
5.  Confirms booked classes and  provides a clear summary.

> ⚠️ **Disclaimer:** This script is for educational and personal use only.  
> Ensure  that your use of aligns with your gym’s terms of service before  proceeding. ---

## 🧠 How It Works (Step-by-Step)

### 1. Configuration and Credentials
-  The credentials retrieved from the `.env` file: 

## This will be Summary output:

📆 Bookings attempted: 2
✅ Successful bookings: 2
⚠️ Already booked: 0
❌ Errors encountered: 0

## This is the Actual output looks like:

🤖 Starting the BULLETPROOF Gym Class Booker...

🚀 Launching Chrome Browser
🔐 Logging into the gym system.
✅ Logged in successfully.
🎯 Target dates for booking: ['12/11/2025', '14/11/2025']

📆 Attempting to book class for 12/11/2025...
✅ Successfully booked class for 12/11/2025

📆 Attempting to book class for 14/11/2025...
⚠️ Class on 14/11/2025 already booked.

📃 Verifying booked classes..
✅ Verification successful — classes found!

📃 BOOKING SUMMARY..

📆 Bookings attempted: 2
✅ Successful bookings: 1
⚠️ Already booked: 1
❌ Errors encountered: 0
=====================================
🏁 Automation completed! Browser will stay open for review.
