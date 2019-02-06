# -*- coding: utf-8 -*-

import psycopg2
from django.db import transaction
from itertools import izip

def get_connection(conn):
    if not conn:
        from django.db import connection
    else:
        connection = psycopg2.connect(**conn)
    return connection


@transaction.commit_on_success
def get_dict(query_string, show_info=False, conn=None):
    connection = get_connection(conn)
    cursor = connection.cursor()
    try:
        cursor.execute(query_string)
    except Exception, e:
        connection.rollback()
        raise e
    col_names = [desc[0] for desc in cursor.description]
    result = []
    for row in cursor.fetchall():
        row_dict = dict(izip(col_names, row))
        result.append(row_dict)
    if not show_info:
        return result
    else:
        time = connection.queries and connection.queries[-1]['time'] or '?'
        return dict(cols=col_names, time=time, result=result, total_rows=len(result))


@transaction.commit_on_success
def get_list(query_string, conn=None):
    connection = get_connection(conn)
    cursor = connection.cursor()
    try:
        cursor.execute(query_string)
    except Exception, e:
        connection._rollback()
        raise e
    result = []
    for row in cursor.fetchall():
        result.append(row)
    
    # If each row returns one value, let`s flat this
    # ((1,), (2,)) -> (1, 2)
    if result and len(result[0]) == 1:
        result = [row[0] for row in result]
    
    return result


@transaction.commit_on_success
def get_list_extra(query_string, conn=None):
    connection = get_connection(conn)
    cursor = connection.cursor()
    try:
        cursor.execute(query_string)
    except Exception, e:
        connection.rollback()
        raise e
    colnames = [desc[0] for desc in cursor.description]
    result = []
    for row in cursor.fetchall():
        result.append(row)
    
    # If each row returns one value, let`s flat this
    # ((1,), (2,)) -> (1, 2)
    if result and len(result[0]) == 1:
        result = [row[0] for row in result]
    
    return dict(rows=result, colnames=colnames)


# Util functions

def get_table_columns(table_name, conn=None):
    connection = get_connection(conn)
    cursor = connection.cursor()
    cursor.execute('select * from %s where 1 = 2' % table_name)
    return [desc[0] for desc in cursor.description]

def table_exists(table_name, conn=None):
    r = get_list("select count(*) from information_schema.tables where table_name "
                 "= '%s'" % table_name,
                 conn=conn)
    return bool(r[0])

def drop_table(table_name, conn=None):
    if table_exists(table_name):
        connection = get_connection(conn)
        cursor = connection.cursor()
        cursor.execute("drop table %s" % table_name)
        connection._commit()
