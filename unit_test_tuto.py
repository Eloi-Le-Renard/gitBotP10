from dialogs.booking_dialog import BookingDialog
from booking_details import BookingDetails

import pytest
import aiounittest
#import unittest2
import asyncio

from botbuilder.dialogs.prompts import (
    AttachmentPrompt, 
    PromptOptions, 
    PromptValidatorContext, 
)

from botbuilder.core import (
    TurnContext, 
    ConversationState, 
    MemoryStorage, 
    MessageFactory, 
)
from botbuilder.schema import Activity, ActivityTypes, Attachment
from botbuilder.dialogs import DialogSet, DialogTurnStatus
#from email_prompt import EmailPrompt
from botbuilder.core.adapters import TestAdapter

booking_details = BookingDetails()
class EmailPromptTest(aiounittest.AsyncTestCase):
    async def test_email_prompt(self):
        async def exec_test(turn_context:TurnContext):
            dialog_context = await dialogs.create_context(turn_context)
            results = await dialog_context.continue_dialog()
            if (results.status == DialogTurnStatus.Empty):
                dialog_context.options = booking_details
                await dialog_context.begin_dialog("dialog_id", BookingDetails())
            elif results.status == DialogTurnStatus.Complete:
                reply = results.result
                await turn_context.send_activity(reply)
            await conv_state.save_changes(turn_context)

        adapter = TestAdapter(exec_test)
        conv_state = ConversationState(MemoryStorage())
        dialogs_state = conv_state.create_property("dialog-state")
        dialogs = DialogSet(dialogs_state)
        dialogs.add(BookingDialog("dialog_id"))

#        step1 = await adapter.send('book a flight to paris from berlin for the 11/11/22 with budget of 999$')
        step1 = await adapter.send('peut importe')
        step2 = await step1.assert_reply("To what city would you like to travel?")
        step3 = await step2.send('paris')
        step4 = await step3.assert_reply("From what city will you be travelling?")
        step5 = await step4.send('berlin')
        step6 = await step5.assert_reply("On what date would you like to travel?")
        step7 = await step6.send('11/11/121')
        step_end = await step7.assert_reply("I’m sorry, for best results, please enter your travel date including the month, day and year.")
        
        

        
        #step1 = await adapter.send('Hello')
        #step2 = await step1.assert_reply("To what city would you like to travel?")
        #step3 = await step2.send('paris')
        #await step3.assert_reply("From what city will you be travelling?")


