#### Setup & run

1. Install dependencies ```pip install -r requirements.txt ```

2. Make sure you have .env file here: ```/backend/.env```

3. Run the server: ```flask run``` in project root directory

4. ```test_api.http``` to check stuff out

### TODO
- views 
  - post request on view? or just get?
  - collection of views - maybe other interactions too?
  - bucket pattern
  - get popular articles
- recommendations
  - save svd as binary data or sth?
  - maybe something better than svd
- basic recommendations
  - just crunch the tags and categories per user
- database seeding
  - need some articles 
  - need users
  - need interactions between them