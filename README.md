# ansible-role-check-mk-agent [![Build Status](https://travis-ci.org/elnappo/ansible-role-check-mk-agent.svg?branch=master)](https://travis-ci.org/elnappo/ansible-role-check-mk-agent)
Installs check mk agent. Run it with xinit or over ssh (default). Get more informations about check mk at [https://mathias-kettner.de/check_mk.html]()

## Requirements
Only testet with Ubuntu and Debian, should run on more platforms.

## Role Variables
* `check_mk_agent_deb_package: check-mk-agent_1.2.4p5-2_all.deb`
* `check_mk_agent_over_ssh: True`
* `check_mk_agent_plugins_requirements: ["smartmontools"]` Requirements for extra plugins
* `check_mk_agent_plugins: ["smart", ]` List of extra plugins to install
* `check_mk_agent_pubkey_file:` Path to ssh pubkey file 

## Included check_mk extra plugins
* apache_status
* arc_raid_status.sh
* db2_mem.sh
* dmi_sysinfo
* dmraid
* j4p_performance
* jar_signature
* mailman_lists
* mk_jolokia
* mk_logwatch
* mk_mysql
* mk_oracle
* mk_oracle_asm
* mk_postgres
* mk_sap
* mk_tsm
* mk_zypper
* nfsexports
* plesk_backups
* plesk_domains
* resolve_hostname
* smart
* sylo
* vxvm_enclosures
* vxvm_multipath
* vxvm_objstatus

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
