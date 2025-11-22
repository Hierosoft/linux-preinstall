# tests/linuxpreinstall/test_module.py

from linuxpreinstall import (
    PackageVersion,
    sorted_versions,
    find_not_decimal,
    rfind_not_decimal,
    split_package_parts,
)
from linuxpreinstall.lplogging import human_readable


def test_human_readable():
    assert human_readable(1_000_000) == "976.56K"
    assert human_readable(1_000_000, 1) == "976.6K"
    assert human_readable(1_000_000, 3) == "976.562K"
    assert human_readable(1_000_000, 10) == "976.5625K"


def test_sorted_versions():
    versions = [
        "4.5", "4.6-api", "4.5.2-api", "4.5-api", "4.7.1-api",
        "4.6.1-api", "4.7-api", "4.5.1-api", "4.40", "4.8-api",
        "4.7.2-api", "4.6.2-api",
    ]
    expected = [
        "4.5", "4.5-api", "4.5.1-api", "4.5.2-api",
        "4.6-api", "4.6.1-api", "4.6.2-api",
        "4.7-api", "4.7.1-api", "4.7.2-api",
        "4.8-api", "4.40",
    ]
    assert sorted_versions(versions) == expected


def test_split_package_parts_basic():
    assert split_package_parts("php7.3-pgsql") == ["php", "7.3", "pgsql"]
    assert split_package_parts("php7.4") == ["php", "7.4"]
    assert split_package_parts("php") == ["php"]


def test_split_package_parts_libapache():
    # Current behavior: version is kept attached (known limitation)
    assert split_package_parts("libapache2-mod-php7.3") == ["libapache2-mod-php7.3"]
    assert split_package_parts("libapache2-mod-php8.1") == ["libapache2-mod-php8.1"]


def test_split_package_parts_hyphenated_prefixes():
    version80 = PackageVersion(original="80", modified="8.0")
    version74 = PackageVersion(original="74", modified="7.4")
    version82 = PackageVersion(original="82", modified="8.2")
    assert split_package_parts("ea-php80-php-fpm") == ["ea-php", version80, "php-fpm"]
    assert split_package_parts("ea-php74") == ["ea-php", version74]
    assert split_package_parts("alt-php82-xml") == ["alt-php", version82, "xml"]
    assert split_package_parts("alt-php-internal-cli") == ["alt-php", "internal-cli"]

    parts = split_package_parts("ea-php71-7.1.33-6.6.4.cpanel.x86_64")
    version71 = PackageVersion(original="71", canonized="7.1")
    assert parts == ["ea-php", version71]


def test_rfind_not_decimal_is_correct():
    # "php7.3-pgsql"
    #  p h p 7 . 3 - p g s q l
    #  0 1 2 3 4 5 6 7 8 9 10 11
    s = "php7.3-pgsql"
    assert rfind_not_decimal(s) == 11                # 'l'

    assert rfind_not_decimal("php7.3") == 2            # 'p' in "php7.3"
    assert rfind_not_decimal("123.456") == -1          # all digits/dot
    assert rfind_not_decimal("version9") == 6          # 'n' in "version9"
    assert rfind_not_decimal("abc123def456") == 8      # 'f' before "456"
    assert rfind_not_decimal("endswithnum123") == 10    # 'm' before "123"


def test_find_not_decimal_forward():
    s = "php7.3-pgsql"
    assert find_not_decimal(s, start=0) == 0    # 'p'
    assert find_not_decimal(s, start=3) == 6    # skips "7.3", finds '-'
    assert find_not_decimal(s, start=6) == 6    # '-'
    assert find_not_decimal(s, start=7) == 7    # 'p' in "pgsql"