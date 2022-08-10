# Introduction
This is a crazy tool powered by python to capture your screen continuously, scan for QR Code, and take attendance automatically. So technically, you just need to run this script and keep your screen open, then your attendance will be taken.
Besides that, a 24/7 webserver is required for this to work, demo of this tools is hosted on replit at [here](sleepyattendix.josephlow5.repl.co/).


> **Note: You are not recommended to use this tool in actual study life.**
You may trigger the rate limit and get caught due to outdated packets, this resp is for education purpose only and will not be updated. 


***Please be a good and responsible student.***

# SleepyAttendix Flask Webserver
	1. Allow new user to register with username and password (as well as change password) 
	2. Take OTP attendance faster for all registered students when input is given
  Reference: [fastAttendix](https://github.com/jyyyyylim/fastAttendix/)
  
  
![image](https://user-images.githubusercontent.com/80668891/183865030-7914e4e1-7841-4afa-8805-59d7bd5d5d40.png)
![image](https://user-images.githubusercontent.com/80668891/183865078-f15b43af-1d4c-41a0-a26f-3107c68a103f.png)
![image](https://user-images.githubusercontent.com/80668891/183865130-7d3502b4-c418-4ea5-9046-aeda58ca9f19.png)

 # QR Attendance Monitor Scanner
    1. Continuously capture user screen 	
    2. Detect QR Code and convert into 3 digits OTP Codes 	
    3. Submit to SleepyAttendix Server when OTP Code is detected 
    4. Auto Hibernate to prevent overheat caused by constant screen capturing

![image](https://user-images.githubusercontent.com/80668891/183865475-bf95bd3d-4f4c-4224-810b-7832a62250f2.png)
