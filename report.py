#!/usr/bin/env python3

# ~~~~~~~~~~{{ Questions }}

# 1. What are the most popular three articles of all time?
#    Which articles have been accessed the most?
# Present this information as a sorted list with the most popular article at the top.
# Example:
# "Princess Shellfish Marries Prince Handsome" - 1201 views
# "Baltimore Ravens Defeat Rhode Island Shoggoths" - 915 views
# "Political Scandal Ends In Political Scandal" - 553 views

# 2. Who are the most popular article authors of all time?
#    That is, when you sum up all of the articles each author has written, which authors get the most page views?
# Present this as a sorted list with the most popular author at the top.
# Example:
# Ursula La Multa - 2304 views
# Rudolf von Treppenwitz - 1985 views
# Markoff Chaney - 1723 views
# Anonymous Contributor - 1023 views

# 3. On which days did more than 1% of requests lead to errors?
# The log table includes a column status that indicates the HTTP status code that the news site sent to the user's browser. (Refer to this lesson for more information about the idea of HTTP status codes.)
# Example:
# July 29, 2016 - 2.5% errors

# ~~~~~~~~~~{{ VIEWS }}

'''
~~~~~~~~~~~~

# accurate attempts to reach article path for all existing articles

create view article_popularity as
  select slug, count(path) as views
    from log, articles
    where path = '/article/' || articles.slug
    group by slug
    order by views desc;

~~~~~~~~~~~~

# no. of requests per day

create view day_requests as
  select date(time) as day, count(id) as total_requests
    from log
    group by day;

~~~~~~~~~~~~

# no. of failed requests per day

create view day_fails as
  select date(time) as day, count(id) as failed_requests
    from log
    where status like '4%' or status like '5%'
    group by day;

'''

# ~~~~~~~~~~{{ SOLUTION }}

import psycopg2


def main():

    # connect to DB and initialize a cursor
    db = psycopg2.connect(dbname='news')
    c = db.cursor()

    # _____________________________________________

    title1 = "1. Most popular three articles of all time:"
    c.execute("""

    select articles.title, article_popularity.views
      from articles, article_popularity
      where articles.slug = article_popularity.slug
      order by views desc
      limit 3;

    """)
    result1 = c.fetchall()
    print_info(title1, result1, template=" * \"{}\" — {} views")

    # _____________________________________________

    title2 = "2. Most popular article authors of all time:"
    c.execute("""

    select authors.name, sum(article_popularity.views) as total_views
      from articles, authors, article_popularity
      where articles.author = authors.id
        and articles.slug = article_popularity.slug
      group by authors.name
      order by total_views desc;

    """)
    result2 = c.fetchall()
    print_info(title2, result2, template=" * {} — {} views")

    # _____________________________________________

    title3 = "3. Days on which more than 1% of requests led to errors:"
    c.execute("""

    with fail_percentages as
      ( select to_char(day_requests.day, 'FMMonth DD, YYYY'),
               round(failed_requests*100/total_requests::numeric, 2)
                 as fail_percent
          from day_requests, day_fails
          where day_requests.day = day_fails.day )

    select * from fail_percentages
      where fail_percent > 1;

    """)
    result3 = c.fetchall()
    print_info(title3, result3, template=" * {} — {}% errors")

    # _____________________________________________

    db.close()


def print_info(title, result, template):
    print(title)
    for row in result:
        print(template.format(row[0], row[1]))
    print("")


if __name__ == '__main__':
    main()
