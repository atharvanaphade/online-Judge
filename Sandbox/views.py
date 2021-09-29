import os
import subprocess
import resource

TESTCASES_NO = 6

USERS_CODE = 'data/users_code/'
STANDARD = 'data/standard/'


def return_codes():
    codes = {
        0: 'AC',  # Correct ans

        1: 'CTE',  # compile time error
        127: 'CTE',

        159: 'AT',  # 31 SIGSYS
        135: 'AT',

        136: 'RTE',  # SIGFPE 
        139: 'RTE',  # Segmentation Error (sigsgev)

        137: 'TLE',

        'wa': 'WA',  # Wrong answer
    }

    return codes


def gaadi_wala_aya(user_question_path, logged_out=False):
    # Gaadi wale ko logout pe bulao

    if logged_out:
        items = ['temp.py', 'exe']
        for i in items:
            fp = user_question_path + i
            if os.path.exists(fp):
                os.system('rm ' + fp)
    else:
        for i in range(TESTCASES_NO):
            fp = user_question_path + 'output{}.txt'.format(i + 1)
            if os.path.exists(fp):
                os.system('rm ' + user_question_path + 'output{}.txt'.format(i + 1))


def check(user_output, expected_output):
    user_output = open(user_output)
    expected_output = open(expected_output)

    lines_user = user_output.readlines()
    l1 = [i.strip() for i in lines_user]
    lines_expected = expected_output.readlines()
    l2 = [i.strip() for i in lines_expected]
    flag = 0
    # print("User output", l1, "Expected output: ",l2)
    if len(l1) == len(l2):
        for i in range(len(l1)):  # check if files of equal length
            if l1[i] == l2[i]:
                flag = 1
            else:
                break
        if flag:
            return 0
        else:
            return 'wa'
    return 'wa'


def get_quota(question_number, test_case_number):
    quota_path = STANDARD + 'description/question{}/quota{}.txt'.format(question_number, test_case_number)
    quota_file = open(quota_path)

    lines = quota_file.readlines()
    time_limit = lines[0].strip()
    memory_limit = lines[1].strip()  # memory

    quota = {
        'time_limit': time_limit,
        'memory_limit': int(memory_limit),
    }

    return quota


def initialize_quota(quota, ext):
    time_limit = int(quota['time_limit'])
    memory_limit = int(quota['memory_limit'])
    # print("CPU time is: ", time_limit, "Memory limit is: ", memory_limit)
    if ext == 'py':
        time_limit = 3

    def setlimits():
        # print("SETTING LIMITS...")
        resource.setrlimit(resource.RLIMIT_CPU, (time_limit, time_limit))
        resource.setrlimit(resource.RLIMIT_AS, (memory_limit, memory_limit))

    return setlimits


def sandbox(exe_path, ext, input_file, output_file, error_file, quota):
    if ext == 'py':
        child = subprocess.Popen(
            ['python3 ' + exe_path], preexec_fn=initialize_quota(quota, ext),
            stdin=input_file, stdout=output_file, stderr=error_file, shell=True
        )
    else:
        child = subprocess.Popen(
            ['./' + exe_path], preexec_fn=initialize_quota(quota, ext),
            stdin=input_file, stdout=output_file, stderr=error_file, shell=True
        )

    child.wait()
    return_code = child.returncode

    if return_code < 0:
        return 128 - return_code
    else:
        return return_code


def run_test_case(test_case_number, user_question_path, code_file_path, ext, question_number):
    input_file_path = STANDARD + 'input/question{}/input{}.txt'.format(question_number, test_case_number)
    input_file = open(input_file_path, "r")  # STANDARD input

    user_output_file_path = user_question_path + 'output{}.txt'.format(test_case_number)
    output_file = open(user_output_file_path, "w+")

    quota = get_quota(question_number, test_case_number)

    error_file_path = user_question_path + "error.txt"
    error_file = open(error_file_path, 'w+')

    if ext == 'py':
        exe_path = code_file_path
    else:
        exe_path = user_question_path + 'exe'

    return_code = sandbox(
        exe_path,
        ext,
        input_file,
        output_file,
        error_file,
        quota
    )
    # process_code = subprocess.run('python3 ' + code_file_path, stdin = test_case_no, stdout = user_out_file)
    input_file.close()
    error_file.close()
    output_file.close()

    expected_output_file_path = STANDARD + 'output/question{}/expected_output{}.txt'.format(question_number,
                                                                                            test_case_number)

    if return_code == 0:
        result_value = check(user_output_file_path, expected_output_file_path)
        return result_value

    return return_code


def compile(user_question_path, code_file_path, err_file):
    lang = code_file_path.split('.')[1]
    if lang == 'c':
        rc = os.system(
            "gcc" + " -o " + user_question_path + 'exe ' + code_file_path + ' -lseccomp ' + '-lm 2>' + err_file)
    else:
        rc = os.system(
            "g++" + " -o " + user_question_path + 'exe ' + code_file_path + ' -lseccomp ' + '-lm 2>' + err_file)

    return rc  # return 0 for success and 1 for error


def user_ka_aukaat_check_kar(username, question_number, ext, attempts=None, run=False):
    user_question_path = USERS_CODE + '{}/question{}/'.format(username, question_number)

    if run:
        user_code_file_path = user_question_path + 'code.{}'.format(ext)

    else:
        user_code_file_path = user_question_path + 'code{}.{}'.format(attempts, ext)

    sandbox_file_py = 'data/include/sandbox.py'

    signals = return_codes()

    with open(user_question_path + 'temp.py', 'w+') as f:
        sand = open(sandbox_file_py, 'r')
        f.write(sand.read())
        sand.close()
        f.close()

    error_file = user_question_path + "error.txt"

    result = []

    if ext != 'py':
        # Compile only if c or cpp
        return_value = compile(user_question_path, user_code_file_path, error_file)  # calling compile()
        # print("compile", return_value)
        if return_value != 0:
            result = ["CTE"] * TESTCASES_NO
            # gaadi_wala_aya(user_question_path)
            return result

    if run:
        return_code = run_test_case(
            test_case_number=7,
            user_question_path=user_question_path,
            code_file_path=user_code_file_path,
            ext=ext,
            question_number=question_number
        )
        # print("pc", return_code)
        result.append(signals[return_code])

    else:
        for i in range(TESTCASES_NO):
            return_code = run_test_case(
                test_case_number=i + 1,
                user_question_path=user_question_path,
                code_file_path=user_code_file_path,
                ext=ext,
                question_number=question_number
            )

            # print("pc", return_code)
            result.append(signals[return_code])
            gaadi_wala_aya(user_question_path)

    return result