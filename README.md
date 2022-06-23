# mp_stickman_game
Use MediaPipe to code a program to control stickman fighter game

In the holistic.py code, it call a dynamic link library ("py_c_call.dll") compiled with C, so the program can run faster.

If you want to use a pure python code, you can remove comment

line 52 "#pyautogui.press(keys="right")" 
line 56 "#pyautogui.press(keys="left")"

Required environment:
python 3.9
pip install mediapipe
pip install pyautogui
