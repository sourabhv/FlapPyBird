#call featurizer by "from tile_coding import TileCoder"
#featurizer = TileCoder(env, numOfTiles)
#s = featurizer.featurize

#window size = (288, 512)
import numpy as np

class TileCoder:
	def __init__(self, env, numOfTiles):
		self.n_features = numOfTiles
		self.width = 288
		self.height = 512


	def create_a_tiling(self, width, height, numOfPartitions, shifts):
		horizontal_partition_points = (np.linspace(0,width,numOfPartitions[0])+ shifts[0])[1:-1] 
		vertical_partition_points = (np.linspace(0,height,numOfPartitions[1])+ shifts[1])[1:-1] 
		tile = []
		tile.append(horizontal_partition_points)
		tile.append(vertical_partition_points)
		return tile

	def create_tilings(self, tiling_particulars):
		tilings = [self.create_a_tiling(self.width, self.height, numOfPartitions, shifts) for 
		numOfPartitions, shifts in tiling_particulars]
		return tilings

	def featurize(self, state, tilings):
		#tilings[0][0] --> is the 1st tile's horizontal partition points
		#tilings[0][1] --> is the 1st tile's vertical partition points
		#feature = [horizontalZone in tile 1, horizontalZone in tile 2, ..., verticalZone in tile 1, verticalZone in tile 2...]
		#or... feature = [horizontalZone in tile 1, verticalZone in tile 1, horizontalZone in tile 2,  verticalZone in tile 2,...]
		xcoordinate = state[0]
		ycoordinate = state[1]


		feature = []

		for i in range(len(tilings)):
			zone = []
			horizontalZone = np.digitize(xcoordinate, tilings[i][0])
			verticalZone = np.digitize(ycoordinate, tilings[i][1])
			zone.append(horizontalZone)
			zone.append(verticalZone)
			feature.append(zone)
		
		flattened_feature = (np.array(feature)).flatten()

		return flattened_feature #ndarray of shape (numOfTile,)