from abjad.tools import systemtools

systemtools.ImportManager.import_structured_package(
	__path__[0],
	globals(),
	package_root_name='experimental')

_documentation_section = 'demos'

del(main)
