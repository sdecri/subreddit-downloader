# subreddit-downloader

A simple application to download all submissions and comments of a subreddit stogin them in a MySQL database. It uses
the python libraries: <a href="https://praw.readthedocs.io/en/latest/">praw</a>
and <a href="https://pypi.org/project/psaw/">psaw</a>.
<br>
To use this application you must provide:
<ul>
<li>reddit_username: a reddit account username</li>
<li>reddit_client_id: a reddit application id</li>
<li>reddit_secret: a reddit application secret</li>
</ul>
More information on how to retrieve these values can be found <a href="https://github.com/reddit-archive/reddit/wiki/OAuth2#getting-started">here</a>.

Before running it, you must create the mysql database using the script db-creation.sql.
<br>
Configuration:<br>
--reddit_username:          [REQUIRED] Reddit username.<br>
--reddit_client_id:          [REQUIRED] Reddit client id.<br>
--reddit_secret:          [REQUIRED] Reddit secret.<br>
--db_host:          Database host. Default 127.0.0.1<br>
--db_port:          Database port. Default 3306<br>
--db_name:          Database name. Default reddit<br>
--db_user:          Database user. Default root<br>
--db_password:      Database password.<br>
--submissions_batch_size:  Number of submissions to download in batch each time. Default: 10.<br>
--comments_persist_batch_size:  Number of comments to persist in batch. Default: 1000.<br>
--num_iterations:  Number of iterations to download submissions in batch. Negative number means no limit. Default:
-1.<br>
--from_date:          Download only submissions created after this date in ISO-8601.<br>
--to_date:          Download only submissions created before this date in ISO-8601.<br>

