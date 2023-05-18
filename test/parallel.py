from multiprocessing import Process
import http.client
import json

conn = http.client.HTTPConnection("localhost", 4000)
headersList = {"Accept": "*/*", "Content-Type": "application/json"}


def test_solution(index):
    print(f"solution  #{index} started")

    payload = json.dumps(
        {
            "tests": [
                {"input": "2", "output": "1", "points": "10"},
                {"input": "4", "output": "1", "points": "10"},
                {"input": "5", "output": "0", "points": "10"},
                {"input": "7", "output": "0", "points": "10"},
            ],
            "lang": "cpp",
            "code": "#include <iostream>\nint main() {\n\tint n;\n\tstd::cin >> n;\n\tstd::cout << (!(n%2));\n}",
        }
    )

    conn.request("POST", "/rce/test?unsafe=true", payload, headersList)
    response = conn.getresponse()

    print(f"solution  #{index} finished")


if __name__ == "__main__":
    is_parallel = True
    tests = 10

    if is_parallel:
        procs = []

        for i in range(0, tests):
            proc = Process(target=test_solution, args=(i,))
            procs.append(proc)
            proc.start()

        for proc in procs:
            proc.join()
    else:
        for i in range(0, tests):
            test_solution(i)
