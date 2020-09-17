if __name__ == "__main__":
  import os
  import sys

  prev, after, *_ = sys.argv[1:]
  prev_dict = {}
  after_dict = {}

  for cluster in os.listdir(prev):
    if os.path.isdir(os.path.join(prev, cluster)):
      for f in os.listdir(os.path.join(prev, cluster)):
        prev_dict[f] = cluster

  for cluster in os.listdir(after):
    if os.path.isdir(os.path.join(after, cluster)):
      for f in os.listdir(os.path.join(after, cluster)):
        after_dict[f] = cluster

  for f in prev_dict:
    if prev_dict[f] != after_dict[f]:
      print('{}: {} -> {}'.format(f, prev_dict[f], after_dict[f]))
