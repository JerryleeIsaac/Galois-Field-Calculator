class InputError(Exception):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

    def __unicode__(self):
        return repr(self.expression) + " " + self.message

    def __str__(self):
        return repr(self.expression) + " " + self.message
