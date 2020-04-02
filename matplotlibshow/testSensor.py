import matplotlib.pyplot as plt
import getopt
import signal
import subprocess
import os
import sys
import _thread
import re
import pandas as pd

def processSensorData(p,n):
    print("Start process sensor data thread")
    regix=re.compile('(.*)SENSORDATA: [0-9](.*)')
    df = pd.DataFrame(columns=['time', 'ax', 'ay', 'az', 'gx','gy','gz', 'mx','my','mz'])
    c = n
    while c > 0:
        s = p.stdout.readline().decode('utf-8').strip()
        if regix.search(s):
            l = s.split("SENSORDATA: ")
            ldt = l[1].split(',')
            ld=[]
            ld.append(ldt[0])
            for i in  ldt[1:]:
                ld.append(float(i))
            df.loc[df.shape[0]]=ld
            mat = "{:12}\t{:12}\t{:12}\t{:12}\t{:12}\t{:12}\t{:12}\t{:12}\t{:12}\t{:12}"
            print(mat.format(ld[0],ld[1],ld[2],ld[3],ld[4],ld[5],ld[6],ld[7],ld[8],ld[8]))
            c -= 1
    df.to_csv("./data.csv")
    k = subprocess.Popen(
        'ps -A -f | grep "adb"',
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
        close_fds=True)
    for l in k.stdout.readlines():
        reResult = re.search(r'(\w*)(\s*)(\d*)(\d*) (.*) adb logcat',
                             l.decode('utf-8'), re.I)
        if reResult:
            os.kill(int(reResult.group(3)), signal.SIGKILL)
    k.terminate()
    p.terminate()


def processData():
    fig = plt.figure(figsize=(16,14))

    ax1 = fig.add_subplot(211)
    ax2 = fig.add_subplot(212)
    plt.ion()

    ydax=[0]
    yday=[0]
    ydaz=[0]

    ydgx=[0]
    ydgy=[0]
    ydgz=[0]

    xaxis=[0]

    showC= 21
    plt.style.use("fivethirtyeight")
    regix=re.compile('(.*)SENSORDATA: [0-9](.*)')
    c = 0
    df = pd.read_csv("./data.csv")
    row = df.shape[0]
    while c < row:
        ld = df.loc[c][2:]
        c += 1

        if c > showC:
            ydax.remove(ydax[0])
            yday.remove(yday[0])
            ydaz.remove(ydaz[0])

            ydgx.remove(ydgx[0])
            ydgy.remove(ydgy[0])
            ydgz.remove(ydgz[0])
            ydax.append(ld[0])
            yday.append(ld[1])
            ydaz.append(ld[2])

            ydgx.append(ld[3])
            ydgy.append(ld[4])
            ydgz.append(ld[5])
        else:
            xaxis.append(c)
            ydax.append(ld[0])
            yday.append(ld[1])
            ydaz.append(ld[2])

            ydgx.append(ld[3])
            ydgy.append(ld[4])
            ydgz.append(ld[5])



        ax1.cla()
        ax2.cla()

        ax1.plot(xaxis, ydax, color='r', label='ax',marker='o')
        ax1.plot(xaxis, yday, color='g', label='ay',marker='o')
        ax1.plot(xaxis, ydaz, color='b', label='az',marker='o')

        ax2.plot(xaxis, ydgx, color='r', label='gx',marker='o')
        ax2.plot(xaxis, ydgy, color='g', label='gy',marker='o')
        ax2.plot(xaxis, ydgz, color='b', label='gz',marker='o')


        ax1.legend()
        ax2.legend()

        plt.pause(0.5)
        # mat = "{:12}\t{:12}\t{:12}\t{:12}\t{:12}\t{:12}\t{:12}\t{:12}"
        # print(mat.format(ld[0],ld[1],ld[2],ld[3],ld[4],ld[5],ld[6],ld[7]))
        print(str(ld))

def processCsvData(p):
    fig = plt.figure(figsize=(16,14))

    ax1 = fig.add_subplot(211)
    ax2 = fig.add_subplot(212)
    plt.ion()

    ydax=[0]
    yday=[0]
    ydaz=[0]

    ydgx=[0]
    ydgy=[0]
    ydgz=[0]

    xaxis=[0]

    showC= 21
    plt.style.use("fivethirtyeight")
    regix=re.compile('(.*)SENSORDATA: [0-9](.*)')
    c = 0
    while True:
        s = p.stdout.readline().decode('utf-8').strip()
        if regix.search(s):
            l = s.split("SENSORDATA: ")
            ldt = l[1].split(',')
            ld=[]
            for i in  ldt[1:]:
                ld.append(float(i))
            c += 1

            if c > showC:
                ydax.remove(ydax[0])
                yday.remove(yday[0])
                ydaz.remove(ydaz[0])

                ydgx.remove(ydgx[0])
                ydgy.remove(ydgy[0])
                ydgz.remove(ydgz[0])
                ydax.append(ld[0])
                yday.append(ld[1])
                ydaz.append(ld[2])

                ydgx.append(ld[3])
                ydgy.append(ld[4])
                ydgz.append(ld[5])
            else:
                xaxis.append(c)
                ydax.append(ld[0])
                yday.append(ld[1])
                ydaz.append(ld[2])

                ydgx.append(ld[3])
                ydgy.append(ld[4])
                ydgz.append(ld[5])



            ax1.cla()
            ax2.cla()

            ax1.plot(xaxis, ydax, color='r', label='ax')
            ax1.plot(xaxis, yday, color='g', label='ay')
            ax1.plot(xaxis, ydaz, color='b', label='az')

            ax2.plot(xaxis, ydgx, color='r', label='gx')
            ax2.plot(xaxis, ydgy, color='g', label='gy')
            ax2.plot(xaxis, ydgz, color='b', label='gz')


            ax1.legend()
            ax2.legend()

            plt.pause(0.000000001)
            mat = "{:12}\t{:12}\t{:12}\t{:12}\t{:12}\t{:12}\t{:12}\t{:12}\t{:12}"
            print(mat.format(ldt[0],ld[0],ld[1],ld[2],ld[3],ld[4],ld[5],ld[6],ld[7]))




opts, args = getopt.getopt(sys.argv[1:], '-c:-s',
                           ['collect', 'show'])
for opt_name, opt_value in opts:
    if opt_name in ('-c', '--collect'):
        n = int(opt_value)
        plog = subprocess.Popen('adb logcat -c;adb logcat -c;adb logcat | grep "SENSORDATA"', shell= True, stdout=subprocess.PIPE  , stderr=subprocess.PIPE)
        _thread.start_new_thread(processSensorData, (plog,n))
        plog.wait()
    if opt_name in ('-s', '--show'):
        processData()



