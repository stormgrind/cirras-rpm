#!/bin/sh

[ -f /etc/sysconfig/boxgrinder ]    && . /etc/sysconfig/boxgrinder
[ -f /etc/sysconfig/rhq ]           && . /etc/sysconfig/rhq
[ -f /etc/sysconfig/rhq-cli ]       && . /etc/sysconfig/rhq-cli

RHQ_SERVER_IP=127.0.0.1
RHQ_CLI_LOCATION=http://$RHQ_SERVER_IP:7080/client/download
RHQ_CLI_NAME=rhq-remoting-cli

rm -rf $RHQ_CLI_HOME
mkdir -p $RHQ_CLI_HOME

sleep=0
downloaded=0
while [ "$downloaded" = "0" ]; do
    sleep 5
    sleep=`expr $sleep + 5`

    http_code=`curl -o /dev/null -s -m 5 -w '%{http_code}' $RHQ_CLI_LOCATION`

    if [ $http_code -eq "200" ]
    then
        wget $RHQ_CLI_LOCATION -O $RHQ_CLI_HOME/$RHQ_CLI_NAME-$RHQ_CLI_VERSION.zip
        downloaded=1        
    fi
done

cd $RHQ_CLI_HOME
unzip $RHQ_CLI_NAME-$RHQ_CLI_VERSION.zip

# dirty fix
cp $RHQ_HOME/jbossas/server/default/deploy/rhq.ear/lib/rhq-core-client-api-$RHQ_VERSION.jar $RHQ_CLI_HOME/$RHQ_CLI_NAME-$RHQ_VERSION/lib/