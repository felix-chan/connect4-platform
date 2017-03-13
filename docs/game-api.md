# Game player API

## Login system
### **POST** `v1/player/login`

#### Request parameters

|Variables      | Type   | Description                        |
|---------------|--------|------------------------------------|
|username       | char   |Login username                      |
|password       | char   |Password to login account           |

#### Request response

> {"status":1,"info":"Login Success","session":"c2Vzc2lvbiBrZXkgaGVyZQ==","expire":"2017-03-20 23:59:59","time":"2017-03-15 00:00:00"}

**status**

| Status code | Description |
|:---:|:--- |
| `1` | Login success |
| `2` | Wrong username or password |
| `3` | Forbidden |
| `4` |  Already login into other device |
| `800` | Other reason, please refer to *info* |
| `888` | Unknown error |

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
> {"status":1,"info":"Logout Success","time":"2017-03-15 00:00:00"}

**status**

| Status code | Description |
|:---:|:--- |
|`1` | Logout success |
| `2` | Invalid session ID |
| `3` | Forbidden |
| `800` | Other reason, please refer to *info* |
| `888` | Unknown error |

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

> {"status":1,"room":[{"roomid":"1001","game":"connect_four","holder":"user1"},{"roomid":"1002","game":"connect_four","holder":"user2"}],"time":"2017-03-15 00:00:00","info":"Success"}

**status**

| Status code | Description |
|:---:|:--- |
| `1` | Success |
| `2` | Invalid session ID |
| `3` | Forbidden |
| `4` | Empty room |
| `20` | Server closed |
| `800` | Other reason, please refer to *info* |
| `888` | Unknown error |

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
> {"status":1,"info":"Join success","permission":"c2Vzc2lvbiBrZXkgaGVyZSBqaGtsamdsa2RmbGtqIHRyamxrZXllcg==","game":"connect_four","opponent":"user1","time":"2017-03-15 00:00:00"}

**status**

| Status code | Description |
|:---:|:--- |
| `1` | Success |
| `2` | Invalid session ID |
| `3` | Forbidden |
| `4` | Game closed |
| `5` | Room full |
| `9` | Room is not opened |
| `10`| Invalid input |
| `20` | Server closed |
| `800` | Other reason, please refer to *info* |
| `888` | Unknown error |

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
> {"status":1,"info":"Create success","permission":"c2Vzc2lvbiBrZXkgaGVyZSBqaGtsamdsa2RmbGtqIHRyamxrZXllcg==","game":"connect_four","private":0,"invited":"user01","start_time":"2017-11-23 05:30:00","time":"2017-03-15 00:00:00"}

**status**

| Status code | Description |
|:---:|:--- |
| `1` | Success |
| `2` | Invalid session ID |
| `3` | Forbidden |
| `4` | Invalid start_time |
| `5` | Invalid game | 
| `6` | Invalid invited user |
| `7` | Open too many rooms | 
| `8` | Start time longer than 48 hours |
| `9` | Room is not opened |
| `10`| Invalid input |
| `20` | Server closed |
| `800` | Other reason, please refer to *info* |
| `888` | Unknown error |

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

(Optional) The user name of invited opponent. It will not be shown if no user is invited.

**start_time**

The room opening time.  Current time will be shown if `game_start` variable is not set.

**time**

Server current time

## Playing game

### **GET** `v1/player/opponent_info`

### **GET** `v1/player/game_status`

### **POST** `v1/player/move`

