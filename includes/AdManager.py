from includes.ldap_helpers import *
from includes.helpers import write_json_log, write_json_error


class AdManager(object):
    def __init__(self, ldap_config):
        self.settings = ldap_config
        self.tree_base = ldap_config['tree_base']
        self.connection = connect(ldap_config['bind_user'], ldap_config['bind_password'], ldap_config['hosts'])

    def new_account(self, account):
        write_json_log({
            'action': 'new_account',
            'account': account,
            'message': 'Creating account: ' + account['username'] + ' - ' + account['identifier'],
            'level': 'information'
        })
        if create_or_modify_account(account, self.connection, self.tree_base, self.settings):
            write_json_log({
                'action': 'new_account_success',
                'account': account,
                'message': 'Created account: ' + account['username'] + ' - ' + account['identifier'],
                'level': 'information'
            })
        else:
            write_json_error({
                'action': 'new_account_fail',
                'account': account,
                'message': 'Failed to create account: ' + account['username'] + ' - ' + account['identifier'],
                'level': 'warning'
            })

    def modify_account(self, account):
        write_json_log({
            'action': 'modify_account',
            'account': account,
            'message': 'Modifying account: ' + account['username'] + ' - ' + account['identifier'],
            'level': 'information'
        })
        if create_or_modify_account(account, self.connection, self.tree_base, self.settings):
            write_json_log({
                'action': 'modify_account_success',
                'account': account,
                'message': 'Modified account: ' + account['username'] + ' - ' + account['identifier'],
                'level': 'information'
            })
        else:
            write_json_error({
                'action': 'modify_account_fail',
                'account': account,
                'message': 'Failed to modify account: ' + account['username'] + ' - ' + account['identifier'],
                'level': 'warning'
            })

    def restore_account(self, account):
        write_json_log({
            'action': 'restore_account',
            'account': account,
            'message': 'Restoring account: ' + account['username'] + ' - ' + account['identifier'],
            'level': 'information'
        })
        if create_or_modify_account(account, self.connection, self.tree_base, self.settings):
            write_json_log({
                'action': 'restore_account_success',
                'account': account,
                'message': 'Restored account: ' + account['username'] + ' - ' + account['identifier'],
                'level': 'information'
            })
            self.enable_account(account)
        else:
            write_json_error({
                'action': 'restore_account_fail',
                'account': account,
                'message': 'Failed to restore account: ' + account['username'] + ' - ' + account['identifier'],
                'level': 'warning'
            })

    def delete_account(self, account):
        write_json_log({
            'action': 'delete_account',
            'account': account,
            'message': 'Deleting/Disabling account: ' + account['username'] + ' - ' + account['identifier'],
            'level': 'information'
        })
        if delete_or_disable_account(account, self.connection, self.settings):
            write_json_log({
                'action': 'delete_account_success',
                'account': account,
                'message': 'Deleted/Disabled account: ' + account['username'] + ' - ' + account['identifier'],
                'level': 'information'
            })
        else:
            write_json_error({
                'action': 'delete_account_fail',
                'account': account,
                'message': 'Failed to delete/disable account: ' + account['username'] + ' - ' + account['identifier'],
                'level': 'warning'
            })

    def enable_account(self, account):
        write_json_log({
            'action': 'enable_account',
            'account': account,
            'message': 'Enabling account: ' + account['username'] + ' - ' + account['identifier'],
            'level': 'information'
        })
        result = get_user_by_identifier(account['identifier'], self.tree_base, self.connection)
        if result:
            account_dn = result[0][0]
            if enable_account(account_dn, self.connection):
                write_json_log({
                    'action': 'enable_account_success',
                    'account': account,
                    'message': 'Enabled account: ' + account['username'] + ' - ' + account['identifier'],
                    'level': 'information'
                })
            else:
                write_json_error({
                    'action': 'enable_account_fail',
                    'account': account,
                    'message': 'Failed to enable account: ' + account['username'] + ' - ' + account['identifier'],
                    'level': 'warning'
                })

    def disable_account(self, account):
        write_json_log({
            'action': 'disable_account',
            'account': account,
            'message': 'Disable account: ' + account['username'] + ' - ' + account['identifier'],
            'level': 'information'
        })
        result = get_user_by_identifier(account['identifier'], self.tree_base, self.connection)
        if result:
            account_dn = result[0][0]
            if disable_account(account_dn, self.connection):
                write_json_log({
                    'action': 'disable_account_success',
                    'account': account,
                    'message': 'Disabled account: ' + account['username'] + ' - ' + account['identifier'],
                    'level': 'information'
                })
            else:
                write_json_error({
                    'action': 'disable_account_fail',
                    'account': account,
                    'message': 'Failed to disable account: ' + account['username'] + ' - ' + account['identifier'],
                    'level': 'warning'
                })

    def change_account_password(self, account):
        write_json_log({
            'action': 'change_account_password',
            'account': account,
            'message': 'Changing account password: ' + account['username'] + ' - ' + account['identifier'],
            'level': 'information'
        })
        result = get_user_by_identifier(account['identifier'], self.tree_base, self.connection)
        if result:
            account_dn = result[0][0]
            if set_password(account_dn, account['password'], self.connection):
                write_json_log({
                    'action': 'change_account_password_success',
                    'account': account,
                    'message': 'Changing account password: ' + account['username'] + ' - ' + account['identifier'],
                    'level': 'information'
                })
            else:
                write_json_error({
                    'action': 'change_account_password_fail',
                    'account': account,
                    'message': 'Failed to change account password: ' + account['username'] + ' - ' + account[
                        'identifier'],
                    'level': 'warning'
                })

    def create_group(self, group, group_type):
        write_json_log({
            'action': 'create_group',
            'group': group,
            'group_type': group_type,
            'message': 'Creating group',
            'level': 'information'
        })
        group_cn = build_group_cn(group)
        group_dn = build_group_dn(group_cn, group_type, self.settings['base_group_ou_dn'])
        if create_group(group_cn, group_dn, group['label'], self.tree_base, self.connection):
            write_json_log({
                'action': 'create_group_success',
                'group': group,
                'group_type': group_type,
                'group_cn': group_cn,
                'group_dn': group_dn,
                'message': 'Created group',
                'level': 'information'
            })
        else:
            write_json_error({
                'action': 'create_group_fail',
                'group': group,
                'group_type': group_type,
                'group_cn': group_cn,
                'group_dn': group_dn,
                'message': 'Failed to create group',
                'level': 'warning'
            })

    def restore_group(self, group, group_type):
        write_json_log({
            'action': 'restore_group',
            'group': group,
            'group_type': group_type,
            'message': 'Restoring group',
            'level': 'information'
        })
        group_cn = build_group_cn(group)
        group_dn = build_group_dn(group_cn, group_type, self.settings['base_group_ou_dn'])
        if create_group(group_cn, group_dn, group['label'], self.tree_base, self.connection):
            write_json_log({
                'action': 'restore_group_success',
                'group': group,
                'group_type': group_type,
                'group_cn': group_cn,
                'group_dn': group_dn,
                'message': 'Restored group',
                'level': 'information'
            })
        else:
            write_json_error({
                'action': 'restore_group_fail',
                'group': group,
                'group_type': group_type,
                'group_cn': group_cn,
                'group_dn': group_dn,
                'message': 'Failed to restore group',
                'level': 'warning'
            })

    def delete_group(self, group, group_type):
        write_json_log({
            'action': 'delete_group',
            'group': group,
            'group_type': group_type,
            'message': 'Deleting group',
            'level': 'information'
        })
        group_cn = build_group_cn(group)
        group_dn = build_group_dn(group_cn, group_type, self.settings['base_group_ou_dn'])
        if delete_group(group_dn, self.tree_base, self.connection):
            write_json_log({
                'action': 'delete_group_success',
                'group': group,
                'group_type': group_type,
                'group_cn': group_cn,
                'group_dn': group_dn,
                'message': 'Deleted group',
                'level': 'information'
            })
        else:
            write_json_error({
                'action': 'delete_group_fail',
                'group': group,
                'group_type': group_type,
                'group_cn': group_cn,
                'group_dn': group_dn,
                'message': 'Failed to delete group',
                'level': 'warning'
            })

    def add_account_to_group(self, account, group, group_type):
        write_json_log({
            'action': 'add_account_to_group',
            'account': account,
            'group': group,
            'group_type': group_type,
            'message': 'Adding account to group',
            'level': 'information'
        })
        result = get_user_by_identifier(account['identifier'], self.tree_base, self.connection)
        if result:
            account_dn = result[0][0]
            group_cn = build_group_cn(group)
            group_dn = build_group_dn(group_cn, group_type, self.settings['base_group_ou_dn'])
            group_result = get_group(group_dn, self.tree_base, self.connection)
            if not group_result:
                self.create_group(group, group_type)
            if add_to_group(account_dn, group_dn, self.tree_base, self.connection):
                write_json_log({
                    'action': 'add_account_to_group_success',
                    'account': account,
                    'account_dn': account_dn,
                    'group': group,
                    'group_type': group_type,
                    'group_cn': group_cn,
                    'group_dn': group_dn,
                    'message': 'Added account to group: ' + account['username'] + ' - ' + account[
                        'identifier'] + ' -->> ' + group_cn,
                    'level': 'information'
                })
            else:
                write_json_error({
                    'action': 'add_account_to_group_fail',
                    'account': account,
                    'account_dn': account_dn,
                    'group': group,
                    'group_type': group_type,
                    'group_cn': group_cn,
                    'group_dn': group_dn,
                    'message': 'Failed to add account to group: ' + account['username'] + ' - ' + account[
                        'identifier'] + ' --!! ' + group_cn,
                    'level': 'warning'
                })

    def remove_account_from_group(self, account, group, group_type):
        write_json_log({
            'action': 'remove_account_from_group',
            'account': account,
            'group': group,
            'group_type': group_type,
            'message': 'Removing account from group',
            'level': 'information'
        })
        result = get_user_by_identifier(account['identifier'], self.tree_base, self.connection)
        if result:
            account_dn = result[0][0]
            group_cn = build_group_cn(group)
            group_dn = build_group_dn(group_cn, group_type, self.settings['base_group_ou_dn'])
            group_result = get_group(group_dn, self.tree_base, self.connection)
            if not group_result:
                self.create_group(group, group_type)
            if remove_from_group(account_dn, group_dn, self.tree_base, self.connection):
                write_json_log({
                    'action': 'remove_account_from_group_success',
                    'account': account,
                    'account_dn': account_dn,
                    'group': group,
                    'group_type': group_type,
                    'group_cn': group_cn,
                    'group_dn': group_dn,
                    'message': 'Removed account from group: ' + account['username'] + ' - ' + account[
                        'identifier'] + ' ---- ' + group_cn,
                    'level': 'information'
                })
            else:
                write_json_error({
                    'action': 'remove_account_from_group_fail',
                    'account': account,
                    'account_dn': account_dn,
                    'group': group,
                    'group_type': group_type,
                    'group_cn': group_cn,
                    'group_dn': group_dn,
                    'message': 'Failed to remove account from group: ' + account['username'] + ' - ' + account[
                        'identifier'] + ' --!! ' + group_cn,
                    'level': 'warning'
                })

    def add_group_to_group(self, target_group, target_group_type, des_group, des_group_type):
        write_json_log({
            'action': 'add_group_to_group',
            'target_group': target_group,
            'target_group_type': target_group_type,
            'des_group': des_group,
            'des_group_type': des_group_type,
            'message': 'Adding group to group',
            'level': 'information'
        })
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
            write_json_log({
                'action': 'add_group_to_group_success',
                'target_group': target_group,
                'target_group_type': target_group_type,
                'des_group': des_group,
                'des_group_type': des_group_type,
                'message': 'Added group to group',
                'level': 'information'
            })
        else:
            write_json_error({
                'action': 'add_group_to_group_fail',
                'target_group': target_group,
                'target_group_type': target_group_type,
                'des_group': des_group,
                'des_group_type': des_group_type,
                'message': 'Failed to add group to group',
                'level': 'warning'
            })

    def remove_group_from_group(self, target_group, target_group_type, des_group, des_group_type):
        write_json_log({
            'action': 'remove_group_from_group',
            'target_group': target_group,
            'target_group_type': target_group_type,
            'des_group': des_group,
            'des_group_type': des_group_type,
            'message': 'Removing group from group',
            'level': 'information'
        })
        target_group_dn = build_group_dn(build_group_cn(target_group), target_group_type,
                                         self.settings['base_group_ou_dn'])
        des_group_dn = build_group_dn(build_group_cn(des_group), des_group_type, self.settings['base_group_ou_dn'])
        if remove_from_group(target_group_dn, des_group_dn, self.tree_base, self.connection):
            write_json_log({
                'action': 'remove_group_from_group_success',
                'target_group': target_group,
                'target_group_type': target_group_type,
                'des_group': des_group,
                'des_group_type': des_group_type,
                'message': 'Removed group from group',
                'level': 'information'
            })
        else:
            write_json_error({
                'action': 'remove_group_from_group_fail',
                'target_group': target_group,
                'target_group_type': target_group_type,
                'des_group': des_group,
                'des_group_type': des_group_type,
                'message': 'Failed to remove group from group',
                'level': 'warning'
            })
