from config import env, AUTH


def init_db():
    if not env.get("MONGO_URI"):
        return None
    from pymongo import MongoClient
    client = MongoClient(env["MONGO_URI"])
    return client["bot"]


DB = init_db()


def auth_user(user_id):
    if DB != None:
        DB.users.update_one({"user_id": user_id}, {
            "$set": {"auth": True}}, upsert=True)
    if user_id not in AUTH:
        AUTH.append(user_id)


def unauth_user(user_id):
    if DB != None:
        DB.users.delete_one({"user_id": user_id})
    if user_id in AUTH:
        AUTH.remove(user_id)


def is_auth(user_id):
    return user_id in AUTH or user_id == int(env["OWNER_ID"])


def get_auth_users():
    return [user["user_id"] for user in DB.users.find({})] if DB != None else AUTH


def __load_auth():
    AUTH.clear()
    AUTH.extend(get_auth_users())


__load_auth()
