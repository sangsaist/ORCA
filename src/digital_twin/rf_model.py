"""
rf_model
-----------
RF Coexistence Model for the ORCA Digital Twin.

Estimates RF coexistence margin between active spacecraft
payloads using a lightweight conflict matrix.
"""

from .config import (
    RF_BASE_MARGIN,
    RF_WARNING_MARGIN,
    RF_CRITICAL_MARGIN,
    RF_CONFLICT_MATRIX,
)


class RFModel:
    """
    Simplified RF Coexistence Model.
    """

    def __init__(self):

        # Configuration
        self.base_margin = RF_BASE_MARGIN
        self.warning_margin = RF_WARNING_MARGIN
        self.critical_margin = RF_CRITICAL_MARGIN

        self.conflict_matrix = RF_CONFLICT_MATRIX

        # State Variables
        self.margin = self.base_margin
        self.status = "SAFE"

        self.total_penalty = 0.0
        self.conflict_count = 0
        self.conflicts = []

    def update(self, payload_states):
        """
        Evaluate RF coexistence.

        Parameters
        ----------
        payload_states : dict

        Example

        {
            "PNT":"ACTIVE",
            "SATCOM":"TX_ACTIVE",
            "EARTH_OBSERVATION":"OFF",
            "EDGE_AI":"OFF"
        }
        """

        self.total_penalty = 0.0
        self.conflict_count = 0
        self.conflicts = []

        payloads = list(payload_states.keys())

        # Evaluate every payload pair
        for i in range(len(payloads)):

            for j in range(i + 1, len(payloads)):

                p1 = payloads[i]
                p2 = payloads[j]

                s1 = payload_states[p1]
                s2 = payload_states[p2]

                forward = (p1, s1, p2, s2)
                reverse = (p2, s2, p1, s1)

                if forward in self.conflict_matrix:

                    penalty = self.conflict_matrix[forward]

                    self.total_penalty += penalty
                    self.conflict_count += 1

                    self.conflicts.append(
                        f"{p1} ↔ {p2}"
                    )

                elif reverse in self.conflict_matrix:

                    penalty = self.conflict_matrix[reverse]

                    self.total_penalty += penalty
                    self.conflict_count += 1

                    self.conflicts.append(
                        f"{p2} ↔ {p1}"
                    )

        # Calculate RF Margin
        self.margin = self.base_margin - self.total_penalty

        # Determine RF Status
        if self.margin < self.critical_margin:

            self.status = "CRITICAL"

        elif self.margin < self.warning_margin:

            self.status = "WARNING"

        else:

            self.status = "SAFE"

        return self.margin

    # ------------------------------------
    # Getter Functions
    # ------------------------------------

    def get_margin(self):
        return round(self.margin, 2)

    def get_status(self):
        return self.status

    def get_penalty(self):
        return round(self.total_penalty, 2)

    def get_conflict_count(self):
        return self.conflict_count

    def get_conflicts(self):
        return self.conflicts.copy()

    # ------------------------------------
    # Telemetry
    # ------------------------------------

    def get_state(self):

        return {

            "rf_margin": self.get_margin(),

            "rf_status": self.get_status(),

            "rf_penalty": self.get_penalty(),

            "rf_conflict_count": self.get_conflict_count(),

            "rf_conflicts": self.get_conflicts(),

        }