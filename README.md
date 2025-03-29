﻿# cloud_project_backend-Translator_ChatBot-

"""
Translation is working: input "Hola" (Spanish) was likely translated internally to English → 
Lex responded with "Hello! I’m here to help you with translations." → then app translated it back 
to Spanish for the user as:
"¡Hola! Estoy aquí para ayudarlo con las traducciones".

Polly generated the audio correctly (MP3 binary response in "audio").

The flow is functioning like this:
User input: "Hola"

→ Translate from Spanish to English → "Hello"
→ Lex processes "Hello" → sends back: "Hello! I'm here to help you with translations."
→ Translate back to Spanish → "¡Hola! Estoy aquí para ayudarlo con las traducciones."
→ Polly speaks the final Spanish output

This is the expected flow — Spanish in → English logic → Spanish out — full 
Lex + Translate + Polly pipeline is working end-to-end.

Tested using postman API
"""
