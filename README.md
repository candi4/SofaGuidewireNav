# SOFA_RL
Use SOFA framework for Reinforcement Learning

## Preparation
### 1. Install Anaconda
[Download](https://www.anaconda.com/download/success) and [install](https://docs.anaconda.com/free/anaconda/install/windows/) anaconda. I recommend referring to google.   
From now on, when using python or anaconda (conda), use `Anaconda Prompt`.
### 2. Make virtual environment
Make virtual environment using anaconda with python version 3.8.
```
conda create -n sofarl python=3.8
conda activate sofarl
```

### 3. Install SOFA framework
Download ~~[SOFA v23.12.01 (.zip)](https://www.sofa-framework.org/download/)~~  [SOFA_v23.06.00_Win64.zip](https://github.com/sofa-framework/sofa/releases).   
Then, extract the zip file into preferred directory.   

### 4. Define the environment variables
Follow `1.3.2. using python3` in [SofaPython3 Documentation](https://sofapython3.readthedocs.io/en/latest/content/Installation.html#setup-your-environment). Here is the Korean explanation:   
- 시작 버튼 우클릭 -> '시스템' 클릭 -> '고급 시스템 설정' 클릭 -> '고급' 탭에서 '환경 변수' 버튼 클릭 -> 시스템 변수 새로 만들기
   - 변수 이름: `SOFA_ROOT`, 변수 값: SOFA 디렉토리
   - 변수 이름: `PYTHONPATH`, 변수 값: SOFA 디렉토리에서 plugins\SofaPython3\lib\python3\site-packages   

### 5. Test SOFA
After that, you can use `SofaPython3` within your virtual environment.   
Try the following command at `Anaconda Prompt`.
```
(sofarl) C:\Users\user>python
Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)] :: Anaconda, Inc. on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> import Sofa
---------------------------------------
Checking SOFA_ROOT and SOFAPYTHON3_ROOT
Using environment variable SOFA_ROOT: C:\Users\user\SOFA_v23.06.00_Win64
Warning: environment variable SOFAPYTHON3_ROOT is empty. Trying to guess it.
Guessed SOFAPYTHON3_ROOT: C:\Users\user\SOFA_v23.06.00_Win64\plugins\SofaPython3
Found Sofa.Helper.dll in C:\Users\user\SOFA_v23.06.00_Win64\bin
Found SofaPython3.dll in C:\Users\user\SOFA_v23.06.00_Win64\plugins\SofaPython3\bin
---------------------------------------
>>>
```
If the output appears as shown above, you can use SOFA via python.


### 6. Install requirements
Navigate to the SOFA directory, activate your virtual environment, and enter the following command.
```
pip install -r requirements.txt # In SOFA_RL directory, Within vitual environment
```
Then, the python modules listed in `requirements.txt` will be installed in your virtual environment.

### 7. Recommended installations
Other things to install for convenience   
- [Visual Studio Code (vscode)](https://code.visualstudio.com/): Convinent tool for editing codes. Additionally, install the `Python` extension in vscode for a python programming interface.

## 