#!/usr/bin/env python
"""

Purpose: Generate output to redo table creations and insertions
that were not done when using
mysql  Ver 8.0.36-0ubuntu0.22.04.1 for Linux on x86_64 ((Ubuntu))
to restore the database.

Usage:
- Linux:
  python3 dxinstall-backup-validator.py 1>redo-rows.sql
  
- Windows:
  python3 dxinstall-backup-validator.py 1>redo-rows.sql 2>screen_output.txt
- from the console into mysql:
```
mysql
use NAME;
source redo-tables.sql
source redo-rows.sql
```
- where NAME is the database name.

"""

# Additional issues
## Output of source redo-tables.sql is:
"""
ERROR 1067 (42000): Invalid default value for 'comment_date'
ERROR 1067 (42000): Invalid default value for 'link_updated'
ERROR 1067 (42000): Invalid default value for 'post_date'
ERROR 1067 (42000): Invalid default value for 'user_registered'
ERROR 1067 (42000): Invalid default value for 'scheduled_date_gmt'
ERROR 1067 (42000): Invalid default value for 'date_created_gmt'
ERROR 1067 (42000): Invalid default value for 'log_date_gmt'
ERROR 1067 (42000): Invalid default value for 'comment_date'
ERROR 1067 (42000): Invalid default value for 'created'
ERROR 1067 (42000): Invalid default value for 'link_updated'
ERROR 1067 (42000): Invalid default value for 'post_date'
ERROR 1067 (42000): Invalid default value for 'user_registered'
ERROR 1067 (42000): Invalid default value for 'date_created'
ERROR 1067 (42000): Invalid default value for 'date_created'
ERROR 1067 (42000): Invalid default value for 'date_created'
ERROR 1067 (42000): Invalid default value for 'date_created'
ERROR 1067 (42000): Invalid default value for 'date_created'
ERROR 1067 (42000): Invalid default value for 'timestamp'
ERROR 1067 (42000): Invalid default value for 'date_created'
ERROR 1067 (42000): Invalid default value for 'access_granted'
"""
# SOLVED: Added the following to the beginning of the SQL file as per <https://stackoverflow.com/a/69987301>:
# SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO"; 
# SET time_zone = "+00:00";

## "There has been a critical error on this website."
# (shows upon visiting the site)
# /var/log/nginx/error.log (log location differs according to conf in /etc/nginx/sites-enabled) says:
"""
2024/03/29 16:01:43 [error] 26277#26277: *1 FastCGI sent in stderr: "PHP message: PHP Fatal error:  Uncaught TypeError: call_user_func_array(): Argument #1 (>
Stack trace:
#0 /var/www/dxinstalls.com/wp-includes/class-wp-hook.php(348): WP_Hook->apply_filters()
#1 /var/www/dxinstalls.com/wp-includes/plugin.php(517): WP_Hook->do_action()
#2 /var/www/dxinstalls.com/wp-settings.php(643): do_action()
#3 /var/www/dxinstalls.com/wp-config.php(81): require_once('...')
#4 /var/www/dxinstalls.com/wp-load.php(50): require_once('...')
#5 /var/www/dxinstalls.com/wp-blog-header.php(13): require_once('...')
#6 /var/www/dxinstalls.com/index.php(17): require('...')
#7 {main}
  thrown in /var/www/dxinstalls.com/wp-includes/class-wp-hook.php on line 324" while reading response header from upstream, client: 127.0.0.1, server: design>

"""
# SOLVED: downgraded back to PHP 7.4 as per <https://wordpress.org/support/topic/php-fatal-error-uncaught-typeerror-call_user_func_array-argument-1-callb/>

## Redirecting to old domain after restore
# See <https://wordpress.stackexchange.com/questions/187574/redirecting-to-old-domain-after-migration>:
# Add the following to wp-config.php: define('RELOCATE',true);


from __future__ import division
from __future__ import print_function
import os
import sys

from collections import OrderedDict

BACKUP = "/var/www/dxinstalls.com/xcloner-44bc6/database-backup.sql"

# The tables in restored_tables are the only tables actually restored
# after running the sql produced by xcloner, according to mysql> SHOW TABLES;
restored_tables = (
    b"wp_9dghqw_commentmeta",
    b"wp_9dghqw_options",
    b"wp_9dghqw_postmeta",
    b"wp_9dghqw_term_relationships",
    b"wp_9dghqw_term_taxonomy",
    b"wp_9dghqw_termmeta",
    b"wp_9dghqw_terms",
    b"wp_9dghqw_usermeta",
    b"wp_atrz2c_actionscheduler_groups",
    b"wp_atrz2c_commentmeta",
    b"wp_atrz2c_ee_ai_reportdata",
    b"wp_atrz2c_ee_product_feed",
    b"wp_atrz2c_ee_product_sync_call",
    b"wp_atrz2c_ee_product_sync_data",
    b"wp_atrz2c_ee_products_sync_list",
    b"wp_atrz2c_ee_tiktok_catalog",
    b"wp_atrz2c_failed_jobs",
    b"wp_atrz2c_mailchimp_carts",
    b"wp_atrz2c_mailchimp_jobs",
    b"wp_atrz2c_options",
    b"wp_atrz2c_postmeta",
    b"wp_atrz2c_queue",
    b"wp_atrz2c_term_relationships",
    b"wp_atrz2c_term_taxonomy",
    b"wp_atrz2c_termmeta",
    b"wp_atrz2c_terms",
    b"wp_atrz2c_usermeta",
    b"wp_atrz2c_wc_admin_note_actions",
    b"wp_atrz2c_wc_category_lookup",
    b"wp_atrz2c_wc_customer_lookup",
    b"wp_atrz2c_wc_download_log",
    b"wp_atrz2c_wc_order_addresses",
    b"wp_atrz2c_wc_order_operational_data",
    b"wp_atrz2c_wc_orders",
    b"wp_atrz2c_wc_orders_meta",
    b"wp_atrz2c_wc_product_attributes_lookup",
    b"wp_atrz2c_wc_product_download_directories",
    b"wp_atrz2c_wc_product_meta_lookup",
    b"wp_atrz2c_wc_rate_limits",
    b"wp_atrz2c_wc_tax_rate_classes",
    b"wp_atrz2c_wfBadLeechers",
    b"wp_atrz2c_wfBlockedCommentLog",
    b"wp_atrz2c_wfBlockedIPLog",
    b"wp_atrz2c_wfBlocks",
    b"wp_atrz2c_wfBlocksAdv",
    b"wp_atrz2c_wfConfig",
    b"wp_atrz2c_wfCrawlers",
    b"wp_atrz2c_wfFileMods",
    b"wp_atrz2c_wfHits",
    b"wp_atrz2c_wfHoover",
    b"wp_atrz2c_wfIssues",
    b"wp_atrz2c_wfKnownFileList",
    b"wp_atrz2c_wfLeechers",
    b"wp_atrz2c_wfLockedOut",
    b"wp_atrz2c_wfLocs",
    b"wp_atrz2c_wfLogins",
    b"wp_atrz2c_wfNet404s",
    b"wp_atrz2c_wfNotifications",
    b"wp_atrz2c_wfPendingIssues",
    b"wp_atrz2c_wfReverseCache",
    b"wp_atrz2c_wfSNIPCache",
    b"wp_atrz2c_wfScanners",
    b"wp_atrz2c_wfStatus",
    b"wp_atrz2c_wfThrottleLog",
    b"wp_atrz2c_wfVulnScanners",
    b"wp_atrz2c_woocommerce_api_keys",
    b"wp_atrz2c_woocommerce_attribute_taxonomies",
    b"wp_atrz2c_woocommerce_log",
    b"wp_atrz2c_woocommerce_order_itemmeta",
    b"wp_atrz2c_woocommerce_order_items",
    b"wp_atrz2c_woocommerce_payment_tokenmeta",
    b"wp_atrz2c_woocommerce_payment_tokens",
    b"wp_atrz2c_woocommerce_sessions",
    b"wp_atrz2c_woocommerce_shipping_zone_locations",
    b"wp_atrz2c_woocommerce_shipping_zone_methods",
    b"wp_atrz2c_woocommerce_shipping_zones",
    b"wp_atrz2c_woocommerce_tax_rate_locations",
    b"wp_atrz2c_woocommerce_tax_rates",
    b"wp_atrz2c_xcloner_scheduler",
    b"wp_atrz2c_yoast_seo_links",
    b"wp_atrz2c_yoast_seo_meta",
)

redo = (  # This list can be regenerated using this program, if restored_tables is correct.
    b"wp_9dghqw_comments",
    b"wp_9dghqw_posts",
    b"wp_9dghqw_users",
    b"wp_atrz2c_actionscheduler_actions",
    b"wp_atrz2c_actionscheduler_logs",
    b"wp_atrz2c_comments",
    b"wp_atrz2c_duplicator_packages",
    b"wp_atrz2c_posts",
    b"wp_atrz2c_users",
    b"wp_atrz2c_wc_admin_notes",
    b"wp_atrz2c_wc_order_coupon_lookup",
    b"wp_atrz2c_wc_order_product_lookup",
    b"wp_atrz2c_wc_order_stats",
)


def echo0(*args, **kwargs):
    """Print to stderr
    
    Only INSERT statements should go to stdout in this program,
    so redirecting output to a new SQL file (to redo missed insertions)
    is possible.
    """
    print(*args, file=sys.stderr, **kwargs)


def percent_str(ratio):
    return "{}%".format(round(ratio))    


def percent_int_str(index, size):
    return "{}%".format(round(index/size))


def no_enclosures(value, pairs=((b"`", b"`"),)):
    for pair in pairs:
        if len(pair) != 2:
            raise ValueError(
                "Each pair must be 2 strings or a string of length 2"
                " but pair={}".format(pair)
            )
        elif isinstance(pair[1], int):
            raise ValueError(
                "A bytes pair must be split into two bytes objects,"
                " otherwise indexing it will result in int"
                " (That could also be resolved by slicing,"
                " but that would break list/tuple compatibility)!"
            )
        if len(value) >= len(pair[0]) + len(pair[1]):
            # ^ Slicing is used, since indexing a bytes object would
            #   result in an int!
            if value.startswith(pair[0]) and value.endswith(pair[1]):
                value = value[1:-1]
    return value


def collect_info(backup_sql_path):
    used_tables = []
    created_tables = []
    warned_tables = set()
    line_n = 0
    total = os.stat(backup_sql_path).st_size
    last_ratio = 0
    create_statements = OrderedDict()
    creating = None
    inserting = None
    multi_line = None
    with open(backup_sql_path, 'rb') as stream:
        for rawL in stream:
            line_n += 1  # Start at 1
            line = rawL.strip()
            parts = line.split()
            create_table = None
            use_table = None
            index = stream.tell()
            new_ratio = index / total
            table = None
            if last_ratio - new_ratio > .1:
                echo0("{} complete".format(percent_str(new_ratio)))
                last_ratio = new_ratio
            if parts[:2] == [b"INSERT", b"INTO"]:
                if (creating is not None) or (inserting is not None):
                    raise NotImplementedError(
                        "got {} before {} ended".format(line, creating)
                    )
                use_table = no_enclosures(parts[2])
                table = use_table
                if not line.endswith(b";"):
                    raise NotImplementedError("Multi-line inserting is not implemented.")
                if table in redo:
                    sys.stdout.buffer.write(rawL)
                    sys.stdout.flush()
            elif parts[:2] == [b"CREATE", b"TABLE"]:
                if (creating is not None) or (inserting is not None):
                    raise NotImplementedError(
                        "got {} before {} ended".format(line, creating)
                    )
                create_table = no_enclosures(parts[2])
                table = create_table
                create_statements[table] = line
                creating = create_table
                multi_line = rawL.rstrip() + b"\n"
            elif creating:
                multi_line += rawL.rstrip() + b"\n"
                if line.endswith(b";"):  # Not necessarily where it is, but typically
                    # (detected at end to avoid having to check if in quotes).
                    create_statements[creating] = multi_line
                    creating = None
                    multi_line = None
            if table:
                if parts[2] == table:
                    # There were no backquotes to remove.
                    echo0("Warning: unknown table name syntax: {}".format(line))
                if use_table:
                    use_table = table  # with no backquotes
                    if table not in used_tables:
                        used_tables.append(table)
                    if use_table not in created_tables:
                        if use_table not in warned_tables:
                            echo0('File "{}" line {}: Warning:'
                                  ' table {} was used before created'
                                  ''.format(backup_sql_path, line_n, table))
                            warned_tables.add(use_table)
                elif create_table is not None:
                    create_table = table  # with no backquotes
                    if not create_table:
                        echo0('File "{}" line {}: Warning:'
                              ' table {} was used before created'
                              ''.format(backup_sql_path, line_n, table))
                        
                        raise NotImplementedError(
                            "Table wasn't detected in: {}".format(create_table)
                        )
                    created_tables.append(table)

    return {
        'used_tables': used_tables,
        'created_tables': created_tables,
        'create_statements': create_statements,
    }


def main():
    results = collect_info(BACKUP)
    echo0("used_tables:")
    for table in results['used_tables']:
        echo0("- {}".format(table))
    
    echo0("")
    echo0("Used tables not actually restored"
          " according to SHOW TABLE; results saved in restored_tables:")
    echo0("")
    # echo0("Create statements:")
    # for table, line in results['create_statements'].items():
    #     echo0("{}: {}".format(table, line))
    echo0("Created tables not actually restored"
          "--at least not in Jake's results in the restored_tables list"
          " pasted from SHOW TABLE;")
    echo0("redo = (")
    for table in results['used_tables']:
        if table not in restored_tables:
            echo0('    "{}",'.format(table))
    echo0(")")

    with open("redo-tables.sql", "wb") as stream:
        for table in results['created_tables']:
            if table not in restored_tables:
                stream.write(results['create_statements'][table])

    return 0


if __name__ == "__main__":
    sys.exit(main())
