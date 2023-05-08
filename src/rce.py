import subprocess
import os

class RemoteCodeExecution:
    def __init__(self):
        self.tmp_dir = "tmp"
        self.src_file = "code.cpp"

    def unsafe_execute_code(self, code, input):
        source = open(f'{self.tmp_dir}/{self.src_file}', 'w')
        source.write(code)
        source.close()

        cmd = f'g++ -std=c++2a -O2 -o ./{self.tmp_dir}/a.out ./{self.tmp_dir}/{self.src_file} && ./{self.tmp_dir}/a.out'

        result = subprocess.run(cmd, input=input.encode(),stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

        out = {
            "output": result.stdout.decode('utf-8'),
            "error": result.stderr.decode('utf-8')
        }

        return out

    def execute_code(self, code, input):
        cwd = os.getcwd()

        docker_cmd = f'docker run --rm -i -v {cwd}/{self.tmp_dir}:/tmp gcc:latest /bin/bash << \'EOF\'\n' \
                     f'cd /tmp && cat > code.cpp << \'CODE\'\n' \
                     f'{code}\n' \
                     f'CODE\n' \
                     f'g++ -std=c++20 -O2 -o a.out {self.src_file} && echo "{input}" | ./a.out\n' \
                     f'EOF\n'

        result = subprocess.run(docker_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

        out = {
            "output": result.stdout.decode('utf-8'),
            "error": result.stderr.decode('utf-8')
        }

        return out
