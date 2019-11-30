all:
	python step05_generate_alreadycoded.py > data/coded_blacklist.csv

dev3:
	cat data/header.csv > data/uncoded_rules_codifying.csv
	python step1_prepcodify_reddit.py -t dev3 -n 204 >> data/uncoded_rules_codifying.csv
	python step1_prepcodify_minecraft.py -t dev3 -n 641 >> data/uncoded_rules_codifying.csv

full:
	python step1_prepcodify_minecraft.py -t all -n -1 > data/tmp/minecraft_uncoded_rules_codifying.csv
	python step1_prepcodify_reddit.py -t all -n -1 > data/tmp/reddit_uncoded_rules_codifying.csv
