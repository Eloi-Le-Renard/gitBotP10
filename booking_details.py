# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.


class BookingDetails:
    def __init__(
        self,
        destination: str = None,
        origin: str = None,
        travel_date: str = None,
        unsupported_airports=None,
        return_date: str = None,
        budget: str = None
    ):
        if unsupported_airports is None:
            unsupported_airports = []
        self.destination = destination
        self.origin = origin
        self.travel_date = travel_date
        self.unsupported_airports = unsupported_airports
        self.return_date = return_date
        self.budget = budget
        
    def __repr__(self):
        res = "self.destination = "+str(self.destination)+", self.origin = "+str(self.origin)+", self.travel_date = "+str(self.travel_date)+", self.return_date = "+str(self.return_date)+", self.budget = "+str(self.budget)
        return res
    
            
    def __str__(self):
        res = "self.destination = "+str(self.destination)+", self.origin = "+str(self.origin)+", self.travel_date = "+str(self.travel_date)+", self.return_date = "+str(self.return_date)+", self.budget = "+str(self.budget)
        return res
