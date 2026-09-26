from connection import connection

async def get_user(tg_id):
    try:
        con = await connection()
        users = await con.fetchrow("""
        select * from users where tg_id = $1
        """ , str(tg_id))
        return users
    except Exception as error:
        print(f"Error in geting user: {error}")
    finally:
        await con.close()

async def save_user(tg_id , user_name , full_name):
    try:
        con = await connection()
        await con.execute("""
        insert into users (tg_id , user_name , full_name) values
        ($1 , $2 , $3)
        """ , str(tg_id) , user_name , full_name)
        print("User saved!")
    except Exception as error:
        print(f"Error in saving user: {error}")
    finally:
        await con.close()

async def show_history(tg_id):
    try:
        con = await connection()
        history = await con.fetch("""
        select users.full_name , users.balance , * from tranzactions
        join users on users.tg_id = tranzactions.tg_id
        where tranzactions.tg_id = $1
        """ , str(tg_id))
        return history
    except Exception as error:
        print(f"Error is showing history: {error}")
    finally:
        await con.close()

async def show_profile(tg_id):
    try:
        con = await connection()
        show_p = await con.fetchrow("""
        select * from users where tg_id = $1
        """ , str(tg_id))
        return show_p
    except Exception as error:
        print(f"Error in showing profile: {error}")
    finally:
        await con.close()

async def deposit(tg_id , amount):
    try:
        con = await connection()
        await con.execute("""
        insert into tranzactions (type , tg_id , amount) values
        ('deposit' , $1 , $2)
        """ , str(tg_id) , amount)
        await con.execute("""
        update users
        set balance = balance + $2 
        where tg_id = $1
        """ , str(tg_id) , amount)
        print("Deposit finished!")
    except Exception as error:
        print(f"Error in deposit: {error}")
    finally:
        await con.close()

async def withdraw(tg_id , amount):
    try:
        con = await connection()
        await con.execute("""
        insert into tranzactions (type , tg_id , amount) values
        ('withdraw' , $1 , $2)
        """ , str(tg_id) , amount)
        await con.execute("""
        update users
        set balance = balance - $2 
        where tg_id = $1 and balance >= $2
        """ , str(tg_id) , amount)
        print("Withdraw finished!")
    except Exception as error:
        print(f"Error in withdraw: {error}")
    finally:
        await con.close()

async def add_dolg(info , amount , tg_id):
    try:
        con = await connection()
        await con.execute("""
        insert into dop (type , info , amount , tg_id) values
        ('dolg' , $1 , $2 , $3)
        """, info , amount , str(tg_id))
        print("Dolg added succsessfully!")
    except Exception as error:
        print(f"Erro in adding dolg: {error}")
    finally:
        await con.close()

async def add_goal(info , amount , tg_id):
    try:
        con = await connection()
        await con.execute("""
        insert into dop (type , info , amount , tg_id) values
        ('dolg' , $1 , $2 , $3)
        """, info , amount , str(tg_id))
        print("Goal added succsessfully!")
    except Exception as error:
        print(f"Erro in adding goal: {error}")
    finally:
        await con.close()

async def show_your_dolg(tg_id):
    try:
        con = await connection()
        show_dolg = await con.fetch("""
        select * from dop where tg_id = $1 and type = 'dolg'
        """ , str(tg_id))
        return show_dolg
    except Exception as error:
        print(f"Error in showing dolg: {error}")
    finally:
        await con.close()

async def show_your_goals(tg_id):
    try:
        con = await connection()
        show_goals = await con.fetch("""
        select * from dop where tg_id = $1 and type = 'goal'
        """ , str(tg_id))
        return show_goals
    except Exception as error:
        print(f"Error in showing goals: {error}")
    finally:
        await con.close()

async def update_dolg(tg_id , dop_id , amout_to_get):
    try:
        con = await connection()
        await con.execute("""
            insert into tranzactions (type, tg_id, amount)
            values ('to dolg', $1, $2)
        """, str(tg_id), amout_to_get)

        await con.execute("""
            update users
            set balance = balance - $2
            where tg_id = $1 and balance >= $2
        """, str(tg_id), amout_to_get)

        await con.execute("""
            update dop
            set amount = amount - $1
            where dop_id = $3 and tg_id = $3
        """, amout_to_get, dop_id , str(tg_id))
        print("Added to dolg OK")
    except Exception as error:
        print(f"Error in update amoutn of dolg: {error}")
    finally:
        await con.close()

async def update_goal(tg_id , dop_id , amoutn_to_add):
    try:
        con = await connection()
        await con.execute("""
            insert into tranzactions (type, tg_id, amount)
            values ('to dolg', $1, $2)
        """, str(tg_id), amoutn_to_add)

        await con.execute("""
            update users
            set balance = balance - $2
            where tg_id = $1 and balance >= $2
        """, str(tg_id), amoutn_to_add)

        await con.execute("""
            update dop
            set amount = amount - $1
            where dop_id = $2 and tg_id = $3
        """, amoutn_to_add, dop_id , str(tg_id))
        print("Added to dolg OK")
    except Exception as error:
        print(f"Error in update amoutn of dolg: {error}")
    finally:
        await con.close()