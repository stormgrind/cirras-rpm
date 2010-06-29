#!/bin/bash

[ -f /etc/sysconfig/rhq-cli ] && . /etc/sysconfig/rhq-cli

# check if rhq-cli is installed

[ ! -e $RHQ_CLI_HOME/rhq-remoting-cli-$RHQ_CLI_VERSION/bin/rhq-cli.sh ] && exit 1

# check if all variables are set

RHQ_SERVER_IP=127.0.0.1

[ "x$RHQ_SERVER_PORT" = "x" ]   && exit 1
[ "x$RHQ_CLI_HOME" = "x" ]      && exit 1
[ "x$RHQ_CLI_VERSION" = "x" ]   && exit 1
[ "x$RHQ_CLI_USERNAME" = "x" ]  && exit 1
[ "x$RHQ_CLI_PASSWORD" = "x" ]  && exit 1

export RHQ_CLI_JAVA_HOME=/usr/lib/jvm/jre-1.6.0

$RHQ_CLI_HOME/rhq-remoting-cli-$RHQ_CLI_VERSION/bin/rhq-cli.sh -u $RHQ_CLI_USERNAME -p $RHQ_CLI_PASSWORD -s $RHQ_SERVER_IP -t $RHQ_SERVER_PORT -f /usr/share/cirras-rhq/import-servers.js >> /var/log/cirras-rhq/import.log 2>&1