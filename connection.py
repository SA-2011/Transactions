import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()
ps = os.getenv("ps")

async def connection():
    try:
        con = await asyncpg.connect(
            database = "Bot_db",
            host = "localhost",
            user = "postgres",
            port = 5432,
            password = ps
        )
        print("Connection OK")
        return con
    except Exception as error:
        print(f"Connection Error: {error}")

async def create_table():
    con = await connection()
    try:
        await con.execute("""
        create table if not exists users(
            user_id serial primary key,
            user_name varchar(100),
            full_name varchar(100),
            balance numeric(12 , 2) check (balance >= 0) default 0,
            tg_id varchar unique,
            created_at timestamp default now(),
            is_active boolean default true
        );
        create table if not exists tranzactions(
            tranzactions_id serial primary key,
            type varchar(50),
            tg_id varchar references users(tg_id) on delete cascade,
            created_at timestamp default now(),
            amount numeric(12 , 2) default 0
        );
        create table if not exists dop(
            dop_id serial primary key,
            type varchar(50),
            info text,
            amount numeric(12,0),
            tg_id varchar references users(tg_id) on delete cascade
        );
    """)
        print("Table created!")
    except Exception as error:
        print(f"Erro in creating table: {error}")
    finally:
        await con.close()