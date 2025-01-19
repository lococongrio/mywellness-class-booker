from dataclasses import dataclass
from typing import List, Optional
import yaml

from classmatcher import ClassEventMatcher, CompositeClassEventMatcher


@dataclass
class MatcherConfig:
    eventTypeId: str
    day: Optional[int] = None
    hour: Optional[int] = None

    def create_matcher(self) -> ClassEventMatcher:
        return ClassEventMatcher(self.eventTypeId, self.day, self.hour)


@dataclass
class Config:
    facilityId: str
    matchers: List[MatcherConfig]

    def create_matcher(self) -> CompositeClassEventMatcher:
        matchers = [match_config.create_matcher() for match_config in self.matchers]
        return CompositeClassEventMatcher(matchers)


def load_config(file_path: str = "config.yaml") -> Config:
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
        return Config(
            facilityId=data['facilityId'],
            matchers=[MatcherConfig(**matcher) for matcher in data['matchers']]
        )
