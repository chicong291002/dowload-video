# **Guide to installing Video Download Basic**

> Video Download Basic is a simple application that helps you download videos from YouTube and convert video formats from mp4 to other formats. This application is written in Python language and uses the PyTube library to perform video downloads.
> 

## **Guide to installing Video Download Basic from the setup file**

### Step 1: Download the setup file from Github

Access the project's Github page at: [https://github.com/chicong291002/dowload-video/releases](https://github.com/chicong291002/dowload-video/releases)

- Windows

Download the installation file vdbsetup_Windows-v1.1.zip.

- Linux

Download the installation file vdbinstaller_Linux-v1.1.zip.

Reference image:

![image](https://user-images.githubusercontent.com/88141204/236811454-9ffb2bf8-b80f-4316-a0c1-a7d9ea939082.png)


### **Step 2: Install Video Download Basic**

- Windows

Run the vdbsetup.exe file after extracting it and follow the steps in the installation wizard. After the installation is complete, Video Download Basic will be installed on your computer.

- Linux

Unzip and run the vdb file in the vdb directory to use.

Note: ffmpeg should be installed before use

ffmpeg can be installed with the following command

```powershell
sudo apt-get install ffmpeg
```

After running the command, a VideoDownloadBasic folder will be created in the same directory as the vdb_installer.run file.

### **Step 3: Use Video Download Basic**

- Windows

After the installation is complete, you can start Video Download Basic by searching for it in the Start menu.

## **Guide to installing Video Download Basic from the source code**

### **Step 1: Download the source code from Github**

First, you need to download the source code of Video Download Basic from Github. You can access the project's Github page at: [https://github.com/chicong291002/dowload-video/releases/tag/v1.5.0](https://github.com/chicong291002/dowload-video/releases/tag/v1.5.0)

Download the latest version of the VideoDownloadBasic.zip file that corresponds to your operating system (VideoDownloadBasic_Windows.zip-v1.1, VideoDownloadBasic_Linux-v1.1.zip). Proceed to download and extract it.

![image](https://user-images.githubusercontent.com/88141204/236811619-b3742151-06f3-40d4-9554-656a4eb95d93.png)

### **Step 2: Install Python (if you don't have Python already installed)**

Video Download Basic is written in Python, so you need to install Python on your computer if you don't already have it. You can download the latest version of Python from the official Python website at [https://www.python.org/downloads/](https://www.python.org/downloads/).

After downloading, install Python using the downloaded .exe file.

### **Step 3: Install necessary libraries**

You can install the necessary libraries using the requirements.txt file that comes with the Video Download Basic source code. Open Command Prompt or Terminal and navigate to the directory that contains the application source code, then run the following command to install the necessary libraries:

- Windows

```powershell
pip install -r requirements.txt
```

The above command will install all the necessary libraries to run the Video Download Basic application.

- Linux

If pip is not installed, use the following command to install pip:

```powershell
sudo apt-get update
sudo apt-get install python3-pip
```

Next, run this command to install the libraries:

```powershell
pip install -r requirements.txt
```

Then use the following command to download tkinter:

```powershell
sudo apt-get install python3-tk
```

Finally, use this command to download ffmpeg:

```powershell
sudo apt-get install ffmpeg
```

### **Step 4: Run the application**

After installing Python and the necessary libraries, you can run the Video Download Basic application. Open Command Prompt or Terminal and navigate to the directory that contains the application's source code.

Run the following command to start the application:

```powershell
python main.py
```

Or

```powershell
python3 main.py
```

Then, the Video Download Basic application will start up and display on the screen.

## **Conclusion**

In this article, we have guided you to install the Video Download Basic application from the source code and from the setup file. You can use this application to download videos from YouTube and convert them to other formats.
