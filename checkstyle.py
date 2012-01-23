#! /usr/bin/python3

import xml.dom
import xml.dom.minidom
import out
import os
import os.path

def childrenNamed(node, targetName):
    return [kid for kid in node.childNodes if kid.nodeType == xml.dom.Node.ELEMENT_NODE and kid.localName == targetName]

def errors(fileNode):
    return childrenNamed(fileNode, 'error')

def checkstyleProblems(reportFilename='target/checkstyle-result.xml'):
    report = xml.dom.minidom.parse(reportFilename)
    for srcFile in report.documentElement.getElementsByTagName('file'):
        errs = errors(srcFile)
        if len(errs) > 0:
            for err in errs:
                yield srcFile.getAttribute('name'), int(err.getAttribute('line')), err.getAttribute('message')

def runTarget(checkstyleFile='target/checkstyle-result.xml'):
    if os.path.exists(checkstyleFile):
        os.remove(checkstyleFile)
    os.system('mvn checkstyle:checkstyle')
    return os.path.exists(checkstyleFile)

if __name__ == '__main__':
    import sys

    if not runTarget():
        sys.exit()

    print()
    print()

    lastFile = ''
    noFailures = True
    for srcFile, line, message in checkstyleProblems():
        if srcFile != lastFile:
            out.printlns('', os.path.relpath(srcFile), '-' * 79)
            lastFile = srcFile

        line = str(line)
        print(out.red(line), '-', message)
        noFailures = False

    if noFailures:
        print(out.banner(out.green('CHECKSTYLE PASSED')))
