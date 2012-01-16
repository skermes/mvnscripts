#! /usr/bin/python3

import xml.dom
import xml.dom.minidom
import out

def childrenNamed(node, targetName):
    return [kid for kid in node.childNodes if kid.nodeType == xml.dom.Node.ELEMENT_NODE and kid.localName == targetName]

def errors(fileNode):
    return childrenNamed(fileNode, 'error')

def checkstyleProblems(reportFilename):
    report = xml.dom.minidom.parse(reportFilename)
    for srcFile in report.documentElement.getElementsByTagName('file'):
        errs = errors(srcFile)
        if len(errs) > 0:
            for err in errs:
                yield srcFile.getAttribute('name'), err.getAttribute('line'), err.getAttribute('message')

if __name__ == '__main__':
    import os
    import os.path
    import sys

    checkstyleFile = 'target/checkstyle-result.xml'
    if os.path.exists(checkstyleFile):
        os.remove(checkstyleFile)
    os.system('mvn checkstyle:checkstyle')
    if not os.path.exists(checkstyleFile):
        sys.exit()

    print()
    print()

    lastFile = ''
    noFailures = True
    for srcFile, line, message in checkstyleProblems(checkstyleFile):
        if srcFile != lastFile:
            out.printlns('', os.path.relpath(srcFile), '-' * 79)
            lastFile = srcFile

        print(out.red(line), '-', message)
        noFailures = False

    if noFailures:
        print(out.banner(out.green('CHECKSTYLE PASSED')))
