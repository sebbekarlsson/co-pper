import argparse
from copper_client.parsers.PHPParser import PHPParser
import hashlib
import time
import os

parser = argparse.ArgumentParser()
PHPParser = PHPParser()

def watch():
    parser.add_argument('--file')
    parser.add_argument('--language')
    args = parser.parse_args()
    
    if args.language == '' or args.language == None:
        print('Please specify a --language')
        quit()

    try:
        while True:
            time.sleep(1)
            check = True
            ok = True

            if os.path.exists('{}.latest'.format(args.file)):
                latest_file = open('{}.latest'.format(args.file), 'rb')
                this_file = open(args.file, 'rb')
                latest_hash = hashlib.md5(latest_file.read()).hexdigest()
                this_hash = hashlib.md5(this_file.read()).hexdigest()
                latest_file.close()
                this_file.close()
            else:
                check = False
            

            if check:
                if latest_hash != this_hash:
                    print('Detected change in: {}'.format(args.file))
                    ok = True
                else:
                    ok = False
                
            if ok:
                if args.language == 'php':
                    PHPParser.parse(args.file)

    except KeyboardInterrupt:
        print('interrupted!')
