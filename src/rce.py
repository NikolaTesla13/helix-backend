from multiprocessing import set_start_method
from typing import List
import subprocess
import shlex
import time
import os


class RemoteCodeExecution:
    def __init__(self):
        self.tmp_dir = "tmp"
        self.src_file = "task"

        self.interpreters = {
            "cpp": [],
            "c": [],
            "py": ["python3"],
        }
        self.compiler = {"cpp": "g++", "c": "gcc", "py": ""}
        self.compiler_opts = {
            "cpp": ["-std=c++2a", "-O0"],
            "c": ["-std=c99", "-O0"],
            "py": [],
        }

        self.benchmark = True

    def compile(self, code: str, lang: str):
        start = time.time()

        src_file = self.src_file + "-" + str(int(time.time())) + "." + lang
        bin_file = src_file.replace("." + lang, ".bin")

        source = open(f"{self.tmp_dir}/{src_file}", "w")
        source.write(code)
        source.close()

        if self.compiler[lang] != "":
            cmd = [
                self.compiler[lang],
                *self.compiler_opts[lang],
                "-o",
                f"{self.tmp_dir}/{bin_file}",
                f"{self.tmp_dir}/{src_file}",
            ]
            proc = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False
            )
            _, error = proc.communicate()
        else:
            error = b""
            bin_file = src_file

        return {
            "files": [src_file, bin_file],
            "error": error.decode("utf-8"),
            "perf": time.time() - start,
        }

    def unsafe_execute_code(self, lang: str, code: str, input: str):
        comp_res = self.compile(code, lang)
        comp_perf = comp_res["perf"]
        if comp_res["error"]:
            return {
                "output": "",
                "error": comp_res["error"],
                "pers": {"runtime": "0 ms", "compilation": f"{comp_perf * 1000:.4} ms"},
            }

        if self.benchmark:
            start = time.time()

        src_file, bin_file = comp_res["files"]

        result = subprocess.run(
            [*self.interpreters[lang], f"{self.tmp_dir}/{bin_file}"],
            input=input.encode(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False,
        )

        try:
            os.remove(f"{self.tmp_dir}/{src_file}")
            os.remove(f"{self.tmp_dir}/{bin_file}")
        except:
            pass

        out = {
            "output": result.stdout.decode("utf-8"),
            "error": result.stderr.decode("utf-8"),
        }

        if self.benchmark:
            duration = time.time() - start
            out["perf"] = {
                "runtime": f"{duration * 1000:.4} ms",
                "compilation": f"{comp_perf * 1000:.4} ms",
            }

        return out

    # TODO: update this
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
