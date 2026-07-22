import hashlib
from supabase_client import supabase
import datetime


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def username_exists(username):
    result = supabase.table("users").select("*").eq("username", username).execute()
    return len(result.data) > 0


def add_user(username, full_name, password, email):
    hashed_password = hash_password(password)
    supabase.table("users").insert({
        "username": username,
        "full_name": full_name,
        "password": hashed_password,
        "email": email
    }).execute()


def get_stored_password(username):
    result = supabase.table("users").select("password").eq("username", username).execute()
    if len(result.data) == 0:
        return None
    return result.data[0]["password"]


def get_full_name(username):
    result = supabase.table("users").select("full_name").eq("username", username).execute()
    if len(result.data) == 0:
        return None
    return result.data[0]["full_name"]


def seed_default_user():
    if not username_exists("admin"):
        add_user("admin", "Admin", "Admin123!", "admin@example.com")

def add_post(username, content, image_url=None):
    supabase.table("posts").insert({
        "username": username,
        "content": content,
        "image_url": image_url
    }).execute()


def get_posts_by_user(username):
    result = supabase.table("posts").select("content, created_at, image_url").eq("username", username).order("id", desc=True).execute()
    return [(row["content"], row["created_at"], row["image_url"]) for row in result.data]


def update_password(username, new_password):
    hashed_password = hash_password(new_password)
    supabase.table("users").update({"password": hashed_password}).eq("username", username).execute()


def update_photo_path(username, path):
    supabase.table("users").update({"photo_path": path}).eq("username", username).execute()


def get_photo_path(username):
    result = supabase.table("users").select("photo_path").eq("username", username).execute()
    if len(result.data) == 0:
        return None
    return result.data[0]["photo_path"]

def update_contact_info(username, email, phone):
    supabase.table("users").update({"email": email, "phone": phone}).eq("username", username).execute()


def get_contact_info(username):
    result = supabase.table("users").select("email, phone").eq("username", username).execute()
    if len(result.data) == 0:
        return "", ""
    return result.data[0]["email"], result.data[0]["phone"]

def update_username(old_username, new_username):
    supabase.table("users").update({"username": new_username}).eq("username", old_username).execute()

def upload_post_image(username, file_path):
    file_name = f"{username}_{datetime.datetime.now().timestamp()}.png"

    with open(file_path, "rb") as file:
        supabase.storage.from_("post-images").upload(file_name, file)

    public_url = supabase.storage.from_("post-images").get_public_url(file_name)
    return public_url


def get_all_posts(exclude_username=None):
    query = supabase.table("posts").select("username, content, created_at, image_url").order("id", desc=True)

    if exclude_username:
        query = query.neq("username", exclude_username)

    result = query.execute()
    return [(row["username"], row["content"], row["created_at"], row["image_url"]) for row in result.data]


def send_message(sender, receiver, content):
    supabase.table("messages").insert({
        "sender": sender,
        "receiver": receiver,
        "content": content
    }).execute()


def get_conversation(user_a, user_b):
    result = supabase.table("messages").select("sender, content, created_at").or_(
        f"and(sender.eq.{user_a},receiver.eq.{user_b}),and(sender.eq.{user_b},receiver.eq.{user_a})"
    ).order("id").execute()
    return [(row["sender"], row["content"], row["created_at"]) for row in result.data]


def get_conversations_list(username):
    result = supabase.table("messages").select("sender, receiver, content, created_at").or_(
        f"sender.eq.{username},receiver.eq.{username}"
    ).order("id", desc=True).execute()

    seen = {}
    for row in result.data:
        other_person = row["receiver"] if row["sender"] == username else row["sender"]
        if other_person not in seen:
            seen[other_person] = (row["content"], row["created_at"])

    return seen

def search_usernames(prefix, exclude_username):
    result = supabase.table("users").select("username").ilike("username", f"{prefix}%").neq("username", exclude_username).limit(6).execute()
    return [row["username"] for row in result.data]