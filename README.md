# schoolsoft-api-app
A wrapper for schoolsofts undocumented api they use in their app.

<h3>Usage:</h3>

Get the school name from the schoolsoft url.
Schoolname is found like this:

"sms13.schoolsoft.se/   __*school*__   /jsp/student/right_student_startpage.jsp"

```
>>> import schoolsoft_api
>>> username, password, school = 'username', 'password', 'school' # Place real values here.
>>> # Easy way
>>> api = schoolsoft_api.Api(username, password, school)
>>> api.lunch
[{'saturday': '', 'week': 15, 'updById': 1917, 'creByType': -1, 'creDate': '2021-04-12 08:59:27.0', 'dishCategoryName': 'Lunch.....
>>> api.lessons
[{'id': 8671972, 'orgId': 28, 'creById': -1, 'updById': -1, 'creByType': -1, 'updByType': -1, 'creDate': 1610098253000, 'updDate': 16100982.....
>>> # Attributes available: api.token, api.user, api.lunch, api.calendar, api.lessons 

>>> # Hard way, but this way you can write data to files easier
>>> app_key = schoolsoft_api.get_app_key(username, password, school)
>>> org_id = app_key['orgs'][0]['orgId']
>>> token = schoolsoft_api.get_updated_token(school, app_key_json=app_key)['token']
>>> schoolsoft_api.get_lunch(token, school, org_id)
[{'saturday': '', 'week': 33, 'updById': 1917, 'creByType': -1, 'creDate': '2020-08-11 14:41:04.0', 'dishCategoryName': 'Lunch', 'creById': 6271, 'thursday': '', 'dates': ['2020-08-10', '2020-08-11', '2020-08-12', '2020-08-13', '2020-08-14', '2020-08-15', '2020-08-16'], 'orgId': 28, 'updDate': '2020-08-14 09:46:56.0', 'empty': False, 'updByType': -1, 'sunday': '', 'tuesday': '', 'dish': 3, 'wednesday': '', 'friday': 'Spagetti med köttfärsås.\r\n\r\nSpagetti med sojafärssås', 'id': -1, 'monday': ''}]
>>> schoolsoft_api.get_lessons(token, school, org_id)
[{'weeks': 7329532, 'excludingWeeks': 0, 'creById': 6272, 'source': 1, 'externalRef': '', 'subjectId': 2947, 'orgId': 28, 'updDate': '2020-08-15 14:06:48.0', 'updByType': -1, 'excludeClass': 0, 'startTime': '1970-01-01 08:20:00.0', 'id': 295125, 'includingWe.......
```

1. Obtain a permanent app key. This only needs to be generated once.
2. Generate a temporary token. This needs to get generated once every 3h~.
3. Call the API with the token.

<h3>Note:</h3>

- **Activate mobile login on the schoolsoft webpage!**
- Use `get_updated_token()` to prevent requesting too many new tokens
