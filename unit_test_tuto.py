# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.


"""Flight booking dialog."""

from datatypes_date_time.timex import Timex

from botbuilder.dialogs import WaterfallDialog, WaterfallStepContext, DialogTurnResult
from botbuilder.dialogs.prompts import ConfirmPrompt, TextPrompt, PromptOptions
from botbuilder.core import MessageFactory, BotTelemetryClient, NullTelemetryClient
from dialogs.cancel_and_help_dialog import CancelAndHelpDialog
from dialogs.date_resolver_dialog import DateResolverDialog


class BookingDialog(CancelAndHelpDialog):
    """Flight booking implementation."""

    def __init__(
        self,
        dialog_id: str = None,
        telemetry_client: BotTelemetryClient = NullTelemetryClient(),
    ):
        super(BookingDialog, self).__init__(
            dialog_id or BookingDialog.__name__, telemetry_client
        )
        self.telemetry_client = telemetry_client
        text_prompt = TextPrompt(TextPrompt.__name__)
        text_prompt.telemetry_client = telemetry_client

        waterfall_dialog = WaterfallDialog(
            WaterfallDialog.__name__,
            [
                self.destination_step,
                self.origin_step,
                self.travel_date_step,
                self.return_date_step,
                self.budget_step,
                self.test2,
                self.test3,
                #self.confirm_step,
                
                self.final_step2,
            ],
        )
        waterfall_dialog.telemetry_client = telemetry_client

        self.add_dialog(text_prompt)
        # self.add_dialog(ConfirmPrompt(ConfirmPrompt.__name__))
        self.add_dialog(
            DateResolverDialog(DateResolverDialog.__name__, self.telemetry_client)
        )
        self.add_dialog(waterfall_dialog)

        self.initial_dialog_id = WaterfallDialog.__name__

    async def destination_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        """Prompt for destination."""
        booking_details = step_context.options
        if booking_details.destination is None:
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    #prompt=MessageFactory.text(f"To what city would you like to travel? {booking_details}")
                    prompt=MessageFactory.text("To what city would you like to travel?")
                ),
            )  # pylint: disable=line-too-long,bad-continuation

        return await step_context.next(booking_details.destination)

    async def origin_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """Prompt for origin city."""
        

        booking_details = step_context.options

        # Capture the response to the previous step's prompt
        booking_details.destination = step_context.result
        if booking_details.origin is None:
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("From what city will you be travelling?")
#                    prompt=MessageFactory.text(f"From what city will you be travelling? {booking_details}")
                ),
            )  # pylint: disable=line-too-long,bad-continuation

        return await step_context.next(booking_details.origin)

    async def travel_date_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        """Prompt for travel date.
        This will use the DATE_RESOLVER_DIALOG."""

        booking_details = step_context.options

        # Capture the results of the previous step
        booking_details.origin = step_context.result
        if not booking_details.travel_date or self.is_ambiguous(
            booking_details.travel_date
        ):
            return await step_context.begin_dialog(
                DateResolverDialog.__name__, booking_details.travel_date
            )  # pylint: disable=line-too-long

        return await step_context.next(booking_details.travel_date)

    async def return_date_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        """Prompt for return date.
        This will use the DATE_RESOLVER_DIALOG."""
        # marche pas
        #step_context.prompt(TextPrompt.__name__,PromptOptions(prompt=MessageFactory.text("test ?")))
        
        booking_details = step_context.options

        # Capture the results of the previous step
        booking_details.travel_date = step_context.result
        if booking_details.return_date is None:
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text(f"return date ? {booking_details}")
                ),
            )
        
        if not booking_details.return_date or self.is_ambiguous(
            booking_details.return_date
        ):
            return await step_context.begin_dialog(
                DateResolverDialog.__name__, booking_details.return_date
            )  # pylint: disable=line-too-long

        return await step_context.next(booking_details.return_date)

    async def budget_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        """Prompt for travel date.
        This will use the DATE_RESOLVER_DIALOG."""

        booking_details = step_context.options

        # Capture the results of the previous step
        booking_details.return_date = step_context.result
        
        if booking_details.budget is None:
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("budget ?")
#                    prompt=MessageFactory.text(f"budget ? {booking_details}")
                ),
            )
        #if not booking_details.budget:
        #    return await step_context.begin_dialog(
        #        DateResolverDialog.__name__, booking_details.budget
        #    )  # pylint: disable=line-too-long

        return await step_context.next(booking_details.budget)
    
    
    async def test2(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        #logger.warning("log confirm_step()")
        booking_details = step_context.options
        booking_details.budget = step_context.result
        
        msg = (
            f"Please confirm, I have you traveling to: { booking_details.destination }"
            f" from: { booking_details.origin } on: { booking_details.travel_date}."
            f" return: { booking_details.return_date } for: { booking_details.budget}."
         #   f" OBJECT: { booking_details } "
        )
        return await step_context.prompt(TextPrompt.__name__,PromptOptions(prompt=MessageFactory.text(
            msg)))

   # TODO
    async def test3(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
    #properties = {'custom_dimensions': {'key_1': 'value_1', 'key_2': 'value_2'}}
#logger.warning('action', extra=properties)
        
        booking_details = step_context.options
        booking_details.validate = step_context.result
        
        if booking_details.validate == "yes":
            msg = "you say YESA, i confirmed your flight"
        else:
            msg = "you say NO, let's restart"
            logger.warning("user say no", properties={'test': {'key_1': 'value_1', 'key_2': 'value_2'}})#step_context.dialogs)
            #logger.warning("user say no")
        # voir journal log severity == 0 and message == "notConfirmed"
        self.telemetry_client.track_trace(name='notConfirmed', properties={"destination":str(booking_details.destination),
                                                                            "origin":str(booking_details.origin),
                                                                            "travel_date":str(booking_details.travel_date),
                                                                            "return_date":str(booking_details.return_date),
                                                                            "budget":str(booking_details.budget)})
        
        return await step_context.prompt(TextPrompt.__name__,PromptOptions(prompt=MessageFactory.text(
            msg)))


    async def confirm_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        """Confirm the information the user has provided."""

        # TODO
        #logger.info("log_info (i)")
        logger.warning("log confirm_step()")

        booking_details = step_context.options

        # Capture the results of the previous step
        booking_details.budget = step_context.result
        msg = (
            f"Please confirm, I have you traveling to: { booking_details.destination }"
            f" from: { booking_details.origin } on: { booking_details.travel_date}."
        )

        # Offer a YES/NO prompt.
        return await step_context.prompt(
            ConfirmPrompt.__name__, PromptOptions(prompt=MessageFactory.text(msg))
        )

    async def final_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """Complete the interaction and end the dialog."""
        if step_context.result:
            booking_details = step_context.options
            booking_details.travel_date = step_context.result

            return await step_context.end_dialog(booking_details)

        return await step_context.end_dialog()

    async def final_step2(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """Complete the interaction and end the dialog."""
        return await step_context.end_dialog()

    def is_ambiguous(self, timex: str) -> bool:
        """Ensure time is correct."""
        timex_property = Timex(timex)
        return "definite" not in timex_property.types


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
                #await dialog_context.prompt("emailprompt", options)
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

