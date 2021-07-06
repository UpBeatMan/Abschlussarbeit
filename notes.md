gh repo clone UpBeatMan/Abschlussarbeit

Forensics Software Thesis

Follow the master plan
and free your mind! (:

- [x] Kali einsatzbereit machen
- [x] Milestones Transfer
- [x] Arbeitsgeschwindigkeit erhöhen

To use ResultVisualization.ipynb with the Jupyter Notebook let Visual Studio Code install `ipykernel`.

```
Windows PowerShell
Copyright (C) Microsoft Corporation. All rights reserved.

Try the new cross-platform PowerShell https://aka.ms/pscore6

Loading personal and system profiles took 1514ms.
(base) PS C:\Users\<username>\Abschlussarbeit> conda activate dfsc-env
(dfsc-env) PS C:\Users\<username>\Abschlussarbeit> & C:/Users/<username>/.conda/envs/dfsc-env/python.exe c:\Users\<username>\.vscode\extensions\ms-python.python-2021.6.944021595\pythonFiles\shell_exec.py conda install --name dfsc-env ipykernel -y C:/Users/<username>/AppData/Local/Temp/tmp-1495210vS6CZPKYhI.log
Executing command in shell >> conda install --name dfsc-env ipykernel -y
Collecting package metadata (current_repodata.json): done
Solving environment: failed with initial frozen solve. Retrying with flexible solve.
Solving environment: failed with repodata from current_repodata.json, will retry with next repodata source.
Collecting package metadata (repodata.json): done
Solving environment: done

## Package Plan ##

  environment location: C:\Users\<username>\.conda\envs\dfsc-env

  added / updated specs:
    - ipykernel


The following packages will be downloaded:

    package                    |            build
    ---------------------------|-----------------
    ipykernel-5.3.4            |   py39h7b7c402_0         780 KB
    ipython-7.22.0             |   py39hd4e2768_0        1013 KB
    jedi-0.17.2                |   py39haa95532_1         942 KB
    jupyter_core-4.7.1         |   py39haa95532_0          84 KB
    pyzmq-20.0.0               |   py39hd77b12b_1         402 KB
    tornado-6.1                |   py39h2bbff1b_0         598 KB
    ------------------------------------------------------------
                                           Total:         3.7 MB

The following NEW packages will be INSTALLED:

  backcall           pkgs/main/noarch::backcall-0.2.0-pyhd3eb1b0_0
  decorator          pkgs/main/noarch::decorator-5.0.9-pyhd3eb1b0_0
  ipykernel          pkgs/main/win-64::ipykernel-5.3.4-py39h7b7c402_0
  ipython            pkgs/main/win-64::ipython-7.22.0-py39hd4e2768_0
  ipython_genutils   pkgs/main/noarch::ipython_genutils-0.2.0-pyhd3eb1b0_1
  jedi               pkgs/main/win-64::jedi-0.17.2-py39haa95532_1
  jupyter_client     pkgs/main/noarch::jupyter_client-6.1.12-pyhd3eb1b0_0
  jupyter_core       pkgs/main/win-64::jupyter_core-4.7.1-py39haa95532_0
  libsodium          pkgs/main/win-64::libsodium-1.0.18-h62dcd97_0
  parso              pkgs/main/noarch::parso-0.7.0-py_0
  pickleshare        pkgs/main/noarch::pickleshare-0.7.5-pyhd3eb1b0_1003
  prompt-toolkit     pkgs/main/noarch::prompt-toolkit-3.0.17-pyh06a4308_0
  pygments           pkgs/main/noarch::pygments-2.9.0-pyhd3eb1b0_0
  pyzmq              pkgs/main/win-64::pyzmq-20.0.0-py39hd77b12b_1
  tornado            pkgs/main/win-64::tornado-6.1-py39h2bbff1b_0
  traitlets          pkgs/main/noarch::traitlets-5.0.5-pyhd3eb1b0_0
  wcwidth            pkgs/main/noarch::wcwidth-0.2.5-py_0
  zeromq             pkgs/main/win-64::zeromq-4.3.3-ha925a31_3



Downloading and Extracting Packages
jedi-0.17.2          | 942 KB    | ##################################################################################################################################################################################### | 100%
ipython-7.22.0       | 1013 KB   | ##################################################################################################################################################################################### | 100%
pyzmq-20.0.0         | 402 KB    | ##################################################################################################################################################################################### | 100%
tornado-6.1          | 598 KB    | ##################################################################################################################################################################################### | 100%
ipykernel-5.3.4      | 780 KB    | ##################################################################################################################################################################################### | 100%
jupyter_core-4.7.1   | 84 KB     | ##################################################################################################################################################################################### | 100%
Preparing transaction: done
Verifying transaction: done
Executing transaction: done
(dfsc-env) PS C:\Users\<username>\Abschlussarbeit>
```

```
(dfsc-env) PS C:\Users\<username>\Abschlussarbeit> conda install selenium
Collecting package metadata (current_repodata.json): done
Solving environment: done


==> WARNING: A newer version of conda exists. <==
  current version: 4.10.1
  latest version: 4.10.3

Please update conda by running

    $ conda update -n base -c defaults conda



## Package Plan ##

  environment location: C:\Users\<username>\.conda\envs\dfsc-env

  added / updated specs:
    - selenium


The following packages will be downloaded:

    package                    |            build
    ---------------------------|-----------------
    brotlipy-0.7.0             |py39h2bbff1b_1003         411 KB
    cffi-1.14.5                |   py39hcd4344a_0         223 KB
    cryptography-3.4.7         |   py39h71e12ea_0         642 KB
    idna-3.2                   |     pyhd3eb1b0_0          48 KB
    pysocks-1.7.1              |   py39haa95532_0          55 KB
    selenium-3.141.0           |py39h2bbff1b_1000         815 KB
    urllib3-1.26.6             |     pyhd3eb1b0_1         112 KB
    win_inet_pton-1.1.0        |   py39haa95532_0          35 KB
    ------------------------------------------------------------
                                           Total:         2.3 MB

The following NEW packages will be INSTALLED:

  brotlipy           pkgs/main/win-64::brotlipy-0.7.0-py39h2bbff1b_1003
  cffi               pkgs/main/win-64::cffi-1.14.5-py39hcd4344a_0
  cryptography       pkgs/main/win-64::cryptography-3.4.7-py39h71e12ea_0
  idna               pkgs/main/noarch::idna-3.2-pyhd3eb1b0_0
  pycparser          pkgs/main/noarch::pycparser-2.20-py_2
  pyopenssl          pkgs/main/noarch::pyopenssl-20.0.1-pyhd3eb1b0_1
  pysocks            pkgs/main/win-64::pysocks-1.7.1-py39haa95532_0
  selenium           pkgs/main/win-64::selenium-3.141.0-py39h2bbff1b_1000
  urllib3            pkgs/main/noarch::urllib3-1.26.6-pyhd3eb1b0_1
  win_inet_pton      pkgs/main/win-64::win_inet_pton-1.1.0-py39haa95532_0


Proceed ([y]/n)? y


Downloading and Extracting Packages
pysocks-1.7.1        | 55 KB     | ########################################################### | 100%
idna-3.2             | 48 KB     | ########################################################### | 100%
urllib3-1.26.6       | 112 KB    | ########################################################### | 100%
cffi-1.14.5          | 223 KB    | ########################################################### | 100%
cryptography-3.4.7   | 642 KB    | ########################################################### | 100%
brotlipy-0.7.0       | 411 KB    | ########################################################### | 100%
selenium-3.141.0     | 815 KB    | ########################################################### | 100%
win_inet_pton-1.1.0  | 35 KB     | ########################################################### | 100%
Preparing transaction: done
Verifying transaction: done
Executing transaction: done
(dfsc-env) PS C:\Users\<username>\Abschlussarbeit>
```

```
(base) PS C:\Users\<username>> conda update conda
Collecting package metadata (current_repodata.json): done
Solving environment: \
Warning: 2 possible package resolutions (only showing differing packages):
  - defaults/noarch::decorator-4.4.2-pyhd3eb1b0_0, defaults/noarch::networkx-2.5.1-pyhd3eb1b0_0
  - defaults/noarch::decorator-5.0.9-pyhd3eb1b0_0, defaults/noarch::networkx-2.5-pydone

## Package Plan ##

  environment location: C:\ProgramData\Anaconda3

  added / updated specs:
    - conda


The following NEW packages will be INSTALLED:

  cfitsio            pkgs/main/win-64::cfitsio-3.470-he774522_6

The following packages will be UPDATED:

  astroid                              2.6.0-py38haa95532_0 --> 2.6.2-py38haa95532_0
  conda                               4.10.1-py38haa95532_1 --> 4.10.3-py38haa95532_0
  imagecodecs                      2021.3.31-py38h5da4933_0 --> 2021.6.8-py38h5da4933_0
  networkx                                         2.5-py_0 --> 2.5.1-pyhd3eb1b0_0
  pip                                 21.1.2-py38haa95532_0 --> 21.1.3-py38haa95532_0
  pylint                               2.8.3-py38haa95532_1 --> 2.9.1-py38haa95532_1
  typed-ast                            1.4.2-py38h2bbff1b_1 --> 1.4.3-py38h2bbff1b_1
  typing_extensions                    3.7.4.3-pyha847dfd_0 --> 3.10.0.0-pyh06a4308_0
  urllib3                               1.26.4-pyhd3eb1b0_0 --> 1.26.6-pyhd3eb1b0_1
  xlsxwriter                             1.3.8-pyhd3eb1b0_0 --> 1.4.3-pyhd3eb1b0_0
  xlwings                             0.23.0-py38haa95532_0 --> 0.24.1-py38haa95532_0
  zope.interface                       5.3.0-py38h2bbff1b_0 --> 5.4.0-py38h2bbff1b_0

The following packages will be DOWNGRADED:

  decorator                              5.0.9-pyhd3eb1b0_0 --> 4.4.2-pyhd3eb1b0_0


Proceed ([y]/n)? y

Preparing transaction: done
Verifying transaction: done
Executing transaction: done
(base) PS C:\Users\<username>>
```
