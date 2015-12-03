export MINION_NAMES="sir-lancelot sir-robin sir-galahad"
export MASTER_NAME="arthur"
export AWS_KEY_ID='XXX'
export AWS_KEY_SECRET='XXX'
export EC2_PEM_PATH="`pwd`/salt-demo.pem"
if test $1 = 'up'; then
    vagrant up $MASTER_NAME
    vagrant status $MASTER_NAME
    vagrant up
    for minion in $MINION_NAMES; do
        vagrant status $minion
    done
    vagrant ssh $MASTER_NAME --command "sudo salt-key --accept-all -y"
    vagrant ssh $MASTER_NAME --command "sudo salt '*' state.highstate"
else
    vagrant $@
fi
