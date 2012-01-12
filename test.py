#! /usr/bin/python3

import glob
import os.path
import xml.dom
import xml.dom.minidom
import out

FAILED = 'fail'
SKIPPED = 'skip'

def childNamed(node, targetName):
    for kid in node.childNodes:
        if kid.nodeType == xml.dom.Node.ELEMENT_NODE and kid.localName == targetName:
            return kid
    return None

def failure(testNode):
    return childNamed(testNode, 'failure')

def error(testNode):
    return childNamed(testNode, 'error')

def skipped(testNode):
    return childNamed(testNode, 'skipped')

def content(node):
    return ''.join(text.data for text in node.childNodes if text.nodeType == xml.dom.Node.TEXT_NODE)

def failedTests(reportFolder):
    prefixLen = len(reportFolder) + 1
    fixtures = [report[prefixLen:-4] for report in glob.glob(os.path.join(reportFolder, '*.txt'))]

    for fixture in fixtures:
        report = xml.dom.minidom.parse(os.path.join(reportFolder, 'TEST-' + fixture + '.xml'))
        for test in report.documentElement.getElementsByTagName('testcase'):
            fail = failure(test)
            if fail is not None:
                yield test.getAttribute('name'), fixture, FAILED, fail.getAttribute('message')

            err = error(test)
            if err is not None:
                yield test.getAttribute('name'), fixture, FAILED, '\n'.join(content(err).split('\n')[:2])

            skip = skipped(test)
            if skip is not None:
                yield test.getAttribute('name'), fixture, SKIPPED, None

if __name__ == '__main__':
    import os
    import shutil
    import sys

    reportDirectory = 'target/surefire-reports'
    # If the compile fails, we don't want to look at old test reports.
    if os.path.exists(reportDirectory):
        shutil.rmtree(reportDirectory)
    os.system('mvn test')
    if not os.path.exists(reportDirectory):
        sys.exit()

    print()
    print()

    lastFixture = ''
    noFailures = True
    putNewlineBefore = False
    for test, fixture, problem, cause in failedTests(reportDirectory):
        if fixture != lastFixture:
            out.printlns('', fixture, '-' * 79)
            lastFixture = fixture
            putNewlineBefore = False

        if problem == FAILED:
            if putNewlineBefore:
                print()
            out.printlns(out.red(test), cause, '')
            noFailures = False;
            putNewlineBefore = False
        elif problem == SKIPPED:
            print(out.yellow(test))
            putNewlineBefore = True

    if noFailures:
        out.printlns('', out.banner(out.green('ALL TESTS SUCCESSFUL')))
