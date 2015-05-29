---
layout: post
title:  "Week 1 - Buildozer integration and new menu"
date:   2015-05-17
---

Hi!

I started to work with **Kivy Designer** this week. In the last weeks, I studied the Kivy Documentation and made some contributions to Kivy Designer.
I submitted **my first PR today**, I'm very happy about this first week. I had developed a **completely new menu, with a better design, easier to use, and more powerful.**

## Whats is new

Kivy Designer is now integrated with Buildozer. Now it's **possible to build and run your Python application on Desktop, Android and iOS** devices! To handle these multiple targets and options, I created a **"Build Profile"** settings.

There are three default profiles:

* Desktop
* Android - Buildozer
* iOS - Buildozer 

The user is able to edit these profiles, create new ones or even delete them. With build profiles I hope to turn **multi-platform development easier**. Now it's just necessary to change the profile to build the same application to the desired target :)


## Bounding period

* I studied a lot about Kivy  
* Added a initial support for Python 3
* Fixed Kivy Designer code style
* Tried to help users on #Kivy(I'm not yet experienced enough to support major part of the users, but I've been always reading and trying to help when possible)
* While studying Kivy Designer, I had found a lot of bugs and had some ideas to new improvements; [Everything is listed here](https://github.com/aron-bordin/kivy-designer/issues)

## My first PR

I did my first PR to the project :) I'm still waiting the review.

New improvements:

* [add view -> fullscreen](https://github.com/aron-bordin/kivy-designer/issues/50)
* [Save View settings](https://github.com/aron-bordin/kivy-designer/issues/44)
* [Close project button](https://github.com/aron-bordin/kivy-designer/issues/43)
* [Buildozer integration](https://github.com/aron-bordin/kivy-designer/issues/30)
* [New menu](https://github.com/aron-bordin/kivy-designer/issues/91)
* [Android logcat](https://github.com/aron-bordin/kivy-designer/issues/34)

Bugs(some bugs are related):

* [Recent files not showing useful information](https://github.com/aron-bordin/kivy-designer/issues/2)
* [Remove some buttons on Start page](https://github.com/aron-bordin/kivy-designer/issues/1)
* [Project ­> Add File is not working](https://github.com/aron-bordin/kivy-designer/issues/11)
* [Rerun project](https://github.com/aron-bordin/kivy-designer/issues/14)
* [.py still opened after new prj](https://github.com/aron-bordin/kivy-designer/issues/17)
* [Click and hold previous files](https://github.com/aron-bordin/kivy-designer/issues/18)
* [Error when screen is too small](https://github.com/aron-bordin/kivy-designer/issues/48)
* [It's necessary open the project setting to be able to use it](https://github.com/aron-bordin/kivy-designer/issues/54)
* [tab autocomplete not working on kivy_console](https://github.com/aron-bordin/kivy-designer/issues/55)
* [kivy console is always listening the keyboard](https://github.com/aron-bordin/kivy-designer/issues/56)
* [kivy console cannot run non-unicode commands](https://github.com/aron-bordin/kivy-designer/issues/57)
* [cannot clear kivy console](https://github.com/aron-bordin/kivy-designer/issues/58)
* [user can delete PS1 on console input](https://github.com/aron-bordin/kivy-designer/issues/59)
* [tab commands not working on console](https://github.com/aron-bordin/kivy-designer/issues/60)
* [Project ­> Add File doesnt check if a file with the same name exists](https://github.com/aron-bordin/kivy-designer/issues/68)
* [hard-coded cd](https://github.com/aron-bordin/kivy-designer/issues/75)
* [cannot open buildozer project](https://github.com/aron-bordin/kivy-designer/issues/76)
* [MainApp class must inherits only the App](https://github.com/aron-bordin/kivy-designer/issues/82)
* [load_proj_config do nothing](https://github.com/aron-bordin/kivy-designer/issues/84)
* [autosave backup .buildozer and bin folder](https://github.com/aron-bordin/kivy-designer/issues/85)
* [Improve rj preferences UI](https://github.com/aron-bordin/kivy-designer/issues/20)



## Next week
In the next week, I'll be fixing more bugs and developing the Buildozer Settings UI, a easy to use interface to edit the buildozer.spec file.

I'll try to improve Kivy Designer performance as well, but I'll try to get some tips with my mentors before start working with it ;/

And if possible, I'll add support to the Hanga builder.



Thats it, thanks for reading :)

Aron Bordin.