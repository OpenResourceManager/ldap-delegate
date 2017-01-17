from __future__ import print_function

import socket

from socketIO_client import SocketIO, LoggingNamespace

from includes.AdManager import AdManager
from includes.helpers import read_config, read_encrypted_message

IO = None
HOST_NAME = None
BC_KEY = None
SERVER_ADDRESS = 'localhost'
SERVER_PORT = 3000


def load_config():
    global HOST_NAME, SERVER_ADDRESS, SERVER_PORT, BC_KEY
    c = read_config()
    config = c['general']
    HOST_NAME = socket.gethostname()
    SERVER_ADDRESS = config['control_server_hostname']
    SERVER_PORT = config['control_server_port']
    try:
        if not config['bc_key']:
            raise Exception('You have not provided a `bc_key` in your config file! Hint: `php artisan slerp:bckey`')
    except KeyError:
        raise KeyError('You have not provided a `bc_key` in your config file! Hint: `php artisan slerp:bckey`')
    BC_KEY = config['bc_key']


def connect_to_sio():
    global IO
    print('Connecting...')
    IO = SocketIO(SERVER_ADDRESS, SERVER_PORT, LoggingNamespace)
    print('Connected!')


def on_create_account(*args):
    for arg in args:
        message = read_encrypted_message(arg, BC_KEY)
        ldap_conf = message['conf']['ldap']
        account = message['data']
        if ldap_conf['enabled']:
            ad = AdManager(ldap_conf)
            ad.new_account(account)


def on_delete_account(*args):
    for arg in args:
        message = read_encrypted_message(arg, BC_KEY)
        ldap_conf = message['conf']['ldap']
        account = message['data']
        if ldap_conf['enabled']:
            ad = AdManager(ldap_conf)
            ad.delete_account(account)


def on_restore_account(*args):
    for arg in args:
        message = read_encrypted_message(arg, BC_KEY)
        ldap_conf = message['conf']['ldap']
        account = message['data']
        if ldap_conf['enabled']:
            ad = AdManager(ldap_conf)
            ad.restore_account(account)


def on_create_duty(*args):
    for arg in args:
        message = read_encrypted_message(arg, BC_KEY)
        ldap_conf = message['conf']['ldap']
        duty = message['data']
        if ldap_conf['enabled']:
            ad = AdManager(ldap_conf)
            ad.create_group(duty, 'Duty')


def on_destroy_duty(*args):
    for arg in args:
        message = read_encrypted_message(arg, BC_KEY)
        ldap_conf = message['conf']['ldap']
        duty = message['data']
        if ldap_conf['enabled']:
            ad = AdManager(ldap_conf)
            ad.delete_group(duty, 'Duty')


def on_restore_duty(*args):
    for arg in args:
        message = read_encrypted_message(arg, BC_KEY)
        ldap_conf = message['conf']['ldap']
        duty = message['data']
        if ldap_conf['enabled']:
            ad = AdManager(ldap_conf)
            ad.restore_group(duty, 'Duty')


def on_create_campus(*args):
    for arg in args:
        message = read_encrypted_message(arg, BC_KEY)
        ldap_conf = message['conf']['ldap']
        campus = message['data']
        if ldap_conf['enabled']:
            ad = AdManager(ldap_conf)
            ad.create_group(campus, 'Campus')


def on_destroy_campus(*args):
    for arg in args:
        message = read_encrypted_message(arg, BC_KEY)
        ldap_conf = message['conf']['ldap']
        campus = message['data']
        if ldap_conf['enabled']:
            ad = AdManager(ldap_conf)
            ad.delete_group(campus, 'Campus')


def on_restore_campus(*args):
    for arg in args:
        message = read_encrypted_message(arg, BC_KEY)
        ldap_conf = message['conf']['ldap']
        campus = message['data']
        if ldap_conf['enabled']:
            ad = AdManager(ldap_conf)
            ad.restore_group(campus, 'Campus')


def on_create_building(*args):
    for arg in args:
        message = read_encrypted_message(arg, BC_KEY)
        ldap_conf = message['conf']['ldap']
        building = message['data']
        if ldap_conf['enabled']:
            ad = AdManager(ldap_conf)
            ad.create_group(building, 'Building')


def on_destroy_building(*args):
    for arg in args:
        message = read_encrypted_message(arg, BC_KEY)
        ldap_conf = message['conf']['ldap']
        building = message['data']
        if ldap_conf['enabled']:
            ad = AdManager(ldap_conf)
            ad.delete_group(building, 'Building')


def on_restore_building(*args):
    for arg in args:
        message = read_encrypted_message(arg, BC_KEY)
        ldap_conf = message['conf']['ldap']
        building = message['data']
        if ldap_conf['enabled']:
            ad = AdManager(ldap_conf)
            ad.restore_group(building, 'Building')


def on_create_room(*args):
    for arg in args:
        message = read_encrypted_message(arg, BC_KEY)
        ldap_conf = message['conf']['ldap']
        room = message['data']
        if ldap_conf['enabled']:
            ad = AdManager(ldap_conf)
            ad.create_group(room, 'Room')


def on_destroy_room(*args):
    for arg in args:
        message = read_encrypted_message(arg, BC_KEY)
        ldap_conf = message['conf']['ldap']
        room = message['data']
        if ldap_conf['enabled']:
            ad = AdManager(ldap_conf)
            ad.delete_group(room, 'Room')


def on_restore_room(*args):
    for arg in args:
        message = read_encrypted_message(arg, BC_KEY)
        ldap_conf = message['conf']['ldap']
        room = message['data']
        if ldap_conf['enabled']:
            ad = AdManager(ldap_conf)
            ad.restore_group(room, 'Room')


def on_create_department(*args):
    for arg in args:
        message = read_encrypted_message(arg, BC_KEY)
        ldap_conf = message['conf']['ldap']
        department = message['data']
        if ldap_conf['enabled']:
            ad = AdManager(ldap_conf)
            ad.create_group(department, 'Department')


def on_destroy_department(*args):
    for arg in args:
        message = read_encrypted_message(arg, BC_KEY)
        ldap_conf = message['conf']['ldap']
        department = message['data']
        if ldap_conf['enabled']:
            ad = AdManager(ldap_conf)
            ad.delete_group(department, 'Department')


def on_restore_department(*args):
    for arg in args:
        message = read_encrypted_message(arg, BC_KEY)
        ldap_conf = message['conf']['ldap']
        department = message['data']
        if ldap_conf['enabled']:
            ad = AdManager(ldap_conf)
            ad.restore_group(department, 'Department')


def on_create_course(*args):
    for arg in args:
        message = read_encrypted_message(arg, BC_KEY)
        ldap_conf = message['conf']['ldap']
        course = message['data']
        if ldap_conf['enabled']:
            ad = AdManager(ldap_conf)
            ad.create_group(course, 'Course')


def on_destroy_course(*args):
    for arg in args:
        message = read_encrypted_message(arg, BC_KEY)
        ldap_conf = message['conf']['ldap']
        course = message['data']
        if ldap_conf['enabled']:
            ad = AdManager(ldap_conf)
            ad.delete_group(course, 'Course')


def on_restore_course(*args):
    for arg in args:
        message = read_encrypted_message(arg, BC_KEY)
        ldap_conf = message['conf']['ldap']
        course = message['data']
        if ldap_conf['enabled']:
            ad = AdManager(ldap_conf)
            ad.restore_group(course, 'Course')


def on_course_account_assignment(*args):
    for arg in args:
        message = read_encrypted_message(arg, BC_KEY)
        ldap_conf = message['conf']['ldap']
        data = message['data']
        account = data['account']
        course = data['course']
        if ldap_conf['enabled']:
            ad = AdManager(ldap_conf)
            ad.add_account_to_group(account, course, 'Course')


def on_course_account_unassignment(*args):
    for arg in args:
        message = read_encrypted_message(arg, BC_KEY)
        ldap_conf = message['conf']['ldap']
        data = message['data']
        account = data['account']
        course = data['course']
        if ldap_conf['enabled']:
            ad = AdManager(ldap_conf)
            ad.remove_account_from_group(account, course, 'Course')


def on_department_account_assignment(*args):
    for arg in args:
        message = read_encrypted_message(arg, BC_KEY)
        ldap_conf = message['conf']['ldap']
        data = message['data']
        account = data['account']
        department = data['department']
        if ldap_conf['enabled']:
            ad = AdManager(ldap_conf)
            ad.add_account_to_group(account, department, 'Department')


def on_department_account_unassignment(*args):
    for arg in args:
        message = read_encrypted_message(arg, BC_KEY)
        ldap_conf = message['conf']['ldap']
        data = message['data']
        account = data['account']
        department = data['department']
        if ldap_conf['enabled']:
            ad = AdManager(ldap_conf)
            ad.remove_account_from_group(account, department, 'Department')


def on_duty_account_assignment(*args):
    for arg in args:
        message = read_encrypted_message(arg, BC_KEY)
        ldap_conf = message['conf']['ldap']
        data = message['data']
        account = data['account']
        duty = data['duty']
        if ldap_conf['enabled']:
            ad = AdManager(ldap_conf)
            ad.add_account_to_group(account, duty, 'Duty')


def on_duty_account_unassignment(*args):
    for arg in args:
        message = read_encrypted_message(arg, BC_KEY)
        ldap_conf = message['conf']['ldap']
        data = message['data']
        account = data['account']
        duty = data['duty']
        if ldap_conf['enabled']:
            ad = AdManager(ldap_conf)
            ad.remove_account_from_group(account, duty, 'Duty')


def on_room_account_assignment(*args):
    for arg in args:
        message = read_encrypted_message(arg, BC_KEY)
        ldap_conf = message['conf']['ldap']
        data = message['data']
        account = data['account']
        room = data['room']
        if ldap_conf['enabled']:
            ad = AdManager(ldap_conf)
            ad.add_account_to_group(account, room, 'Room')


def on_room_account_unassignment(*args):
    for arg in args:
        message = read_encrypted_message(arg, BC_KEY)
        ldap_conf = message['conf']['ldap']
        data = message['data']
        account = data['account']
        room = data['room']
        if ldap_conf['enabled']:
            ad = AdManager(ldap_conf)
            ad.remove_account_from_group(account, room, 'Room')


def main():
    # Load the configuration
    load_config()
    # Connect to the server
    connect_to_sio()
    # Emmit that we're here
    IO.emit('join', {'hostname': HOST_NAME})
    # Account Listeners
    IO.on('create_account', on_create_account)
    IO.on('delete_account', on_delete_account)
    IO.on('restore_account', on_restore_account)
    # Duty Listeners
    IO.on('create_duty', on_create_duty)
    IO.on('delete_duty', on_destroy_duty)
    IO.on('restore_duty', on_restore_duty)
    # Campus Listeners
    IO.on('create_campus', on_create_campus)
    IO.on('delete_campus', on_destroy_campus)
    IO.on('restore_campus', on_restore_campus)
    # Building Listeners
    IO.on('create_building', on_create_building)
    IO.on('delete_building', on_destroy_building)
    IO.on('restore_building', on_restore_building)
    # Room Listeners
    IO.on('create_room', on_create_room)
    IO.on('delete_room', on_destroy_room)
    IO.on('restore_room', on_restore_room)
    # Department Listeners
    IO.on('create_department', on_create_department)
    IO.on('delete_department', on_destroy_department)
    IO.on('restore_department', on_restore_department)
    # Course Listeners
    IO.on('create_course', on_create_course)
    IO.on('delete_course', on_destroy_course)
    IO.on('restore_course', on_restore_course)
    # Account Assignment Listeners
    IO.on('course_account_assignment', on_course_account_assignment)
    IO.on('course_account_unassignment', on_course_account_unassignment)
    IO.on('department_account_assignment', on_department_account_assignment)
    IO.on('department_account_unassignment', on_department_account_unassignment)
    IO.on('duty_account_assignment', on_duty_account_assignment)
    IO.on('duty_account_unassignment', on_duty_account_unassignment)
    IO.on('room_account_assignment', on_room_account_assignment)
    IO.on('room_account_unassignment', on_room_account_unassignment)
    # Hang out
    IO.wait()


if __name__ == "__main__":
    main()
