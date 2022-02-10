
import rospy
from std_msgs.msg import String
import Function_Luxmetre as FL

#Activation du mode PC du Luxmètre
PC_activation = FL.mode_PC_activation()
rge = PC_activation[1]


if __name__ == '__main__':

	rospy.init_node('luxmetre_publisher')

	pub = rospy.Publisher("/luxmetre", String, queue_size=10)

	rate = rospy.Rate(2)

	while not rospy.is_shutdown():
		# récupération de la mesure d'éclairement
		measure = FL.data_collect(rge)
		msg = String()
		msg.data = measure
		pub.publish(msg)
		rate.sleep()

	rospy.loginfo("Node was stopped")
