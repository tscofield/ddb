import os
import sys


# Default mode is cython
standalone_script=None

# to run test with single file script
# EXPORT ddb_exe_type=script

if 'ddb_exe_type' in os.environ:
    if os.environ['ddb_exe_type'].lower()=='script':
        standalone_script=True
    else:
        standalone_script=None  


if standalone_script==True:
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..','builds')))

    try:
        from standalone import ddb
    except Exception as ex:
        print ex
        exit(1)
    print ("DDB STANDALONE")
else:
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

    try:
        from source import ddb
    except Exception as ex:
        print ex
        exit(1)
    print ("DDB CYTHON")
