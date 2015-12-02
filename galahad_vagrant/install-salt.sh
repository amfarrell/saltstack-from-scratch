add-apt-repository ppa:saltstack/salt -y
apt-get update -y
apt-get install salt-minion -y
cp /etc/salt/minion /etc/salt/minion.bak
cat /etc/salt/minion.bak | sed 's/^#log_level_logfile:/log_level_logfile: info/' | sudo sed 's/^#master:\ salt/master: arthur/' > /etc/salt/minion
service salt-minion restart
