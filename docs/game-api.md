# Game player API

## Login system
###**POST** `v1/player/login`

####Request parameters
|Variables      | Type   | Description                        |
|---------------|--------|------------------------------------|
|username       | char   |Login username                      |
|password       | char   |Password to login account           |

####Request response
>{"status":1,"info":"Login Success","session":"c2Vzc2lvbiBrZXkgaGVyZQ==","expire":"2017-03-20 23:59:59","time":"2017-03-15 00:00:00"}

**status**
`1`: Login success
`2`: Wrong username or password
`3`: Forbidden
`4`:  Already login into other device
`800`: Other reason, please refer to *info*
`888`: Unknown error

**info**
Text explanation about the login status

**time**
Server current time

**session**
Login session ID which will be used in other connection. Variable will not be returned if login status is not `1`.

**expire**
Login expire time for this session. The session will be expired after the returned timestemp.

###**POST** `v1/player/logout`

####Request parameters
|Variables      | Type   | Description                        |
|---------------|--------|------------------------------------|
|session        | char   |Login session ID of current session |

####Request response
>{"status":1,"info":"Logout Success","time":"2017-03-15 00:00:00"}

**status**
`1`: Logout success
`2`: Invalid session ID
`3`: Forbidden
`800`: Other reason, please refer to *info*
`888`: Unknown error

**info**
Text explanation about the login status

**time**
Server current time
