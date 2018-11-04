'''
extract useful stuff from simple.py

'''

import tensorflow as tf

x = tf.constant(1.0, name='input')
w = tf.Variable(0.8, name='weight')
y = tf.muliply(w, x, name='output')
y_ = tf.constant(0.0, name='correct_value')

loss = (y - y_)**2
train_step = tf.train.GradientDescentOptimizer(0.025).minimize(loss)

for value in [x, w, y, y_, loss]:
    tf.summary.scalar(value.op.name, value)

summaries = tf.summary.merge_all()

sess = tf.Session()
writer = tf.summary.FileWriter('log_simple_stats', sess.graph)

sess.run(tf.initialize_all_variables())
for i in range(100):
    writer.add_summary(sess.run(summaries), i)
    sess.run(train_step)

import webbrowser, os
os.system('tensorboard --logdir=log_simple_stats/')
webbrowser.open("http://localhost:6060/log_simple_stats")