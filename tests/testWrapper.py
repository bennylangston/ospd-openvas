# -*- coding: utf-8 -*-
# Copyright (C) 2018 Greenbone Networks GmbH
#
# SPDX-License-Identifier: GPL-2.0-or-later
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA

""" Unit Test for ospd-openvas """

import unittest
from unittest.mock import patch
from ospd_openvas.wrapper import OSPD_PARAMS
from tests.dummywrapper import DummyWrapper

OSPD_PARAMS_OUT = {
    'auto_enable_dependencies': {
        'type': 'boolean',
        'name': 'auto_enable_dependencies',
        'default': 1,
        'mandatory': 1,
        'description': 'Automatically enable the plugins that are depended on',
    },
    'cgi_path': {
        'type': 'string',
        'name': 'cgi_path',
        'default': '/cgi-bin:/scripts',
        'mandatory': 1,
        'description': 'Look for default CGIs in /cgi-bin and /scripts',
    },
    'checks_read_timeout': {
        'type': 'integer',
        'name': 'checks_read_timeout',
        'default': 5,
        'mandatory': 1,
        'description': 'Number  of seconds that the security checks will ' \
                       'wait for when doing a recv()',
    },
    'drop_privileges': {
        'type': 'boolean',
        'name': 'drop_privileges',
        'default': 0,
        'mandatory': 1,
        'description': '',
    },
    'network_scan': {
        'type': 'boolean',
        'name': 'network_scan',
        'default': 0,
        'mandatory': 1,
        'description': '',
    },
    'non_simult_ports': {
        'type': 'string',
        'name': 'non_simult_ports',
        'default': '22',
        'mandatory': 1,
        'description': 'Prevent to make two connections on the same given ' \
                       'ports at the same time.',
    },
    'open_sock_max_attempts': {
        'type': 'integer',
        'name': 'open_sock_max_attempts',
        'default': 5,
        'mandatory': 0,
        'description': 'Number of unsuccessful retries to open the socket ' \
                       'before to set the port as closed.',
    },
    'timeout_retry': {
        'type': 'integer',
        'name': 'timeout_retry',
        'default': 5,
        'mandatory': 0,
        'description': 'Number of retries when a socket connection attempt ' \
                       'timesout.',
    },
    'optimize_test': {
        'type': 'integer',
        'name': 'optimize_test',
        'default': 5,
        'mandatory': 0,
        'description': 'By default, openvassd does not trust the remote ' \
                       'host banners.',
    },
    'plugins_timeout': {
        'type': 'integer',
        'name': 'plugins_timeout',
        'default': 5,
        'mandatory': 0,
        'description': 'This is the maximum lifetime, in seconds of a plugin.',
    },
    'report_host_details': {
        'type': 'boolean',
        'name': 'report_host_details',
        'default': 1,
        'mandatory': 1,
        'description': '',
    },
    'safe_checks': {
        'type': 'boolean',
        'name': 'safe_checks',
        'default': 1,
        'mandatory': 1,
        'description': 'Disable the plugins with potential to crash ' \
                       'the remote services',
    },
    'scanner_plugins_timeout': {
        'type': 'integer',
        'name': 'scanner_plugins_timeout',
        'default': 36000,
        'mandatory': 1,
        'description': 'Like plugins_timeout, but for ACT_SCANNER plugins.',
    },
    'time_between_request': {
        'type': 'integer',
        'name': 'time_between_request',
        'default': 0,
        'mandatory': 0,
        'description': 'Allow to set a wait time between two actions ' \
                       '(open, send, close).',
    },
    'unscanned_closed': {
        'type': 'boolean',
        'name': 'unscanned_closed',
        'default': 1,
        'mandatory': 1,
        'description': '',
    },
    'unscanned_closed_udp': {
        'type': 'boolean',
        'name': 'unscanned_closed_udp',
        'default': 1,
        'mandatory': 1,
        'description': '',
    },
    'use_mac_addr': {
        'type': 'boolean',
        'name': 'use_mac_addr',
        'default': 0,
        'mandatory': 0,
        'description': 'To test the local network. ' \
                       'Hosts will be referred to by their MAC address.',
    },
    'vhosts': {
        'type': 'string',
        'name': 'vhosts',
        'default': '',
        'mandatory': 0,
        'description': '',
    },
    'vhosts_ip': {
        'type': 'string',
        'name': 'vhosts_ip',
        'default': '',
        'mandatory': 0,
        'description': '',
    },
}


@patch('ospd_openvas.db.OpenvasDB')
@patch('ospd_openvas.nvticache.NVTICache')
class TestOspdOpenvas(unittest.TestCase):

    @patch('ospd_openvas.wrapper.subprocess')
    def test_redis_nvticache_init(self, mock_subproc, mock_nvti, mock_db):
        mock_subproc.check_call.return_value = True
        w = DummyWrapper(mock_nvti, mock_db)
        w.redis_nvticache_init()
        self.assertEqual(mock_subproc.check_call.call_count, 1)

    @patch('ospd_openvas.wrapper.subprocess')
    def test_parse_param(self, mock_subproc, mock_nvti, mock_db):

        mock_subproc.check_output.return_value = \
            'non_simult_ports = 22'.encode()
        w =  DummyWrapper(mock_nvti, mock_db)
        w.parse_param()
        self.assertEqual(mock_subproc.check_output.call_count, 1)
        self.assertEqual(OSPD_PARAMS, OSPD_PARAMS_OUT)

    def test_load_vts(self, mock_nvti, mock_db):
        w =  DummyWrapper(mock_nvti, mock_db)
        w.load_vts()
        self.maxDiff = None
        self.assertEqual(w.vts, w.VT)

    def test_get_custom_xml(self, mock_nvti, mock_db):
        out = '<custom><required_ports>Services/www, 80</re' \
              'quired_ports><category>3</category><' \
              'excluded_keys>Settings/disable_cgi_s' \
              'canning</excluded_keys><family>Produ' \
              'ct detection</family><filename>manti' \
              's_detect.nasl</filename><timeout>0</' \
              'timeout></custom>'
        w =  DummyWrapper(mock_nvti, mock_db)
        vt = w.VT['1.3.6.1.4.1.25623.1.0.100061']
        res = w.get_custom_vt_as_xml_str(
            '1.3.6.1.4.1.25623.1.0.100061',
            vt.get('custom'))
        self.assertEqual(len(res), len(out))

    def test_get_severities_xml(self, mock_nvti, mock_db):
        w =  DummyWrapper(mock_nvti, mock_db)
        out = '<severities><severity type="cvss_base_v2">' \
              'AV:N/AC:L/Au:N/C:N/I:N/A:N</severity></severities>'
        vt =w.VT['1.3.6.1.4.1.25623.1.0.100061']
        severities = vt.get('severities')
        res = w.get_severities_vt_as_xml_str(
            '1.3.6.1.4.1.25623.1.0.100061', severities)

        self.assertEqual(res, out)

    def test_get_params_xml(self, mock_nvti, mock_db):
        w =  DummyWrapper(mock_nvti, mock_db)
        out = '<vt_params><vt_param type="checkbox" id="Do not randomize the  ' \
              'order  in  which ports are scanned"><name>Do not ran' \
              'domize the  order  in  which ports are scanned</name' \
              '><default>no</default></vt_param><vt_param type="ent' \
              'ry" id="Data length : "><name>Data length : </name><' \
              '/vt_param></vt_params>'

        vt = w.VT['1.3.6.1.4.1.25623.1.0.100061']
        params = vt.get('vt_params')
        res = w.get_params_vt_as_xml_str(
            '1.3.6.1.4.1.25623.1.0.100061', params)
        self.assertEqual(len(res), len(out))

    def test_get_refs_xml(self, mock_nvti, mock_db):
        w =  DummyWrapper(mock_nvti, mock_db)
        out = '<vt_refs><ref type="url" id="http://www.mantisbt.org/"/>' \
              '</vt_refs>'
        vt = w.VT['1.3.6.1.4.1.25623.1.0.100061']
        refs = vt.get('vt_refs')
        res = w.get_refs_vt_as_xml_str(
            '1.3.6.1.4.1.25623.1.0.100061', refs)

        self.assertEqual(res, out)

    def test_get_dependencies_xml(self, mock_nvti, mock_db):
        w =  DummyWrapper(mock_nvti, mock_db)
        out = '<dependencies><dependency vt_id="1.2.3.4"/><dependency vt' \
              '_id="4.3.2.1"/></dependencies>'
        dep = ['1.2.3.4', '4.3.2.1']
        res = w.get_dependencies_vt_as_xml_str(
            '1.3.6.1.4.1.25623.1.0.100061', dep)

        self.assertEqual(res, out)

    def test_get_ctime_xml(self, mock_nvti, mock_db):
        w =  DummyWrapper(mock_nvti, mock_db)
        out = '<creation_time>2009-03-19 11:22:36 +0100 ' \
              '(Thu, 19 Mar 2009)</creation_time>'
        vt = w.VT['1.3.6.1.4.1.25623.1.0.100061']
        ctime = vt.get('creation_time')
        res = w.get_creation_time_vt_as_xml_str(
            '1.3.6.1.4.1.25623.1.0.100061', ctime)

        self.assertEqual(res, out)

    def test_get_mtime_xml(self, mock_nvti, mock_db):
        w =  DummyWrapper(mock_nvti, mock_db)
        out = '<modification_time>$Date: 2018-08-10 15:09:25 +0200 ' \
              '(Fri, 10 Aug 2018) $</modification_time>'
        vt = w.VT['1.3.6.1.4.1.25623.1.0.100061']
        mtime = vt.get('modification_time')
        res = w.get_modification_time_vt_as_xml_str(
            '1.3.6.1.4.1.25623.1.0.100061', mtime)

        self.assertEqual(res, out)

    def test_get_summary_xml(self, mock_nvti, mock_db):
        w =  DummyWrapper(mock_nvti, mock_db)
        out = '<summary>some summary</summary>'
        vt = w.VT['1.3.6.1.4.1.25623.1.0.100061']
        summary = vt.get('summary')
        res = w.get_summary_vt_as_xml_str(
            '1.3.6.1.4.1.25623.1.0.100061', summary)

        self.assertEqual(res, out)

    def test_get_impact_xml(self, mock_nvti, mock_db):
        w =  DummyWrapper(mock_nvti, mock_db)
        out = '<impact>some impact</impact>'
        vt = w.VT['1.3.6.1.4.1.25623.1.0.100061']
        impact = vt.get('impact')
        res = w.get_impact_vt_as_xml_str(
            '1.3.6.1.4.1.25623.1.0.100061', impact)

        self.assertEqual(res, out)

    def test_get_insight_xml(self, mock_nvti, mock_db):
        w =  DummyWrapper(mock_nvti, mock_db)
        out = '<insight>some insight</insight>'
        vt = w.VT['1.3.6.1.4.1.25623.1.0.100061']
        insight = vt.get('insight')
        res = w.get_insight_vt_as_xml_str(
            '1.3.6.1.4.1.25623.1.0.100061', insight)

        self.assertEqual(res, out)

    def test_get_solution_xml(self, mock_nvti, mock_db):
        w =  DummyWrapper(mock_nvti, mock_db)
        out = '<solution type="WillNotFix">some solution</solution>'
        vt =w.VT['1.3.6.1.4.1.25623.1.0.100061']
        solution = vt.get('solution')
        solution_type = vt.get('solution_type')

        res = w.get_solution_vt_as_xml_str(
            '1.3.6.1.4.1.25623.1.0.100061', solution, solution_type)

        self.assertEqual(res, out)

    def test_get_detection_xml(self, mock_nvti, mock_db):
        w =  DummyWrapper(mock_nvti, mock_db)
        out = '<detection qod_type="remote_banner"/>'
        vt = w.VT['1.3.6.1.4.1.25623.1.0.100061']
        detection_type = vt.get('qod_type')

        res = w.get_detection_vt_as_xml_str(
            '1.3.6.1.4.1.25623.1.0.100061', qod_type=detection_type)

        self.assertEqual(res, out)

    def test_get_affected_xml(self, mock_nvti, mock_db):
        w =  DummyWrapper(mock_nvti, mock_db)
        out = '<affected>some affection</affected>'
        vt = w.VT['1.3.6.1.4.1.25623.1.0.100061']
        affected =  vt.get('affected')

        res = w.get_affected_vt_as_xml_str(
            '1.3.6.1.4.1.25623.1.0.100061', affected=affected)

        self.assertEqual(res, out)

    def test_build_credentials(self, mock_nvti, mock_db):
        w =  DummyWrapper(mock_nvti, mock_db)
        cred_out = [
            'auth_port_ssh|||22',
            'SSH Authorization[entry]:SSH login name:|||username',
            'SSH Authorization[password]:SSH key passphrase:|||pass',
            'SSH Authorization[file]:SSH private key:|||',
            'SMB Authorization[entry]:SMB login:|||username',
            'SMB Authorization[password]:SMB password :|||pass',
            'SNMP Authorization[password]:SNMP Community:some comunity',
            'SNMP Authorization[entry]:SNMPv3 Username:username',
            'SNMP Authorization[password]:SNMPv3 Password:pass',
            'SNMP Authorization[radio]:SNMPv3 Authentication Algorithm:some auth algo',
            'SNMP Authorization[password]:SNMPv3 Privacy Password:privacy pass',
            'SNMP Authorization[radio]:SNMPv3 Privacy Algorithm:privacy algo',
            'ESXi Authorization[entry]:ESXi login name:|||username',
            'ESXi Authorization[password]:ESXi login password:|||pass']
        cred_dict = {
            'ssh': {'type': 'ssh',
                    'port': '22',
                    'username': 'username',
                    'password': 'pass',
            },
            'smb': {'type': 'smb',
                    'username': 'username',
                    'password': 'pass',
            },
            'esxi': {'type': 'esxi',
                    'username': 'username',
                    'password': 'pass',
            },
            'snmp': {'type': 'snmp',
                     'username': 'username',
                     'password': 'pass',
                     'community': 'some comunity',
                     'auth_algorithm': 'some auth algo',
                     'privacy_password': 'privacy pass',
                     'privacy_algorithm': 'privacy algo',
            },
        }
        self.maxDiff=None
        ret = w.build_credentials_as_prefs(cred_dict)
        self.assertEqual(len(ret), len(cred_out))
        self.assertIn('auth_port_ssh|||22', cred_out)

    def test_build_credentials_ssh_up(self, mock_nvti, mock_db):
        w =  DummyWrapper(mock_nvti, mock_db)
        cred_out = [
            'auth_port_ssh|||22',
            'SSH Authorization[entry]:SSH login name:|||username',
            'SSH Authorization[password]:SSH password (unsafe!):|||pass']
        cred_dict = {
            'ssh': {'type': 'up',
                    'port': '22',
                    'username': 'username',
                    'password': 'pass',
            }
        }
        self.maxDiff=None
        ret = w.build_credentials_as_prefs(cred_dict)
        self.assertEqual(ret, cred_out)

    def test_process_vts(self, mock_nvti, mock_db):
        vts = {
            '1.3.6.1.4.1.25623.1.0.100061': {
                'Data length : ': 'new value',
                'Do not randomize the  order  in  which ports are ' \
                'scanned': 'new value'},
            'vt_groups': ['family=debian', 'family=general']
        }
        vt_out = (
            ['1.3.6.1.4.1.25623.1.0.100061'],
            [['Mantis Detection[checkbox]:Do not randomize the  order  i' \
              'n  which ports are scanned', 'new value'],
             ['Mantis Detection[entry]:Data length : ', 'new value']]
            )
        w =  DummyWrapper(mock_nvti, mock_db)
        w.load_vts()
        ret = w.process_vts(vts)
        self.assertEqual(len(ret), len(vt_out))

    def test_get_openvas_timestamp_scan_host_end(self, mock_nvti, mock_db):
        mock_db.get_host_scan_scan_end_time.return_value = '12345'
        w =  DummyWrapper(mock_nvti, mock_db)
        w.create_scan('123-456', '192.168.0.1', '192.168.0.1', None, [])
        w.get_openvas_timestamp_scan_host('123-456', '192.168.0.1')
        for result in  w.scan_collection.results_iterator('123-456', False):
            self.assertEqual(result.get('value'), '12345')

    def test_get_openvas_timestamp_scan_host_start(self, mock_nvti, mock_db):
        mock_db.get_host_scan_scan_end_time.return_value = None
        mock_db.get_host_scan_scan_end_time.return_value = '54321'
        w =  DummyWrapper(mock_nvti, mock_db)
        w.create_scan('123-456', '192.168.0.1', '192.168.0.1', None, [])
        w.get_openvas_timestamp_scan_host('123-456', '192.168.0.1')
        for result in  w.scan_collection.results_iterator('123-456', False):
            self.assertEqual(result.get('value'), '54321')

    def test_scan_is_finished(self, mock_nvti, mock_db):
        mock_db.get_single_item.return_value = 'finished'
        w =  DummyWrapper(mock_nvti, mock_db)
        ret = w.scan_is_finished('123-456')
        self.assertEqual(ret, True)

    def test_scan_is_stopped(self, mock_nvti, mock_db):
        mock_db.get_single_item.return_value = 'stop_all'
        mock_db.kb_connect_item.return_value = mock_db
        mock_db.set_redisctx.return_value = None
        w =  DummyWrapper(mock_nvti, mock_db)
        ret = w.scan_is_stopped('123-456')
        self.assertEqual(ret, True)
