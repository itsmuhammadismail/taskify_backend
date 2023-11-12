def user_entity(user) -> dict:
    return {
        "id": str(user["_id"]),
        "first_name": user["first_name"],
        "last_name": user["last_name"],
        "email": user["email"],
        "dob": user["dob"],
        "gender": user["gender"],
        "university": user.get("university", ""),
        "mobile": user.get("mobile", ""),
        "country": user.get("country", ""),
        "password": user.get("password", ""),
    }


def users_entity(users) -> list:
    return [user_entity(user) for user in users]
