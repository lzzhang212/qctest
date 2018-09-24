#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018-9-16 22:21
# @Author  : lzzhang
# @Site    : 
# @File    : qingcloudcli.py
# @Software: PyCharm


import click
import json
from .para_check import ParaChecker
from .request_send import HTTPRequest

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version='1.0.0')
def cli():
    """This is a command line tool for qingcloud.
    )"""
    pass


ACTION_DESCRIBE_INSTANCES = 'DescribeInstances'
ACTION_RUN_INSTANCES = 'RunInstances'
ACTION_TERMINATE_INSTANCES = 'TerminateInstances'


def get_valid_paras(all_locals, all_paras_keys, list_paras):
    """获取有效的参数
    """
    valid_paras = {}
    for key in all_locals.keys():
        if key in all_paras_keys and all_locals[key]:
            if key in list_paras:
                # click接收的可重复参数为tuple类型需要转为list
                valid_paras[key] = list(all_locals[key])
            else:
                valid_paras[key] = all_locals[key]
    return valid_paras


@cli.command()
@click.option('--instances', multiple=True, help='The IDs of instances.')
@click.option('--image_id', multiple=True, help='The ID of image.')
@click.option('--instance_class', type=int, help='Instance type.')
@click.option('--status', multiple=True,
               help='Status of the instance, include pending, running, stopped, suspended, terminated, ceased')
@click.option('--search_word',
              help='Filter instances by the specified search words, support instanceId and instance name.')
@click.option('--tags', multiple=True, help='Filter instances by the specified tags.')
@click.option('--dedicated_host_group_id',
              help='Filter instances by the specified dedicated host group id.')
@click.option('--dedicated_host_id', help='Filter instances by the specified dedicated host id.')
@click.option('--owner', help='Filter instances by the specified owner.')
@click.option('--verbose', type=int, help='Set 1 will return more detailed results.')
@click.option('--offset', default=0, type=int, help='Offset of the return results.')
@click.option('--limit', default=20, type=int, help='Limitation of the return results.')
def describe_instances(instances=None,
                       image_id=None,
                       instance_type=None,
                       instance_class=None,
                       status=None,
                       search_word=None,
                       tags=None,
                       dedicated_host_group_id=None,
                       dedicated_host_id=None,
                       owner=None,
                       verbose=0,
                       offset=None,
                       limit=20):
    """ 获取指定主机,不指定过滤条件默认获取所有主机
    """
    action = ACTION_DESCRIBE_INSTANCES
    para_checker = ParaChecker()
    request = HTTPRequest()

    # 检查入参
    all_paras_keys = ['instances', 'image_id', 'instance_type', 'instance_class', 'status',
                      'search_word', 'tags', 'dedicated_host_group_id', 'dedicated_host_id',
                      'owner', 'verbose', 'offset', 'limit']
    integer_paras = ['instance_class', 'offset', 'limit', 'verbose']
    list_paras = ['instances', 'image_id', 'status', 'tags']
    valid_paras = get_valid_paras(locals(), all_paras_keys, list_paras)

    if not para_checker.check_paras(valid_paras,
                                    required_paras=[],
                                    integer_paras=integer_paras,
                                    list_paras=list_paras
                                    ):
        return None

    resp = request.send_request(action, valid_paras, method='GET')
    print(json.dumps(resp, sort_keys=True, indent=4, separators=(', ', ': ')))
    return None


@cli.command()
@click.option('--image_id', required=True,
              help='Specify the id of image you want to run.')
@click.option('--login_mode', required=True, type=click.Choice(['keypair', 'passwd']),
              help="Specify the login mode, 'keypair' and 'passwd' are available for linux,"
                   "'passwd' for windows.")
@click.option('--instance_type', type=click.Choice(['c1m1','c1m2','c1m4','c2m2','c2m4',
                                                       'c2m8','c4m4','c4m8','c4m16','small_b',
                                                       'small_c','medium_a','medium_b','medium_c',
                                                       'large_a','large_b','large_c']),
              help="Specify the instance type, you can refer to "
                   "https://docs.qingcloud.com/product/api/common/includes/instance_type.html#instance-type")
@click.option('--cpu', type=int, help='Specify the num of cpu core, valid in [1,2,4,8,16].')
@click.option('--memory', type=int,
              help='Specify the memory size(MB).Valid in [1024,2048,4096,6144,8192,12288,16384,24576,32768].')
@click.option('--os_disk_size', type=int, help='Specify the OS disk size(GB).'
                                               'Linux:20-100,default=20,Windows:50-100,default=50.')
@click.option('--count', default=1, type=int, help='Specify the number of instances you want to run.')
@click.option('--instance_name', help='Specify the name of instance you want to run.')
@click.option('--login_keypair', help='With login_mode:keypair, you should specify the keypair.')
@click.option('--login_passwd', help='With login_mode:passwd, you should specify the passwd.')
@click.option('--vxnets', help='Specify the IDs of vxnets the instance will join.')
@click.option('--security_group', help='Specify the ids of security group.')
@click.option('--volumes', multiple=True, help='Specify the volumes you want to attach to the instance.'
                                               'You must specify the count=1 at the same time.')
@click.option('--hostname', help='Specify the hostname.')
@click.option('--need_newsid', type=int, help='1: generate new SID, default:0.')
@click.option('--instance_class', type=click.Choice(['0','1']), help='0:performance, 1:high-performance.')
@click.option('--cpu_model', type=click.Choice(['Westmere', 'SandyBridge', 'IvyBridge', 'Haswell', 'Broadwell']),
              help='Specify the CPU model.')
@click.option('--cpu_topology', help='Specify the CPU topology.')
@click.option('--gpu', type=int, help='Specify the number of GPU.')
@click.option('--nic_mqueue', type=int, help='1/0: enable/disable the nic_mqueue.')
@click.option('--need_userdata', default=0, type=int, help='Whether to enable User Data.')
@click.option('--userdata_type', type=click.Choice(['plain','exec','tar']),
              help='Specify the type of User Data.')
@click.option('--userdata_value', help='The value of User Data.')
@click.option('--userdata_path', help='Specify the path of User Data.')
@click.option('--userdata_file', default='/etc/rc.local', help='Specify the path for EXEC file.')
@click.option('--target_user', help='Specify the target user.')
@click.option('--dedicated_host_group_id', help='Specify the dedicated host gourp id.')
@click.option('--dedicated_host_id', help='Specify the dedicated host id.')
@click.option('--instance_group', help='Join the instance group.')
def run_instances(image_id, login_mode,
                  instance_type=None,
                  cpu=None,
                  memory=None,
                  os_disk_size=None,
                  count=1,
                  instance_name="",
                  login_keypair=None,
                  login_passwd=None,
                  vxnets=None,
                  security_group=None,
                  volumes=None,
                  hostname=None,
                  need_newsid=False,
                  instance_class=None,
                  cpu_model=None,
                  cpu_topology=None,
                  gpu=0,
                  nic_mqueue=0,
                  need_userdata=0,
                  userdata_type=None,
                  userdata_value=None,
                  userdata_path=None,
                  userdata_file=None,
                  target_user=None,
                  dedicated_host_group_id=None,
                  dedicated_host_id=None,
                  instance_group=None
                  ):
    """ 创建指定主机
    """
    action = ACTION_RUN_INSTANCES
    para_checker = ParaChecker()
    request = HTTPRequest()

    # 获取有效入参
    all_paras_keys = ['image_id', 'login_mode', 'instance_type', 'cpu', 'memory', 'os_disk_size',
                      'count', 'instance_name', 'login_keypair', 'login_passwd', 'vxnets', 'security_group',
                      'volumes', 'hostname', 'need_newsid', 'instance_class', 'cpu_model', 'cpu_topology',
                      'gpu', 'nic_mqueue', 'need_userdata', 'userdata_type', 'userdata_value', 'userdata_path',
                      'userdata_file', 'target_user', 'dedicated_host_group_id', 'dedicated_host_id', 'instance_group']
    required_paras = ['image_id', 'login_mode']
    integer_paras = ['cpu', 'memory', 'os_disk_size', 'count',
                     'need_newsid', 'gpu', 'nic_mqueue', 'need_userdata'
                     ]
    list_paras = ['volumes']
    valid_paras = get_valid_paras(locals(), all_paras_keys, list_paras)
    # 检测入参
    if 'instance_type' not in valid_paras:
        required_paras.append('cpu')
        required_paras.append('memory')
    if valid_paras['login_mode'] == 'keypair':
        required_paras.append('login_keypair')
    elif valid_paras['login_mode'] == 'passwd':
        required_paras.append('login_passwd')
    else:
        raise Exception('para [login_mode] should be [keypair] or [passwd]')
    if not para_checker.check_paras(valid_paras,
                                    required_paras=required_paras,
                                    integer_paras=integer_paras,
                                    list_paras=list_paras,
                                    ):
        return None
    resp = request.send_request(action, valid_paras, method='GET')
    if resp['ret_code'] != 0:
        print(resp)
    return None


@cli.command()
@click.option('--instances', multiple=True, help='Specify the IDs of instances you want to terminate.')
@click.option('--direct_cease', default=0, type=int,
              help='1:cease the instance directly, 0:server will save the instance in recycle.')
def terminate_instances(instances, direct_cease=0):
    """ 销毁主机
    """
    action = ACTION_TERMINATE_INSTANCES
    para_checker = ParaChecker()
    request = HTTPRequest()
    # 获取有效入参
    all_paras_keys = ['instances', 'direct_cease']
    list_paras = ['instances']
    valid_paras = get_valid_paras(locals(), all_paras_keys, list_paras)

    if not para_checker.check_paras(valid_paras,
                                    required_paras=['instances'],
                                    integer_paras=[],
                                    list_paras=list_paras
                                    ):
        return None

    resp = request.send_request(action, valid_paras, method='GET')
    print(resp)
    return None


if __name__ == '__main__':
    cli()
