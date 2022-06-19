import rospy
from custom_msgs.msg import Luxmetre
from std_msgs.msg import String
import Function_Luxmetre as FL
from datetime import datetime
import sys

#Activation du mode PC du Luxmètre
PC_activation = FL.mode_PC_activation()
rge = PC_activation[1]


if __name__ == '__main__':

	rospy.init_node('luxmetre_publisher')
	pub = rospy.Publisher("/luxmetre", Luxmetre, queue_size=10)
	r = rospy.Rate(2)
	total_device = int(sys.argv[1])


while not rospy.is_shutdown():
	measures = FL.data_collect(rge)
	for i in range(0, total_device):
		globals()["msg%s" % i] = Luxmetre()
		globals()["msg%s" % i].timestamp = measures[i * 3]
		globals()["msg%s" % i].lux_number = measures[i * 3 + 1]
		globals()["msg%s" % i].measure = measures[i * 3 + 2]
		#print(type(globals()["msg%s" % i]))
		pub.publish(globals()["msg%s" % i])
	r.sleep()

rospy.loginfo("Node was stopped")

"""
for i in range(0, 2):
	globals()["msg%s" % i] = Luxmetre()
	globals()["msg%s" % i].timestamp = measures[i * 3]
	globals()["msg%s" % i].lux_number = measures[i * 3 + 1]
	globals()["msg%s" % i].measure = measures[i * 3 + 2]
	print(type("msg%s" % i)
"""