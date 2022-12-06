#OK ? acient
from dialogs.booking_dialog import BookingDialog


###################### ###################### ###################### ######################
# ###################### ###################### ###################### ######################
# ###################### ###################### ###################### ######################
# TODO remettre ?
import pytest
import aiounittest
#import unittest2
import asyncio

#current = pathlib.Path(__file__).parent.parent
#libpath = current.joinpath("D:\\mySample\\code\\github\\VideoTutorial\\BotTutorialSample\\Python_tutorial\\24-CustomPrompt\\prompt")
#sys.path.append(str(libpath))

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
#class EmailPromptTest(unittest2.TestCase):
    async def test_email_prompt(self):
        async def exec_test(turn_context:TurnContext):
            dialog_context = await dialogs.create_context(turn_context)

            results = await dialog_context.continue_dialog()
            if (results.status == DialogTurnStatus.Empty):
                options = PromptOptions(
                    prompt = Activity(
                        type = ActivityTypes.message, 
                        text = "What can I help you with today?"
                        )
                    )
                await dialog_context.prompt("emailprompt", options)
                
                #await dialog_context.prompt(options)

            elif results.status == DialogTurnStatus.Complete:
                reply = results.result
                await turn_context.send_activity(reply)

            await conv_state.save_changes(turn_context)

        adapter = TestAdapter(exec_test)

        conv_state = ConversationState(MemoryStorage())
        dialogs_state = conv_state.create_property("dialog-state")
        dialogs = DialogSet(dialogs_state)
        dialogs.add(BookingDialog())
        step1 = await adapter.test('Hello', 'What can I help you with today?')
        step2 = await step1.send('popopopop')
        await step2.assert_reply("To what city would you like to travel?")

        conv_state = ConversationState(MemoryStorage())
        dialogs_state = conv_state.create_property("dialog-state")
        dialogs = DialogSet(dialogs_state)
        dialogs.add(BookingDialog())
        step1 = await adapter.test('Hello', 'What can I help you with today?')
        step2 = await step1.send('b2O')
        await step2.assert_reply("To what city would you like to travel?")

