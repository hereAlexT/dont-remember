# project-23-dont-remember


## Backend API Endpoints

### User Management
Accepted Token: Bearer Token <br>
state has three value "remember" and "forget"

```
POST /api/v1/signup
payload:
{username: [username], password:[password]}
return:
{status: 200, message: "Success"}
{status: 409, message: "User already exist"}
POST /api/v1/login 
payload: 
{username: [username], password: [password]}
return:
{status: 404, message: "User not found"}
{status: 200, message: "Login success", token: [token]}
{status: 401, message: "Wrong password"}
--
POST /api/v1/logout
payload: 
{token: [token]}
return:
{status: 404, message: "Wrong Token"}
{status: 200, message: "Logout success"}
{status: 401, message: "Wrong token"}
--
GET /api/v1/next_word 
return: 
{status: 404, message: "No more words"}
{status: 200, message: "Success",word_uuid: [uuid] ,word: [word], defination: [defination]}
{status: 401, message: "Wrong token"}
--
POST /api/v1/update_word 
payload:
{token: [token], word_uuid: [uuid], curr_state: [curr_state]}
--
GET /api/v1/word_history 
return:
{status: 404, message: "No words in word list"}
{status: 200, message: "Success", word_list: [{word: [word], defination: [defination], word_uuid: [uuid], timestamp: [timestamp], state: [state]}]
{status: 401, message: "Wrong token"}
--
POST /api/v1/add_new_word
payload:
{token: [token], word: [word], defination: [defination]}
return:
{status: 200, message: "Success", word_uuid: [uuid]}
{status: 409, message: "Word already exist"}
{status: 404, message: "Word not found"}
{status: 401, message: "Wrong token"}
```
### Databases 
```
Postgres
USER_table:
[uuid, username, password, token, token_expiration]
Word_table:
[uuid, dic_uuid, user_uuid, last_review_time, next_review_time]
Dic_table:
[uuid, word, definition, language_A, language_B] #language is language of word, language_b is word of defination
```