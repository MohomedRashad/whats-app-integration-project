def get_user_phone_number(request):
    """
    Retrieves the logged-in user's phone number from the request object.
    Args:
        request: The HttpRequest object.
    Returns:
        The user's phone number as a string, or None if the user is not logged in
        or if the user doesn't have a phone number.
    """
    if not request.user.is_authenticated:
        return None  # Or raise an exception if you prefer

    user = request.user
    if hasattr(user, 'phone_number'): #Check if the user model has the field
      return user.phone_number or None # returns None if the field is empty
    else:
      return None
