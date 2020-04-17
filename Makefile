all:
	python step05_generate_alreadycoded.py > data/coded_blacklist.csv

dev3:
	echo "this is the dev data"
	cat data/header.csv > data/uncoded_rules_codifying.csv
	python step1_prepcodify_wow.py -t dev3 -n 153 >> data/uncoded_rules_codifying.csv
	python step1_prepcodify_reddit.py -t dev3 -n 274 >> data/uncoded_rules_codifying.csv
	python step1_prepcodify_minecraft.py -t dev3 -n 641 >> data/uncoded_rules_codifying.csv

full:
	echo "this is all the data"
	cat data/header.csv > data/all_data_raw/wow_uncoded_rules_codifying.csv
	cat data/header.csv > data/all_data_raw/reddit_uncoded_rules_codifying.csv
	cat data/header.csv > data/all_data_raw/minecraft_uncoded_rules_codifying.csv
	python step1_prepcodify_wow.py -t all -n -1 >> data/all_data_raw/wow_uncoded_rules_codifying.csv
	python step1_prepcodify_reddit.py -t all -n -1 >> data/all_data_raw/reddit_uncoded_rules_codifying.csv
	python step1_prepcodify_minecraft.py -t all -n -1 >> data/all_data_raw/minecraft_uncoded_rules_codifying.csv

build: full
	echo "this is the train and test datasets, off the top of the full data"
	head -1830 data/all_data_raw/reddit_uncoded_rules_codifying.csv > /tmp/reddit.csv	
	head -25022 data/all_data_raw/minecraft_uncoded_rules_codifying.csv  > /tmp/mc.csv
	cp data/all_data_raw/wow_uncoded_rules_codifying.csv /tmp/wow.csv
