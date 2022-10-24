from .template import Template


class Quality(Template):

    def __init__(self, data):
        Template.__init__(self, data)

        self._predicted_level = data.get("predicted_level", None)
        self._prediction = data.get("prediction", None)
        self._suggestions = data.get("suggestions", None)
        self._tags = data.get("tags", None)
        self._linguistic_prediction = data.get("linguistic_prediction", None)
        self._log_level_score = data.get("log_level_score", None)

    def __repr__(self):
        return {
            "app_name": self._app_name,
            "predicted_level": self._predicted_level,
        }

    @property
    def predicted_level(self):
        """str: Predicted log level for the log message (e.g., WARNING)."""
        return self._predicted_level

    @property
    def prediction(self):
        """int: Prediction for the log message.
            1 (one) for INFO, DEBUG, TRACE
            0 (zero) for WARNING, WARN, ERROR, EXCEPTION, CRITICAL
        """
        return self._prediction

    @property
    def suggestions(self):
        """List[List[str], str]: list of suggestions to improve the quality of
         the message

        Examples:
            [['VERB NOUN NOUN ADP NOUN PUNCT', 'VERB NOUN NOUN PUNCT ADP',
              'AUX PART VERB NOUN NOUN PUNCT', 'VERB NOUN NOUN NOUN NOUN'],
              'X PUNCT PUNCT PROPN PROPN PUNCT'
            ]

        """
        return self._suggestions

    @property
    def tags(self):
        """str: universal POS tags for the template

        Examples:
            'X PUNCT PUNCT PROPN VERB PART VERB X PUNCT PUNCT'

        """
        return self._tags

    @property
    def linguistic_prediction(self):
        """float: confidence of the prediction in [0, 1]

        Examples:
            'X PUNCT PUNCT PROPN VERB PART VERB X PUNCT PUNCT'

        """
        return self._linguistic_prediction

    @property
    def log_level_score(self):
        """int: log level score"""
        return self._log_level_score
