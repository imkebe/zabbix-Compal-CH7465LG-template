# zabbix-Compal-CH7465LG-template
Python based Zabbix handler for Compal CH7645LG

1. Download dependencies
```
pip3 install py-zabbix connect_box
```
2. Edit ./compalsender.py variables (HOST, PASS, ZBXSRV, IP)
3. Put ./compalsender.py into CRON (or simillar) service. Define schedule (see https://crontab.guru/)
```
*/2 * * * * python3 /path/to/zabbix-Compal-CH7465LG-template/compalsender.py
```
3. Import zabbix-Compal-CH7465LG-template.xml to Zabbix.

# ToDo
[ ] Router/AP Mode
  [ ] Devices
  [ ] IP Configuration
  [ ] etc.
[ ] Configuration changes
[ ] Reboot/Factory Reset
