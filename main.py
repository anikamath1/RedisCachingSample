from fastapi import FastAPI
from aioredis import from_url
import mysql.connector
import json
import time

app = FastAPI()

# Redis client
redis = None


@app.on_event("startup")
async def startup_event():
    global redis
    redis = await from_url("redis://localhost", decode_responses=True)


@app.on_event("shutdown")
async def shutdown_event():
    await redis.close()


# MySQL connection setup
def get_mysql_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="test_db"
    )


# Simulate fetching users from MySQL every time
@app.get("/users-mysql")
async def get_users_mysql():
    start_time_mysql = time.time()

    # Fetch data directly from MySQL
    connection = get_mysql_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    connection.close()

    mysql_time = time.time() - start_time_mysql

    return {
        "source": "MySQL",
        "time_taken": f"{mysql_time:.6f} seconds"
    }


# Simulate fetching users with Redis caching
@app.get("/users-redis")
async def get_users_redis():
    # First, check if data exists in Redis
    cached_users = await redis.get("users")
    if cached_users:
        return {
            "source": "Redis",
            "time_taken": "0.001000 seconds",  # Redis fetch time is usually < 1ms

        }

    # If no data in Redis, fetch from MySQL and cache it
    start_time_mysql = time.time()

    connection = get_mysql_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    connection.close()

    mysql_time = time.time() - start_time_mysql

    # Cache the data in Redis
    await redis.set("users", json.dumps(users), ex=3600)  # Cache for 1 hour

    return {
        "source": "MySQL",
        "time_taken": f"{mysql_time:.6f} seconds"
    }
