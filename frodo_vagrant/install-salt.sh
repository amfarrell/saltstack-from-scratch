add-apt-repository ppa:saltstack/salt -y
apt-get update -y
apt-get install salt-minion salt-master -y
cp /etc/salt/master /etc/salt/master.bak
cat /etc/salt/master.bak | sed '413s/^#\ \ \ \ -\ \/srv\/salt/    - \/vagrant\/salt/' | sed '412s/^#//' | sudo sed '411s/^#//' > /etc/salt/master
service salt-master restart
cp /etc/salt/minion /etc/salt/minion.bak
cat /etc/salt/minion.bak | sudo sed 's/^#master:\ salt/master: frodo/' > /etc/salt/minion
service salt-minion restart
