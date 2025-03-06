from dataclasses import dataclass
from mywellness import ClassEvent
from typing import List, Optional

@dataclass
class ClassEventMatcher:
    event_name: Optional[str] = None
    event_type_id: Optional[str] = None
    day: Optional[int] = None
    starting_hour: Optional[int] = None

    def matches(self, classEvent: ClassEvent) -> bool:
        return (not self.event_name or classEvent.name == self.event_name) \
            and (not self.event_type_id or classEvent.eventTypeId == self.event_type_id) \
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
