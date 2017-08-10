# ansible-role-check-mk-agent [![Build Status](https://travis-ci.org/elnappo/ansible-role-check-mk-agent.svg?branch=master)](https://travis-ci.org/elnappo/ansible-role-check-mk-agent)
Installs check mk\_agent. Run it with xinetd or over SSH (default). Get more informations about check\_mk at [https://mathias-kettner.de/check_mk.html]()

## Requirements
Only testet with Ubuntu 14.04 and 16.04, should run on more platforms.

## Install
    $ ansible-galaxy install elnappoo.check-mk-agent

## Role Variables
* `check_mk_agent_deb_package: check-mk-agent_1.4.0p7-1_all.deb` Path to deb package
* `check_mk_agent_over_ssh: True`
* `check_mk_agent_with_sudo: False`
* `check_mk_agent_add_host_pubkey: False`
* `check_mk_agent_plugins_requirements_apt: []` Requirements for extra plugins (apt)
* `check_mk_agent_plugins_requirements_yum: []` Requirements for extra plugins (yum)
* `check_mk_agent_plugins: []` List of extra plugins to install
* `check_mk_agent_pubkey_file:` Path to SSH pubkey file

## Included check_mk extra plugins
* apache\_status
* db2\_mem
* dnsclient
* hpux\_lunstats
* hpux\_statgrab
* jar\_signature
* kaspersky\_av
* lnx\_quota
* mailman\_lists
* mk\_inventory.aix
* mk\_inventory.linux
* mk\_inventory.solaris
* mk\_jolokia
* mk\_logins
* mk\_logwatch
* mk\_logwatch\_aix
* mk\_mysql
* mk\_oracle
* mk\_oracle.aix
* mk\_oracle.solaris
* mk\_oracle\_asm
* mk\_oracle\_crs
* mk\_postgres
* mk\_sap
* mk\_tsm
* mk\_zypper
* netstat.aix
* netstat.linux
* nfsexports
* nfsexports.solaris
* nginx\_status
* plesk\_backups
* plesk\_domains
* runas
* smart
* symantec\_av
* unitrends\_backup
* unitrends\_replication
* vxvm
* websphere\_mq

## Dependencies
None.

## Example Playbook

```yaml
- hosts: servers
  remote_user: root
  roles:
     - { role: elnappoo.check-mk-agent, check_mk_agent_pubkey_file: omd_rsa.pub }
```

## License

MIT

## Author Information

elnappo <elnappo@nerdpol.io>

