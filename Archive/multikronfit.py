import tensorflow as tf
from tensorflow.keras import layers
import random
import snap
import numpy as np

eps = 1e-6

def tf_kron(a,b):
  a_shape = [a.shape[0],a.shape[1]]
  b_shape = [b.shape[0],b.shape[1]]
  return tf.reshape(tf.reshape(a,[a_shape[0],1,a_shape[1],1])*tf.reshape(b,[1,b_shape[0],1,b_shape[1]]),[a_shape[0]*b_shape[0],a_shape[1]*b_shape[1]])


class KroneckerProduct(layers.Layer):

  def __init__(self, size=2):
    super(KroneckerProduct, self).__init__()
    theta_init = tf.random_normal_initializer()
    self.theta = tf.Variable(initial_value=w_init(shape=(size, size), dtype='float32'), trainable=True)

  def call(self, inputs):
    return tf_kron(inputs, self.theta)


def construct_graph(kernels):
  """
  Constructs the final generated graph
  ------------------------------------
  input : List of parameter matrices Θ_i
  output: Final generated matrix P, the Kronecker product of all the kernels
  """
  curr = kernels[0]

  for kernel in kernels[1:]:
    curr = tf_kron(curr, kernel)

  return curr

def diff_in_log_likelihood(G, generated, p1, p2):
  """
  input : Two permutation sequences, p1 and p2
  output: P(σ_1|G,Θ)/P(σ_2|G,Θ) or P(curr|G,Θ)/P(prev|G,Θ)
  """
  n = G.GetNodes()

  diff = 1

  for i in range(n):
    for j in range(n):
      p1_i, p1_j = p1[i], p1[j]
      p2_i, p2_j = p2[i], p2[j]
      if G.IsEdge(i+1, j+1):
        diff *= generated[p1_i][p1_j]/generated[p2_i][p2_j] + eps
      else:
        diff *= (1 - generated[p1_i][p1_j])/(1 - generated[p2_i][p2_j]) + eps

  return diff


def sample_permutation(G, generated):
  """
  Metropolis sampling of the node permutation
  ------------------------------------------
  input : Kronecker initiator matrix Θ and a graph G on N nodes 
  output: Permutation σ(i) ∼ P(σ|G, Θ)
  """
  n = G.GetNodes()

  curr = list(range(n))
  converged = False

  i = 1
  while not converged:
    i = random.randint(0, n-1)
    j = random.randint(0, n-1)
    prev = curr[:]
    # Swap two places in the permutation randomly
    curr[i], curr[j] = curr[j], curr[i]
    u = random.random()
    if u > diff_in_log_likelihood(G, generated, curr, prev):
      curr = prev[:]
    i += 1

    if i > 5:
      converged = True

  return curr



def calculate_likelihood(G, generated, permutation):
  # Setup
  n = G.GetNodes()
  #scale = np.power(n, np.log(n)/(1.2*n))
  scale = 1

  likelihood = 1

  for i in range(n):
    for j in range(n):
      pi = permutation[i]
      pj = permutation[j]

      print(likelihood)

      if G.IsEdge(i+1, j+1):
        likelihood *= generated[pi][pj]
      else:
        likelihood *= (1 - generated[pi][pj])

      likelihood *= scale

  return likelihood


def optimize(G, kernel_sizes):
  kernels = []

  # Define all the kernels, the parameter matrices
  for k_sz in kernel_sizes:
    k = tf.Variable(np.random.rand(k_sz, k_sz), trainable=True)
    kernels.append(k)

  # Define the likelihood function to optimize
  def likelihood():
    """
    input : List of parameter matrices Θ_i, and graph G [UPPER SCOPE VARS]
    output: Log-likelihood l(Θ), and gradient ∂ l(Θ) [CALCULATED AUTOMATICALLY]
    """
    print('Generating graph')
    generated = construct_graph(kernels)
    print('Sampling permutation')
    permutation = sample_permutation(G, generated)
    print('Calculating likelihood')
    likelihood = calculate_likelihood(G, generated, permutation)
    print('Likelihood given these kernels [{}]'.format(likelihood))
    return -likelihood

  # Define which optimizer to use and how many epochs to run
  optimizer = tf.keras.optimizers.SGD(0.1)
  num_epochs = 3

  # Main training loop
  with tf.GradientTape() as tape:
    for epoch in range(num_epochs):
        print("Epoch {}".format(epoch))
        optimizer.minimize(likelihood, var_list=kernels)

  return kernels


if __name__ == '__main__':

  # Run the main script
  target_graph = 'ENZYMES_g123'
  G = snap.LoadEdgeList(snap.PUNGraph, target_graph + "/" + target_graph + ".txt", 0, 1, ' ')
  print("Loaded {} with {} nodes".format(target_graph, G.GetNodes()))

  kernel_sizes = [2, 3, 3, 5]

  count = 0
  while count < 100:
    print("Count: ", count)
    print('Finding the optimal kernels')
    optimized_kernels = optimize(G, kernel_sizes)
    final_graph = construct_graph(optimized_kernels)

    print(final_graph)
    print("max : ", np.max(final_graph))
    print("min: ",np.min(final_graph))

    norm = np.linalg.norm(final_graph)
    final_graph /= np.max(final_graph)
    
    generated = snap.TUNGraph.New()
    for i in range(len(final_graph)):
      generated.AddNode(i)

    # for i in range(len(final_graph)):
    #   for j in range(i, len(final_graph)):
    #     # rand = random.uniform(0, np.max(final_graph))
    #     rand = random.random()
    #     if final_graph[i][j] < rand:
    #       generated.AddEdge(i, j)

    edges = 0
    while edges < G.GetEdges():
      a = random.randint(0, G.GetNodes()-1)
      b = random.randint(0, G.GetNodes()-1)
      if a != b:
        rand = random.random()
        if final_graph[a][b] < rand:
          generated.AddEdge(a, b)
          edges +=1

    snap.DrawGViz(generated, snap.gvlNeato, "attempt" + str(count) + ".png", "fuck", False)
    # snap.DrawGViz(G, snap.gvlNeato, "target.png", "target", False)
    print("Target Graph Edges: ", G.GetEdges())
    print("Generated Graph Edges: ", generated.GetEdges())
    snap.SaveEdgeList(generated,  "attempt" + str(count) + '.txt')










