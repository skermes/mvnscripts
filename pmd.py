#! /usr/bin/python3

import xml.dom
import xml.dom.minidom
import out

def text(tag):
    return ''.join(node.data for node in tag.childNodes if node.nodeType == xml.dom.Node.TEXT_NODE)

def pmdViolations(reportFilename):
    report = xml.dom.minidom.parse(reportFilename)
    for srcFile in report.documentElement.getElementsByTagName('file'):
        for violation in srcFile.getElementsByTagName('violation'):
            yield srcFile.getAttribute('name'), violation.getAttribute('beginline'), text(violation)

if __name__ == '__main__':
    import os
    import os.path
    import sys

    pmdFile = 'target/site/pmd.xml'
    if os.path.exists(pmdFile):
        os.remove(pmdFile)
    os.system('mvn pmd:pmd')
    if not os.path.exists(pmdFile):
        sys.exit()

    print()
    print()

    lastFile = ''
    noFailures = True
    for srcFile, line, message in pmdViolations(pmdFile):
        if srcFile != lastFile:
            out.printlns('', os.path.relpath(srcFile), '-' * 79)
            lastFile = srcFile

        print(out.red(line), '-', message.strip())
        noFailures = False

    if noFailures:
        print(out.banner(out.green('PMD PASSED')))
