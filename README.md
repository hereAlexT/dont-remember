# project-23-dont-remember

## Local Development Environment


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
payload:
{token: [token}, last_word: [word], status: [remember or forgot]}
return: 
{status: 404, message: "No more words"}
{status: 200, message: "Success",word_uuid: [uuid] ,word: [word], defination: [defination]}
{status: 401, message: "Wrong token"}
Word Selection Priority:
1. reviewed words
2. new words
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
--
POST /api/v1/new_team # register a new team


--
POST /api/v1/team_man #add oir delete a team
# add a new memebr, delete a memeber ( you can only add or delete your self) 
# a user can only be addedto one team


--
GET /api/v1/team_info

return:
body: {
team_id: [team_id],
team_memeber: [
"user1": {
}
],
}


```
### Databases 
```
Postgres
table name: users
[uuid, username, password, token, token_expiration, study_plan]
tablenames: words
[uuid, dic_uuid, user_uuid, last_review_time, next_review_time]
tablenames: dic
[uuid, word, definition, speech_part, example,language_A, language_B] #language is language of word, language_b is word of defination
tablesnames: team
[uuid, team_info_uuid, user_uuid]
tablesnames: team_info
[uuid, name]
```
Note: language_A and language_B should follow [ISO 639-1 standard language codes]("https://www.andiamo.co.uk/resources/iso-language-codes/)


# Note:
The defualt value of study_plan is always 20.

# depolyment
begin deploy
```
terraform apply -var-file="secret.tfvars" -auto-approve
terraform apply -var-file="secret.tfvars" -auto-approve -parallelism=20

```

