import rospy
from std_msgs.msg import String
#import Function_Luxmetre as FL
from datetime import datetime


def callback_receive_luxmetre_data(msg):
	now = datetime.now()
	timestamp = datetime.timestamp(now)
	try:
		file.write(str(timestamp) + "," + msg.data + "\n")
	except:
		pass

rospy.init_node('luxmetre_subscriber')
pub = rospy.Subscriber("/luxmetre", String, callback_receive_luxmetre_data)
file = open("data_luxmetre.csv", "w")
file.write("timestamp" + "," + "Lux" + "\n")

rospy.spin()
rospy.loginfo("Node was stopped")
