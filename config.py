#!/usr/bin/env python
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
"""Configuration for the bot."""

import os


class DefaultConfig:
    """Configuration for the bot."""

    PORT = 8000
    APP_ID = os.environ.get("MicrosoftAppId", "44210fcc-87ef-419e-bd84-2e13fe65e15a")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "T7-8Q~Y~TMWB5uvQ_OiYG7G7mO4GHuVoRkuD3cx3")
    LUIS_APP_ID = os.environ.get("LuisAppId", "dec0cdc8-eeb5-44e0-9ccc-5c742a8fc1b7")
    LUIS_API_KEY = os.environ.get("LuisAPIKey", "b766bd55572648bb8dbcc423f10e558b")
    # LUIS endpoint host name, ie "westus.api.cognitive.microsoft.com"
    LUIS_API_HOST_NAME = os.environ.get("LuisAPIHostName", "luise-p10.cognitiveservices.azure.com")
    APPINSIGHTS_INSTRUMENTATION_KEY = os.environ.get(
        "AppInsightsInstrumentationKey", "f0163947-d8c0-436b-8636-36cee15e8872"
    )