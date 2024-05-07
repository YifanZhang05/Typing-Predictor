from utilities import *
from ngram import *

words = ["the", "child", "will", "go", "out", "to", "play", ",", "and", 
  "the", "child", "can", "not", "be", "sad", "anymore", ".", "the", "child", "will"]
ngram_dict = build_ngram_counts(words, 2)
# print(ngram_dict)

ngram_counts= {("i", "love"): [["js", "py3", "c", "no", "c++"], [2, 2, 20, 10, 9]],
	("u", "r"): [["cool", "nice", "lit", "kind", "good"], [8, 7, 5, 5, 3]],
	("toronto", "is"): [["six", "drake"], [2, 3]]}
#print(prune_ngram_counts(ngram_counts, 3))

#print(probify_ngram_counts(build_ngram_counts(parse_file("test_text_parsing.txt"), 2)))

words2 = ["the", "child", "will", "the", "child", "can", "the",
							"child", "will", "the", "child", "may", "go", "home", "."]
#print(build_ngram_model(words2, 2, 15))
model = build_ngram_model(words2, 2, 15)

# print(write_model(ngram_counts, 2, "test_file2.txt", True))
# #print(read_model("raw_test_file2.txt", True))
# model3 = read_model("test_file.txt", False)
# print(model3)

update_model("a", "n", "v")