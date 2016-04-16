class CodeFunction(object):
    type = ''
    name = ''
    parameters = []
    description = ''


    def __init__(self, return_type, name, parameters, description=''):
        self.return_type = return_type
        self.name = name
        self.parameters = parameters
        self.description= description
