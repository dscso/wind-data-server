# wind-data-server
This is the wind data proxy/API server for the klima-ag.de website.
It's composed a little python-script, which proxying the wind data to all (web)clients via websocket. It also safe them and make them reachable over an http API.
We are using now an Sqlite3 database, because it's esay to handle with an one-file-database
