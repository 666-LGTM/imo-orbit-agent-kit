import unittest

from orbit_agent_kit.llm import MockMiMoClient, estimate_tokens


class LLMTest(unittest.TestCase):
    def test_estimate_tokens_handles_empty_text(self) -> None:
        self.assertEqual(estimate_tokens(""), 0)

    def test_estimate_tokens_counts_chinese_text(self) -> None:
        self.assertGreaterEqual(estimate_tokens("你好，MiMo"), 3)

    def test_mock_client_is_deterministic(self) -> None:
        client = MockMiMoClient()
        result = client.complete("# Planner", "项目想法：测试")
        self.assertIn("目标用户", result.content)
        self.assertFalse(result.live)
        self.assertGreater(result.input_tokens, 0)
        self.assertGreater(result.output_tokens, 0)


if __name__ == "__main__":
    unittest.main()
