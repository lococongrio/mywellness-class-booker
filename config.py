from classmatcher import ClassEventMatcher, CompositeClassEventMatcher
from dataclasses import dataclass
from mywellness import MyWellnessCredential
from typing import List, Optional
import os
import pytz
import yaml

password_key='HWF_PASSWORD'
username_key='HWF_USERNAME'

@dataclass
class MatcherConfig:
    eventName: Optional[str] = None
    eventTypeId: Optional[str] = None
    day: Optional[int] = None
    hour: Optional[int] = None

    def create_matcher(self) -> ClassEventMatcher:
        return ClassEventMatcher(self.eventName, self.eventTypeId or None, self.day, self.hour)


@dataclass
class MyWellnessConfig:
    appId: str
    client: str
    clientversion: str


@dataclass
class AppConfig:
    facilityId: str
    timezone: str
    maxSuspendSeconds: int
    matchers: List[MatcherConfig]
    mywellness: MyWellnessConfig

    def create_matcher(self) -> CompositeClassEventMatcher:
        matchers = [match_config.create_matcher() for match_config in self.matchers]
        return CompositeClassEventMatcher(matchers)
    
    def load_credentials(self) -> Optional[MyWellnessCredential]:
        missing_keys = [key for key in [password_key, username_key] if not key in os.environ]
        if missing_keys:
            print(f"Missig environment variables to load credentials: {missing_keys}")
            return None
        
        return MyWellnessCredential(
            os.environ[username_key],
            os.environ[password_key],
            self.mywellness.appId,
            self.mywellness.client,
            self.mywellness.clientversion,
        )
    
    def load_timezone(self):
        return pytz.timezone(self.timezone)



def load_config(file_path: str = "config.yaml") -> AppConfig:
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
        return AppConfig(
            facilityId=data['facilityId'],
            timezone=data['timezone'],
            maxSuspendSeconds=data['maxSuspendSeconds'],
            matchers=[MatcherConfig(**matcher) for matcher in data['matchers']],
            mywellness=MyWellnessConfig(**data["mywellness"]),
        )
