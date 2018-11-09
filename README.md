# Log Analysis

The main goal of this project is making queries to the [news database](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) and print some analysis as output.

## Run the code

After navigating to the project directory in your terminal you can run it by using this command:

```bash
python log-analysis.py
```

## View
this view is for showing the articles and their views. To be used in two queries the most three popular articles and the most three authors.
```SQL
CREATE VIEW article_views AS 
SELECT
   title,
   author,
   COUNT(*) AS views 
FROM
   log,
   articles 
WHERE
   path LIKE '/article/%' 
   AND substr(path, 10) = slug 
   AND method = 'GET' 
GROUP BY
   title,
   author 
ORDER BY
   views DESC;
```