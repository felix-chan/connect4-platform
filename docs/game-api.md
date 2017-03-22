# Game player API

## Login system
### **POST** `v1/player/login`

#### Request parameters

|Variables      | Type   | Description                        |
|---------------|--------|------------------------------------|
|username       | char   |Login username                      |
|password       | char   |Password to login account           |

#### Request response

> `{"status":"success","info":"Login Success","session":"c2Vzc2lvbiBrZXkgaGVyZQ==","expire":"2017-03-20 23:59:59","time":"2017-03-15 00:00:00"}

**status**

| Status code | Description |
|:---:|:--- |
| `success` | Login success |
| `login_fail` | Wrong username or password |
| `forbidden` | Forbidden |
| `already_login` |  Already login into other device |
| `other_reason` | Other reason, please refer to *info* |
| `unknown_error` | Unknown error |

**info**

Text explanation about the login status

**time**

Server current time

**session**

Login session ID which will be used in other connection. Variable will not be returned if login status is not `1`.

**expire**

Login expire time for this session. The session will be expired after the returned timestamp.

### **POST** `v1/player/logout`

#### Request parameters

|Variables      | Type   | Description                        |
|---------------|--------|------------------------------------|
|session        | char   |Login session ID of current session |

#### Request response
> `{"status":"success","info":"Logout Success","time":"2017-03-15 00:00:00"}

**status**

| Status code | Description |
|:---:|:--- |
| `success` | Logout success |
| `invalid_session` | Invalid session ID |
| `forbidden` | Forbidden |
| `other_reason` | Other reason, please refer to *info* |
| `unknown_error` | Unknown error |

**info**

Text explanation about the login status

**time**

Server current time

## Joining game

### **GET** `v1/player/game_list`

#### Request parameters

|Variables      | Type   | Description                        |
|---------------|--------|------------------------------------|
|session        | char   |Login session ID of current session |

#### Request response

> `{"status":"success","room":[{"roomid":"1001","game":"connect_four","holder":"user1"},{"roomid":"1002","game":"connect_four","holder":"user2"}],"time":"2017-03-15 00:00:00","info":"Success"}

**status**

| Status code | Description |
|:---:|:--- |
| `success` | Logout success |
| `invalid_session` | Invalid session ID |
| `forbidden` | Forbidden |
| `empty_room` | Empty room |
| `server_close` | Server closed |
| `other_reason` | Other reason, please refer to *info* |
| `unknown_error` | Unknown error |

**room**

Array of room detail, which contains:

 - *roomid*: The unique room ID
 - *game*: The type of game, all should be `connect_four` in first stage
 - *holder*: The user who create this room

**info**

Text explanation about the login status

**time**

Server current time

### **POST** `v1/player/join_game`

#### Request parameters

|Variables      | Type   | Description                        |
|---------------|--------|------------------------------------|
|session        | char   |Login session ID of current session |
|roomid         | char   | Unique room ID                     |

#### Request response
> `{"status":"success","info":"Join success","permission":"c2Vzc2lvbiBrZXkgaGVyZSBqaGtsamdsa2RmbGtqIHRyamxrZXllcg==","game":"connect_four","opponent":"user1","time":"2017-03-15 00:00:00"}

**status**

| Status code | Description |
|:---:|:--- |
| `success` | Logout success |
| `invalid_session` | Invalid session ID |
| `forbidden` | Forbidden |
| `game_close` | Game closed |
| `room_full` | Room full |
| `room_not_open` | Room is not opened |
| `invalid_input`| Invalid input |
| `server_close` | Server closed |
| `other_reason` | Other reason, please refer to *info* |
| `unknown_error` | Unknown error |

**info**

Text explanation about the login status

**permission**

Key to identify the room and granted permission in game playing API.

**game**

Type of game in this room. Only `connect_four` is supported.

**time**

Server current time

### **POST** `v1/player/create_game`

#### Request parameters

|Variables      | Type   | Description                        |
|---------------|--------|------------------------------------|
|session        | char   |Login session ID of current session |
|game           | char   |(Optional) Game type, only connect_four is supported. Default value is `connect_four` |
|game_start     | int    |(Optional) `0` for start yourself, `1` for start by opponent. Default value is `0`|
|start_time     | char   |(Optional) Date and time for room start. Empty value represent the room open now. Date time must follow the format **YYYY-MM-DDThh:mm:ssTZD* e.g. `2016-11-23T03:45:00+08:00` |
|private        | int    |(Optional) `0` for public room and `1` for private room. Default value is `0` |
|invite         | char   |(Optional) User ID of opponent you want to play with  |

#### Request response
> `{"status":"success","info":"Create success","permission":"c2Vzc2lvbiBrZXkgaGVyZSBqaGtsamdsa2RmbGtqIHRyamxrZXllcg==","game":"connect_four","private":0,"invited":"user01","start_time":"2017-11-23 05:30:00","time":"2017-03-15 00:00:00"}

**status**

| Status code | Description |
|:---:|:--- |
| `success` | Logout success |
| `invalid_session` | Invalid session ID |
| `forbidden` | Forbidden |
| `invalid_start` | Invalid start_time |
| `invalid_game` | Invalid game | 
| `invalid_user` | Invalid invited user |
| `too_many_rooms` | Open too many rooms | 
| `too_late_start` | Start time longer than 48 hours |
| `room_not_open` | Room is not opened |
| `invalid_input`| Invalid input |
| `server_close` | Server closed |
| `other_reason` | Other reason, please refer to *info* |
| `unknown_error` | Unknown error |

**info**

Text explanation about the login status

**permission**

Key to identify the room and granted permission in game playing API.

**game**

Type of game in this room. Only `connect_four` is supported.

**private**

| Status code | Description |
|:---:|:--- |
|`0`  |Public room, which will show in room list |
|`1`  |Private room, only invited user or user with direct link can be access. It will not shown in room list|

**invited**

The user name of invited opponent. It will not be shown if no user is invited.

**start_time**

The room opening time.  Current time will be shown if `game_start` variable is not set.

**time**

Server current time

## Playing game

### **GET** `v1/player/opponent_info`

#### Request parameters

|Variables      | Type   | Description                        |
|---------------|--------|------------------------------------|
|session        | char   |Login session ID of current session |
|roomid         | char   |(Optional) Unique room ID           |
|user           | char   |(Optional) Username of opponent     |

\# Either `roomid` or `user` is needed for for the request.

#### Request response
> `{"status":"success","info":"Success","user":{"name":"User 1","user":"user1","game_played":20,"member_since":"2015-01-02"},"time":"2017-03-15 00:00:00"}

**status**

| Status code | Description |
|:---:|:--- |
| `success` | Logout success |
| `invalid_session` | Invalid session ID |
| `forbidden` | Forbidden |
| `invalid_roomid` | Invalid room ID | 
| `invalid_user` | Invalid user |
| `invalid_input`| Invalid input |
| `server_close` | Server closed |
| `other_reason` | Other reason, please refer to *info* |
| `unknown_error` | Unknown error |

**info**

Text explanation about the login status

**user**

User information include user nickname, user ID, game played and registration date. There will be game result in later stage.

**time**

Server current time

### **GET** `v1/player/game_status`

**This is long polling request. Please refer to remarks for the connection advice.**

#### Request parameters

|Variables      | Type   | Description                        |
|---------------|--------|------------------------------------|
|session        | char   |Login session ID of current session |
|roomid         | char   | Unique room ID                     |
|permission     | char   | Permission key for access game room|

#### Request response
> `{"status":"success","info":"Success","gameboard":[[-1,-1,0,-1,-1,-1,-1],[-1,-1,1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1]],"new_step":[2,3],"your_turn":1,"end_game":0,"winner":"","time":"2017-03-15 00:00:00"}

**status**

| Status code | Description |
|:---:|:--- |
| `success` | Logout success |
| `invalid_session` | Invalid session ID |
| `forbidden` | Forbidden |
| `invalid_roomid` | Invalid room ID | 
| `too_many_request` | Too many request |
| `invalid_input`| Invalid input |
| `server_close` | Server closed |
| `other_reason` | Other reason, please refer to *info* |
| `unknown_error` | Unknown error |

**info**

Text explanation about the login status

**gameboard**

The chess position on the gameboard. `-1` for empty place, `0` for you and `1` for opponent.

**new_step**

The position of last step. The variable will be empty / does not return if the gameboard is empty.

**your_turn**

| Status code | Description |
|:---:|:--- |
| `1` | It is your turn and you can go to next step |
| `0` | You have to wait for opponent's response    |

**end_game**

| Status code | Description |
|:---:|:--- |
| `1` | The game is finished |
| `2` | The opponent withdraw the game |
| `0` | The game is still on-going |

**winner**

If will return either `Tie` or winner user name. Empty string will be return if the game is still on-going.

**time**

Server current time

### **POST** `v1/player/move`

#### Request parameters

|Variables      | Type   | Description                        |
|---------------|--------|------------------------------------|
|session        | char   |Login session ID of current session |
|roomid         | char   | Unique room ID                     |
|permission     | char   | Permission key for access game room|
|column         | int    | Column ID for your next step, first column is 1|
|row            | int    | Row ID for your next step, first column is 1|

#### Request response
> `{"status":"success","info":"Success","gameboard":[[-1,-1,0,-1,-1,-1,-1],[-1,-1,1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1]],"new_step":[2,3],"your_turn":1,"end_game":0,"winner":"","time":"2017-03-15 00:00:00"}

**status**

| Status code | Description |
|:---:|:--- |
| `success` | Logout success |
| `invalid_session` | Invalid session ID |
| `forbidden` | Forbidden |
| `invalid_roomid` | Invalid room ID | 
| `too_many_request` | Too many request |
| `invalid_input`| Invalid input |
| `server_close` | Server closed |
| `occupied` | Position occupied | 
| `other_reason` | Other reason, please refer to *info* |
| `unknown_error` | Unknown error |

**info**

Text explanation about the login status

**gameboard**

The chess position on the gameboard. `-1` for empty place, `0` for you and `1` for opponent.

**new_step**

The position of last step. The variable will be empty / does not return if the gameboard is empty.

**your_turn**

| Status code | Description |
|:---:|:--- |
| `1` | It is your turn and you can go to next step |
| `0` | You have to wait for opponent's response    |

**end_game**

| Status code | Description |
|:---:|:--- |
| `1` | The game is finished |
| `2` | The opponent withdraw the game |
| `0` | The game is still on-going |

**winner**

If will return either `Tie` or winner user name. Empty string will be return if the game is still on-going.

**time**

Server current time
