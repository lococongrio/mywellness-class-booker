import os
from typing import Optional
from mywellness import MyWellnessCredential

password_key='HWF_PASSWORD'
username_key='HWF_USERNAME'

def load_credentials() -> Optional[MyWellnessCredential]:
    missing_keys = [key for key in [password_key, username_key] if not key in os.environ]
    if missing_keys:
        print(f"Missig environment variables to load credentials: {missing_keys}")
        return None
    
    return MyWellnessCredential(os.environ[username_key], os.environ[password_key])
