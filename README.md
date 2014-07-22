This python script scrapes from specified websites for currently available psych studies. It sends an email if one is found that has not previously been available.

launchd is used to run the script every 30 minutes when the computer is on.



To install the launch daemon:
sudo cp com.lauren.psych.launchDaemon.plist /Library/LaunchDaemons
launchctl load -w /Library/LaunchDaemons/com.lauren.psych.launchDaemon.plist






To uninstall the launch daemon:
launchctl unload -w /Library/LaunchDaemons/com.lauren.psych.launchDaemon.plist
sudo rm /Library/LaunchDaemons/com.lauren.psych.launchDaemon.plist
