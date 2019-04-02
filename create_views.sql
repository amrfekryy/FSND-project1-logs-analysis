

create or replace view article_popularity as
  select slug, count(path) as views
    from log, articles
    where path = '/article/' || articles.slug
    group by slug
    order by views desc;


-- create or replace view day_requests as
--   select date(time) as day, count(id) as total_requests
--     from log
--     group by day;


-- create or replace view day_fails as
--   select date(time) as day, count(id) as failed_requests
--     from log
--     where status like '4%' or status like '5%'
--     group by day;
