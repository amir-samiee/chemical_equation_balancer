# Chemical Equation/Reaction Balancer
With this program, you can solve almost any chemical equation/reaction (it has been tested on different kinds of equations/reactions) except the ones that can not be balanced or the ones that have infinite possible ways to balance.

Example of impossible reactions: Ca(PO4)2 + SiO2 = P4O10 + CaSiO3  
This equation has 0 possible ways to balance.

Example of infinite reactions: As2S3 + NO3 + H2O = AsO4 + H + NO + S  
This equation can be balanced in infinite ways.
<br/>
<br/>
![balancer_preview](https://user-images.githubusercontent.com/81751940/114858184-5fd54b00-9dfe-11eb-8849-86f3eab93296.png)
<br/>
<br/>

# How to enter my reaction?
You can enter your reactions in 8 different formats:
```
1) reagents = products
2) reagents => products
3) reagents ==> products
4) reagents ===> products
5) reagents -> products
6) reagents --> products
7) reagents ---> products
8) reagents → products
```
exsample: `Cu + HNO3 ==> Cu(NO3)2 + NO + H2O`
(-using spaces is not secessary- example: `Cu+HNO3==>Cu(NO3)+NO+H2O`)
<br/>
<br/>
<br/>

# Usage 
If you are not able (or don't want) to install any libraries, run these commands:
```
apt update
apt upgrade
python3 no_color.py
```
else:
```
apt update
apt upgrade
pip install colorama
python3 balancer.py
```
(-you might need to use "sudo" command before the first 4 lines- example: `sudo apt update`,if you still had a problem runing the program use this command: `chmod +x *`)

# Test some reactions
If you enter "test", the program will show you some reactions and balances them.
<br/>

# Issues
If there is any problems with the script or you need any help for runung, working with, etc. please let me know in "Issues" section.

<br/>
<br/>
<br/>

- New Version :
    - known bugs fixed
    - no need to install numpy anymore
