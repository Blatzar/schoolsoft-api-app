# schoolsoft-api-app
A wrapper for schoolsofts undocumented api they use in their app.

<h3>Usage:</h3>

```
>>> import schoolsoft_api
>>> app_key = schoolsoft_api.get_app_key(name, password)
>>> token = schoolsoft_api.get_updated_token(app_key_json=app_key)['token']
>>> schoolsoft_api.get_lunch(token, school)

[{'saturday': '', 'week': 33, 'updById': 1917, 'creByType': -1, 'creDate': '2020-08-11 14:41:04.0', 'dishCategoryName': 'Lunch', 'creById': 6271, 'thursday': '', 'dates': ['2020-08-10', '2020-08-11', '2020-08-12', '2020-08-13', '2020-08-14', '2020-08-15', '2020-08-16'], 'orgId': 28, 'updDate': '2020-08-14 09:46:56.0', 'empty': False, 'updByType': -1, 'sunday': '', 'tuesday': '', 'dish': 3, 'wednesday': '', 'friday': 'Spagetti med köttfärsås.\r\n\r\nSpagetti med sojafärssås', 'id': -1, 'monday': ''}]
```

1. Obtain a permanent app key. This only needs to be generated once.
2. Generate a temporary token. This needs to get generated once every ~3h.
3. Call the API with the token.

<h3>Note:</h3>

- Some functions might not work for you since OrgID might impact the request urls, please report it in [issues](https://github.com/Blatzar/schoolsoft-api-app/issues). I cannot do further testing to prove this hypothesis since I only own one account.
- Use `get_updated_token()` to prevent requesting too many new tokens
