# Temperature monitor API





## Setup

### Requirements

* First of all, you need a server that will work 24/7
* You also need a permanent ip address for this server (or domain name with or permanent ip)
* Next you need database for collecting data (for example PostgreSQL docker container)

### Preparations

**Prepare database**
* Create a user `recorder_api` in database
* Create a schema `recorder_api` (schema name must be same as user)

**Write down a environment variables**

On this step you need to remember or write down special environment variables

* After user creation combine an info about user, host and database in special string named `DB_DNS`:
```dotenv
DB_DSN=postgresql://recorder_api:passowrd@api_or_ip_address:5432/databasename
```
* Generate any strong `ADMIN_TOKEN`. It will need to manage devices and get collected data
```dotenv
ADMIN_TOKEN=SOME_STRONG_STRING_FOR_WEB_API_MANAGE_ACCESS
```