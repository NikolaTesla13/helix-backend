from typing import List
import subprocess
import shlex
import time
import os


class RemoteCodeExecution:
    def __init__(self):
        self.tmp_dir = "tmp"
        self.src_file = "task"

        self.cc = "g++"
        self.cc_opts = ["-std=c++2a", "-O0"]

    def compile(self, code: str) -> str:
        src_file = self.src_file + "-" + str(int(time.time())) + ".cpp"
        bin_file = src_file.replace(".cpp", ".bin")

        source_code = code.encode()

        subprocess.run(
            [
                self.cc,
                *self.cc_opts,
                "-o",
                f"{self.tmp_dir}/{bin_file}",
                "-x",
                "c++",
                "-",
            ],
            input=source_code,
            check=True,
        )

        return bin_file

    def unsafe_execute_code(self, code: str, input: str):
        bin_file = self.compile(code)

        result = subprocess.run(
            f"{self.tmp_dir}/{bin_file}",
            input=input.encode(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False,
        )

        os.remove(f"{self.tmp_dir}/{bin_file}")

        out = {
            "output": result.stdout.decode("utf-8"),
            "error": result.stderr.decode("utf-8"),
        }

        return out

    def unsafe_test_code(self, code: str, tests: List[dict]):
        source = open(f"{self.tmp_dir}/{self.src_file}", "w")
        source.write(code)
        source.close()

        cmd = f"{self.cc} {self.cc_opts} -o ./{self.tmp_dir}/{self.bin_file} ./{self.tmp_dir}/{self.src_file}"

        result = subprocess.run(
            shlex.split(cmd),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        if result.returncode != 0:
            return {
                "test_results": [0] * len(tests),
                "error": result.stderr.decode("utf-8"),
            }

        test_results = []
        bin_path = f"./{self.tmp_dir}/{self.bin_file}"
        for test in tests:
            result = subprocess.run(
                bin_path,
                input=str(test["input"]).encode(),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            if result.returncode != 0:
                return {
                    "test_results": [0] * len(tests),
                    "error": result.stderr.decode("utf-8"),
                }

            if result.stdout.decode("utf-8") == str(test["output"]):
                test_results.append(int(test["points"]))
            else:
                test_results.append(0)

        return {"test_results": test_results, "error": ""}

    def execute_code(self, code: str, input: str):
        cwd = os.getcwd()

        docker_cmd = (
            f"docker run --rm -i -v {cwd}/{self.tmp_dir}:/tmp gcc:latest /bin/bash << 'EOF'\n"
            f"cd /tmp && cat > code.cpp << 'CODE'\n"
            f"{code}\n"
            f"CODE\n"
            f'g++ -std=c++20 -O2 -o a.out {self.src_file} && echo "{input}" | ./a.out\n'
            f"EOF\n"
        )

        result = subprocess.run(
            docker_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
        )

        out = {
            "output": result.stdout.decode("utf-8"),
            "error": result.stderr.decode("utf-8"),
        }

        return out
