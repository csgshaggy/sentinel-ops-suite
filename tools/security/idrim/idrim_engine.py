# tools/security/idrim/idrim_engine.py

from .collectors.iam_collector import IAMCollector
from .collectors.role_collector import RoleCollector
from .collectors.group_collector import GroupCollector

from .analyzers.drift_analyzer import DriftAnalyzer
from .baselines.baseline_manager import BaselineManager

from .outputs.idrim_reporter import IDRIMReporter


class IDRIMEngine:
    """
    Identity Drift & Role Integrity Monitor (IDRIM)
    Core orchestration engine responsible for:
    - Collecting IAM state
    - Loading and saving baselines
    - Computing drift
    - Emitting drift events
    """

    def __init__(self):
        # Collectors
        self.iam_collector = IAMCollector()
        self.role_collector = RoleCollector()
        self.group_collector = GroupCollector()

        # Baseline + analysis
        self.baseline_manager = BaselineManager()
        self.drift_analyzer = DriftAnalyzer()

        # Output pipeline
        self.reporter = IDRIMReporter()

    def collect_current_state(self):
        """
        Pulls the full IAM state from collectors.
        Returns a deterministic dictionary structure.
        """
        return {
            "users": self.iam_collector.collect(),
            "roles": self.role_collector.collect(),
            "groups": self.group_collector.collect(),
        }

    def run(self):
        """
        Main execution path:
        - Collect current IAM state
        - Load baseline
        - Analyze drift
        - Emit events
        Returns list of drift events.
        """
        current_state = self.collect_current_state()
        baseline = self.baseline_manager.load_baseline()

        drift_events = self.drift_analyzer.analyze(
            baseline=baseline,
            current=current_state
        )

        for event in drift_events:
            self.reporter.emit(event)

        return drift_events

    def rebuild_baseline(self):
        """
        Rebuilds IAM baseline snapshot using current state.
        Returns the new baseline.
        """
        current_state = self.collect_current_state()
        self.baseline_manager.save_baseline(current_state)
        return current_state

    def diff(self):
        """
        Computes a diff between baseline and current IAM state.
        Returns a structured diff object.
        """
        current_state = self.collect_current_state()
        baseline = self.baseline_manager.load_baseline()

        return self.drift_analyzer.compute_diff(
            baseline=baseline,
            current=current_state
        )
