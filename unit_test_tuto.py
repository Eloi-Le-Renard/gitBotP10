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