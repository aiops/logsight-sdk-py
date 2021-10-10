
class Quality:

    def __init__(self, data):
        self._actual_level = data.get("actual_level", None)
        self._predicted_level = data.get("predicted_level", None)
        self._prediction = data.get("prediction", None)

    def __repr__(self):
        return {
            "app_name": self._app_name,
            "predicted_level": self._predicted_level,
        }

    @property
    def actual_level(self):
        """str: Actual log level for the log message (e.g., WARNING)."""
        return self._actual_level

    @property
    def predicted_level(self):
        """str: Predicted log level for the log message (e.g., WARNING)."""
        return self._predicted_level

    @property
    def prediction(self):
        """int: Prediction for the log message.
            1 (one) for INFO, DEBUG, TRACE.
            0 (zero) for WARNING, WARN, ERROR, EXCEPTION, CRITICAL.
        """
        return self._prediction
