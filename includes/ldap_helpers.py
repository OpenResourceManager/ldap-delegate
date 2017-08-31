from __future__ import print_function
import ldap
from ldap import modlist


def connect(bind_user, bind_pass, hosts):
    connection = False
    for host in hosts:
        try:
            ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, 0)
            ldap.set_option(ldap.OPT_REFERRALS, 0)
            ldap.protocol_version = ldap.VERSION3
            connection = ldap.initialize('ldaps://' + host + ':636')
            connection.simple_bind_s(bind_user, bind_pass)
            if connection:
                return connection
        except ldap.LDAPError, error_message:
            print("Error connecting to LDAP server: " + host + ' ' + str(error_message))
    return connection


def build_duty_ou_dn(name, base_account_ou):
    return 'OU=' + ldap.dn.escape_dn_chars(name) + ',' + base_account_ou


def build_trash_ou_dn(base_account_ou):
    return 'OU=Trash,' + base_account_ou


def build_group_cn(group):
    return group['code']


def build_group_dn(cn, type_name, base_ou):
    return 'CN=' + ldap.dn.escape_dn_chars(cn) + ',' + 'OU=' + ldap.dn.escape_dn_chars(type_name) + ',' + base_ou


def build_account_dn(cn, ou):
    return 'CN=' + ldap.dn.escape_dn_chars(cn) + ',' + ou


def build_account_ou(account, base_ou, duties_map_to_ou):
    ou = base_ou
    if duties_map_to_ou:
        ou = 'OU=' + ldap.dn.escape_dn_chars(account['primary_duty']['code']) + ',' + ou
    return ou


def build_account_ext_name(account):
    ext_name = account['name_last'].capitalize() + ','
    ext_name = ext_name + ' ' + account['name_first'].capitalize()
    middle = form_middle_name(account)
    if middle:
        ext_name = ext_name + ' ' + middle.capitalize()

    return str(ext_name)


def build_initials(account):
    middle = form_middle_name(account)
    f = account['name_first'][0].capitalize()
    if len(middle) > 0:
        m = middle[0].capitalize()
    else:
        m = ''
    l = account['name_last'][0].capitalize()
    return str(f + m + l)


def build_home_share_path(account, pattern):
    parts = pattern.split('%')
    path = []
    for part in parts:
        if part.lower() == 'samaccountname':
            path.append(account['username'])
        elif part.lower() == 'employeeid':
            path.append(account['identifier'])
        else:
            path.append(part)
    return ''.join(path)


def build_unicode_password(password):
    try:
        unicode_pass = unicode('\"' + password + '\"', 'iso-8859-1')
    except TypeError:
        unicode_pass = '\"' + password + '\"'

    return unicode_pass.encode('utf-16-le')


def form_set_password_action(unicode_password):
    return [(ldap.MOD_REPLACE, 'unicodePwd', [unicode_password]), (ldap.MOD_REPLACE, 'pwdLastSet', '-1')]


def form_set_account_control_action(account_control):
    return [(ldap.MOD_REPLACE, 'userAccountControl', str(account_control))]


def form_add_member_action(account_dn):
    return [(ldap.MOD_ADD, 'member', str(account_dn))]


def form_modify_action(attributes):
    modify_actions = []
    for key, value in attributes.iteritems():
        key = str(key).strip(' \t\n\r')
        value = str(value).strip(' \t\n\r')
        if key and value:
            modify_actions.append((ldap.MOD_REPLACE, key, value))
    return modify_actions


def form_del_member_action(account_dn):
    return [(ldap.MOD_DELETE, 'member', str(account_dn))]


def form_middle_name(account):
    if 'name_middle' in account:
        if account['name_middle']:
            return str(account['name_middle'])
    return ''


def form_user(account, mail_domain, home_share_path, home_drive_letter='H'):
    return {
        'description': 'ID: ' + str(account['identifier']) + ' - automatically managed by ORM',
        'displayName': str(account['name_full']),
        'givenName': str(account['name_first'].capitalize()),
        'middleName': form_middle_name(account),
        'sn': str(account['name_last'].capitalize()),
        'extensionName': build_account_ext_name(account),
        'employeeID': str(account['identifier']),
        'homeDirectory': str(home_share_path),
        'homeDrive': str(home_drive_letter[0].upper()) + ':',
        'mail': str(account['username']) + '@' + str(mail_domain),
        'sAMAccountName': str(account['username']),
        'initials': build_initials(account),
        'userAccountControl': '514',
        'objectClass': ['top', 'organizationalPerson', 'person', 'user']
    }


def form_group(cn, dn, display_name):
    return {
        'objectClass': ['top', 'group'],
        'cn': str(cn),
        'distinguishedName': str(dn),
        'groupType': '-2147483646',
        'description': str(cn) + ' ' + str(display_name) + ' - automatically managed by ORM',
        'name': str(cn),
        'sAMAccountName': str(cn),
        'displayName': str(display_name)
    }


def form_ou(cn, dn):
    return {
        'objectClass': ['top', 'organizationalUnit'],
        'distinguishedName': str(dn),
        'ou': str(cn)
    }


def get_user_by_dn(dn, base_dn, connection):
    ldap_filter = '(&(objectClass=top)(objectClass=person)(objectClass=user)(distinguishedName=' + dn + '))'
    return __get_user(base_dn, connection, ldap_filter)


def get_user_by_username(username, base_dn, connection):
    ldap_filter = '(&(objectClass=top)(objectClass=person)(objectClass=user)(sAMAccountName=' + username + '))'
    return __get_user(base_dn, connection, ldap_filter)


def get_user_by_identifier(identifier, base_dn, connection):
    ldap_filter = '(&(objectClass=top)(objectClass=person)(objectClass=user)(employeeID=' + identifier + '))'
    return __get_user(base_dn, connection, ldap_filter)


def __get_user(base_dn, connection, ldap_filter):
    attributes = ['objectGUID', 'cn', 'samAccountName', 'employeeID', 'distinguishedName', 'description', 'displayName',
                  'extensionName', 'givenName', 'homeDirectory', 'homeDrive', 'mail', 'middleName', 'name',
                  'objectCategory', 'objectClass', 'primaryGroupID', 'sAMAccountName', 'sAMAccountType', 'sn',
                  'initials', 'userAccountControl', 'userPrincipalName', ]
    return perform_search(ldap_filter, base_dn, connection, attributes)


def get_group(dn, base_dn, connection):
    ldap_filter = '(&(objectClass=top)(objectClass=group)(distinguishedName=' + dn + '))'
    return perform_search(ldap_filter, base_dn, connection, ['objectGUID'])


def get_ou(dn, base_dn, connection):
    ldap_filter = '(&(objectClass=top)(|(objectClass=organizationalUnit)(objectClass=container))(distinguishedName=' + dn + '))'
    return perform_search(ldap_filter, base_dn, connection, ['objectGUID'])


def verify_parent_ou_exists(target_dn, tree_base, connection):
    parent_ou_parts = target_dn.split(',')
    parent_ou_parts.pop(0)
    parent_ou_dn = ','.join(parent_ou_parts)
    # Create the parent ou for the group if it does not exist
    if not get_ou(parent_ou_dn, tree_base, connection):
        cn = parent_ou_dn.split(',').pop(0).strip('OU=')
        formed_ou = form_ou(cn, parent_ou_dn)
        if not create_object(parent_ou_dn, formed_ou, connection):
            return False
    return True


def perform_search(ldap_filter, base_dn, connection, attributes):
    try:
        results = connection.search_s(str(base_dn).strip(' \t\n\r'), ldap.SCOPE_SUBTREE, ldap_filter, attributes)
        if not results[0][0]:
            return False
        else:
            return results
    except ldap.LDAPError, error_message:
        print("Search error: " + str(error_message))
        return False


def create_object(dn, formed_object, connection):
    try:
        return connection.add_s(dn, modlist.addModlist(formed_object))
    except ldap.LDAPError, error_message:
        print("Add error: " + str(error_message))
        return False


def modify_object(dn, action, connection):
    try:
        return connection.modify_s(dn, action)
    except ldap.LDAPError, error_message:
        print("Modify error: " + str(error_message))
        return False


def delete_object(dn, connection):
    try:
        return connection.delete_s(dn)
    except ldap.LDAPError, error_message:
        print("Delete error: " + str(error_message))
        return False


def rename_object(current_dn, new_cn, new_ou, connection):
    try:
        return connection.rename_s(current_dn, 'CN=' + new_cn, new_ou)
    except ldap.LDAPError, error_message:
        print("Rename error: " + str(error_message))
        return False


def create_ou(cn, dn, connection):
    ou_object = form_ou(cn, dn)
    result = create_object(dn, ou_object, connection)
    if result:
        return result
    else:
        print('Error creating OU: ' + dn)
        return False


def create_group(cn, dn, display_name, tree_base, connection):
    verify_parent_ou_exists(dn, tree_base, connection)
    group_object = form_group(cn, dn, display_name)
    result = create_object(dn, group_object, connection)
    if result:
        return result
    else:
        print('Error creating Group: ' + dn)
        return False


def delete_group(dn, tree_base, connection):
    group_exists = get_group(dn, tree_base, connection)
    if group_exists:
        result = delete_object(dn, connection)
        if not result:
            return False
    return True


def set_password(dn, password, connection):
    unicode_passwd = build_unicode_password(password)
    set_password_action = form_set_password_action(unicode_passwd)
    result = modify_object(dn, set_password_action, connection)
    if result:
        return result
    else:
        print('Error setting password for: ' + dn)
        return False


def enable_account(dn, connection):
    enable_account_action = form_set_account_control_action('512')
    result = modify_object(dn, enable_account_action, connection)
    if result:
        return result
    else:
        print('Error enabling account: ' + dn)
        return False


def disable_account(dn, connection):
    disable_account_action = form_set_account_control_action('514')
    result = modify_object(dn, disable_account_action, connection)
    if result:
        return result
    else:
        print('Error disabling account: ' + dn)
        return False


def check_group_membership(target_dn, group_dn, tree_base, connection):
    ldap_filter = '(&(distinguishedName=' + target_dn + ')(memberof=' + group_dn + '))'
    result = perform_search(ldap_filter, tree_base, connection, ['objectGUID'])
    if result:
        return True
    else:
        return False


def add_to_group(target_dn, group_dn, tree_base, connection):
    if not check_group_membership(target_dn, group_dn, tree_base, connection):
        add_member = form_add_member_action(target_dn)
        result = modify_object(group_dn, add_member, connection)
        if result:
            return result
        else:
            print('Error adding ' + target_dn + ' to Group: ' + group_dn)
            return False
    return True


def remove_from_group(target_dn, group_dn, tree_base, connection):
    if check_group_membership(target_dn, group_dn, tree_base, connection):
        del_member = form_del_member_action(target_dn)
        result = modify_object(group_dn, del_member, connection)
        if result:
            return result
        else:
            print('Error removing ' + target_dn + ' from Group: ' + group_dn)
            return False
    return True


def add_account_to_primary_duty_group(account_dn, group_dn, group_cn, group_display_name, tree_base, connection):
    if not get_group(group_dn, tree_base, connection):
        create_group(group_cn, group_dn, group_display_name, tree_base, connection)
    if add_to_group(account_dn, group_dn, tree_base, connection):
        return True
    else:
        return False


def create_account(account, connection, settings):
    ou = build_account_ou(account, settings['base_user_ou_dn'], settings['duties_map_to_ou'])
    dn = build_account_dn(account['username'], ou)
    primary_duty_group_dn = build_group_dn(account['primary_duty']['code'], 'Duty', settings['base_group_ou_dn'])
    home_share_path = build_home_share_path(account, settings['home_drive_path_pattern'])
    new_account = form_user(account, settings['email_domain'], home_share_path, settings['home_drive_letter'])
    verify_parent_ou_exists(dn, settings['tree_base'], connection)
    if create_object(dn, new_account, connection):
        # If we should propagate the password then set it
        if account['should_propagate_password']:
            set_password(dn, account['password'], connection)
        # Enable the account
        enable_account(dn, connection)
        # Add the account to a group based on it's primary duty
        add_account_to_primary_duty_group(
            dn,
            primary_duty_group_dn,
            account['primary_duty']['code'],
            account['primary_duty']['label'],
            settings['tree_base'],
            connection
        )

    return True


def modify_account(account, old_ldap_account, connection, settings):
    new_ou = build_account_ou(account, settings['base_user_ou_dn'], settings['duties_map_to_ou'])
    new_dn = build_account_dn(account['username'], new_ou)
    home_share_path = build_home_share_path(account, settings['home_drive_path_pattern'])
    renamed = False
    primary_duty_group_dn = build_group_dn(account['primary_duty']['code'], 'Duty', settings['base_group_ou_dn'])
    new_attributes = form_user(account, settings['email_domain'], home_share_path, settings['home_drive_letter'])
    old_dn = old_ldap_account[0][0]
    old_attributes = old_ldap_account[0][1]
    final_attributes = {}

    # Strip any attributes from the modification that have not changed
    for k, v in new_attributes.iteritems():
        if not k == 'objectClass':
            if not k == 'userAccountControl':
                if not v == '':
                    if v:
                        if k in old_attributes:
                            if not v == old_attributes[k][0]:
                                final_attributes[k] = v
                        else:
                            final_attributes[k] = v

    # If the old dn does not equal the new dn move the account object
    if not new_dn == old_dn:
        verify_parent_ou_exists(new_dn, settings['tree_base'], connection)
        rename_object(old_dn, account['username'], new_ou, connection)
        renamed = True

    # Determine if we are modifying a new DN or the original DN based on if the account moved
    dn_to_modify = new_dn if renamed else old_dn

    # If the final attributes to modify are not empty modify the account
    if final_attributes:
        modify_actions = form_modify_action(final_attributes)
        modify_object(dn_to_modify, modify_actions, connection)
        enable_account(dn_to_modify, connection)

    # If we should propagate the password then set it
    if account['should_propagate_password']:
        set_password(dn_to_modify, account['password'], connection)

    # Add the account to a group based on it's primary duty
    add_account_to_primary_duty_group(
        dn_to_modify,
        primary_duty_group_dn,
        account['primary_duty']['code'],
        account['primary_duty']['label'],
        settings['tree_base'],
        connection
    )

    return True


def create_or_modify_account(account, connection, tree_base, settings):
    old_account = get_user_by_identifier(account['identifier'], tree_base, connection)
    if old_account:
        modify_account(account, old_account, connection, settings)
    else:
        create_account(account, connection, settings)
    return True


def delete_or_disable_account(account, connection, settings):
    result = get_user_by_username(account['username'], settings['tree_base'], connection)
    account_dn = result[0][0]
    if settings['delete_users']:
        delete_object(account_dn, connection)
    else:
        disable_account(account_dn, connection)
        if settings['use_trash_ou']:
            if account_dn != ''.join(['CN=', account['username'], ',', build_trash_ou_dn(settings['base_user_ou_dn'])]):
                rename_object(
                    account_dn,
                    account['username'],
                    build_trash_ou_dn(settings['base_user_ou_dn']),
                    connection
                )
    return True
