from dataclasses import dataclass
from typing import List
from mywellness import ClassEvent

@dataclass
class ClassEventMatcher:
    event_type_id: str
    day: int | None = None
    starting_hour: int | None = None

    def matches(self, classEvent: ClassEvent) -> bool:
        return classEvent.eventTypeId == self.event_type_id \
            and (self.day is None or self.day == classEvent.day_of_week()) \
            and (self.starting_hour is None or self.starting_hour == classEvent.start_hour())

@dataclass
class CompositeClassEventMatcher:
    matchers: List[ClassEventMatcher]

    def matches(self, classEvent: ClassEvent) -> bool:
        for matcher in self.matchers:
            if matcher.matches(classEvent):
                return True
        return False
