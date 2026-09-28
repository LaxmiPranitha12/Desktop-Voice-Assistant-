"""Automated verification tests for Phase 2 - Voice Foundation.

Tests microphone detection, speech recognition handling, predefined response system,
TTS synthesis, and assistant lifecycle.
"""

import sys
import unittest
from src.config.settings import settings
from src.core.assistant import VoiceAssistant
from src.intents.basic_responses import BasicResponseSystem
from src.intents.parser import CommandParser
from src.speech.microphone import MicrophoneManager
from src.speech.recognition import SpeechRecognizer
from src.speech.tts import TextToSpeech


class TestMicrophoneManager(unittest.TestCase):
    """Verifies microphone detection and initialization."""

    def test_microphone_detection(self):
        mic_manager = MicrophoneManager()
        self.assertTrue(mic_manager.is_available, "Microphone should be detected on the system.")
        self.assertIsNotNone(mic_manager.device_name)
        devices = mic_manager.list_devices()
        self.assertGreater(len(devices), 0, "At least one audio input device should be available.")

    def test_invalid_device_index_fallback(self):
        # Passing an impossible device index should fall back to default gracefully
        mic_manager = MicrophoneManager(device_index=9999)
        self.assertTrue(mic_manager.is_available)
        self.assertIsNone(mic_manager.device_index)


class TestTextToSpeech(unittest.TestCase):
    """Verifies TTS initialization and synthesis."""

    def test_tts_initialization(self):
        tts = TextToSpeech()
        self.assertTrue(tts.is_ready, "TTS engine should initialize successfully.")

    def test_tts_speak_execution(self):
        tts = TextToSpeech()
        # Should execute cleanly without raising exceptions
        tts.speak("Testing Voice Foundation pipeline.")


class TestBasicResponseSystem(unittest.TestCase):
    """Verifies predefined responses and intent extraction."""

    def setUp(self):
        self.system = BasicResponseSystem()

    def test_greetings(self):
        for phrase in ["Hello Nova", "hi nova", "hey", "hello"]:
            res = self.system.get_response(phrase)
            self.assertEqual(res.intent, "greeting")
            self.assertEqual(res.text, "Hello! How can I help you?")
            self.assertFalse(res.should_exit)

    def test_status_inquiry(self):
        res = self.system.get_response("how are you?")
        self.assertEqual(res.intent, "status")
        self.assertEqual(res.text, "I'm doing well. What can I do for you?")
        self.assertFalse(res.should_exit)

    def test_identity_inquiry(self):
        res = self.system.get_response("who are you")
        self.assertEqual(res.intent, "identity")
        self.assertIn("Nova", res.text)
        self.assertFalse(res.should_exit)

    def test_capabilities_inquiry(self):
        res = self.system.get_response("what can you do")
        self.assertEqual(res.intent, "capabilities")
        self.assertIn("Nova", res.text)
        self.assertFalse(res.should_exit)

    def test_shutdown_commands(self):
        for phrase in ["exit", "quit", "goodbye", "bye nova"]:
            res = self.system.get_response(phrase)
            self.assertEqual(res.intent, "shutdown")
            self.assertTrue(res.should_exit)
            self.assertIn("Goodbye", res.text)

    def test_silence_handling(self):
        res = self.system.get_response(None)
        self.assertEqual(res.intent, "silence")
        self.assertEqual(res.text, "")
        self.assertFalse(res.should_exit)

    def test_unintelligible_speech_handling(self):
        res = self.system.get_response("")
        self.assertEqual(res.intent, "unintelligible")
        self.assertEqual(res.text, "I didn't catch that. Could you please repeat?")
        self.assertFalse(res.should_exit)

    def test_unrecognized_command(self):
        res = self.system.get_response("arbitrary unrecognized phrase 12345")
        self.assertEqual(res.intent, "unknown")
        self.assertEqual(res.text, "I'm sorry, I didn't quite catch that. Could you please repeat?")
        self.assertFalse(res.should_exit)


class TestCommandParser(unittest.TestCase):
    """Verifies CommandParser structure."""

    def test_parser_intent_result(self):
        parser = CommandParser()
        result = parser.parse("Hello Nova")
        self.assertEqual(result.intent_name, "greeting")
        self.assertEqual(result.confidence, 1.0)
        self.assertEqual(result.response_text, "Hello! How can I help you?")
        self.assertFalse(result.should_exit)


class TestVoiceAssistantPipeline(unittest.TestCase):
    """Verifies end-to-end pipeline coordination."""

    def setUp(self):
        self.assistant = VoiceAssistant()

    def test_start_and_readiness(self):
        self.assistant.start()
        self.assertTrue(self.assistant.is_running)

    def test_continuous_flow_after_unrecognized(self):
        self.assistant.start()
        res = self.assistant.process_command("completely unknown command")
        self.assertTrue(self.assistant.is_running, "Assistant must remain running after unrecognized command.")
        self.assertEqual(res.intent_name, "unknown")

    def test_continuous_flow_after_silence(self):
        self.assistant.start()
        res = self.assistant.process_command(None)
        self.assertTrue(self.assistant.is_running, "Assistant must remain running after silence.")
        self.assertEqual(res.intent_name, "silence")

    def test_clean_shutdown_on_exit(self):
        self.assistant.start()
        res = self.assistant.process_command("goodbye")
        self.assertFalse(self.assistant.is_running, "Assistant must stop running after exit command.")
        self.assertEqual(res.intent_name, "shutdown")
        self.assistant.stop()


if __name__ == "__main__":
    unittest.main()
