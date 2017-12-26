import inspect
import json
import logging
import os
import datetime
import sys
import re
from Config import path_to_git_project_master, project_name


def create_log_file():
    path = os.path.join(os.path.abspath(os.path.dirname(__file__) + '/../../'), 'log')
    now = datetime.datetime.now()
    if not os.path.exists(path):
        os.makedirs(path)
    file_name = os.path.join(path, now.strftime('%Y-%m-%d') + '.log')
    return file_name


log = logging
log.basicConfig(
    stream=sys.stdout,
    format=u'%(levelname)-8s [%(asctime)s]  %(message)s',
    level=logging.INFO,
    filename=create_log_file())
template = '::[{file_name} => {module_name}, line: {line}]:: \n{link_to_line}\n'


def log_step(number, message):
    inspect_stack_called_file, url_to_file = get_stack()
    log.info("\n")
    log.info('{template} :::::::::: {step}. {message} :::::::::: '.format(
        template=template.format(
            module_name=inspect_stack_called_file[3],
            file_name=os.path.split(inspect.stack()[1][1])[1],
            line=inspect_stack_called_file[2],
            link_to_line=url_to_file),
        step=number,
        message=message))


def log_info(message):
    inspect_stack_called_file, url_to_file = get_stack()
    log.info('{template} {message}'.format(
        template=template.format(
            module_name=inspect_stack_called_file[3],
            file_name=os.path.split(inspect.stack()[1][1])[1],
            line=inspect_stack_called_file[2],
            link_to_line=url_to_file),
        message=message))


def get_stack():
    inspect_stack_called_file = inspect.stack()[2]
    full_path_to_file = inspect_stack_called_file[1]
    try:
        path_to_file = re.findall('.*{project_name}(.*)'.format(project_name=project_name), full_path_to_file)[0]
    except IndexError:
        path_to_file = full_path_to_file
    line_from_file = inspect_stack_called_file[2]
    url_to_file = '{git_master_url}/{path_to_file}#L{line_number}'.format(
        git_master_url=path_to_git_project_master,
        path_to_file=path_to_file,
        line_number=line_from_file)
    return inspect_stack_called_file, url_to_file


def log_pretty_json(json_message, message=""):
    pretty_json_string_with_message = '{message}\n{json_message}'.format(message=message,
                                                                         json_message=json.dumps(json_message,
                                                                                                 sort_keys=True,
                                                                                                 indent=4))
    inspect_stack_called_file, url_to_file = get_stack()
    log.info('{template} {message}'.format(
        template=template.format(
            module_name=inspect_stack_called_file[3],
            file_name=os.path.split(inspect.stack()[1][1])[1],
            line=inspect_stack_called_file[2],
            link_to_line=url_to_file),
        message=pretty_json_string_with_message))


def error(message):
    inspect_stack_called_file, url_to_file = get_stack()
    log.error('{template} {message}'.format(
        template=template.format(
            module_name=inspect_stack_called_file[3],
            file_name=os.path.split(inspect.stack()[1][1])[1],
            line=inspect_stack_called_file[2],
            link_to_line=url_to_file),
        message=message))


def end_log():
    log_info(":::::::::: END LOG ::::::::::")
    log.info("\n\n")
