try:
	from setuptools import setup
except Importerror
	from distutils.core import setup

config = {
		'description':'A simple text editor written in python; using pyside for GUI',
		'author' : 'Abu_Rah',
		'url' : 'URL to get it at.',
		'download_url':'where to download at.',
		'author_email':'82013248b@gmail.com',
		'version':'0.1',
		'install_requires':['distribute', "pyside"],
		'packages':['pycode'],
		'scripts':[],
		'name':'projectname'
}

setup(**config)