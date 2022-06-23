// pch.cpp: source file corresponding to the pre-compiled header

#include "pch.h"

void key_right(){
	keybd_event(VK_RIGHT, 0, 0, 0);
	keybd_event(VK_RIGHT, 0, KEYEVENTF_KEYUP, 0);
}

void key_left() {
	keybd_event(VK_LEFT, 0, 0, 0);
	keybd_event(VK_LEFT, 0, KEYEVENTF_KEYUP, 0);
}