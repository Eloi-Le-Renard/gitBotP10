        adapter = TestAdapter(exec_test)
        conv_state = ConversationState(MemoryStorage())
        dialogs_state = conv_state.create_property("dialog-state")
        dialogs = DialogSet(dialogs_state)
        dialogs.add(BookingDialog("dialog_id"))
        
        step1 = await adapter.test('book a flight to paris from berlin for the 11/11/22 with budget of 999$', 'return date ?')
        step2 = await step1.send('11/11/22')
        await step2.assert_reply("Please confirm, I have you traveling to: Paris from: Berlin on: 2022-11-11. return: 11/11/22 for max: 999 $.")

step1 = await adapter.test('Hello', 'To what city would you like to travel?')
        step2 = await step1.send('paris')
        await step2.assert_reply("From what city will you be travelling?")

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

class EmailPromptTest(aiounittest.AsyncTestCase):
    async def test_email_prompt(self):
        async def exec_test(turn_context:TurnContext):
            dialog_context = await dialogs.create_context(turn_context)
            dialog_context.begin_dialog(BookingDetails())

        adapter = TestAdapter(exec_test)
        step1 = await adapter.test('Hello', 'What can I help you with today?')
        step2 = await step1.send('popopopop')
        await step2.assert_reply("To what city would you like to travel?")

