BytePedaler's WeatherPi

Thanks for stopping by! In July 2024 I started this dream project of mine 
with some very rough python script. While the code is undoubtedly still 
rough, the progress has been steady and I've been learning a ton in the 
process! The goal of this project is to gather hyperlocal weather data. 
Currently, the focus is primarily on weather trends in the downtown 
Portland, Oregon area.

Current terminal initialization procedure:
1. Create systemd service:
    sudo nano /etc/systemd/system/weatherpi.service
2. systemd input:
    [Unit]
    Description=WeatherPi Sensor Service
    After=network.target

    [Service]
    ExecStart=/usr/bin/python3 /home/[ENTER_USER_NAME]/weatherPi/code/main.py
    WorkingDirectory=/home/[ENTER_USER_NAME]/weatherPi/code
    StandardOutput=append:/home/[ENTER_USER_NAME]/weatherPi/log.txt
    StandardError=append:/home/[ENTER_USER_NAME]/weatherPi/error.txt
    Restart=always
    User=[ENTER_USER_NAME]

    [Install]
    WantedBy=multi-user.target
3. Enable the service and start:
    sudo systemctl daemon-reload
    sudo systemctl enable weatherpi.service
    sudo systemctl start weatherpi.service
4. (Optional): Check status of service:
    sudo systemctl status weatherpi.service

5. To enable auto-update from GitHub Repo:
    chmod +x ~/weatherPi/update.sh

    Then open your crontab:
        crontab -e

    Then add this line:
        0 * * * * /home/$USER/weatherPi/update.sh



Upcoming updates:
1. Fix for gas sensor (currently not outputting correctly).
2. Cleaner data presentation in CSV.
3. Fix for timing delay causing missed reading every 15th recording.
4. Improved data recording accuracy.




Old version:
Previous terminal initialization procedure:
1. cd weatherpi/
2. cd weatherPi/
3. ls
4. python3 main.py