#! /usr/bin/python3

import xml.dom
import xml.dom.minidom
import out
import os.path

def dupmsg(duplication, fileone, filetwo):
    return ''.join([duplication.getAttribute('lines'),
                    ' lines of code duplicated with ',
                    os.path.basename(filetwo.getAttribute('path')),
                    ':',
                    filetwo.getAttribute('line')])

def duplications(reportFilename):
    report = xml.dom.minidom.parse(reportFilename)
    for duplication in report.documentElement.getElementsByTagName('duplication'):
        fileone = duplication.getElementsByTagName('file')[0]
        filetwo = duplication.getElementsByTagName('file')[1]
        yield fileone.getAttribute('path'), fileone.getAttribute('line'), dupmsg(duplication, fileone, filetwo)

if __name__ == '__main__':
    import os
    import sys

    cpdFile = 'target/site/cpd.xml'
    if os.path.exists(cpdFile):
        os.remove(cpdFile)
    os.system('mvn pmd:cpd')
    if not os.path.exists(cpdFile):
        sys.exit()

    print()
    print()

    lastFile = ''
    noDups = True
    for srcFile, line, message in duplications(cpdFile):
        if (srcFile != lastFile):
            out.printlns('', os.path.relpath(srcFile), '-' * 79)
            lastFile = srcFile

        print(out.red(line), '-', message)
        noDups = False

    if noDups:
        print(out.banner(out.green('NO DUPLICATE CODE')))
