import socket

""" status options """
STATUS_OPTIONS = (
    ('pending', 'Pending'),
    ('authorised', 'Authorised'),
    ('declined', 'Declined'),
    ('cleared', 'Cleared'),
    ('canceled', 'Canceled'),
)


""" auth options """
AUTH_OPTIONS = (
    ('dm', 'Department Manager Only'),
    ('dmmd', 'Department Manager and Managing Director')
)


""" auth response """
AUTH_RESPONSE = (
    ('null', '-'),
    ('accepted', 'Accepted'),
    ('declined', 'Declined')
)


""" group managers """
GROUP_MANAGERS = {
    'Production': 'tracey@primarysite.net',
    'Finance': 'geoff.collier@primarysite.net',
    'Sales & Marketing': 'rachel.panther@primarysite.net',
    'Technical': 'stewart.houten@primarysite.net',
}


""" MD EMAIL """
MD_EMAIL = "geoff.millington@primarysite.net"

""" hostname """
try:
    HOSTNAME = socket.gethostname()
except:
    HOSTNAME = 'localhost'
