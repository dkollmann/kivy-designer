---
layout: post
title:  "Report 1 - Bounding period and two weeks of code"
date:   2015-05-28
---

Hi!

I started to work with **Kivy Designer** two weeks ago. I made a good progress with my proposal, coded and learned a lot with it :)

<a target="_blank" href="{{ "/assets/uploads/about.jpg" | prepend: site.baseurl }}">
	<img src="{{ "/assets/uploads/about.png" | prepend: site.baseurl }}" style="max-width: 600px" >
</a>


## Bounding period

* I studied a lot about Kivy, reading the documentation and fixing some small bugs
* Added a initial support for Python 3
* Fixed Kivy Designer code style
* Tried to help users on #Kivy(I'm not yet experienced enough to support major part of the users, but I've been always reading and trying to help when possible)
* While studying Kivy Designer, I had found a lot of bugs and had some ideas to new improvements; [Everything is listed here](https://github.com/aron-bordin/kivy-designer/issues)


## I have coded...

### Buildozer integration

Kivy Designer is now integrated with Buildozer. Now it's **possible to build and run your Python application on Desktop, Android and iOS** devices! To handle these multiple targets and options, I created a **"Build Profile"** settings.

### Build profiles 

There are three default profiles:

* Desktop
* Android - Buildozer
* iOS - Buildozer 

The user is able to edit these profiles, create new ones or even delete them. With build profiles I hope to turn **multi-platform development easier**. Now it's just necessary to change the profile to build the same application to the desired target :)

<a target="_blank" href="{{ "/assets/uploads/profiler_settings.png" | prepend: site.baseurl }}">
	<img src="{{ "/assets/uploads/profiler_settings.png" | prepend: site.baseurl }}" style="max-width: 600px" >
</a>

### buildozer.spec editor
The Buildozer requires a .spec file(INI format) to read the project settings. You can check the [default spec here](https://raw.githubusercontent.com/kivy/buildozer/master/buildozer/default.spec). 
I implemented a GUI to edit this file.
<a target="_blank" href="{{ "/assets/uploads/spec_editor.png" | prepend: site.baseurl }}">
	<img src="{{ "/assets/uploads/spec_editor.png" | prepend: site.baseurl }}" style="max-width: 600px" >
</a>

And to be easier to edit some properties, when necessary, all possible values are already provided:

<a target="_blank" href="{{ "/assets/uploads/spec_permissions.png" | prepend: site.baseurl }}">
	<img src="{{ "/assets/uploads/spec_permissions.png" | prepend: site.baseurl }}" style="max-width: 600px" >
</a>

### My progress
Major part of my code is waiting for review, but I did a good progress in my proposal, so I'm ok with my schedule.


Thats it, thanks for reading :)

Aron Bordin.