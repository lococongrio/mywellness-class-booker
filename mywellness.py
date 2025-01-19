from pydantic import BaseModel
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List
import pytz
import requests
import time

utc=pytz.UTC

class BookingInfo(BaseModel):
    bookingOpensOn: datetime
    bookingOpensOnMinutesInAdvance: int
    cancellationMinutesInAdvance: int
    bookingHasWaitingList: bool
    bookingTimeInAdvanceType: str
    bookingTimeInAdvanceValue: int
    bookingUserStatus: str
    bookingAvailable: bool
    dayInAdvanceStartHour: int
    dayInAdvanceStartMinutes: int

class ClassEvent(BaseModel):
    room: str
    roomId: str
    hasLayout: bool
    id: str
    cannotTrack: bool
    name: str
    startDate: datetime
    partitionDate: int
    endDate: datetime
    recurrenceStartDate: datetime
    recurrenceEndDate: datetime
    isSingleOccurrence: bool
    calendarEventType: str
    eventTypeId: str
    staffId: str
    staffUserId: str
    assignedTo: str
    facilityName: str
    facilityId: str
    chainId: str
    pictureUrl: str
    maxParticipants: int = field(default=None)
    isParticipant: bool = field(default=None)
    hasBeenDone: bool = field(default=None)
    metsPerHour: int = field(default=None)
    estimatedCalories: int = field(default=None)
    estimatedMove: int = field(default=None)
    autoLogin: bool
    tags: List[str]
    waitingListPosition: int
    waitingListCounter: int
    isInWaitingList: bool
    liveEvent: bool
    autoStartEvent: bool
    availablePlaces: int
    extData: object
    skus: List[str]
    actualizedStartDateTime: datetime
    numberOfParticipants: int
    bookOpenedNotificationReminderEnabled: bool
    bookingInfo: BookingInfo
    hasPenaltiesOn: bool = field(default=False)

    def day_of_week(self) -> int:
        return self.startDate.weekday()
    
    def start_hour(self) -> int:
        return self.startDate.hour

    def book(self, session: 'MyWellnessSession'):
        return session.book_event(self.id, self.partitionDate)
    
    def booking_opens_in(self, within=timedelta(seconds=10)) -> bool:
        return self.bookingInfo.bookingOpensOn < (utc.localize(datetime.now()) + within)
    
    def is_signed_up(self):
        return self.isParticipant or self.isInWaitingList

    def signup_closed(self):
        return self.startDate < datetime.now()
    
    def status(self):
        if self.isParticipant:
            return "Signed up"
        elif self.isInWaitingList:
            return f"Waiting ({self.waitingListPosition}/{self.waitingListCounter})" 
        else:
            if self.signup_closed():
                booking = "Expired" 
            elif self.booking_opens_in(timedelta()):
                booking = "Open"
            elif self.booking_opens_in():
                booking = "Opens soon"
            else:
                booking = f"Closed until {self.bookingInfo.bookingOpensOn}"

            return f"Not signed up ({booking})"
    
    def to_string_with_status(self):
        return f"{self.to_string()}. Status: {self.status()}"
    
    def to_string(self):
        return f"{self.name} on {self.startDate} by {self.assignedTo} @ {self.room}"


class UserContext(BaseModel):
    id: str

class LoginResponseData(BaseModel):
    userContext: UserContext

class LoginResponse(BaseModel):
    data: LoginResponseData
    token: str

@dataclass
class MyWellnessCredential:
    username: str
    password: str

    def login(self) -> "MyWellnessSession":
        response = requests.post(
            "https://services.mywellness.com/Application/EC1D38D7-D359-48D0-A60C-D8C0B8FB9DF9/Login?_c=en-US",
            json={
                "keepMeLoggedIn": True,
                "password": self.password,
                "username": self.username
            },
            headers={
                "referer": "https://widgets.mywellness.com/",
                "x-mwapps-appid": "EC1D38D7-D359-48D0-A60C-D8C0B8FB9DF9",
                "x-mwapps-client": "enduserweb",
                "x-mwapps-clientversion": "1.13.10-1629,enduserweb"
            })
        parsed = LoginResponse.parse_raw(response.text)
        return MyWellnessSession(parsed.token, parsed.data.userContext.id)


@dataclass
class MyWellnessSession:
    token: str
    user_id: str

    def _authorization_headers(self):
        return { "Authorization": f"Bearer {self.token}"}

    def search_events(self, facilityId: str, from_date: str, to_date: str) -> List[ClassEvent]:
        query_url=f"https://calendar.mywellness.com/v2/enduser/class/Search?eventTypes=Class&facilityId={facilityId}&fromDate={from_date}&toDate={to_date}"
        response = requests.get(query_url, headers=self._authorization_headers())
        if response.status_code == 200:
            return [ClassEvent(**classEventData) for classEventData in response.json()]
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            return []
    

    def book_event(self, event_id: str, partitionDate: str):
        booking = {
            "partitionDate": partitionDate,
            "userId": self.user_id,
            "classId": event_id
        }
        response = requests.post(
            "https://calendar.mywellness.com/v2/enduser/class/Book?_c=nl-NL",
            json = booking,
            headers=self._authorization_headers()
        )
        if (response.status_code != 200):
            print(f"Event booking failed ({response.status_code}): {response.text}")

        return response.status_code == 200
    
    def burst_booking(self, events: List[ClassEvent]):
        if not events:
            print("No classes to sign up for")
            return

        print(f"Attempting to sign up for classes: {events}")

        counter = 0
        while events and counter < 100:
            for event in events:
                if(event.book(self)):
                    print(f"Successfully booked {event.to_string()} ")
                    events.remove(event)
            counter += 1
            time.sleep(0.1)

        print(f"Giving up on registering for {events}")
