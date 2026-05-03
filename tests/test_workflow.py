import json
import tempfile
import unittest
from pathlib import Path

from orbit_agent_kit.agents import run_workflow
from orbit_agent_kit.llm import MockMiMoClient
from orbit_agent_kit.report import write_report


class WorkflowTest(unittest.TestCase):
    def test_workflow_generates_all_agents(self) -> None:
        result = run_workflow("生成 MiMo Orbit 申请证明包", MockMiMoClient())
        self.assertEqual(len(result.runs), 5)
        self.assertGreater(result.total_tokens, 0)
        self.assertFalse(result.live)

    def test_report_writes_expected_files(self) -> None:
        result = run_workflow("生成 MiMo Orbit 申请证明包", MockMiMoClient())
        with tempfile.TemporaryDirectory() as temp_dir:
            out_dir = Path(temp_dir)
            write_report(result, out_dir)

            evidence = json.loads((out_dir / "evidence.json").read_text(encoding="utf-8"))
            self.assertEqual(evidence["total_tokens"], result.total_tokens)
            self.assertTrue((out_dir / "summary.md").exists())
            self.assertTrue((out_dir / "index.html").exists())


if __name__ == "__main__":
    unittest.main()
