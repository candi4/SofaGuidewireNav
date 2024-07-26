# SofaGuidewireNav
Use [SOFA framework](https://github.com/sofa-framework/sofa) for guidewire navigation.


## Preparation
### 1. Install Anaconda
[Download](https://www.anaconda.com/download/success) and [install](https://docs.anaconda.com/free/anaconda/install/windows/) anaconda.    
### 2. Make virtual environment
Make virtual environment using anaconda with python version 3.8 and activate it.
```
conda create -n sofarl python=3.8
conda activate sofarl
```

### 3. Install SOFA framework
Download [SOFA_v23.06.00_Win64.zip](https://github.com/sofa-framework/sofa/releases/tag/v23.06.00).   
Then, extract the zip file into preferred directory.   

### 4. Define the environment variables
Follow `1.3.2. using python3` in [SofaPython3 Documentation](https://sofapython3.readthedocs.io/en/latest/content/Installation.html#using-python3). Here is the explanation for Windows user:   
- Right click **Start** button -> Click on the **System** -> Click on the **Advanced System Settings** -> Under the **Advanced** tab, click on the **Environment Variable** button -> Add new **System variables**
   - Variable: `SOFA_ROOT`, Value: \<SOFA-install-directory>
   - Variable: `PYTHONPATH`, Value: %SOFA_ROOT%\plugins\SofaPython3\lib\python3\site-packages   

For Ubuntu user:    
* Add two lines to bashrc file
   ```
   gedit ~/.bashrc
   ```
   ```
   export SOFA_ROOT=/path/to/SOFA_install
   export PYTHONPATH=/path/to/SofaPython3/lib/python3/site-packages:$PYTHONPATH
   ```
   ```
   source ~/.bashrc
   ```

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


## Installation
Install this repo as a Python package.
```
pip install git+https://github.com/candi4/SofaGuidewireNav.git
```
* If using Ubuntu server, install headless version opencv.
   ```
   pip uninstall opencv-python -y
   pip install opencv-python-headless
   ```
* Verify installation
   ```
   # In python
   import SofaGW
   SofaGW.test_installation()
   ```
   You can see the simulation screen   
 <img src="readme_files/example.gif">

## How to use   
1. Imports the module.   
   ```
   from SofaGW import SimController
   ```
2. Creates an object `sim` using the class `SimController`.
   ```
   sim = SimController(timeout=10,
                        vessel_filename='vessel/phantom.obj')
   ```
3. Use `sim.action`, `sim.step`, `sim.GetImage`, and `sim.reset`.  
   * `sim.action`: Moves the guidewire in the simulation.   
   * `sim.step`: Calculates dynamics in the simulation for one step.   
   * `GetImage`: Takes a picture of the simulation.      
   * `sim.reset`: Resets the simulation to its initial state. 
   * `sim.close`: Closes the simulation.    
- You can refer [example_module.py](example.py).   


## TODO
* Add parameter for controling youngModulus and youngModulusExtremity of GW