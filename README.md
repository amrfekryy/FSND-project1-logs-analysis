# [FSND](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004) Project1 - Logs Analysis

This is a command line reporting tool that connects to the database of a newspaper website and provides insights derived from users activity.

Questions answered by the program:
- What are the most popular three articles of all time?
- What are the most popular article authors of all time?
- On which days did more than 1% of requests lead to errors?

### Usage:
The following steps assume that you already have installed and configured the [virtual machine](https://classroom.udacity.com/courses/ud197/lessons/3423258756/concepts/14c72fe3-e3fe-4959-9c4b-467cf5b7c3a0) of the FSND.

1. download and unzip [newsdata.sql](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) into `vagrant` directory. This file contains the database design (tables), and data for each table.

2. set up the local database "news", and load data into it using the command
    `psql -d news -f newsdata.sql`

3. add the following views to the database, which are required for the python program to work:
   ```
    create view article_popularity as
      select slug, count(path) as views
        from log, articles
        where path = '/article/' || articles.slug
        group by slug
        order by views desc;

    create view day_requests as
      select date(time) as day, count(id) as total_requests
        from log
        group by day;

    create view day_fails as
      select date(time) as day, count(id) as failed_requests
        from log
        where status like '4%' or status like '5%'
        group by day;
   ```

4. run the python file from the command line
   `python3 report.py`
   and you will see the answers to the questions as in output.txt file.
