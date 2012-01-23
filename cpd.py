#! /usr/bin/python3

import xml.dom
import xml.dom.minidom
import out
import os
import os.path

def dupmsg(duplication, fileone, filetwo):
    return ''.join([duplication.getAttribute('lines'),
                    ' lines of code duplicated with ',
                    os.path.basename(filetwo.getAttribute('path')),
                    ':',
                    filetwo.getAttribute('line')])

def duplications(reportFilename='target/site/cpd.xml'):
    report = xml.dom.minidom.parse(reportFilename)
    for duplication in report.documentElement.getElementsByTagName('duplication'):
        fileone = duplication.getElementsByTagName('file')[0]
        filetwo = duplication.getElementsByTagName('file')[1]
        yield fileone.getAttribute('path'), int(fileone.getAttribute('line')), dupmsg(duplication, fileone, filetwo)

def runTarget(cpdFile='target/site/cpd.xml'):
    if os.path.exists(cpdFile):
        os.remove(cpdFile)
    os.system('mvn pmd:cpd')
    return os.path.exists(cpdFile)

if __name__ == '__main__':
    import sys

    if not runTarget():
        sys.exit()

    print()
    print()

    lastFile = ''
    noDups = True
    for srcFile, line, message in duplications():
        if (srcFile != lastFile):
            out.printlns('', os.path.relpath(srcFile), '-' * 79)
            lastFile = srcFile

        line = str(line)
        print(out.red(line), '-', message)
        noDups = False

    if noDups:
        print(out.banner(out.green('NO DUPLICATE CODE')))
