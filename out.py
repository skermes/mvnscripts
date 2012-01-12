def decorate(prefix, suffix, message):
    return prefix + message + suffix

def color(color, message):
    return decorate(decorate('\033[', 'm', color), '\033[0m', message)

def red(message):
    return color('0;31', message)

def yellow(message):
    return color('0;33', message)

def green(message):
    return color('0;32', message)

def banner(message, shellwidth=80):
    line = '-' * (shellwidth - 1)
    return decorate(line + '\n', line, message + '\n')

def printlns(*lines):
    print(*lines, sep='\n')
