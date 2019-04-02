#!/usr/bin/env python3

import psycopg2

DBNAME = "news"


def db_connect():
    """Creates and returns a database connection and cursor.

    This function creates and returns a database connection and cursor to the
    database defined by DBNAME.

    returns:
    db, c - a tuple.
    The first element is a connection to the database.
    The second element is a cursor for the database.
    """

    # create a DB connection
    db = psycopg2.connect(dbname=DBNAME)
    # create a cursor
    c = db.cursor()

    return db, c


def execute_query(query):
    """Returns the results of an SQL query.

    This function takes an SQL query as a parameter,
    executes the query and returns the results as a list of tuples.

    args:
    query - an SQL query statement to be executed.

    returns:
    A list of tuples containing the results of the query.
    """

    # connect to DB
    db, c = db_connect()
    # execute query
    c.execute(query)
    # fetch and return the result
    results = c.fetchall()
    # close DB connection
    db.close()

    return results


def print_top_articles():
    """Prints out the top 3 articles of all time."""

    title = "1. Most popular three articles of all time:"
    query = ("""

    select articles.title, article_popularity.views
      from articles, article_popularity
      where articles.slug = article_popularity.slug
      order by views desc
      limit 3;

    """)
    results = execute_query(query)

    print_info(title, results, template=" * \"{}\" — {} views")


def print_top_authors():
    """Prints a list of authors ranked by article views."""

    title = "2. Most popular article authors of all time:"
    query = ("""

    select authors.name, sum(article_popularity.views) as total_views
      from articles, authors, article_popularity
      where articles.author = authors.id
        and articles.slug = article_popularity.slug
      group by authors.name
      order by total_views desc;

    """)
    results = execute_query(query)

    print_info(title, results, template=" * {} — {} views")


def print_errors_over_one():
    """Prints out the error report.

    This function prints out the days and that day's error percentage where
    more than 1% of logged access requests were errors.
    """

    title = "3. Days on which more than 1% of requests led to errors:"
    query = ("""

    with fail_percentages as
      ( select time::date as day,
               (count(*) filter (where status like '4%' or status like '5%')
                / count(*)::numeric) * 100 as fail_percent
          from log
          group by day )

    select to_char(day, 'FMMonth DD, YYYY'),
           round(fail_percent, 2)
      from fail_percentages
      where fail_percent > 1;

    """)
    results = execute_query(query)

    print_info(title, results, template=" * {} — {}% errors")


def print_info(title, results, template):
    """Prints out query results as a plain text

    This function prints a question and answer in the form of
    a title and a bullet list. It extracts information from query results
    and plug it into a template for each list item.

    args:
    title - a title that represent the question to be answered.
    results - a list of tuples containing the results of the query.
    template - a string with placeholders to be formatted with results.
    """

    print(title)
    for row in results:
        print(template.format(row[0], row[1]))
    print("")


if __name__ == '__main__':
    print_top_articles()
    print_top_authors()
    print_errors_over_one()
