#!/usr/bin/env python3

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
