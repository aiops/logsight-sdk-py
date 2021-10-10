
class Quality:
    """
    [
       {
          "@timestamp":"2021-10-10T17:03:56.470394",
          "actual_level":"INFO",
          "app_name":"hello_app",
          "message":"0.1. Hello World!",
          "param_0":"0.1.",
          "template":"<*> Hello World!"

          "linguistic_prediction":0.9992597103118896,
          "log_level_score":1,
          "predicted_level":"INFO, DEBUG, TRACE",
          "prediction":0,
          "tags":"X PUNCT X PROPN PROPN PUNCT",

          "suggestions":[
             [
                "VERB NOUN NOUN NOUN ADP NOUN PUNCT",
                "VERB DET NOUN NOUN PUNCT ADP NOUN PUNCT DET DET NOUN NOUN"
             ],
             "X PUNCT X PROPN PROPN PUNCT"
          ],
          "tag":null,
       }
    ]
    """

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
