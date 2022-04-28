from flask import Flask,render_template,url_for,redirect,request
import pandas as pd
import numpy as np
from io import BytesIO
import base64
import matplotlib.pyplot as plt

app=Flask(__name__)

@app.route("/mysuperplot", methods=["GET"])
def plotView():
        plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
        sizes = [15, 30, 45, 10]
        labels = ['青蛙', 'Hogs', 'Dogs', 'Logs']
        plt.pie(sizes,labels = labels)
        # plt.show()
        buffer = BytesIO()
        plt.savefig(buffer)
        plot_data =buffer.getvalue()
        imb=base64.b64encode(plot_data)
        ims = imb.decode()
        imd = "data:image/png;base64," + ims
        return render_template("image.html",image=imd)

if __name__ == '__main__':
	app.run(host='0.0.0.0',port='9000',debug=True)