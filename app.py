from splinter import Browser
browser = Browser('chrome')
browser.driver.fullscreen_window()


def visit(url):
    browser.visit(url)


def get_element(elm_id=None, elm_name=None):
    if elm_id:
        return browser.find_by_id(elm_id)
    return browser.find_by_name(elm_name)


def get_element_by_name(name):
    return browser.find_by_name(name)


def get_element_by_selector(selector):
    return browser.find_by(selector=selector)


def get_element_by_class(elm_class):
    elm_class = elm_class if elm_class.startswith('.') else '.' + elm_class
    # browser.is_element_visible_by_css('', wait_time=3)
    return browser.find_by_css(elm_class)


def get_element_by_id(elm_id):
    return browser.find_by_id(elm_id)

def set_value(elm, value):
    elm.fill(value)


def click(elm):
    elm.click()


def get_attribute_from_element(elm, attr):
    return elm[attr]


def wait_for_page_load():
    pass


def assert_page_contains(value):
    if value not in browser.html:
        raise AssertionError("%s is not in content" % value)


def assert_method_returns(label, value):
    method = methods.get(label)
    res = method()
    if res != value:
        raise AssertionError('%s method did not return %s (instead it returned %s)' % (label, value, res))


def get_element(find_type, value):
    if find_type == 'name':
        return get_element_by_name(value)
    elif find_type == 'class':
        return get_element_by_class(value)
    elif find_type == 'id':
        return get_element_by_id(value)
    return None


def run_line(line):
    cmds = line.split(' ')
    cmd = cmds[0]
    if cmd == 'visit':
        visit(cmds[1])
    elif cmd == 'click':
        get_element(cmds[1], cmds[2]).click()
    elif cmd == 'fill':
        elm = get_element(cmds[1], cmds[2])
        set_value(elm, ''.join(cmds[3:]))
    elif cmd == 'assert':
        # TODO define assertions somewhere
        assertion_type = cmds[1]
        if assertion_type == 'html_contains':
            assert_page_contains(' '.join(cmds[2:]))
        elif assertion_type == 'method_returns':
            assert_method_returns(cmds[2], ' '.join(cmds[3:]))

    else:
        print('nope')


methods = {}


def setup_method(line):
    cmds = line.split(' ')
    label = cmds[0]
    # TODO security :) and performance, find first space etc
    method = None
    ldict = locals()
    exec(' '.join(cmds[1:]) + ' as method', globals(), ldict)
    methods[label] = ldict['method']


def run_file(file_path):
    setting_up_methods = False
    with open(file_path) as f:
        for line in f.readlines():
            if line:
                line = line.strip()
                if not line:
                    continue
                if line.startswith('['):
                    scenario_name = line[1:-1]
                    print('Running scenario %s' % scenario_name)
                    setting_up_methods = scenario_name == 'Method_Definitions'
                elif setting_up_methods:
                    setup_method(line)
                else:
                    run_line(line)
    print('Done')

if __name__ == '__main__':
    try:
        run_file('sample_input.sg')
    finally:
        import time
        time.sleep(5)
        browser.quit()
