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
        step1 = await adapter.test('book a flight to paris from berlin for the 11/11/22 with budget of 999$', 'return date ?')
        step2 = await step1.send('11/11/22')
        await step2.assert_reply("Please confirm, I have you traveling to: Paris from: Berlin on: 2022-11-11. return: 11/11/22 for max: 999 $.")

