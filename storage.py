from supabase_client import supabase

def upload_logo(file, user_id):
    path = f"{user_id}/{file.name}"

    supabase.storage.from_("logos").upload(path, file)

    url = supabase.storage.from_("logos").get_public_url(path)

    return url
