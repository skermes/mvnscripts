#! /usr/bin/python3

import xml.dom
import xml.dom.minidom
import out
import os
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

def bugsFound(reportFilename='target/findbugsXml.xml'):
    report = xml.dom.minidom.parse(reportFilename)
    srcdir = text(report.documentElement.getElementsByTagName('SrcDir')[0])
    for bug in report.documentElement.getElementsByTagName('BugInstance'):
        yield os.path.join(srcdir, fileName(bug)), int(lineNumber(bug)), message(bug)

def runTarget(findbugsFile='target/findbugsXml.xml'):
    if os.path.exists(findbugsFile):
        os.remove(findbugsFile)
    os.system('mvn findbugs:findbugs')
    return os.path.exists(findbugsFile)

if __name__ == '__main__':
    import sys

    if not runTarget():
        sys.exit()

    print()
    print()

    lastFile = ''
    noFailures = True
    for srcFile, line, msg in bugsFound():
        if srcFile != lastFile:
            out.printlns('', os.path.relpath(srcFile), '-' * 79)
            lastFile = srcFile

        line = str(line)
        print(out.red(line), '-', msg)
        noFailures = False

    if noFailures:
        print(out.banner(out.green('FIND BUGS PASSED')))
