#! /usr/bin/python3

import glob
import os.path
import xml.dom
import xml.dom.minidom

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

def color(message, color):
    return '\033[' + color + 'm' + message + '\033[0m'

def red(message):
    return color(message, '0;31')

def green(message):
    return color(message, '0;32')

def yellow(message):
    return color(message, '0;33')

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
            print()
            print(fixture)
            print('-' * max(79, len(fixture)))
            lastFixture = fixture
            putNewlineBefore = False

        if problem == FAILED:
            if putNewlineBefore:
                print()
            print(red(test))
            print(cause)
            print()
            noFailures = False;
            putNewlineBefore = False
        elif problem == SKIPPED:
            print(yellow(test))
            putNewlineBefore = True

    if noFailures:
        msg = 'ALL TESTS SUCCESSFUL'
        print('-' * len(msg))
        print(green(msg))
        print('-' * len(msg))
