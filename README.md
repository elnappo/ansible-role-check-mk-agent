# ansible-role-check-mk-agent
[![Build Status](https://travis-ci.org/elnappo/ansible-role-check-mk-agent.svg?branch=master)](https://travis-ci.org/elnappo/ansible-role-check-mk-agent) [![Ansible Galaxy](https://img.shields.io/badge/galaxy-elnappo.check--mk--agent-blue.svg?style=flat)](https://galaxy.ansible.com/elnappo/check-mk-agent/)

Installs check mk\_agent. Run it with systemd-socket, SSH with sudo or SSH as root (default). Get more information about check\_mk at [https://mathias-kettner.de/check_mk.html]()

## Features
* Install check_mk agent
* Query check_mk agent over systemd-socket (only with check_mk_agent >= v1.4), SSH as root or SSH with sudo
* Setup firewall if systemd-socket ist used (ufw or firewalld)
* Add SSH host key to check_mk server
* Install check_mk agent plugins/local checks and their dependencies
* **Add hosts to check_mk server via WATO API**

## Requirements
* Python requests >= v2.5.0

Tested on Ubuntu 16.04, 18.04 and CentOS 7, should also run under Debian and RedHat.

## Install
    $ ansible-galaxy install elnappo.check_mk_agent

## Role Variables
* `check_mk_agent_over_ssh: true`
* `check_mk_agent_over_xinetd: false`
* `check_mk_agent_with_sudo: false` Adds a user which is allowed to run check_mk_agent with sudo
* `check_mk_agent_add_host_pubkey: false` Import SSH host keys into your check_mk servers known_hosts file
* `check_mk_agent_monitoring_host:` Hostname of your check_mk server
* `check_mk_agent_monitoring_user:` Username under which your check_mk instance runs
* `check_mk_agent_plugins_requirements: []` Requirements for extra plugins
* `check_mk_agent_plugins: []` List of extra plugins to install
* `check_mk_agent_local_checks: {}`
* `check_mk_agent_pubkey_file:` Path to SSH pubkey file
* `check_mk_agent_add_to_wato: false`
* `check_mk_agent_monitoring_host_folder: ""`
* `check_mk_agent_monitoring_host_discovery_mode: new`
* `check_mk_agent_monitoring_host_url:`
* `check_mk_agent_monitoring_host_wato_username:`
* `check_mk_agent_monitoring_host_wato_secret:`
* `check_mk_agent_setup_firewall: true` Add firewall rule (ufw/firewalld) when using systemd-socket or xinetd
* `check_mk_agent_manual_install: false` Leave agent package installation to the user

## Included check_mk extra plugins
Could be found under `files/plugins/`. As it is hard to keep these plugins
up-to-date, these will be removed in a future version from the repository.


## Dependencies
None.

## Example Playbook

```yaml
- hosts: servers
  vars:
    check_mk_agent_pubkey_file: omd_rsa.pub
    check_mk_agent_add_host_pubkey: true
    check_mk_agent_monitoring_host: checkmk.example.com
    check_mk_agent_monitoring_user: monitoring
    check_mk_agent_add_to_wato: true
    check_mk_agent_monitoring_host_url: http://cmk.example.com/monitoring/
    check_mk_agent_monitoring_host_wato_username: ansible
    check_mk_agent_monitoring_host_wato_secret: 7JTuBt6nETYHG1GS
    check_mk_agent_local_checks:
      filecount:
        src: files/check_mk_local_checks/filecount
        cache_time: 600
      filestat:
        src: files/check_mk_local_checks/filestat
    check_mk_agent_plugins:
      - name: smart
        asynchronous: 300
      - name: mk_apt
        asynchronous: 86400
      - name: lvm


  roles:
     - elnappo.check_mk_agent
```

### Asynchronous plug-in execution

Checkmk is able to manage Asynchronous execution of plug-ins, [More information in checkmk documentation](https://checkmk.com/cms_agent_linux.html#Asynchronous%20execution)

To use plug-in in Asynchronous, need to add asynchronous information like with
```
check_mk_agent_plugins:
  - name: smart
    asynchronous: 300
```


## License

MIT

## Author Information

elnappo <elnappo@nerdpol.io>
