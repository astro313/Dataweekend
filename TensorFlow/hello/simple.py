import tensorflow as tf

# create a graph
graph = tf.get_default_graph()
ops = graph.get_operations()
print ops

# define some stuff
input_val = tf.constant(1.0)
print input_val

ops = graph.get_operations()
print ops
print ops[0].node_def

for ooo in ops:
    print ooo.name

# eval
# create seesion
ses = tf.Session()
ses.run(input_val)

# build neuron w/ 1 param
# init variable
weight = tf.Variable(0.8)   # value is adaptive during training
# added 4 operations
for op in graph.get_operations():
    print op.name

# def some computation
outval = weight * input_val

op = graph.get_operations()
print op[-1].name

for op_in in op[-1].inputs:
    print op_in

# eval computation
# generate an operation to set all varaibles (here, weight)
init = tf.initialize_all_variables()
ses.run(init)
ses.run(outval)

# visualization
x = tf.constant(1.0, name='input')
w = tf.Variable(0.8, name='weight')
y = tf.multiply(w, x, name='output')

writer = tf.summary.FileWriter('./graphs/simple/', ses.graph)

import os
print('open http://localhost:6006/')
os.system('tensorboard --logdir=graphs/')

# neuron learn
ideal = tf.constant(0.0)
loss = (y - ideal)**2

# gradient descent opt
optim = tf.train.GradientDescentOptimizer(learning_rate=0.025)
grads_vars = optim.compute_gradients(loss)
print grads_vars
ses.run(tf.initialize_all_variables())

# gradient
print ses.run(grads_vars[1][0])
print 2. * ses.run(w)        # derivative of loss = 2 * res.
old_w = ses.run(w)

ses.run(optim.apply_gradients(grads_vars))
ses.run(w)
print old_w - (2. * old_w * 0.025)  # removed gradient * learning rate

train_step = optim.minimize(loss)
for i in range(100):
    ses.run(train_step)
ses.run(y)
ses.run(w)

# visualize training
ses.run(tf.initialize_all_variables())  # revert
for i in range(100):
    print 'before step{}, y={}'.format(i, ses.run(y))
    ses.run(train_step)

# use tensorboard
ses.run(tf.initialize_all_variables())
# create operation that reports current val of y
summary_y = tf.summary.scalar('output', y)
writer = tf.summary.FileWriter('./graphs/train/')
# train
for i in range(100):
    summary_str = ses.run(summary_y)
    writer.add_summary(summary_str, i)
    ses.run(train_step)

print('open http://localhost:6006/')
os.system('tensorboard --logdir=graphs/')



