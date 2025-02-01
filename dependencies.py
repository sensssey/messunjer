# dependencies.py
from fastapi import Depends
from .auth import get_current_active_user

get_current_active_user = get_current_active_user