# ipchanges
This program checks your public IP. If it has changed since last check, it sends an email with the new IP as body of the message.
You will need to create a plain-text file called "iplog", which is where the IP is saved and compared. The file should be placed in the same folder of the script. (you can of course change path and file name, as long as you reflect that in the variables of the script).

If added as a crontab job, it can be an alternative to the DDNS. Particularly useful if you need to connect to your own router that does not have static IP.
