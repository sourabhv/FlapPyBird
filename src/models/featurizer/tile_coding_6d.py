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
		self.velocity = 20

	def create_a_tiling_6d(self, width, height, velocity, numOfPartitions, shifts):
		birdPosition_partition_points = (np.linspace(0,height,numOfPartitions[0])+ shifts[0])[1:-1] 
		velocity_partition_points = (np.linspace(0,velocity,numOfPartitions[0])+ shifts[0])[1:-1]
		pipe1_y_partition_points = (np.linspace(0,height,numOfPartitions[0])+ shifts[0])[1:-1]
		pipe1_x_partition_points = (np.linspace(0,width,numOfPartitions[0])+ shifts[0])[1:-1]
		pipe2_y_partition_points = (np.linspace(0,height,numOfPartitions[0])+ shifts[0])[1:-1]
		pipe2_x_partition_points = (np.linspace(0,width,numOfPartitions[0])+ shifts[0])[1:-1]

		tile = []
		tile.append(birdPosition_partition_points)
		tile.append(velocity_partition_points)
		tile.append(pipe1_y_partition_points)
		tile.append(pipe1_x_partition_points)
		tile.append(pipe2_y_partition_points)
		tile.append(pipe2_x_partition_points)
		return tile

	
	def create_tilings_6d(self, tiling_particulars):
		tilings = [self.create_a_tiling_6d(self.width, self.height, self.velocity, numOfPartitions, shifts) for 
		numOfPartitions, shifts in tiling_particulars]
		return tilings


	def featurize_6d(self, state, tilings):
		#tilings[0][0] --> is the 1st tile's horizontal partition points
		#tilings[0][1] --> is the 1st tile's vertical partition points
		#feature = [horizontalZone in tile 1, horizontalZone in tile 2, ..., verticalZone in tile 1, verticalZone in tile 2...]
		#or... feature = [horizontalZone in tile 1, verticalZone in tile 1, horizontalZone in tile 2,  verticalZone in tile 2,...]
		bird_y = state[0]
		bird_vel = state[1]
		pipe1_y = state[2]
		pipe1_x = state[3]
		pipe2_y = state[4]
		pipe2_x = state[5]

		feature = []

		for i in range(len(tilings)):
			zone = []
			birdPosition_zone = np.digitize(bird_y, tilings[i][0])
			velocity_zone = np.digitize(bird_vel, tilings[i][1])
			pipe1_y_zone = np.digitize(pipe1_y, tilings[i][2])
			pipe1_x_zone = np.digitize(pipe1_x, tilings[i][3])
			pipe2_y_zone = np.digitize(pipe2_y, tilings[i][4])
			pipe2_x_zone  = np.digitize(pipe2_x, tilings[i][5])

			zone.append(birdPosition_zone)
			zone.append(velocity_zone)
			zone.append(pipe1_y_zone)
			zone.append(pipe1_x_zone)
			zone.append(pipe2_y_zone)
			zone.append(pipe2_x_zone)

			feature.append(zone)
			
		flattened_feature = (np.array(feature)).flatten()

		return flattened_feature #ndarray of shape (numOfTile,)