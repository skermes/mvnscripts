#! /usr/bin/python3

import xml.dom
import xml.dom.minidom
import out
import os.path

def text(tag):
    return ''.join(node.data for node in tag.childNodes if node.nodeType == xml.dom.Node.TEXT_NODE);

def fileName(bug):
    for kid in bug.childNodes:
        if kid.nodeType == xml.dom.Node.ELEMENT_NODE and kid.localName == 'SourceLine':
            return kid.getAttribute('sourcepath')

def lineNumber(bug):
    for kid in bug.childNodes:
        if kid.nodeType == xml.dom.Node.ELEMENT_NODE and kid.localName == 'SourceLine':
            return kid.getAttribute('start')

def message(bug):
    msg = text(bug.getElementsByTagName('LongMessage')[0])
    return msg[:msg.rfind(' in ')]

def bugsFound(reportFilename):
    report = xml.dom.minidom.parse(reportFilename)
    srcdir = text(report.documentElement.getElementsByTagName('SrcDir')[0])
    for bug in report.documentElement.getElementsByTagName('BugInstance'):
        yield os.path.join(srcdir, fileName(bug)), lineNumber(bug), message(bug)

if __name__ == '__main__':
    import os
    import sys

    findbugsFile = 'target/findbugsXml.xml'
    if os.path.exists(findbugsFile):
        os.remove(findbugsFile)
    os.system('mvn findbugs:findbugs')
    if not os.path.exists(findbugsFile):
        sys.exit()

    print()
    print()

    lastFile = ''
    noFailures = True
    for srcFile, line, msg in bugsFound(findbugsFile):
        if srcFile != lastFile:
            out.printlns('', os.path.relpath(srcFile), '-' * 79)
            lastFile = srcFile

        print(out.red(line), '-', msg)
        noFailures = False

    if noFailures:
        print(out.banner(out.green('FIND BUGS PASSED')))
