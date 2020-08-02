# channel Table
class FyTAI__channel(object):
	def __init__(self, client):
		super(FyTAI__channel, self).__init__()
		self.collection = client['channel']

		#Basic projection
		self.projection_basic = {
			'_id': 0
		}

	# find channel
	def find__one(self, channel_hash):
		return self.collection.find({'hash': channel_hash})

	# insert channel
	def insert__one(self, channel_object):
		self.collection.insert(channel_object)
		return "success"

	# update channel
	def update__one(self, channel_object):
		self.collection.update(
			{
				hash: channel_object.hash		
			},
			{
				'$set': channel_object
			}
		)
		return "success"

# video Table
class FyTAI__video(object):
	def __init__(self, client):
		super(FyTAI__video, self).__init__()
		self.collection = client['video']

		#Basic projection
		self.projection_basic = {
			'_id': 0
		}

	# find video
	def find__one(self, video_hash):
		return self.collection.find({'hash': video_hash})

	# insert video
	def insert__one(self, video_object):
		self.collection.insert(video_object)
		return "success"

	# update channel
	def update__one(self, video_object):
		self.collection.update(
			{
				hash: video_object.hash		
			},
			{
				'$set': video_object
			}
		)
		return "success"