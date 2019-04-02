# slowcooker
ECE 4970 Capstone

to start web server:
  sudo python slowcooker_server

to start daemon:
  sudo run_daemon.sh
  
  web server needs to always be running to serve web traffic
  run_daemon runs the slowcooker_daemon.py every 10 seconds to update temperatures, alarms, etc.
