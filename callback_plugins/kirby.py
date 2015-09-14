
import ansible.utils  # unused, but necessary to avoid circular imports
from ansible.callbacks import display
import ConfigParser
import os
import re
import subprocess

version = '0.1.0'


class CallbackModule(object):
    """Plugin for analyzing task coverage"""

    def __init__(self):
        config_file = os.environ.get('KIRBY_CONFIG', None)
        if config_file is None:
            config_file = os.getcwd() + '/kirby.cfg'

        self.setting_manager = SettingManager(config_file)

        if self.setting_manager.enable and not self._check_options():
            display('[kirby] disable kirby...', stderr=True)
            self.setting_manager.enable = False

        if self.setting_manager.enable:
            self.runner = ServerspecRunner(self.setting_manager.serverspec_dir,
                                           self.setting_manager.serverspec_cmd)

            self.num_changed_tasks = 0
            self.num_tested_tasks = 0
            self.not_tested_tasks = []

    def _check_options(self):
        manager = self.setting_manager
        if not hasattr(manager, 'serverspec_dir') or manager.serverspec_dir is None:
            display("[kirby] 'serverspec_dir' is not correctly defined")
            return False

        if not hasattr(manager, 'serverspec_cmd') or manager.serverspec_cmd is None:
            display("[kirby] 'serverspec_cmd' is not correctly defined")
            return False

        return True

    def playbook_on_start(self):
        if self.setting_manager.enable:
            result = self.runner.run()

            if result is None:
                display('[kirby] serverspec\'s settings are invalid...disable kirby', stderr=True)
                self.setting_manager.enable = False
                return

            self.num_tests = result[0]
            self.num_failed_tests = result[1]
            self.failed_tests = result[2]
            self.dirty = False

    def playbook_on_setup(self):
        self.playbook_on_task_start('setup', False)

    def playbook_on_task_start(self, name, is_conditional):
        if self.setting_manager.enable:
            self.curr_task_name = name

            if self.dirty and 'coverage_skip' not in self.curr_task_name:
                self._clean()

    def runner_on_ok(self, host, res):
        if self.setting_manager.enable:
            if 'changed' in res and res['changed']:
                if 'coverage_skip' in self.curr_task_name:
                    self.dirty = True
                    return

                result = self.runner.run()
                prev_num_failed_tests = self.num_failed_tests
                prev_failed_tests = self.failed_tests
                self.num_tests = result[0]
                self.num_failed_tests = result[1]
                self.failed_tests = result[2]

                diff = set(prev_failed_tests) - set(self.failed_tests)
                display('tested by: ', color='yellow')
                for new_passed_test in diff:
                    display('- %s' % new_passed_test, color='yellow')

                self.num_changed_tasks += 1
                if self.num_failed_tests < prev_num_failed_tests:
                    self.num_tested_tasks += 1
                else:
                    self.not_tested_tasks += [self.curr_task_name]

    def playbook_on_stats(self, stats):
        if self.setting_manager.enable:
            if self.dirty:
                self._clean()

            display('*** Kirby Results ***')

            if self.num_changed_tasks > 0:
                coverage = self.num_tested_tasks * 100.0 / self.num_changed_tasks
            else:
                coverage = 0.0
            display('Coverage  : %.0f%% (%d of %d tasks are tested)' % (coverage, self.num_tested_tasks, self.num_changed_tasks))

            if self.num_tested_tasks < self.num_changed_tasks:
                display('Not tested:')
                for task_name in self.not_tested_tasks:
                    display(' - %s' % (task_name))

            if self.num_failed_tests != 0:
                display('')
                display('WARNING: serverspec still detects %d failures' % (self.num_failed_tests))

            display('*** Kirby End *******')

    def _clean(self):
        result = self.runner.run()

        self.num_tests = result[0]
        self.num_failed_tests = result[1]
        self.failed_tests = result[2]

        self.dirty = False


class SettingManager(object):
    def __init__(self, setting_file=None):
        self.parser = ConfigParser.SafeConfigParser()
        if setting_file is not None:
            self.parser.read(setting_file)

        self.enable = self._mk_boolean(self._get_config('defaults', 'enable', 'KIRBY_ENABLE', 'false'))
        self.serverspec_dir = self._get_config('defaults', 'serverspec_dir', 'KIRBY_SERVERSPEC_DIR', None)
        self.serverspec_cmd = self._get_config('defaults', 'serverspec_cmd', 'KIRBY_SERVERSPEC_CMD', None)

    def _get_config(self, section, option, env_var, default):
        value = os.environ.get(env_var, None)
        if value is not None:
            return value

        try:
            value = self.parser.get(section, option)
        except (ConfigParser.NoOptionError, ConfigParser.NoSectionError):
            # use default value
            pass
        if value is not None:
            return value

        return default

    def _mk_boolean(self, value):
        if value is None:
            return False

        val = str(value)
        if val.lower() in ["true", "t", "y", "1", "yes"]:
            return True
        else:
            return False


class ServerspecRunner(object):
    """Run serverspec command and retrieve its results"""
    num_tests_pattern = re.compile(r'(\d+) examples?, (\d+) failures?')
    failed_tests_pattern = re.compile(r'^(rspec .*)$', re.MULTILINE)

    def __init__(self, serverspec_dir, serverspec_cmd):
        self.serverspec_dir = serverspec_dir
        self.serverspec_cmd = serverspec_cmd

    def run(self):
        orig_dir = os.getcwd()
        if self.serverspec_dir is None or not os.path.isdir(self.serverspec_dir):
            return None

        os.chdir(self.serverspec_dir)

        try:
            cmd_result = subprocess.check_output(self.serverspec_cmd, shell=True, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as ex:
            cmd_result = ex.output

        os.chdir(orig_dir)

        # When use serverspec with parallel_tests, the result matches several times.
        # We need only the last one.
        match_result = None
        for match_result in ServerspecRunner.num_tests_pattern.finditer(cmd_result):
            pass
        if match_result is None:
            return None

        num_test = int(match_result.group(1))
        num_failed_test = int(match_result.group(2))

        failed_tests = []
        for match_result in ServerspecRunner.failed_tests_pattern.finditer(cmd_result):
            failed_tests += [match_result.group()]

        return (num_test, num_failed_test, failed_tests)
