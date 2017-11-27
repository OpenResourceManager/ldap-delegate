#!/usr/bin/env python
from __future__ import print_function
from socketIO_client import SocketIO, LoggingNamespace
from includes.AdManager import AdManager
from includes.helpers import read_config, read_encrypted_message
import socket
import sys
import includes.Daemon

IO = None
HOST_NAME = None
BC_KEY = None
DELEGATE_HOST = 'localhost'
DELEGATE_PORT = 3000


class LdapDelegate(includes.Daemon):
    def __init__(self, pidfile, stdin='/dev/null',
                 stdout='/var/log/orm/LdapDelegate/ldap.log', stderr='/var/log/orm/LdapDelegate/ldap_err.log'):
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = pidfile

    @staticmethod
    def load_config():
        global HOST_NAME, DELEGATE_HOST, DELEGATE_PORT, BC_KEY
        c = read_config()
        config = c['general']
        HOST_NAME = socket.gethostname()
        DELEGATE_HOST = config['delegate_server_host']
        DELEGATE_PORT = config['delegate_server_port']
        try:
            if not config['bc_key']:
                raise Exception('You have not provided a `bc_key` in your config file! Hint: `php artisan orm:bckey`')
        except KeyError:
            raise KeyError('You have not provided a `bc_key` in your config file! Hint: `php artisan orm:bckey`')
        BC_KEY = config['bc_key']

    @staticmethod
    def connect_to_sio():
        global IO
        print('Connecting...')
        IO = SocketIO(DELEGATE_HOST, DELEGATE_PORT, LoggingNamespace)
        print('Connected!')

    def on_create_account(*args):
        for arg in args:
            message = read_encrypted_message(arg, BC_KEY)
            ldap_conf = message['conf']['ldap']
            account = message['data']
            if ldap_conf['enabled']:
                ad = AdManager(ldap_conf)
                ad.new_account(account)

    def on_update_account(*args):
        for arg in args:
            message = read_encrypted_message(arg, BC_KEY)
            ldap_conf = message['conf']['ldap']
            account = message['data']
            if ldap_conf['enabled']:
                ad = AdManager(ldap_conf)
                ad.modify_account(account)

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

    def on_create_school(*args):
        for arg in args:
            message = read_encrypted_message(arg, BC_KEY)
            ldap_conf = message['conf']['ldap']
            school = message['data']
            if ldap_conf['enabled']:
                ad = AdManager(ldap_conf)
                ad.create_group(school, 'School')

    def on_destroy_school(*args):
        for arg in args:
            message = read_encrypted_message(arg, BC_KEY)
            ldap_conf = message['conf']['ldap']
            school = message['data']
            if ldap_conf['enabled']:
                ad = AdManager(ldap_conf)
                ad.delete_group(school, 'School')

    def on_restore_school(*args):
        for arg in args:
            message = read_encrypted_message(arg, BC_KEY)
            ldap_conf = message['conf']['ldap']
            school = message['data']
            if ldap_conf['enabled']:
                ad = AdManager(ldap_conf)
                ad.restore_group(school, 'School')

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

    def on_school_account_assignment(*args):
        for arg in args:
            message = read_encrypted_message(arg, BC_KEY)
            ldap_conf = message['conf']['ldap']
            data = message['data']
            account = data['account']
            school = data['school']
            if ldap_conf['enabled']:
                ad = AdManager(ldap_conf)
                ad.add_account_to_group(account, school, 'School')

    def on_school_account_unassignment(*args):
        for arg in args:
            message = read_encrypted_message(arg, BC_KEY)
            ldap_conf = message['conf']['ldap']
            data = message['data']
            account = data['account']
            school = data['school']
            if ldap_conf['enabled']:
                ad = AdManager(ldap_conf)
                ad.remove_account_from_group(account, school, 'School')

    def run(self):
        # Load the configuration
        self.load_config()
        # Connect to the server
        self.connect_to_sio()
        # Emmit that we're here
        IO.emit('join', {'hostname': HOST_NAME})
        # Account Listeners
        IO.on('create_account', self.on_create_account)
        IO.on('update_account', self.on_update_account)
        IO.on('delete_account', self.on_delete_account)
        IO.on('restore_account', self.on_restore_account)
        # Duty Listeners
        IO.on('create_duty', self.on_create_duty)
        IO.on('delete_duty', self.on_destroy_duty)
        IO.on('restore_duty', self.on_restore_duty)
        # Campus Listeners
        IO.on('create_campus', self.on_create_campus)
        IO.on('delete_campus', self.on_destroy_campus)
        IO.on('restore_campus', self.on_restore_campus)
        # Building Listeners
        IO.on('create_building', self.on_create_building)
        IO.on('delete_building', self.on_destroy_building)
        IO.on('restore_building', self.on_restore_building)
        # Room Listeners
        IO.on('create_room', self.on_create_room)
        IO.on('delete_room', self.on_destroy_room)
        IO.on('restore_room', self.on_restore_room)
        # Department Listeners
        IO.on('create_department', self.on_create_department)
        IO.on('delete_department', self.on_destroy_department)
        IO.on('restore_department', self.on_restore_department)
        # Course Listeners
        IO.on('create_course', self.on_create_course)
        IO.on('delete_course', self.on_destroy_course)
        IO.on('restore_course', self.on_restore_course)
        # Account Assignment Listeners
        IO.on('course_account_assignment', self.on_course_account_assignment)
        IO.on('course_account_unassignment', self.on_course_account_unassignment)
        IO.on('department_account_assignment', self.on_department_account_assignment)
        IO.on('department_account_unassignment', self.on_department_account_unassignment)
        IO.on('duty_account_assignment', self.on_duty_account_assignment)
        IO.on('duty_account_unassignment', self.on_duty_account_unassignment)
        IO.on('room_account_assignment', self.on_room_account_assignment)
        IO.on('room_account_unassignment', self.on_room_account_unassignment)
        IO.on('school_account_assignment', self.on_school_account_assignment)
        IO.on('school_account_unassignment', self.on_school_account_unassignment)
        # Hang out
        IO.wait()


if __name__ == "__main__":
    daemon = LdapDelegate('/var/run/ldap-delegate.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print
            "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print
        "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)
