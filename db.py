from supabase_client import supabase

def create_conversation(user_id, title):
    res = supabase.table("conversations").insert({
        "user_id": user_id,
        "title": title
    }).execute()
    return res.data[0]["id"]

def save_message(conversation_id, role, content):
    supabase.table("messages").insert({
        "conversation_id": conversation_id,
        "role": role,
        "content": content
    }).execute()

def get_conversations(user_id):
    return supabase.table("conversations") \
        .select("*") \
        .eq("user_id", user_id) \
        .execute().data

def get_messages(conversation_id):
    return supabase.table("messages") \
        .select("*") \
        .eq("conversation_id", conversation_id) \
        .order("created_at") \
        .execute().data
