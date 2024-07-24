# SofaGuidewireNav
Use [SOFA framework](https://github.com/sofa-framework/sofa) for guidewire navigation.


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
The First line creates the virtual environment. The second line activates the virtual environment.   
From now on, when using python, activate the virtual environment `sofarl` and type `python <file-name>`.

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

### 6. Clone this repository
Navigate to preferred directory and clone this repository.
```
git clone https://github.com/candi4/SofaGuidewireNav.git
```
Or download and unzip the repository.   
   1. Navigate to the [main page of the repository](https://github.com/candi4/SofaGuidewireNav). 
   2. Above the list of files, click `<> Code`. 
   3. Click `Download ZIP`. 
   4. Move the zip file to preferred directory and unzip. 

### 7. Install requirements
Navigate to the SofaGuidewireNav directory, activate your virtual environment, and enter the following command.
```
pip install -r requirements.txt
```
Then, the python modules listed in `requirements.txt` will be installed in your virtual environment.    
* If using Ubuntu server, install headless version opencv.
   ```
   pip uninstall opencv-python -y
   pip install opencv-python-headless
   ```

### 8. Recommended installations
Other things to install for convenience   
- [Visual Studio Code (vscode)](https://code.visualstudio.com/): Convinent tool for editing codes. Additionally, install the `Python` extension in vscode for a python programming interface.

## How to use   
### Option 1. In the repository   
1. Make your own python code into the directory \<SofaGuidewireNav>.   
   * You only need to use four methods: `action`, `step`, `GetImage`, `reset`.
      * `action`: Moves the guidewire in the simulation.   
      * `step`: Calculates dynamics in the simulation for one step.   
      * `GetImage`: Takes a picture of the simulation.      
      * `reset`: Resets the simulation to its initial state. 
      * `close`: Closes the simulation.   
2. Run your code. 
   ```
   python <your_python_file>
   ```   
- You can refer [example_basic.py](example_basic.py).   
   * First, import the module.   
      ```
      from SofaGW.simulation.SimServer import SimController
      ```
   * Second, create an object `sim` using the class `SimController`.
      ```
      sim = SimController(timeout=10,
                          vessel_filename='vessel/phantom.obj')
      ```
   * Third, during the loop, use `sim.action`, `sim.step`, `sim.GetImage`, and `sim.reset`.   
      ```
      for i in range(500):
         ...

      sim.close()
      ```
 - You can see the simulation screen while running [example_basic.py](example_basic.py) by running `python example_basic.py` within your conda virtual environment `sofarl`.   
 <img src="readme_files/example.gif">

### Option 2. As an installed package
1. Move `%SofaGuidewireNav%\SofaGW` into the directory `%anaconda3%\envs\sofarl\Lib\site-packages` or `%anaconda3%\envs\sofarl\lib\python3.8\site-packages`.
2. Make your own python code into any preferred directory.
   * You only need to use four methods: `action`, `step`, `GetImage`, `reset`.
      * `action`: Moves the guidewire in the simulation.   
      * `step`: Calculates dynamics in the simulation for one step.   
      * `GetImage`: Takes a picture of the simulation.      
      * `reset`: Resets the simulation to its initial state. 
      * `close`: Closes the simulation.   
    * Additionally, You have to make sure the parameter `vessel_filename` of `SimController` points the correct directory.
3. Run your code. 
   ```
   python <your_python_file>
   ```   
- You can refer [example_module.py](example_module.py).   
   * First, import the module.   
      ```
      from SofaGW import SimController
      ```
   * Second, create an object `sim` using the class `SimController`.
      ```
      sim = SimController(timeout=10,
                          vessel_filename='vessel/phantom.obj')
      ```
   * Third, during the loop, use `sim.action`, `sim.step`, `sim.GetImage`, and `sim.reset`.   
      ```
      for i in range(500):
         ...

      sim.close()
      ```
 - You can see the simulation screen while running [example_module.py](example_module.py) by running `python example_module.py` within your conda virtual environment `sofarl`.   
 <img src="readme_files/example.gif">


## Task
**Task:** Create an RL model that controls the guidewire to target a specific exit.   
You can use python modules for RL, such as [Stable-Baselines3](https://stable-baselines3.readthedocs.io/en/master/).
