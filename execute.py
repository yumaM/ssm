import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from svar import *
from kalman import *

def draw_heatmap(data, **labels):
	fig, axis = plt.subplots(figsize=(10, 10))
	heatmap = axis.pcolor(data, cmap=plt.cm.Reds)
	axis.set_xticks(np.arange(data.shape[0])+0.5, minor=False)
	axis.set_yticks(np.arange(data.shape[1])+0.5, minor=False)
	axis.invert_yaxis()
	axis.xaxis.tick_top()

	if labels:
		axis.set_xticklabels(labels["row"], minor=False)
		axis.set_yticklabels(labels["column"], minor=False)

	fig.show()
	#plt.savefig('image.png')
	
	return heatmap

def draw_heatmap2(x, y):
	heatmap, xedges, yedges = np.histogram2d(x, y, bins=50)
	extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

	plt.figure()
	plt.imshow(heatmap, extent=extent)
	plt.show()
	#plt.savefig('image.png')
	

if __name__ == "__main__":
	filename = "./ignr/data/exchange.dat"
	#data = np.loadtxt(filename, delimiter="\t")
	df = pd.read_table(filename, index_col="datetime")
	df.index = pd.to_datetime(df.index) # convert index into datetime
	#hourly = df.resample("H", how="mean") # hourly
	daily = df.resample("D", how="mean") # daily
	price = daily.ix[:, daily.columns.map(lambda x: x.endswith("PRICE"))]
	value = daily.ix[:, daily.columns.map(lambda x: x.endswith("VALUE"))]

	# SVAR
	if 1:
		svar = SparseVAR()
		svar.set_data(price)
		##svar.SVAR(5)
		B = svar.GCV()
		draw_heatmap(np.array(B))


	# kalman and EM
	if 0:
		sys_k = 5
		em = EM(price, sys_k)
		em.execute()

		if 0:
			fig, axes = plt.subplots(np.int(np.ceil(sys_k/3.0)), 3, sharex=True)
			j = 0
			for i in range(3):
				while j<sys_k:
					if sys_k<=3:
						axes[j%3].plot(data[0][j], "k--", label="obs")
						axes[j%3].plot(em.kl.xp[j], label="prd")
						axes[j%3].legend(loc="best")
						axes[j%3].set_title(j)
					else:
						axes[i, j%3].plot(data[0][j], "k--", label="obs")
						axes[i, j%3].plot(em.kl.xp[j], label="prd")
						axes[i, j%3].legend(loc="best")
						axes[i, j%3].set_title(j)
					j += 1
					if j%3 == 2: break

			fig.show()
		
			#loss = data[0]-em.kl.xs
			#plt.plot(loss)
			#plt.plot(em.llh)
			#plt.show()
