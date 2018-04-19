#!bash/bin

for filename in /Users/Roy/Research/Chaikin/InformationTheory/sequences/* ; do
	python3 MPM_v3.py "$filename"
	echo "$filename"
done