import subprocess
import os

class RemoteCodeExecution:
    def __init__(self):
        pass

    @staticmethod
    def execute_code(code, input):
        cwd = os.getcwd()
        tmp_dir = "tmp"

        docker_cmd = f'docker run --rm -i -v {cwd}/{tmp_dir}:/tmp gcc:latest /bin/bash << \'EOF\'\n' \
                     f'cd /tmp && cat > code.cpp << \'CODE\'\n' \
                     f'{code}\n' \
                     f'CODE\n' \
                     f'g++ -std=c++20 -O2 -o a.out code.cpp && echo "{input}" | ./a.out\n' \
                     f'EOF\n'

        result = subprocess.run(docker_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

        out = {
            "output": result.stdout.decode('utf-8'),
            "error": result.stderr.decode('utf-8')
        }

        return out
