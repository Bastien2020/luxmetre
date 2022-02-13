
import rospy
from std_msgs.msg import String
import Function_Luxmetre as FL
from datetime import datetime

#Activation du mode PC du Luxmètre
PC_activation = FL.mode_PC_activation()
rge = PC_activation[1]


if __name__ == '__main__':

	rospy.init_node('luxmetre_publisher')
	pub = rospy.Publisher("/luxmetre", String, queue_size=10)
	rate = rospy.Rate(2)
	#file = open("data_luxmetre.csv", "w")
	#file.write("timestamp" + "," + "Lux" + "\n")

	while not rospy.is_shutdown():
		# récupération de la mesure d'éclairement
		measure = FL.data_collect(rge)
		msg = String()
		msg.data = measure
		pub.publish(msg)
		
		#enregistrement de la mesure dans un fichier 
		"""
		now = datetime.now()
		timestamp = datetime.timestamp(now)

		try:
			file.write(str(timestamp) + "," + measure + "\n")
		except:
			pass
		"""
		rate.sleep()

	rospy.loginfo("Node was stopped")
