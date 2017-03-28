from includes.ldap_helpers import *
import ldap


class AdManager(object):
    def __init__(self, ldap_config):
        self.settings = ldap_config
        self.tree_base = ldap_config['tree_base']
        self.connection = connect(ldap_config['bind_user'], ldap_config['bind_password'], ldap_config['hosts'])

    def new_account(self, account):
        if create_or_modify_account(account, self.connection, self.tree_base, self.settings):
            print('LDAP Created Account: ' + account['username'] + ' - ' + account['identifier'])

    def modify_account(self, account):
        if create_or_modify_account(account, self.connection, self.tree_base, self.settings):
            print('LDAP Updated Account: ' + account['username'] + ' - ' + account['identifier'])

    def restore_account(self, account):
        if create_or_modify_account(account, self.connection, self.tree_base, self.settings):
            print('LDAP Restored Account: ' + account['username'] + ' - ' + account['identifier'])
            self.enable_account(account)

    def delete_account(self, account):
        if delete_or_disable_account(account, self.connection, self.settings):
            print('LDAP Deleted/Disabled Account: ' + account['username'] + ' - ' + account['identifier'])

    def enable_account(self, account):
        result = get_user_by_identifier(account['identifier'], self.tree_base, self.connection)
        if result:
            account_dn = result[0][0]
            if enable_account(account_dn, self.connection):
                print('LDAP Enabled Account: ' + account['username'] + ' - ' + account['identifier'])

    def disable_account(self, account):
        result = get_user_by_identifier(account['identifier'], self.tree_base, self.connection)
        if result:
            account_dn = result[0][0]
            if disable_account(account_dn, self.connection):
                print('LDAP Disabled Account: ' + account['username'] + ' - ' + account['identifier'])

    def change_account_password(self, account):
        result = get_user_by_identifier(account['identifier'], self.tree_base, self.connection)
        if result:
            account_dn = result[0][0]
            if set_password(account_dn, account['password'], self.connection):
                print('LDAP Set Password: ' + account['username'] + ' - ' + account['identifier'])

    def create_group(self, group, group_type):
        group_cn = build_group_cn(group)
        group_dn = build_group_dn(group_cn, group_type, self.settings['base_group_ou_dn'])
        if create_group(group_cn, group_dn, group['label'], self.tree_base, self.connection):
            print('LDAP Created Group: ' + group_cn)

    def restore_group(self, group, group_type):
        group_cn = build_group_cn(group)
        group_dn = build_group_dn(group_cn, group_type, self.settings['base_group_ou_dn'])
        if create_group(group_cn, group_dn, group['label'], self.tree_base, self.connection):
            print('LDAP Restored Group: ' + group_cn)

    def delete_group(self, group, group_type):
        group_cn = build_group_cn(group)
        group_dn = build_group_dn(group_cn, group_type, self.settings['base_group_ou_dn'])
        if delete_group(group_dn, self.tree_base, self.connection):
            print('LDAP Deleted Group: ' + group_cn)

    def add_account_to_group(self, account, group, group_type):
        result = get_user_by_identifier(account['identifier'], self.tree_base, self.connection)
        if result:
            account_dn = result[0][0]
            group_cn = build_group_cn(group)
            group_dn = build_group_dn(group_cn, group_type, self.settings['base_group_ou_dn'])
            group_result = get_group(group_dn, self.tree_base, self.connection)
            if not group_result:
                self.create_group(group, group_type)
            if add_to_group(account_dn, group_dn, self.tree_base, self.connection):
                print('LDAP Added Account To Group: ' + account['username'] +
                      ' - ' + account['identifier'] + ' -->> ' + group_cn)

    def remove_account_from_group(self, account, group, group_type):
        result = get_user_by_identifier(account['identifier'], self.tree_base, self.connection)
        if result:
            account_dn = result[0][0]
            group_cn = build_group_cn(group)
            group_dn = build_group_dn(group_cn, group_type, self.settings['base_group_ou_dn'])
            group_result = get_group(group_dn, self.tree_base, self.connection)
            if not group_result:
                self.create_group(group, group_type)
            if remove_from_group(account_dn, group_dn, self.tree_base, self.connection):
                print('LDAP Removed Account From Group: ' + account['username'] +
                      ' - ' + account['identifier'] + ' ---- ' + group_cn)

    def add_group_to_group(self, target_group, target_group_type, des_group, des_group_type):
        # Build the DNs
        target_group_dn = build_group_dn(build_group_cn(target_group), target_group_type,
                                         self.settings['base_group_ou_dn'])
        des_group_dn = build_group_dn(build_group_cn(des_group), des_group_type, self.settings['base_group_ou_dn'])
        # Check to see if the groups exist
        target_result = get_group(target_group_dn, self.tree_base, self.connection)
        des_result = get_group(des_group_dn, self.tree_base, self.connection)

        # If they do not exists create them
        if not target_result:
            self.create_group(target_group, target_group_type)
        if not des_result:
            self.create_group(des_group, des_group_type)

        # Add the target to the destination group
        if add_to_group(target_group_dn, des_group_dn, self.tree_base, self.connection):
            print('LDAP Added Group To Group: ' + build_group_cn(target_group) + ' -->> ' + build_group_cn(des_group))

    def remove_group_from_group(self, target_group, target_group_type, des_group, des_group_type):
        target_group_dn = build_group_dn(build_group_cn(target_group), target_group_type,
                                         self.settings['base_group_ou_dn'])
        des_group_dn = build_group_dn(build_group_cn(des_group), des_group_type, self.settings['base_group_ou_dn'])
        if remove_from_group(target_group_dn, des_group_dn, self.tree_base, self.connection):
            print(
                'LDAP Removed Group From Group: ' + build_group_cn(target_group) + ' ---- ' + build_group_cn(des_group))
