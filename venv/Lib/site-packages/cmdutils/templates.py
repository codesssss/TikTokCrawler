import os
from paste.script.templates import Template

ENTRY_POINT = """
[console_scripts]
%(name)s = %(name)s.command:main
"""

class CmdTemplate(Template):

    summary = 'Create a new command-line utility that uses CmdUtils'
    required_templates = ['basic_package']
    _template_dir = 'paster_template'
    
    def post(self, command, output_dir, vars):
        setup_py = os.path.join(output_dir, 'setup.py')
        command.insert_into_file(setup_py,
                                 'Entry points',
                                 '%(package)s = %(package)s.command:main\n' % vars,
                                 indent=True)
        command.insert_into_file(setup_py,
                                 'Entry points',
                                 '[console_scripts]\n',
                                 indent=True)
        command.insert_into_file(setup_py,
                                 'Extra requirements',
                                 "'CmdUtils',\n",
                                 indent=True)
