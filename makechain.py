import json, sys

KEY_REM = 'remark'
KEY_ID = 'id'
KEY_DEPS = 'deps'
KEY_TITLE = 'title'
KEY_ACTION='action'
KEY_SIMULATION='simulation'
KEY_FEEDBACK='feedback'
KEY_CHALLENGE = 'challenge'
KEY_MODELING = 'modeling'
KEY_NOTES = 'notes'

KEY_PROPS_NEW = [KEY_TITLE, KEY_ACTION, KEY_SIMULATION, KEY_FEEDBACK, KEY_CHALLENGE, KEY_MODELING]
KEY_PROPS_PRE = [KEY_MODELING]



NODE_HEADER='''
  %(id)s [ label=<
    <table border="1" cellborder="0" cellspacing="-1" cellpadding="3" color="#000000" bgcolor="#000000">'''

NODE_FOOTER='''
    </table>> ];
'''

NODE_SECTION_NEW = {}

NODE_SECTION_NEW[KEY_TITLE]='''
      <tr>
        <td bgcolor="#363636" height="5" colspan="4"></td>
      </tr>
      <tr>
        <td bgcolor="#363636" width="10"></td>
        <td bgcolor="#363636" align="left" colspan="2"><font color="#FFFFFF">%(title)s</font></td>
        <td bgcolor="#363636" width="10"></td>
      </tr>
      <tr>
        <td bgcolor="#363636" height="5" colspan="4"></td>
      </tr>'''

NODE_SECTION_NEW[KEY_ACTION]='''
      <tr>
        <td bgcolor="#FFFFFF" width="10"></td>
        <td bgcolor="#FFFFFF" width="50" height="50" valign="top"><img src="sc-button.png" /></td>
        <td bgcolor="#FFFFFF" width="200" align="left" balign="left"><font color="#000000">%(action)s</font></td>
        <td bgcolor="#FFFFFF" width="10"></td>
      </tr>'''

NODE_SECTION_NEW[KEY_SIMULATION]='''
      <tr>
        <td bgcolor="#FFFFFF" width="10"></td>
        <td bgcolor="#FFFFFF" width="50" height="50" valign="top"><img src="sc-gear.png" /></td>
        <td bgcolor="#FFFFFF" width="200" align="left" balign="left"><font color="#000000">%(simulation)s</font></td>
        <td bgcolor="#FFFFFF" width="10"></td>
      </tr>'''

NODE_SECTION_NEW[KEY_FEEDBACK]='''
      <tr>
        <td bgcolor="#FFFFFF" width="10"></td>
        <td bgcolor="#FFFFFF" width="50" height="50" valign="top"><img src="sc-eye.png" /></td>
        <td bgcolor="#FFFFFF" width="200" align="left" balign="left"><font color="#000000">%(feedback)s</font></td>
        <td bgcolor="#FFFFFF" width="10"></td>
      </tr>'''

NODE_SECTION_NEW[KEY_CHALLENGE]='''
      <tr>
        <td bgcolor="#FFFFFF" width="10"></td>
        <td bgcolor="#FFFFFF" width="50" height="50" valign="top"><img src="sc-chal.png" /></td>
        <td bgcolor="#FFFFFF" width="200" align="left" balign="left"><font color="#000000">%(challenge)s</font></td>
        <td bgcolor="#FFFFFF" width="10"></td>
      </tr>'''

NODE_SECTION_NEW[KEY_MODELING]='''
      <tr>
        <td bgcolor="#558729" width="10"></td>
        <td bgcolor="#558729" width="50" height="50" valign="top"><img src="sc-bulb.png" /></td>
        <td bgcolor="#558729" width="200" align="left" balign="left"><font color="#FFFFFF"><i>"%(modeling)s"</i></font></td>
        <td bgcolor="#558729" width="10"></td>
      </tr>'''

NODE_SECTION_PRE = {}

NODE_SECTION_PRE[KEY_MODELING]='''
      <tr>
        <td bgcolor="#555C9F" width="10"></td>
        <td bgcolor="#555C9F" width="50" height="50" valign="top"><img src="sc-bulb.png" /></td>
        <td bgcolor="#555C9F" width="200" align="left" balign="left"><font color="#FFFFFF"><i>"%(modeling)s"</i></font></td>
        <td bgcolor="#555C9F" width="10"></td>
      </tr>'''



def stringtolines(s):
    words = s.split()
    l = 0
    n = ''
    for word in words:
        if len(word) + l >= 37:
            n = n + '<br/>'
            l = 0
        if l != 0:
            n = n + ' '
            l = l + 1
            
        n = n + word
        l = l + len(word)
    return n



short_format = False
if len(sys.argv) >= 2 and sys.argv[1] == '--short':
    short_format = True

chain_json = json.load(sys.stdin)

chain = {}
for atom in chain_json:
    if atom.has_key(KEY_REM):
        continue
        
    if not atom.has_key(KEY_ID):
        sys.stderr.write('atom missing id\n')
        sys.exit(-1)

    atom_id = atom[KEY_ID]

    if atom_id == '':
        sys.stderr.write('atom has blank id\n')
        sys.exit(-1)

    if chain.has_key(atom_id):
        sys.stderr.write('duplicate atom id: ' + atom_id + '\n')
        sys.exit(-1)

    if not atom.has_key(KEY_MODELING):
        sys.stderr.write('missing key: ' + KEY_MODELING + ' in ' + atom_id + '\n')
        sys.exit(-1)

    if atom.has_key(KEY_TITLE):
        if not atom.has_key(KEY_DEPS):
            sys.stderr.write('missing key: ' + KEY_DEPS + ' in ' + atom_id + '\n')
            sys.exit(-1)

        okay_props = KEY_PROPS_NEW + [KEY_TITLE, KEY_DEPS]

    else:
        okay_props = KEY_PROPS_PRE

    for key in atom:
        if key not in [KEY_ID, KEY_NOTES] + okay_props:
            sys.stderr.write('unrecognized key: ' + key + ' in ' + atom_id + '\n')
            sys.exit(-1)

    chain[atom_id] = atom

for atom_id, atom in chain.iteritems():
    if atom.has_key(KEY_DEPS):
        deps = atom[KEY_DEPS]
        for dep in deps:
            if not chain.has_key(dep):
                sys.stderr.write('missing dependency: ' + dep + '\n')
                sys.exit(-1)
    
sys.stdout.write('digraph G {\n')
sys.stdout.write('  graph [ rankdir="BT" outputorder="edgesfirst" ];\n')
sys.stdout.write('  node [ shape="none" width="0" height="0" margin="0" color="invis" fontname="sans" ];\n')
sys.stdout.write('  edge [ penwidth="3" dir="none" ];\n')

for atom_id in sorted(chain.keys()):
    atom = chain[atom_id]

    if atom.has_key(KEY_TITLE):
        sections = NODE_SECTION_NEW
        props = KEY_PROPS_NEW

    else:
        sections = NODE_SECTION_PRE
        props = KEY_PROPS_PRE

    fmt = ''
    fmt += NODE_HEADER

    for key in props:
        if atom.has_key(key):
            if not short_format or key in [KEY_TITLE, KEY_MODELING]:
                atom[key] = stringtolines(atom[key])
                fmt += sections[key]

    fmt += NODE_FOOTER

    sys.stdout.write(fmt % atom)

sys.stdout.write('\n')

for atom_id in sorted(chain.keys()):
    atom = chain[atom_id]

    if atom.has_key(KEY_DEPS):
        for dep in atom[KEY_DEPS]:
            sys.stdout.write('  %s -> %s;\n' % (atom_id, dep))

sys.stdout.write('}\n')
