PHASES = ['before_install', 'install', 'after_install', 'before_script', 'script', 'after_script',
          'after_deploy', 'before_deploy', 'after_failure', 'after_success']

valid_top_level_keys = [
    "addons",
    "android",
    "apt_packages",
    "brew_packages",
    "bundler_args",
    "compiler",
    "cran",
    "d",
    "dart",
    "deploy",
    "dist",
    "dotnet",
    "elixir",
    "env",
    "gemfile",
    "ghc",
    "git",
    "go",
    "haxe",
    "jdk",
    "julia",
    "language",
    "lein",
    "matrix",
    "mono",
    "node",
    "node_js",
    "nodejs",
    "os",
    "osx_image",
    "otp_release",
    "perl",
    "php",
    "podfile",
    "python",
    "r",
    "r_binary_packages",
    "r_build_args",
    "r_check_args",
    "r_github_packages",
    "r_packages",
    "repos",
    "ruby",
    "rust",
    "rvm",
    "sbt_args",
    "scala",
    "services",
    "smalltalk",
    "solution",
    "sudo",
    "virtualenv",
    "warnings_are_errors",
    "with_content_shell",
    "xcode_scheme",
    "xcode_sdk",
    "xcode_workspace",
    "xcode_project"]
#
# def get_category_alt(command):
#     if command in ['mv', 'cp', 'mkdir', 'touch', 'rm', 'ln']:
#         return ("fs")
#     elif command.endswith('.js') or command.endswith('.rb') or command.endswith('.py') or command.endswith(
#             '.coffee') or command in  command in ['python', 'ruby', 'node']:
#         return ("interpreter")
#     elif command.endswith('.sh') or command.endswith('.bash'):
#         return ("x_scripts")
#     elif command.endswith('ake') or command in ['gulp', 'grunt', 'mvn', 'webpack', 'brunch', 'freight']:
#         return ("builders")
#     elif command in ['pip', 'npm', 'gem', 'bower', 'jspm', 'tsd', 'composer', 'bundler', 'bundle']:
#         return ("pkg_mgr")
#     elif command in ['git', 'hg']:
#         return ("vcs")
#     elif 'vfb' in command or command in ['google-chrome', 'chromium-browser', 'phantomjs', 'casperjs',
#                                          'selenium-standalone', 'webdriver-manager']:
#         return ("browser_env")
#     elif command.startswith('mongo') or command.endswith('db') or command.endswith('sql') or command in ['cassandra',
#                                                                                                          'cqlsh',
#                                                                                                          'neo4j',
#                                                                                                          'elasticsearch',
#                                                                                                          'memcached',
#                                                                                                          'redis-server']:
#         return ("storage")
#     else:
#         return ("other")



def get_category(command):
    if command.endswith('.js') or command.endswith('.sh') or command.endswith('.py') or command.endswith(
            '.coffee') or command.endswith('.bash'):
        return ("x_scripts")
    elif command.startswith('$') or command in ['[', ']', '{', '}', 'yes', 'true']:
        return ("unrelated")
    elif command.startswith('mongo') or command.endswith('db') or command.endswith('sql') or command in ['cassandra',
                                                                                                         'cqlsh',
                                                                                                         'firebase',
                                                                                                         'neo4j',
                                                                                                         'elasticsearch',
                                                                                                         'memcached',
                                                                                                         'redis-server']:
        return ("storage")
    elif command.endswith('ake') or command in ['gulp', 'grunt', 'mvn', 'webpack', 'brunch', 'freight']:
        return ("builders")
    elif command in ['pip', 'pip3', 'npm', 'pnpm', 'brew', 'yarn', 'gem', 'bower', 'jspm', 'tsd', 'composer', 'bundler', 'bundle']:
        return ("pkg_mgr")
    elif command in ['git', 'hg']:
        return ("vcs")
    elif 'vfb' in command or command in ['google-chrome', 'chromium-browser', 'phantomjs', 'casperjs',
                                         'selenium-standalone', 'webdriver-manager']:
        return ("browser_env")
    elif command in ['node', 'ruby', 'python3','python', 'java', 'bash', 'sh']:
        return ("interpreter")
    elif command in ['wget', 'curl']:
        return ("internet")
    elif command in ['pwd', 'echo', 'cd', 'printf', 'ls', 'cat', 'popd', 'pushd', 'top', 'head', 'du', 'df', 'tee',
                     'lsb_release', 'lsb-release', 'ps', 'uname', 'date', 'which']:
        return ("not_mutate")
    elif command in ['mv', 'cp', 'mkdir', 'touch', 'rm', 'ln']:
        return ("fs")
    elif command in ['sed', 'awk', 'cut', 'grep', 'egrep','sort', 'wc', 'tr']:
        return ("text_manipulate")
    elif command in ['rvm', 'nvm']:
        return ("version_mgr")
    elif command.startswith('dpkg') or 'apt-' in command or command in ['update-alternatives']:
        return ("pkg_installers")
    elif command in ['service', 'forever', 'start-stop-daemon']:
        return ("daemon_runner")
    elif command in ['nohup', 'source']:
        return ("execute_script")
    elif command in ['hexo', 'meteor', 'jekyll', 'ember']:
        return ("web_framework")
    elif command in ['cordova', 'ionic', 'android', 'titanium']:
        return ("mobile_framework")
    elif command in ['mocha', 'jasmine-node', 'karma', 'protractor', 'phpunit', 'wct']:
        return ("test_framework")
    elif command in ['emsdk', 'coffee', 'tsc']:
        return ("transpiler")
    elif command in ['g++']:
        return ("compiler")
    elif command.endswith('zip') or command in ['tar']:
        return ("compress")
    elif command.startswith('codeclimate') or command in ['istanbul', 'codecov', 'coveralls', 'jscover']:
        return ("code_coverage")
    elif command in ['jshint', 'tslint', 'eslint', 'scss-lint']:
        return ("linting")
    elif command in ['lsc', 'pm2', 'nsp']:
        return ("other_node_modules")
    elif command.startswith('ssh-') or command in ['openssl', 'chown', 'chmod', 'su']:
        return ("security")
    elif command.startswith('docker') or command.startswith('pyvenv'):
        return ("env_setup")
    elif command in ['netstat', 'iptables', 'nc' ]:
        return ("network")
    elif command in ['exit', 'export', 'screen', 'set', 'sleep', 'base64']:
        return ("other_unix")
    elif command.endswith('kill'):
        return ("process_kill")
    else:
        return ("other")
