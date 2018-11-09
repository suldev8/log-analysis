#!/usr/bin/env python3

import psycopg2


def select_query(query):
    db = psycopg2.connect(database='news')
    c = db.cursor()
    c.execute(query)
    q = c.fetchall()
    db.close()
    return q


def print_views(s, rows):
    print('The most three popular {}:'.format(s))
    for row in rows:
        print("- " + row[0] + " -- " + str(row[1]) + " views")
    print("")


def print_erorr_percentage(rows):
    print('More than 1% requests lead to errors in a day:')
    for row in rows:
        print("- " + row[0] + " -- " + str(row[1]) + "% errors")


if __name__ == "__main__":
    Q1 = '''
        SELECT title, views
        FROM article_views
        LIMIT 3;
    '''
    A1 = select_query(Q1)

    Q2 = '''
        SELECT name, sum(views) AS views
        FROM authors, article_views
        WHERE authors.id = article_views.author
        GROUP BY name
        ORDER BY views DESC LIMIT 3;
    '''
    A2 = select_query(Q2)

    Q3 = '''
        SELECT *
        FROM (
            SELECT TO_CHAR(DATE(logerrors.logdate), 'Mon dd, yyyy') AS logdate,
                (errors*100)/numOfStatus AS error_percentage
            FROM
                (SELECT DATE(time) AS logdate, count(*) AS numOfStatus
                FROM log
                GROUP BY logdate
                ) AS logNumOfStatus,
                (SELECT DATE(time) AS logdate, count(*) AS errors
                FROM log
                WHERE status LIKE '4%' OR status LIKE '5%'
                GROUP BY logdate
                ) AS logerrors
            WHERE logerrors.logdate = logNumOfStatus.logdate) AS percent
        WHERE error_percentage > 1;
    '''
    A3 = select_query(Q3)

    print_views('articles', A1)
    print_views('authors', A2)
    print_erorr_percentage(A3)
