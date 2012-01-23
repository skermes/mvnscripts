#! /usr/bin/python3

import xml.dom
import xml.dom.minidom
import out
import os
import os.path

def text(tag):
    return ''.join(node.data for node in tag.childNodes if node.nodeType == xml.dom.Node.TEXT_NODE)

def pmdViolations(reportFilename='target/site/pmd.xml'):
    report = xml.dom.minidom.parse(reportFilename)
    for srcFile in report.documentElement.getElementsByTagName('file'):
        for violation in srcFile.getElementsByTagName('violation'):
            yield srcFile.getAttribute('name'), int(violation.getAttribute('beginline')), text(violation).strip()

def runTarget(pmdFile='target/site/pmd.xml'):
    if os.path.exists(pmdFile):
        os.remove(pmdFile)
    os.system('mvn pmd:pmd')
    return os.path.exists(pmdFile)

if __name__ == '__main__':
    import sys

    if not runTarget():
        sys.exit()

    print()
    print()

    lastFile = ''
    noFailures = True
    for srcFile, line, message in pmdViolations():
        if srcFile != lastFile:
            out.printlns('', os.path.relpath(srcFile), '-' * 79)
            lastFile = srcFile

        line = str(line)
        print(out.red(line), '-', message)
        noFailures = False

    if noFailures:
        print(out.banner(out.green('PMD PASSED')))
