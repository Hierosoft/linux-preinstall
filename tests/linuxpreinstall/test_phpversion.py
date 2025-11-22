# tests/linuxpreinstall/test_phpversion.py
import json

from linuxpreinstall.phpversion import get_php_package_groups


def get_installed_dummy():
    return [
        "ea-php54-php-zip-5.4.45-81.82.2.cpanel.x86_64",
        "ea-php55-pear-1.10.16-4.8.19.cpanel.noarch",
        "ea-php55-php-pdo-5.5.38-64.65.2.cpanel.x86_64",
        "ea-php72-php-xml-7.2.34-11.13.2.cpanel.x86_64",
        "alt-php-internal-cli-8.2.28-6.el7.x86_64",
        "cpanel-php81-date-holidays-croatia-0.1.1-1.cp110~el7.noarch",
    ]


def test_get_php_package_groups_with_dummy_data():
    groups = get_php_package_groups(get_installed_fn=get_installed_dummy)

    for key, group in groups.items():
        assert group == sorted(group), f"Group '{key}' is not sorted"

    assert groups['unversioned_modules'] == [
        "alt-php-internal-cli-8.2.28-6.el7.x86_64",
    ]

    assert set(groups['versioned_modules']) == {
        "ea-php54-php-zip-5.4.45-81.82.2.cpanel.x86_64",
        "ea-php55-pear-1.10.16-4.8.19.cpanel.noarch",
        "ea-php55-php-pdo-5.5.38-64.65.2.cpanel.x86_64",
        "ea-php72-php-xml-7.2.34-11.13.2.cpanel.x86_64",
    }

    assert groups['versions'] == []
    assert groups['other_versioned'] == []
    assert groups['other'] == [
        "cpanel-php81-date-holidays-croatia-0.1.1-1.cp110~el7.noarch",
    ]


def test_get_php_package_groups_edge_cases():
    def edge_dummy():
        return [
            "php7.4-json",
            "php8.1",
            "php-cli",
            "libapache2-mod-php8.2",
            "ea-php83-php-mysqli",
            "alt-php80",
            "alt-php80-mysqli",
            "some-random-php-thing",
            "ea-php71-7.1.33-6.6.4.cpanel.x86_64",
        ]

    groups = get_php_package_groups(get_installed_fn=edge_dummy)

    assert "some-random-php-thing" in groups['other']

    assert "libapache2-mod-php8.2" in groups['other_versioned']

    assert "php-cli" in groups['unversioned_modules']

    assert "php7.4-json" in groups['versioned_modules']
    assert "ea-php83-php-mysqli" in groups['versioned_modules']
    assert "alt-php80-mysqli" in groups['versioned_modules'], \
        "{}".format(json.dumps(groups, indent=2))

    assert "ea-php71" in groups['versions']
    assert "php8.1" in groups['versions']
    assert "alt-php80" in groups['versions'], \
        "{}".format(json.dumps(groups, indent=2))

