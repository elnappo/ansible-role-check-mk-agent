import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_check_mk_agent_server_is_installed(host):
    check_mk_agent = host.package('check-mk-agent')

    assert check_mk_agent.is_installed


def test_check_mk_agent_socket_is_listening(host):
    assert host.socket("tcp://0.0.0.0:6556").is_listening
